# -*- coding: utf-8 -*-
"""Verify non-interactive-hang template files and run fast watchdog tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT = REPO_ROOT / "templates" / "project-ci" / "non-interactive-hang"

REQUIRED = [
    "README.md",
    "run_with_watchdog.py",
    "calibrate_timeout.py",
    "test_watchdog.py",
    "timeouts.json.example",
    "calibrate_presets.json.example",
    "fixtures/pause_probe.bat",
    "fixtures/false_positive_log.bat",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        path = KIT / Path(rel)
        if not path.is_file():
            errors.append(f"Missing: templates/project-ci/non-interactive-hang/{rel}")
        else:
            print(f"[OK] {rel}")

    test_script = KIT / "test_watchdog.py"
    if test_script.is_file():
        result = subprocess.run(
            [sys.executable, str(test_script)],
            cwd=KIT,
            check=False,
        )
        if result.returncode != 0:
            errors.append("test_watchdog.py failed in template kit")
        else:
            print("[OK] test_watchdog.py passed")

    if errors:
        for msg in errors:
            print(f"[FAIL] {msg}", file=sys.stderr)
        return 1

    print("verify_non_interactive_hang_kit: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
