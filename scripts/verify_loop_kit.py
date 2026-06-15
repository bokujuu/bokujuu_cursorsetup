# -*- coding: utf-8 -*-
"""loop-orchestration テンプレ同梱とドキュメント参照を機械検証する。"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT = REPO_ROOT / "templates" / "loop-orchestration"

REQUIRED_KIT_FILES = [
    "README.md",
    "PROMPT.md.template",
    "ROADMAP.md.template",
    "progress.txt.template",
    "prd.json.template",
    "run-once.ps1",
    "ralph.ps1",
    "ralph.mjs",
    "ralph.sh",
    "start-bridge.ps1",
]

REQUIRED_SNIPPETS: dict[Path, list[str]] = {
    REPO_ROOT / "docs" / "loop-engineering.md": [
        "Tier 1",
        "workaround F",
        "@cursor/sdk",
        "WinError 10038",
        "composer-2.5",
    ],
    KIT / "README.md": [
        "Get-Content PROMPT.md | cursor-agent -p",
        "composer-2.5",
        "ralph.mjs",
    ],
    KIT / "run-once.ps1": [
        "composer-2.5",
        "--trust",
        "Get-Content",
    ],
    KIT / "ralph.mjs": [
        "@cursor/sdk",
        "composer-2.5",
    ],
}

OPTIONAL_PATHS = [
    REPO_ROOT / "skills" / "ralph-loop" / "references" / "operational-guide.md",
    REPO_ROOT / "docs" / "pr" / "010-loop-orchestration-kit.md",
]


def fail(messages: list[str]) -> int:
    for msg in messages:
        print(f"[FAIL] {msg}", file=sys.stderr)
    return 1


def ok(message: str) -> None:
    print(f"[OK] {message}")


def main() -> int:
    errors: list[str] = []

    if not KIT.is_dir():
        errors.append(f"Missing kit directory: {KIT}")
        return fail(errors)

    for name in REQUIRED_KIT_FILES:
        path = KIT / name
        if not path.is_file():
            errors.append(f"Missing kit file: {path.relative_to(REPO_ROOT)}")
        else:
            ok(f"kit file present: {name}")

    for path, snippets in REQUIRED_SNIPPETS.items():
        if not path.is_file():
            errors.append(f"Missing doc/script: {path.relative_to(REPO_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}: required snippet missing: {snippet!r}"
                )
        if path.is_file():
            ok(f"snippets in {path.relative_to(REPO_ROOT)}")

    for path in OPTIONAL_PATHS:
        if path.is_file():
            ok(f"optional present: {path.relative_to(REPO_ROOT)}")
        else:
            print(f"[WARN] optional missing: {path.relative_to(REPO_ROOT)}")

    if errors:
        return fail(errors)

    print("verify_loop_kit: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
