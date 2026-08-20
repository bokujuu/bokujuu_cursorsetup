# bokujuu_cursorsetup

Cursor / Codex 用の **グローバル設定一式** を配布する Private リポジトリです。

- **User Rules 原本**: `user-rules/user-rule-cursor-communication.md`（コミュニケーション枠のみ。COM/VBA は `templates/project-rules/excel/` を各リポへ）
- **グローバル Skills（自作）**: `skills/` → インストール先は `%USERPROFILE%\.codex\skills\`
- **Cursor Hooks（任意）**: `hooks/` → `install.ps1` で `%USERPROFILE%\.cursor\hooks\` へ（handoff + knowledge-capture）
- **MCP 雛形**: `mcp/mcp.template.json`（Cursor 用。filesystem / memory / Codex Sol・Terra・Luna。任意は `mcp.optional.json`）
- **Codex MCP 登録**: `install.ps1 -InstallCodexMcp` / `install.sh --install-codex-mcp`（ユーザー全体の `~/.codex/config.toml`）

旧構成（`.cursor/commands`、古い MCP ドキュメント等）は **2026/06 時点で廃止** しました。

## クイックスタート

```powershell
git clone https://github.com/bokujuu/bokujuu_cursorsetup.git
cd bokujuu_cursorsetup
.\scripts\install.ps1
```

詳細は [INSTALL.md](INSTALL.md)。同梱一覧は [MANIFEST.md](MANIFEST.md)。エージェント向け入口は [AGENTS.md](AGENTS.md)。

検証（skill 追加・更新後。**install の後**に実行）:

```powershell
.\scripts\install.ps1
python scripts\verify_repo_setup.py
```

Linux / Cloud: `bash scripts/install.sh` のあと `python3 scripts/verify_repo_setup.py`

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
- Grok / Composer の使い分け: [docs/model-routing.md](docs/model-routing.md)
- エージェント検証の高速化: [docs/fast-agent-test-loop.md](docs/fast-agent-test-loop.md)

## 注意

- **Cursor User Rules**（Settings）は Git 連携されません。`user-rules/` を編集したら Settings へ手動反映してください。
- **Cursor 同梱 skills**（`~/.cursor/skills-cursor/`）はこの repo に含めません。
