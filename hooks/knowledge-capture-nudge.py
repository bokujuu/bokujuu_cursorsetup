# -*- coding: utf-8 -*-
"""Cursor hook: remind agents to persist reusable judgments to knowledge-base.

Events: sessionStart (additional_context), stop (followup if uncommitted Markdown).
Fails open. ASCII stdout for Windows consoles.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


DESK_HINT = (
    "Reusable judgments belong in bokujuu/knowledge-base, not a longer AGENTS.md. "
    "Start from docs/desk.md. If this session found a structure, failure, or restart "
    "state, load capture-external-intelligence. Prefer ctx search for prior sessions."
)


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


def _uncommitted_markdown(root: Path) -> list[str]:
    if not (root / ".git").exists() and not (root / ".git").is_file():
        return []
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "--", "*.md", "*.mdc"],
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    names: list[str] = []
    for line in proc.stdout.splitlines():
        path = line[3:].strip() if len(line) > 3 else ""
        if path:
            names.append(path.replace("\\", "/"))
    return names[:8]


def main() -> int:
    event = (sys.argv[1] if len(sys.argv) > 1 else "stop").strip().lower()
    data = _read_input()

    roots = [root for root in _workspace_roots(data)
             if (root / '.cursor' / 'knowledge-capture.local.md').is_file()]
    if not roots:
        print('{}')
        return 0

    if event in ("sessionstart", "session_start"):
        print(json.dumps({"additional_context": DESK_HINT}, ensure_ascii=True))
        return 0

    if event == "stop":
        md_hits: list[str] = []
        for root in roots:
            if root.is_dir():
                md_hits.extend(_uncommitted_markdown(root))
        if not md_hits:
            print("{}")
            return 0
        msg = (
            "Uncommitted Markdown in this workspace: "
            + ", ".join(md_hits[:5])
            + ". If any of it is reusable judgment, capture it with "
            "capture-external-intelligence into bokujuu/knowledge-base "
            "(desk.md / library layer), then PR only if the user asked."
        )
        print(json.dumps({"followup_message": msg}, ensure_ascii=True))
        return 0

    print("{}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("{}", file=sys.stdout)
        print(f"[knowledge-capture-nudge] {exc}", file=sys.stderr)
        raise SystemExit(0)
