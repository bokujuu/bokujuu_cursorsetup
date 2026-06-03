# User Rules 適用ガイド

Cursor の **Settings → Rules → User Rules** は Git と連携されません。`user-rules/` を更新したら、手動で Settings に反映してください。

## 推奨: 2 層運用

### 層 A — 常時（Settings に貼る）

- **`user-rule-cursor-integrated.md` のみ**（約210行）
- 口調・タスク分類・MCP方針・最小変更原則など共通枠をここに集約

### 層 B — タスク時（必要なときだけ）

次のいずれかで専門ルールを渡す:

1. チャットで「`user-rules/user-rule-python-coding-policy.md` を読んでから実装して」と明示
2. 該当 skill を起動（例: `implement-with-practices`、`agent-handoff-recovery`）
3. タスクに合わせて [rule-index.md](rule-index.md) の組み合わせから **2〜3 ファイル**を選び、該当セクションだけコピー

**層 B を全貼りは非推奨**（COM/VBA は含めない。合計目安 700 行以下）。

### Excel / COM / VBA

- **User Rules には載せない**（全セッションで数百行消費するため）
- Excel 運用があるリポだけ `templates/project-rules/excel/` を `.cursor/rules/` にコピー
- Settings から旧 `user-rule-com-automation` / `user-rule-vba-coding-policy` を削除

## 更新手順

1. このリポジトリで `user-rules/*.md` を編集
2. `git commit` / `push`
3. 他 PC: `git pull` 後、層 A を Settings に再貼り付け（差分確認）
4. 層 B は都度参照（またはプロジェクトの `AGENTS.md` に要約を書く）

## rulemaintenance リポジトリを使う場合

`scripts/sync-from-local.ps1` で `C:\CursorPJs\rulemaintenance` から再同期できます。  
**この repo（`bokujuu_cursorsetup`）を正とする場合**は、sync せずここで直接編集してください。

```powershell
.\scripts\sync-from-local.ps1 -RuleMaintenanceRoot "C:\CursorPJs\rulemaintenance"
```

## 関連

- タスク別の組み合わせ: [rule-index.md](rule-index.md)
- インストール全体: [../INSTALL.md](../INSTALL.md)
