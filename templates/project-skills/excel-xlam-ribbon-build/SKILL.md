---
name: excel-xlam-ribbon-build
description: "Repo-local: RibbonX付きxlamをbas SoTから再現ビルドする。xlam / RibbonX / Excelアドイン作業で使う。"
---

# Excel Xlam Ribbon Build (repo-local)

Copy from global skill `excel-xlam-ribbon-build` and adapt paths to this repository.

## Setup

1. Copy `skills/excel-xlam-ribbon-build/` from [bokujuu_cursorsetup](https://github.com/bokujuu/bokujuu_cursorsetup) to `.codex/skills/excel-xlam-ribbon-build/`
2. Add entry to `.codex/practice-registry.json` (`status: draft` → `adopted` after verify)
3. Replace verification commands and file paths in this `SKILL.md`
4. Append outcomes to `references/skill-memory.md`

## Minimum scripts to implement

| Script | Role |
|--------|------|
| `ribbon_package.py` | `inject_ribbon`, `normalize_xlam_via_excel`, `verify_ribbon_package` |
| `update_xlam.py` | COM VBA inject → inject_ribbon → normalize → assert |
| `verify_*.py` | Static bas/callback + package checks |

See global skill `skills/excel-xlam-ribbon-build/SKILL.md` for OOXML rules and verification layers.
