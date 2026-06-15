# bokujuu_cursorsetup

Cursor / Codex 用の **グローバル設定一式** を配布する Private リポジトリです。

- **User Rules 原本**: `user-rules/`（COM/VBA は `templates/project-rules/excel/` を各リポへ）
- **グローバル Skills（自作）**: `skills/` → インストール先は `%USERPROFILE%\.codex\skills\`
- **Cursor Hooks（任意）**: `hooks/` → `install.ps1` で `%USERPROFILE%\.cursor\hooks\` へ
- **MCP 雛形**: `mcp/mcp.template.json`（キーは各自で設定）

旧構成（`.cursor/commands`、古い MCP ドキュメント等）は **2026/06 時点で廃止** しました。

## クイックスタート

```powershell
git clone https://github.com/bokujuu/bokujuu_cursorsetup.git
cd bokujuu_cursorsetup
.\scripts\install.ps1
```

詳細は [INSTALL.md](INSTALL.md)。同梱一覧は [MANIFEST.md](MANIFEST.md)。エージェント向け入口は [AGENTS.md](AGENTS.md)。

検証（skill 追加・更新後）:

```powershell
python scripts\verify_repo_setup.py
```

## 更新（この PC → GitHub）

```powershell
cd C:\CursorPJs\bokujuu_cursorsetup
.\scripts\sync-from-local.ps1
git add -A
git status
git commit -m "chore: ローカルから user-rules / skills を再同期"
git push origin main
```

## ルール索引

- 適用の考え方: [docs/user-rules-guide.md](docs/user-rules-guide.md)
- タスク別の組み合わせ: [docs/rule-index.md](docs/rule-index.md)

## 注意

- **Cursor User Rules**（Settings）は Git 連携されません。`user-rules/` を編集したら Settings へ手動反映してください。
- **Cursor 同梱 skills**（`~/.cursor/skills-cursor/`）はこの repo に含めません。
