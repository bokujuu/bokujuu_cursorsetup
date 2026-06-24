# -*- coding: utf-8 -*-
"""Fast watchdog tests (no heavy dependencies)."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

CI = Path(__file__).resolve().parent
WATCHDOG = CI / "run_with_watchdog.py"
PAUSE_PROBE = CI / "fixtures" / "pause_probe.bat"
FALSE_POS = CI / "fixtures" / "false_positive_log.bat"
PY = sys.executable
EXIT_HANG = 124


def _run_watchdog(
    *cmd_args: str,
    watchdog_args: list[str] | None = None,
    timeout: str = "30",
) -> tuple[int, float]:
    cmd = [PY, str(WATCHDOG)]
    if watchdog_args:
        cmd.extend(watchdog_args)
    cmd.extend(["--timeout", timeout, "--", "cmd", "/c", *cmd_args])
    start = time.monotonic()
    env = os.environ.copy()
    env["WATCHDOG_CWD"] = str(CI)
    result = subprocess.run(cmd, cwd=CI, env=env)
    return result.returncode, time.monotonic() - start


def test_pause_probe_detected() -> None:
    code, elapsed = _run_watchdog(str(PAUSE_PROBE), timeout="20")
    assert code == EXIT_HANG, f"expected {EXIT_HANG}, got {code}"
    assert elapsed < 15, f"pause hang took too long: {elapsed:.1f}s"


def test_false_positive_log_ok() -> None:
    code, _ = _run_watchdog(str(FALSE_POS), timeout="15")
    assert code == 0, f"expected 0, got {code}"


def test_no_watch_pause_skips_detection() -> None:
    code, elapsed = _run_watchdog(
        str(PAUSE_PROBE),
        watchdog_args=["--watch-pause", "off"],
        timeout="8",
    )
    assert code == EXIT_HANG, f"expected wall-clock {EXIT_HANG}, got {code}"
    assert elapsed >= 7, "should hit wall-clock timeout"


def main() -> int:
    tests = [
        ("T1 pause_probe", test_pause_probe_detected),
        ("T3 false_positive", test_false_positive_log_ok),
        ("T2 no-watch wall-clock", test_no_watch_pause_skips_detection),
    ]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"[OK] {name}")
        except AssertionError as exc:
            failed += 1
            print(f"[FAIL] {name}: {exc}", file=sys.stderr)
        except Exception as exc:
            failed += 1
            print(f"[FAIL] {name}: {exc!r}", file=sys.stderr)
    print(f"[SUMMARY] OK={len(tests) - failed} FAIL={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
