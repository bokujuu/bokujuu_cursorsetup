# User Rules 適用ガイド

Cursor の **Settings → Rules → User Rules** は Git と連携されません。`user-rules/` を更新したら、手動で Settings に反映してください。

## 推奨: 1 ファイル運用

**`user-rules/user-rule-cursor-communication.md` のみ**を Settings → **Rules → User Rules** に貼る（約 50 行）。

- 口調・出力形式・最小変更の共通枠のみ
- チャット応答はです／ます。文書の文体・自然さは skills に委譲する
- コーディング規約・MCP 方針・Git 手順などの技術詳細は**含めない**
- 技術手順は各リポの `AGENTS.md`、`.cursor/rules/`、skills を正とする

### タスク別の技術ルール

専門ルールは User Rules ではなく、次のいずれかで渡す:

1. 対象リポの `AGENTS.md` と `.cursor/rules/`
2. 該当 skill を起動（例: `implement-with-practices`、`excel-deliverable-quality`）
3. [rule-index.md](rule-index.md) のタスク別参照

### Excel / COM / VBA

- **User Rules には載せない**
- Excel 運用があるリポだけ `templates/project-rules/excel/` を `.cursor/rules/` にコピー

## 更新手順

1. このリポジトリで `user-rules/user-rule-cursor-communication.md` を編集
2. `git commit` / `push`
3. 他 PC: `git pull` 後、Settings に再貼り付け（差分確認）

## rulemaintenance リポジトリを使う場合

`scripts/sync-from-local.ps1` で `C:\CursorPJs\rulemaintenance` から再同期できます。  
**この repo（`bokujuu_cursorsetup`）を正とする場合**は、sync せずここで直接編集してください。

```powershell
.\scripts\sync-from-local.ps1 -RuleMaintenanceRoot "C:\CursorPJs\rulemaintenance"
```

## 関連

- タスク別の skill / プロジェクトルール参照: [rule-index.md](rule-index.md)
- インストール全体: [../INSTALL.md](../INSTALL.md)
