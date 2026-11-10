# -*- coding: utf-8 -*-
"""Refresh skills/imozuru from MaryCache/imozuru main.

The vendored tree is a copy of upstream skills/imozuru. This script replaces
that copy from upstream main, then adds only the upstream LICENSE and
references/sources.md. It does not edit SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_URL = "https://github.com/MaryCache/imozuru.git"
UPSTREAM_WEB = "https://github.com/MaryCache/imozuru"
UPDATE_COMMAND = "python scripts/update_imozuru.py"
JST = timezone(timedelta(hours=9))


def clone_upstream(dest: Path) -> str:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", "main", UPSTREAM_URL, str(dest)],
        check=True,
        env=env,
    )
    result = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def upstream_version(upstream_root: Path) -> str:
    path = upstream_root / ".claude-plugin" / "plugin.json"
    if not path.is_file():
        return ""
    data = json.loads(path.read_text(encoding="utf-8"))
    version = data.get("version")
    return str(version) if version else ""


def copyright_line(license_path: Path) -> str:
    for line in license_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Copyright"):
            return line
    return "Copyright (c) 2026 MaryCache"


def sources_markdown(sha: str, version: str, when: datetime, notice: str) -> str:
    release = f"、リリース {version}" if version else ""
    stamp = when.astimezone(JST).strftime("%Y/%m/%d %H:%M")
    return "\n".join([
        "# 出典",
        "",
        f"- リポジトリ: {UPSTREAM_WEB}",
        f"- スキル本文: {UPSTREAM_WEB}/blob/main/skills/imozuru/SKILL.md",
        f"- 取得日: {stamp}（JST）",
        f"- コミット: `{sha}`（取得時点の `main`{release}）",
        f"- ライセンス: MIT（{notice}）。`LICENSE` を同梱",
        "- 改変: `SKILL.md` / `scripts/` / `references/theory.md` / `assets/` は upstream 原文のまま。本ファイルと `LICENSE` の配置のみ追加",
        "- 同梱しない: リポジトリ直下の `tests/`、`examples/`、README、ブランド画像",
        f"- 更新: 本家 `main` を取り直すときは、このリポジトリのルートで `{UPDATE_COMMAND}` を実行する。手でコピーしない。その後 `scripts/install.ps1`（または `scripts/install.sh`）と `python scripts/verify_repo_setup.py`",
        "",
    ])


def file_map(skill_dir: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    if not skill_dir.is_dir():
        return files
    for path in skill_dir.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(skill_dir).as_posix()
        if rel == "references/sources.md":
            continue
        files[rel] = path.read_bytes()
    return files


def build_skill(upstream_root: Path, sha: str, when: datetime) -> Path:
    source = upstream_root / "skills" / "imozuru"
    license_path = upstream_root / "LICENSE"
    if not (source / "SKILL.md").is_file():
        raise SystemExit("upstream skills/imozuru/SKILL.md is missing")
    if not license_path.is_file():
        raise SystemExit("upstream LICENSE is missing")
    parent = Path(tempfile.mkdtemp(prefix="imozuru-built-"))
    built = parent / "skill"
    shutil.copytree(
        source,
        built,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copyfile(license_path, built / "LICENSE")
    (built / "references").mkdir(parents=True, exist_ok=True)
    (built / "references" / "sources.md").write_text(
        sources_markdown(sha, upstream_version(upstream_root), when, copyright_line(license_path)),
        encoding="utf-8",
    )
    return built


def is_current(dest: Path, built: Path, sha: str) -> bool:
    sources = dest / "references" / "sources.md"
    if not sources.is_file():
        return False
    text = sources.read_text(encoding="utf-8")
    return sha in text and UPDATE_COMMAND in text and file_map(dest) == file_map(built)


def refresh(upstream_root: Path, repo_root: Path, sha: str, when: datetime, *, dry_run: bool) -> str:
    if not sha:
        raise SystemExit("upstream commit SHA is empty")
    built = build_skill(upstream_root, sha, when)
    try:
        dest = repo_root / "skills" / "imozuru"
        if dest.is_symlink():
            raise SystemExit(f"refuse symlink: {dest}")
        if is_current(dest, built, sha):
            return "current"
        if dry_run:
            return "would-update"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(built, dest)
        return "updated"
    finally:
        shutil.rmtree(built.parent, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="imozuru-upstream-") as tmp:
        upstream = Path(tmp) / "imozuru"
        sha = clone_upstream(upstream)
        version = upstream_version(upstream)
        status = refresh(upstream, ROOT, sha, datetime.now(JST), dry_run=args.dry_run)
    release = f" ({version})" if version else ""
    print(f"[{status.upper()}] imozuru {sha}{release}")
    if status == "current":
        print("[NEXT] already matches upstream main")
    elif status == "would-update":
        print("[NEXT] re-run without --dry-run")
    else:
        print("[NEXT] .\\scripts\\install.ps1")
        print("[NEXT] python scripts\\verify_repo_setup.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
