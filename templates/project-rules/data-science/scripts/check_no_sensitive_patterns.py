# -*- coding: utf-8 -*-
"""Scan tracked and staged text for common secret patterns."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PATTERNS = (
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub PAT"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"(?i)api[_-]?key\s*=\s*['\"][^'\"]{8,}['\"]"), "api_key assignment"),
)


def git_diff_text() -> str:
    parts: list[str] = []
    for args in (
        ["diff", "--cached"],
        ["diff"],
    ):
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout:
            parts.append(result.stdout)
    return "\n".join(parts)


def main() -> int:
    blob = git_diff_text()
    if not blob.strip():
        print("[OK] No diff to scan")
        return 0

    hits: list[str] = []
    for pattern, label in PATTERNS:
        if pattern.search(blob):
            hits.append(label)

    if hits:
        print("[FAIL] Possible secrets in git diff:", file=sys.stderr)
        for h in hits:
            print(f"  - {h}", file=sys.stderr)
        return 1

    print("[OK] No common secret patterns in diff")
    return 0


if __name__ == "__main__":
    sys.exit(main())
