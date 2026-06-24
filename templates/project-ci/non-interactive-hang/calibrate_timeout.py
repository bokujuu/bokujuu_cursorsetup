# -*- coding: utf-8 -*-
"""Measure successful runs and write timeouts.json (p95 * 1.5 + 5)."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CI_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("WATCHDOG_CWD", CI_DIR.parents[1]))
PRESETS_JSON = CI_DIR / "calibrate_presets.json"
TIMEOUTS_JSON = CI_DIR / "timeouts.json"
FORMULA = "ceil(p95 * 1.5) + 5"


def _p95(samples: list[float]) -> float:
    if not samples:
        return 0.0
    ordered = sorted(samples)
    idx = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[idx]


def _timeout_from_p95(p95: float) -> int:
    return int(math.ceil(p95 * 1.5) + 5)


def _load_presets() -> dict[str, dict]:
    if not PRESETS_JSON.is_file():
        print(f"[ERROR] missing {PRESETS_JSON}", file=sys.stderr)
        return {}
    data = json.loads(PRESETS_JSON.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("calibrate_presets.json must be an object")
    return data


def _run_once(cmd: list[str], env: dict[str, str]) -> tuple[float, int]:
    child_env = os.environ.copy()
    child_env.update(env)
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=ROOT, env=child_env)
    elapsed = time.monotonic() - start
    return elapsed, result.returncode


def main() -> int:
    presets = _load_presets()
    if not presets:
        return 1

    parser = argparse.ArgumentParser(description="Calibrate watchdog timeouts")
    parser.add_argument("--key", required=True, choices=sorted(presets))
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    preset = presets[args.key]
    cmd = preset["command"]
    env = preset.get("env") or {}
    samples: list[float] = []

    print(f"[calibrate] key={args.key} samples={args.samples}")
    print(f"[calibrate] cmd={' '.join(cmd)} env={env}")

    for i in range(args.samples):
        print(f"[calibrate] run {i + 1}/{args.samples} ...")
        elapsed, code = _run_once(cmd, env)
        if code != 0:
            print(
                f"[ERROR] run {i + 1} failed exit={code} after {elapsed:.1f}s",
                file=sys.stderr,
            )
            return code
        samples.append(elapsed)
        print(f"[calibrate] run {i + 1} OK {elapsed:.1f}s")

    p95 = _p95(samples)
    timeout_sec = _timeout_from_p95(p95)
    entry = {
        "command": cmd,
        "env": env,
        "samples_sec": [round(s, 1) for s in samples],
        "p95_sec": round(p95, 1),
        "timeout_sec": timeout_sec,
        "formula": FORMULA,
        "measured_at": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d"),
    }

    print(f"[calibrate] p95={p95:.1f}s timeout_sec={timeout_sec} ({FORMULA})")

    if args.dry_run:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return 0

    data: dict = {}
    if TIMEOUTS_JSON.is_file():
        data = json.loads(TIMEOUTS_JSON.read_text(encoding="utf-8"))
    data[args.key] = entry
    TIMEOUTS_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] Wrote {TIMEOUTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
