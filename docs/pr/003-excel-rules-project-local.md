# PR: COM/VBA ルールをプロジェクトローカルへ移行

## 背景

グローバル User Rules の `user-rule-com-automation` / `user-rule-vba-coding-policy`（合計約 550 行）は、Excel を触らないセッションでもコンテキストを消費していた。

## 変更

- `user-rules/` から上記 2 ファイルを**削除**
- `templates/project-rules/excel/` に `.mdc` 雛形を追加
- `docs/rule-index.md`, `docs/user-rules-guide.md`, `MANIFEST.md`, `user-rule-cursor-integrated.md` を更新

## 利用者アクション（マージ後）

1. `git pull` 後、Cursor **Settings → User Rules** から COM/VBA の記述を削除
2. Excel 運用リポ（例: htmlpcafmock）で `.cursor/rules/` を維持
3. 新規 Excel リポは `templates/project-rules/excel/README.md` に従いコピー

## 参照実装

- htmlpcafmock: `.cursor/rules/pcaf-excel-agent.mdc` 等
