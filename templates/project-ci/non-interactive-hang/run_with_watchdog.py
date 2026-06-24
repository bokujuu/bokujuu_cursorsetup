# -*- coding: utf-8 -*-
"""Run a subprocess with pause-pattern detection and wall-clock timeout.

Bat/cmd: detects Windows pause prompts (JP/EN) and kills after grace.
Exit 124 = hang (pause or wall-clock). Use --key for timeouts.json entries.

Copy to scripts/ci/ and set WATCHDOG_CWD to repo root if layout differs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

PAUSE_PATTERN = re.compile(
    r"(?i)(press any key to continue|続行するには何かキーを)"
)
DEFAULT_TIMEOUT_SEC = 600
PAUSE_GRACE_SEC = 5
TAIL_MAX_LINES = 200
EXIT_HANG = 124

CI_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("WATCHDOG_CWD", CI_DIR.parents[1]))
TIMEOUTS_JSON = CI_DIR / "timeouts.json"
CHILD_ENCODING = os.environ.get("WATCHDOG_CHILD_ENCODING", "cp932")


def _needs_pause_watch(argv: list[str]) -> bool:
    if not argv:
        return False
    first = Path(argv[0]).name.lower()
    if first in {"cmd.exe", "cmd"}:
        rest = " ".join(argv[1:]).lower()
        return ".bat" in rest or rest.endswith(".bat")
    return first.endswith(".bat") or first.endswith(".cmd")


def _kill_tree(pid: int) -> None:
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(pid)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def _maybe_hang_cleanup() -> None:
    script = os.environ.get("WATCHDOG_HANG_CLEANUP", "").strip()
    if not script:
        return
    path = Path(script)
    if not path.is_file():
        return
    subprocess.run(["cmd", "/c", str(path)], cwd=ROOT, check=False)


def _load_entry(key: str | None) -> tuple[int, dict[str, str]]:
    env_override = os.environ.get("WATCHDOG_TIMEOUT_SEC", "").strip()
    default_timeout = DEFAULT_TIMEOUT_SEC
    if env_override:
        try:
            default_timeout = max(1, int(env_override))
        except ValueError:
            pass

    if not key or not TIMEOUTS_JSON.is_file():
        return default_timeout, {}

    try:
        data = json.loads(TIMEOUTS_JSON.read_text(encoding="utf-8"))
        entry = data.get(key, {})
        if not isinstance(entry, dict):
            return default_timeout, {}
        timeout = max(1, int(entry.get("timeout_sec", default_timeout)))
        env = {str(k): str(v) for k, v in (entry.get("env") or {}).items()}
        return timeout, env
    except (OSError, ValueError, TypeError):
        return default_timeout, {}


class _StreamMonitor:
    def __init__(self, *, watch_pause: bool) -> None:
        self.watch_pause = watch_pause
        self._tail: deque[str] = deque(maxlen=TAIL_MAX_LINES)
        self._pause_at: float | None = None
        self._hang_reason: str | None = None
        self._lock = threading.Lock()

    def feed(self, text: str, stream_name: str) -> None:
        if not text:
            return
        sys.stdout.write(text)
        sys.stdout.flush()
        if not self.watch_pause:
            return
        with self._lock:
            for line in text.splitlines(keepends=True):
                self._tail.append(line)
            joined = "".join(self._tail)
            if PAUSE_PATTERN.search(joined):
                if self._pause_at is None:
                    self._pause_at = time.monotonic()
                elif time.monotonic() - self._pause_at >= PAUSE_GRACE_SEC:
                    match = PAUSE_PATTERN.search(joined)
                    pat = match.group(0) if match else "pause prompt"
                    self._hang_reason = (
                        f"[HANG] matched pattern={pat!r} stream={stream_name}"
                    )

    def poll_hang(self) -> str | None:
        with self._lock:
            if self._hang_reason:
                return self._hang_reason
            if (
                self._pause_at is not None
                and time.monotonic() - self._pause_at >= PAUSE_GRACE_SEC
            ):
                self._hang_reason = "[HANG] matched pause prompt (grace elapsed)"
                return self._hang_reason
            return None


def _pump(stream, monitor: _StreamMonitor, stream_name: str) -> None:
    try:
        for raw in iter(stream.readline, b""):
            text = raw.decode(CHILD_ENCODING, errors="replace")
            monitor.feed(text, stream_name)
    finally:
        stream.close()


def run(
    argv: list[str],
    *,
    timeout_sec: int,
    watch_pause: bool,
    child_env: dict[str, str] | None = None,
) -> int:
    if not argv:
        print("[ERROR] missing command", file=sys.stderr)
        return 2

    env = os.environ.copy()
    if child_env:
        env.update(child_env)

    proc = subprocess.Popen(
        argv,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    monitor = _StreamMonitor(watch_pause=watch_pause)
    threads = [
        threading.Thread(target=_pump, args=(proc.stdout, monitor, "stdout"), daemon=True),
        threading.Thread(target=_pump, args=(proc.stderr, monitor, "stderr"), daemon=True),
    ]
    for t in threads:
        t.start()

    deadline = time.monotonic() + timeout_sec
    exit_code: int | None = None
    hung = False
    try:
        while True:
            reason = monitor.poll_hang()
            if reason:
                print(reason, file=sys.stderr)
                _kill_tree(proc.pid)
                proc.wait(timeout=10)
                hung = True
                return EXIT_HANG

            if proc.poll() is not None:
                exit_code = proc.returncode
                break

            if time.monotonic() >= deadline:
                print(
                    f"[HANG] wall_clock timeout>{timeout_sec}s",
                    file=sys.stderr,
                )
                _kill_tree(proc.pid)
                proc.wait(timeout=10)
                hung = True
                return EXIT_HANG

            time.sleep(0.1)
    finally:
        for t in threads:
            t.join(timeout=2)
        if exit_code is None and not hung:
            try:
                exit_code = proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _kill_tree(proc.pid)
                return EXIT_HANG
        if hung:
            _maybe_hang_cleanup()

    return int(exit_code or 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Subprocess runner with hang watchdog")
    parser.add_argument("--key", help="timeouts.json entry (timeout_sec + env)")
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Wall-clock timeout seconds (overrides --key)",
    )
    parser.add_argument(
        "--watch-pause",
        choices=("auto", "on", "off"),
        default="auto",
        help="Pause prompt detection (default: auto for bat/cmd)",
    )
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command after --")
    args = parser.parse_args()
    argv = args.cmd
    if argv and argv[0] == "--":
        argv = argv[1:]

    timeout_from_key, entry_env = _load_entry(args.key)
    timeout_sec = args.timeout if args.timeout is not None else timeout_from_key

    if args.watch_pause == "on":
        watch_pause = True
    elif args.watch_pause == "off":
        watch_pause = False
    else:
        watch_pause = _needs_pause_watch(argv)

    return run(argv, timeout_sec=timeout_sec, watch_pause=watch_pause, child_env=entry_env)


if __name__ == "__main__":
    raise SystemExit(main())
