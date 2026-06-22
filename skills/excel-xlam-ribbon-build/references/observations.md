# Observations — excel-xlam-ribbon-build

## Confirmed (2026-06-22, excel-addins)

- `inject_ribbon()` 直後の Excel COM Open→Save は、RibbonX Editor 無変更 Save と同等の正規化効果がある
- inject-only vs Excel-normalized の差分は主に `_rels/.rels` の relationship 順序と ZIP entry メタデータ。XML 本体・ContentType は一致しうる
- `customUI/_rels/customUI14.xml.rels` は imageMso のみの RibbonX では不要
- 静的 verify が通ってもリボン非表示になりうる（偽陽性）。注入後正規化が実効対策
- COM 自動化では `IRibbonUI.onLoad` が観測できないことがある。最終確認は Excel 再起動後の対話操作

## Avoid

- ElementTree で `[Content_Types].xml` 全体を再シリアライズ（`ns0:` 付与で RibbonX 無効化）
- `customUI.xml` と `customUI14.xml` の二重同梱
- 複数 xlam で同一 callback 名（先にロードされた側が使われる）

## Related skills

- `excel-deliverable-quality` — `.xlsm` / 帳票成果物の COM ビルド規約
- `implement-with-practices` — ライブラリ固有の repo-local skill 起票
