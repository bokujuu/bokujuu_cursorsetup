#!/usr/bin/env python3
import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


TOOLCALL_PREFIX = "ToolCall: "
PATCH_FILE_RE = re.compile(r"^\*\*\* (Add|Update|Delete) File: (.+)$", re.MULTILINE)
PATCH_MOVE_RE = re.compile(r"^\*\*\* Move to: (.+)$", re.MULTILINE)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract machine-oriented context for a Codex session/thread ID."
    )
    parser.add_argument("--thread-id", required=True, help="Codex thread/session ID")
    parser.add_argument(
        "--codex-home",
        help="Override Codex home directory. Defaults to CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Include raw tool payload excerpts in the output",
    )
    return parser.parse_args()


def resolve_codex_home(explicit):
    if explicit:
        return Path(explicit).expanduser().resolve()

    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()

    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        return (Path(user_profile) / ".codex").resolve()

    home = Path.home()
    return (home / ".codex").resolve()


def isoformat_local(epoch_seconds):
    return datetime.fromtimestamp(epoch_seconds, tz=timezone.utc).astimezone().isoformat()


def safe_json_loads(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def excerpt(text, limit=240):
    if text is None:
        return None
    text = str(text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def classify_shell_command(command):
    command = (command or "").strip()
    lowered = command.lower()

    if any(token in lowered for token in ("benchmark:perf", "run-benchmarks", "engine-benchmark")):
        return "benchmark"
    if any(token in lowered for token in ("node --check", "pytest", "cargo test", "npm test", "pnpm test", "vitest", "jest", "playwright")):
        return "validation"
    if any(token in lowered for token in ("git status", "git diff", "git show", "git log")):
        return "repo-state"
    if any(token in lowered for token in ("npm install", "pnpm add", "yarn add", "pip install", "uv add")):
        return "dependency"
    if any(token in lowered for token in ("serve-static", "http.server", "npm run serve")):
        return "serve"
    if any(token in lowered for token in ("get-content", "select-string", "get-childitem", "rg ", "rg--", "cat ", "ls ", "dir ")):
        return "inspection"
    return "other"


def parse_patch_files(patch_text):
    added = []
    updated = []
    deleted = []
    moved_to = []

    for match in PATCH_FILE_RE.finditer(patch_text or ""):
        action, path = match.groups()
        normalized = path.strip()
        if action == "Add":
            added.append(normalized)
        elif action == "Update":
            updated.append(normalized)
        elif action == "Delete":
            deleted.append(normalized)

    for match in PATCH_MOVE_RE.finditer(patch_text or ""):
        moved_to.append(match.group(1).strip())

    return {
        "added": added,
        "updated": updated,
        "deleted": deleted,
        "moved_to": moved_to,
        "all": dedupe(added + updated + deleted + moved_to),
    }


def dedupe(values):
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def parse_tool_call(message, include_raw):
    if not message or not message.startswith(TOOLCALL_PREFIX):
        return None

    body = message[len(TOOLCALL_PREFIX) :]

    if body.startswith("apply_patch "):
        patch_text = body[len("apply_patch ") :]
        files = parse_patch_files(patch_text)
        item = {
            "tool": "apply_patch",
            "summary": f"apply_patch files={len(files['all'])}",
            "files": files,
        }
        if include_raw:
            item["raw_excerpt"] = excerpt(patch_text, 1200)
        return item

    tool_name, separator, payload_text = body.partition(" ")
    payload = safe_json_loads(payload_text) if separator else None
    item = {
        "tool": tool_name,
        "summary": tool_name,
    }

    if tool_name == "shell_command" and isinstance(payload, dict):
        command = payload.get("command")
        item["command"] = command
        item["command_kind"] = classify_shell_command(command)
        item["workdir"] = payload.get("workdir")
        item["summary"] = excerpt(command, 160)
    elif tool_name == "update_plan" and isinstance(payload, dict):
        plan = payload.get("plan") or []
        item["plan"] = plan
        item["explanation"] = payload.get("explanation")
        statuses = [f"{step.get('status')}:{step.get('step')}" for step in plan if isinstance(step, dict)]
        item["summary"] = " | ".join(statuses[:6]) if statuses else "update_plan"
    else:
        if isinstance(payload, dict):
            item["payload"] = payload
            item["summary"] = excerpt(json.dumps(payload, ensure_ascii=False, sort_keys=True), 160)
        elif payload_text:
            item["payload_excerpt"] = excerpt(payload_text, 320)
            item["summary"] = excerpt(payload_text, 160)

    if include_raw and payload_text and "payload_excerpt" not in item and "payload" not in item:
        item["raw_excerpt"] = excerpt(payload_text, 1200)

    return item


def find_log_databases(codex_home):
    if not codex_home.exists():
        return []
    return sorted(codex_home.glob("logs_*.sqlite"))


def query_thread_rows(database_path, thread_id):
    try:
        connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, ts, ts_nanos, level, target, message, file, line
                FROM logs
                WHERE thread_id = ?
                ORDER BY id
                """,
                (thread_id,),
            )
            return cursor.fetchall()
        finally:
            connection.close()
    except sqlite3.Error:
        return []


def build_bundle(thread_id, codex_home, include_raw):
    all_rows = []
    log_files = []

    for database_path in find_log_databases(codex_home):
        rows = query_thread_rows(database_path, thread_id)
        if rows:
            all_rows.extend((database_path, row) for row in rows)
            log_files.append(str(database_path))

    all_rows.sort(key=lambda item: (item[1][1], item[1][2], item[1][0]))

    if not all_rows:
        return {
            "thread_id": thread_id,
            "codex_home": str(codex_home),
            "log_files": [],
            "found": False,
            "error": "thread_id not found in local Codex logs",
        }

    tool_timeline = []
    shell_commands = []
    apply_patches = []
    update_plans = []
    touched_files = []
    target_counts = Counter()
    level_counts = Counter()

    first_ts = None
    last_ts = None

    for database_path, row in all_rows:
        row_id, ts, ts_nanos, level, target, message, file_name, line_number = row
        level_counts[level] += 1
        if target:
            target_counts[target] += 1

        if first_ts is None:
            first_ts = ts
        last_ts = ts

        tool_call = parse_tool_call(message, include_raw)
        if not tool_call:
            continue

        item = {
            "ts": ts,
            "ts_local": isoformat_local(ts),
            "log_id": row_id,
            "database": str(database_path),
            **tool_call,
        }
        tool_timeline.append(item)

        if item["tool"] == "shell_command":
            shell_commands.append(
                {
                    "ts_local": item["ts_local"],
                    "command_kind": item.get("command_kind"),
                    "command": item.get("command"),
                    "workdir": item.get("workdir"),
                }
            )
        elif item["tool"] == "apply_patch":
            apply_patches.append(
                {
                    "ts_local": item["ts_local"],
                    "files": item["files"],
                    **({"raw_excerpt": item.get("raw_excerpt")} if include_raw else {}),
                }
            )
            touched_files.extend(item["files"]["all"])
        elif item["tool"] == "update_plan":
            update_plans.append(
                {
                    "ts_local": item["ts_local"],
                    "explanation": item.get("explanation"),
                    "plan": item.get("plan", []),
                }
            )

    touched_files = sorted(set(touched_files))
    shell_kind_counts = Counter(item["command_kind"] for item in shell_commands if item.get("command_kind"))

    return {
        "thread_id": thread_id,
        "codex_home": str(codex_home),
        "log_files": log_files,
        "found": True,
        "time_window": {
            "start_local": isoformat_local(first_ts),
            "end_local": isoformat_local(last_ts),
        },
        "counts": {
            "log_rows": len(all_rows),
            "tool_calls": len(tool_timeline),
            "shell_commands": len(shell_commands),
            "apply_patches": len(apply_patches),
            "update_plans": len(update_plans),
            "touched_files": len(touched_files),
        },
        "level_counts": dict(level_counts),
        "target_counts": dict(target_counts.most_common(20)),
        "touched_files": touched_files,
        "next_read_targets": touched_files[:40],
        "shell_command_kind_counts": dict(shell_kind_counts),
        "tool_timeline": tool_timeline,
        "shell_commands": shell_commands,
        "apply_patches": apply_patches,
        "update_plans": update_plans,
    }


def render_markdown(bundle):
    if not bundle.get("found"):
        return "\n".join(
            [
                "# SESSION_CONTEXT",
                "",
                "## ERROR",
                "",
                "```json",
                json.dumps(bundle, ensure_ascii=False, indent=2),
                "```",
            ]
        )

    compact_timeline = []
    for item in bundle["tool_timeline"]:
        compact = {
            "ts_local": item["ts_local"],
            "tool": item["tool"],
            "summary": item.get("summary"),
        }
        if item["tool"] == "shell_command":
            compact["command_kind"] = item.get("command_kind")
            compact["workdir"] = item.get("workdir")
        if item["tool"] == "apply_patch":
            compact["files"] = item.get("files", {}).get("all", [])
        compact_timeline.append(compact)

    sections = [
        "# SESSION_CONTEXT",
        "",
        "## META",
        "",
        "```json",
        json.dumps(
            {
                "thread_id": bundle["thread_id"],
                "codex_home": bundle["codex_home"],
                "log_files": bundle["log_files"],
                "time_window": bundle["time_window"],
                "counts": bundle["counts"],
                "shell_command_kind_counts": bundle["shell_command_kind_counts"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## TOUCHED_FILES",
        "",
        "```json",
        json.dumps(bundle["touched_files"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## UPDATE_PLANS",
        "",
        "```json",
        json.dumps(bundle["update_plans"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## TOOL_TIMELINE",
        "",
        "```json",
        json.dumps(compact_timeline, ensure_ascii=False, indent=2),
        "```",
        "",
        "## SHELL_COMMANDS",
        "",
        "```json",
        json.dumps(bundle["shell_commands"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## APPLY_PATCHES",
        "",
        "```json",
        json.dumps(bundle["apply_patches"], ensure_ascii=False, indent=2),
        "```",
    ]
    return "\n".join(sections)


def main():
    args = parse_args()
    codex_home = resolve_codex_home(args.codex_home)
    bundle = build_bundle(args.thread_id, codex_home, args.include_raw)

    if args.format == "json":
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(bundle))

    if not bundle.get("found"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
