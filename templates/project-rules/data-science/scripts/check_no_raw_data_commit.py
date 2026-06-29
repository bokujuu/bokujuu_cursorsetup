# -*- coding: utf-8 -*-
"""Fail if immutable data paths are staged or committed.

Customize IMMUTABLE_PREFIXES for the project layout.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Paths that must never appear in git index (prefix match)
IMMUTABLE_PREFIXES = (
    "data/raw/",
    "data/external/",
)


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]


def main() -> int:
    staged = git_lines("diff", "--cached", "--name-only")
    tracked_changes = git_lines("diff", "--name-only")
    candidates = set(staged) | set(tracked_changes)

    violations = [
        p
        for p in candidates
        if any(p.replace("\\", "/").startswith(prefix) for prefix in IMMUTABLE_PREFIXES)
    ]

    if violations:
        print("[FAIL] Immutable data paths must not be committed:", file=sys.stderr)
        for v in sorted(violations):
            print(f"  - {v}", file=sys.stderr)
        return 1

    print("[OK] No immutable data paths in staged/tracked changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
