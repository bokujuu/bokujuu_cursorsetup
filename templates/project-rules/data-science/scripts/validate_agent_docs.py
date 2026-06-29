# -*- coding: utf-8 -*-
"""Minimal consistency check between AGENTS.md and docs/agent/."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "AGENTS.md"
AGENT_README = REPO_ROOT / "docs" / "agent" / "README.md"


def main() -> int:
    errors: list[str] = []

    if not AGENTS.is_file():
        errors.append("Missing AGENTS.md at repo root")
    if not AGENT_README.is_file():
        errors.append("Missing docs/agent/README.md")

    if AGENTS.is_file():
        text = AGENTS.read_text(encoding="utf-8")
        if "docs/agent/" not in text and "docs/agent/README.md" not in text:
            errors.append("AGENTS.md should reference docs/agent/ as SoT")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}", file=sys.stderr)
        return 1

    print("[OK] Agent docs layout baseline satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
