---
name: excel-xlam-ribbon-build
description: Builds RibbonX-enabled Excel add-ins (.xlam) from git-managed VBA via OOXML zip injection and Excel COM package normalization. Use when automating xlam, RibbonX, customUI14, inject_ribbon, Office RibbonX Editor alternatives, or ribbon tab not appearing after Python zipfile injection.
---

# Excel Xlam Ribbon Build

Portable practice for **VBA + RibbonX add-in** builds on Windows (Excel COM required).

Companion to `excel-deliverable-quality` (workbook deliverables). This skill covers **`.xlam` add-ins** with Custom UI.

## Core insight

Python `zipfile` injection of `customUI14.xml` can pass static checks yet **fail to show the ribbon**. Office RibbonX Editor「XML 無変更 Save」で直る場合、原因は XML 内容より **OOXML パッケージ正規化**（`_rels/.rels`、Content Types、ZIP メタデータ）であることが多い。

**Fix:** inject 後に Excel COM で `Open → Save → Close` し、`customUI14.xml` が残っていることを zip で確認する。

## Recommended build flow

```
template.xlam
  → COM: inject *.bas → Save
  → inject_ribbon(customUI14.xml)     # zipfile; string-patch Content Types / rels
  → COM: Open → Save → Close           # normalize package
  → verify_ribbon_package()
```

## OOXML rules

| Check | Detail |
|-------|--------|
| Content Types | String-patch `Override` only; never ElementTree-reserialize `[Content_Types].xml` (`ns0:` breaks ribbon) |
| Part | `customUI/customUI14.xml` only (not legacy `customUI.xml`) |
| Namespace | `http://schemas.microsoft.com/office/2009/07/customui` |
| Root rel | `_rels/.rels` → `ui/extensibility` → `customUI/customUI14.xml` |
| Rel order | Insert ribbon rel before `extended-properties` (matches Excel Save) |
| Callbacks | Project-specific prefix (e.g. `ExcelToolkit_*`) for global uniqueness |

Use `imageMso` icons to avoid `customUI/_rels/` for embedded images.

## What not to do

- Office RibbonX Editor in CI (no official CLI; issue #214 open)
- Generate Callbacks if VBA callbacks are hand-maintained SoT
- Byte-level match to Editor output (semantic package equivalence is enough)
- Rely on COM `onLoad` alone for acceptance (use interactive Excel restart for final UI check)

## Verification layers

1. **Unit** — `inject_ribbon`, `patch_rels`, `verify_ribbon_package`
2. **Static** — ZIP integrity, rels, namespace, callback name match in `.bas`
3. **COM** — optional `ComTest_RibbonLoaded` (may not fire headless)
4. **Interactive** — ribbon tab visible after full Excel restart

## Deploy note

If ribbon UI is stale after copy to `%APPDATA%\Microsoft\AddIns`, clear `%LOCALAPPDATA%\Microsoft\Office\16.0\Excel\Ribbon` and restart Excel.

## Reference implementation

[excel-addins](https://github.com/bokujuu/excel-addins) — `scripts/ribbon_package.py`, `scripts/update_xlam.py`, `scripts/verify_excel_toolkit.py`

## Additional resources

- Pitfalls: [references/observations.md](references/observations.md)
- Sources: [references/sources.md](references/sources.md)
- Repo-local template: [templates/project-skills/excel-xlam-ribbon-build/](../../templates/project-skills/excel-xlam-ribbon-build/)
