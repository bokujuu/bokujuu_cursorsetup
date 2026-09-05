# -*- coding: utf-8 -*-
"""Sync owned skills; preserve replaced/retired content outside discovery roots."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import time
import uuid

ROOT = Path(__file__).resolve().parent.parent
MARKER = '.bokujuu-cursorsetup-managed.txt'
LEGACY = {'codex-session-doc', 'empirical-prompt-tuning', 'retrospective-codify',
          'skill-lifecycle', 'system-structure-viz'}


def rename_with_retry(source: Path, target: Path) -> None:
    # Windows file watchers can briefly hold a directory during discovery.
    for attempt in range(4):
        try:
            source.rename(target)
            return
        except PermissionError:
            if attempt == 3:
                raise
            time.sleep(0.25 * (attempt + 1))


def same_tree(source: Path, target: Path) -> bool:
    if not target.is_dir():
        return False
    def files(root):
        return {p.relative_to(root): p.read_bytes() for p in root.rglob('*')
                if p.is_file() and '__pycache__' not in p.parts}
    return files(source) == files(target)


def child(base: Path, name: str) -> Path:
    if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
        raise ValueError(f'Invalid managed name: {name!r}')
    path = base / name
    if path.is_symlink() or (path.exists() and path.resolve().parent != base.resolve()):
        raise ValueError(f'Refuse linked or escaped target: {path}')
    return path


def sync(home: Path, *, dry_run: bool = False,
         source: Path | None = None) -> list[Path]:
    source = source or ROOT / 'skills'
    current = {p.name: p for p in source.iterdir() if p.is_dir()}
    retired = set(json.loads((ROOT / 'scripts/retired-skills.json').read_text(encoding='utf-8')))
    for name, path in current.items():
        child(source, name)
        if not (path / 'SKILL.md').is_file():
            raise ValueError(f'Missing SKILL.md: {path}')
    products = ['.codex']
    # Existing per-product copies are synchronized too, avoiding shadowed stale skills.
    for product in ['.cursor', '.agents']:
        if (home / product / 'skills').is_dir():
            products.append(product)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    destinations = []
    for product in products:
        dest = home / product / 'skills'
        if dest.is_symlink() or (dest.exists() and dest.resolve() != dest.absolute()):
            raise ValueError(f'Refuse linked skill root: {dest}')
        marker = dest / MARKER
        previous = {line.strip() for line in marker.read_text(encoding='utf-8-sig').splitlines()
                    if line.strip()} if marker.exists() else set()
        # Auxiliary roots only update known repository names already installed there.
        names = set(current) if product == '.codex' else {
            n for n in current if (dest / n).exists() or n in previous}
        stale = (previous | LEGACY | retired) - set(current)
        for name in sorted(names | stale):
            child(dest, name)
        backup_root = home / '.codex/skill-archives' / stamp / product
        if backup_root.exists() or backup_root.resolve().parent.parent != (home / '.codex/skill-archives').resolve():
            raise ValueError(f'Invalid archive destination: {backup_root}')
        for name in sorted(names | stale):
            target = child(dest, name)
            if name in stale and not target.exists():
                continue
            if name in names and same_tree(current[name], target):
                print(f'[UNCHANGED] {target}')
                continue
            print(f'[{"ARCHIVE" if name in stale else "SYNC"}] {target}')
            if dry_run:
                continue
            dest.mkdir(parents=True, exist_ok=True)
            if name in names:
                # Complete copy before displacing an existing installation.
                backup_root.mkdir(parents=True, exist_ok=True)
                staging = backup_root / ('.staging-' + uuid.uuid4().hex)
                shutil.copytree(current[name], staging, ignore=shutil.ignore_patterns('__pycache__'))
            if target.exists():
                backup_root.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), str(child(backup_root, name)))
            if name in names:
                try:
                    rename_with_retry(staging, target)
                except OSError:
                    saved = backup_root / name
                    if saved.exists():
                        shutil.move(str(saved), str(target))
                    raise
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            marker.write_text(''.join(name + '\n' for name in sorted(names)), encoding='utf-8')
        destinations.append(dest)
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    sync(Path.home(), dry_run=args.dry_run)


if __name__ == '__main__':
    main()
