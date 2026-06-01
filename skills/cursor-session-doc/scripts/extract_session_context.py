# -*- coding: utf-8 -*-
"""Extract machine-oriented context from a Cursor agent transcript (.jsonl)."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from glob import glob
from pathlib import Path
from typing import Any

PATH_KEYS = ("path", "target_file", "target_notebook", "file_path")
SHELL_TOOLS = {"Shell", "run_terminal_cmd"}
EDIT_TOOLS = {"Write", "StrReplace", "Delete", "EditNotebook"}
READ_TOOLS = {"Read", "Glob", "Grep", "SemanticSearch", "ReadLints"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract session context from Cursor agent-transcripts jsonl."
    )
    parser.add_argument("--session-id", required=True, help="Cursor transcript UUID")
    parser.add_argument(
        "--projects-root",
        help="Override .cursor/projects root (default: %%USERPROFILE%%\\.cursor\\projects)",
    )
    parser.add_argument(
        "--workspace-slug",
        help="Limit search to one workspace slug under projects/",
    )
    parser.add_argument(
        "--include-subagents",
        action="store_true",
        help="Include subagents/*.jsonl summaries",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
    )
    return parser.parse_args()


def resolve_projects_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    profile = os.environ.get("USERPROFILE") or str(Path.home())
    return (Path(profile) / ".cursor" / "projects").resolve()


def iso_local(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().isoformat()


def excerpt(text: str | None, limit: int = 200) -> str | None:
    if not text:
        return None
    text = str(text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def classify_shell(command: str) -> str:
    lowered = (command or "").lower()
    if any(x in lowered for x in ("pytest", "ruff", "pyright", "npm test", "vitest")):
        return "validation"
    if any(x in lowered for x in ("git status", "git diff", "git log", "git commit")):
        return "git"
    if any(x in lowered for x in ("uv sync", "pip install", "npm install")):
        return "dependency"
    if any(x in lowered for x in ("rg ", "grep", "glob")):
        return "search"
    return "other"


def find_transcripts(
    projects_root: Path, session_id: str, workspace_slug: str | None
) -> list[Path]:
    session_id = session_id.removesuffix(".jsonl")
    base = projects_root
    if workspace_slug:
        base = projects_root / workspace_slug
    pattern = str(base / "**" / "agent-transcripts" / "**" / f"{session_id}.jsonl")
    return [Path(p).resolve() for p in glob(pattern, recursive=True)]


def path_from_tool(name: str, inp: dict[str, Any]) -> str | None:
    for key in PATH_KEYS:
        val = inp.get(key)
        if isinstance(val, str) and val.strip():
            return val.replace("\\", "/")
    if name in EDIT_TOOLS | READ_TOOLS:
        for key, val in inp.items():
            if isinstance(val, str) and ("/" in val or "\\" in val) and "." in val:
                if key not in ("description", "prompt", "pattern", "query", "search_term"):
                    return val.replace("\\", "/")
    return None


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def analyze_transcript(path: Path) -> dict[str, Any]:
    stat = path.stat()
    rows = parse_jsonl(path)
    tool_timeline: list[dict[str, Any]] = []
    shell_commands: list[dict[str, Any]] = []
    touched: set[str] = set()
    user_excerpts: list[str] = []
    tool_counts: Counter[str] = Counter()

    for row in rows:
        role = row.get("role")
        message = row.get("message") or {}
        parts = message.get("content") or []
        if not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text" and role == "user":
                text = part.get("text") or ""
                if "<user_query>" in text:
                    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
                    if m:
                        user_excerpts.append(excerpt(m.group(1)) or "")
            if part.get("type") != "tool_use":
                continue
            name = part.get("name") or "unknown"
            inp = part.get("input") or {}
            if not isinstance(inp, dict):
                inp = {}
            tool_counts[name] += 1
            entry: dict[str, Any] = {"tool": name, "summary": excerpt(json.dumps(inp, ensure_ascii=False))}
            fpath = path_from_tool(name, inp)
            if fpath:
                touched.add(fpath)
                entry["path"] = fpath
            if name in SHELL_TOOLS:
                cmd = inp.get("command") or ""
                kind = classify_shell(cmd)
                shell_commands.append({"command": excerpt(cmd, 400), "kind": kind})
                entry["command_kind"] = kind
            if name == "Task":
                entry["subagent_description"] = excerpt(inp.get("description") or inp.get("prompt"))
            tool_timeline.append(entry)

    slug = ""
    parts = path.parts
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 1 < len(parts):
            slug = parts[idx + 1]

    return {
        "transcript_path": str(path),
        "workspace_slug": slug,
        "mtime_local": iso_local(stat.st_mtime),
        "line_count": len(rows),
        "tool_counts": dict(tool_counts),
        "tool_timeline": tool_timeline,
        "shell_commands": shell_commands,
        "touched_files": sorted(touched),
        "user_query_excerpts": [u for u in user_excerpts if u][:20],
    }


def build_bundle(
    session_id: str,
    projects_root: Path,
    workspace_slug: str | None,
    include_subagents: bool,
) -> dict[str, Any]:
    paths = find_transcripts(projects_root, session_id, workspace_slug)
    if not paths:
        return {
            "session_id": session_id,
            "projects_root": str(projects_root),
            "found": False,
            "error": "transcript jsonl not found under agent-transcripts",
        }

    # Prefer main transcript (not under subagents/)
    main_paths = [p for p in paths if "subagents" not in p.parts]
    primary = main_paths[0] if main_paths else paths[0]
    primary_analysis = analyze_transcript(primary)

    subagent_files: list[str] = []
    if include_subagents:
        sub_paths = [p for p in paths if "subagents" in p.parts]
        subagent_files = [str(p) for p in sub_paths]

    return {
        "session_id": session_id,
        "projects_root": str(projects_root),
        "found": True,
        "primary_transcript": primary_analysis,
        "all_transcript_paths": [str(p) for p in paths],
        "subagent_transcripts": subagent_files,
        "next_read_targets": primary_analysis.get("touched_files", [])[:40],
    }


def render_markdown(bundle: dict[str, Any]) -> str:
    if not bundle.get("found"):
        return "# SESSION_CONTEXT\n\n## ERROR\n\n```json\n" + json.dumps(
            bundle, ensure_ascii=False, indent=2
        ) + "\n```\n"

    primary = bundle["primary_transcript"]
    sections = [
        "# SESSION_CONTEXT",
        "",
        "## META",
        "",
        "```json",
        json.dumps(
            {
                "session_id": bundle["session_id"],
                "projects_root": bundle["projects_root"],
                "workspace_slug": primary.get("workspace_slug"),
                "transcript_path": primary.get("transcript_path"),
                "mtime_local": primary.get("mtime_local"),
                "counts": {
                    "jsonl_lines": primary.get("line_count"),
                    "tools": primary.get("tool_counts"),
                    "touched_files": len(primary.get("touched_files", [])),
                },
                "subagent_transcripts": bundle.get("subagent_transcripts"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## TOUCHED_FILES",
        "",
        "```json",
        json.dumps(primary.get("touched_files", []), ensure_ascii=False, indent=2),
        "```",
        "",
        "## USER_QUERY_EXCERPTS",
        "",
        "```json",
        json.dumps(primary.get("user_query_excerpts", []), ensure_ascii=False, indent=2),
        "```",
        "",
        "## TOOL_TIMELINE",
        "",
        "```json",
        json.dumps(primary.get("tool_timeline", []), ensure_ascii=False, indent=2),
        "```",
        "",
        "## SHELL_COMMANDS",
        "",
        "```json",
        json.dumps(primary.get("shell_commands", []), ensure_ascii=False, indent=2),
        "```",
    ]
    return "\n".join(sections) + "\n"


def main() -> int:
    args = parse_args()
    root = resolve_projects_root(args.projects_root)
    bundle = build_bundle(
        args.session_id,
        root,
        args.workspace_slug,
        args.include_subagents,
    )
    if args.format == "json":
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(bundle))
    return 0 if bundle.get("found") else 2


if __name__ == "__main__":
    sys.exit(main())
