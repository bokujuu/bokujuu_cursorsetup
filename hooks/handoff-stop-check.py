# -*- coding: utf-8 -*-
"""Cursor user hook: nudge agent after subagent stop or session stop.

Reads JSON from stdin (Cursor hooks). Fails open on any error.
Stdout: JSON with optional followup_message (ASCII only for Windows cp932).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _read_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    raw = raw.lstrip("\ufeff").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _workspace_roots(data: dict) -> list[Path]:
    roots: list[Path] = []
    for key in ("workspace_roots", "workspaceRoots", "roots"):
        val = data.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str) and item.strip():
                    roots.append(Path(item))
    cwd = data.get("cwd") or data.get("working_directory")
    if isinstance(cwd, str) and cwd.strip():
        p = Path(cwd)
        if p not in roots:
            roots.append(p)
    return roots


def _scan_plan_drift(root: Path) -> list[str]:
    plans_dir = root / ".cursor" / "plans"
    if not plans_dir.is_dir():
        return []
    issues: list[str] = []
    for plan in sorted(plans_dir.glob("*.plan.md")):
        text = plan.read_text(encoding="utf-8", errors="replace")
        pending = len(re.findall(r"status:\s*pending", text))
        in_prog = len(re.findall(r"status:\s*in_progress", text))
        if pending or in_prog:
            issues.append(f"{plan.name}: pending={pending} in_progress={in_prog}")
    return issues


def _local_extension_hint(root: Path) -> str:
    local = root / ".cursor" / "handoff-recovery.local.md"
    if local.is_file():
        return f"Read {local} for repo verify commands."
    agents = root / "AGENTS.md"
    if agents.is_file():
        return f"Read {agents} for verify commands."
    return ""


def main() -> int:
    event = (sys.argv[1] if len(sys.argv) > 1 else "stop").strip().lower()
    data = _read_input()

    roots = _workspace_roots(data)
    if not roots:
        print("{}")
        return 0

    plan_issues: list[str] = []
    hints: list[str] = []
    for root in roots:
        if root.is_dir():
            plan_issues.extend(_scan_plan_drift(root))
            hint = _local_extension_hint(root)
            if hint:
                hints.append(hint)

    if event == "subagentstop":
        msg = (
            "Subagent finished. Parent must: read changed files, run repo verify/build, "
            "update .cursor/plans todos if applicable, and reply with one integrated summary "
            "(not only 'subagent completed'). Load agent-handoff-recovery if unsure."
        )
        if hints:
            msg += " " + hints[0]
        print(json.dumps({"followup_message": msg}, ensure_ascii=True))
        return 0

    if event == "stop" and plan_issues:
        msg = (
            "Handoff check: open plan todos remain - "
            + "; ".join(plan_issues[:3])
            + ". Reconcile todo status vs git/verify before ending. "
            "Load agent-handoff-recovery skill."
        )
        if hints:
            msg += " " + hints[0]
        print(json.dumps({"followup_message": msg}, ensure_ascii=True))
        return 0

    print("{}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("{}", file=sys.stdout)
        print(f"[handoff-stop-check] {exc}", file=sys.stderr)
        raise SystemExit(0)
