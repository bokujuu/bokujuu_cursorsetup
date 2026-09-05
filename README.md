# bokujuu_cursorsetup

Cursor / Codex 用の **グローバル設定一式** を配布する Private リポジトリです。

- **User Rules 原本**: `user-rules/user-rule-cursor-communication.md`（コミュニケーション枠のみ。COM/VBA は `templates/project-rules/excel/` を各リポへ）
- **グローバル Skills（自作）**: `skills/` → インストール先は `%USERPROFILE%\.codex\skills\`
- **Cursor Hooks（任意）**: `hooks/` → `install.ps1 -InstallHooks` で `%USERPROFILE%\.cursor\hooks\` へ（handoff + knowledge-capture）
- **MCP 雛形**: `mcp/mcp.template.json`（Cursor 用。filesystem / memory / blender / Codex Sol・Terra・Luna。任意は `mcp.optional.json`）
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

## 更新

GitHubの最新版をfetchし、未コミット変更を保護して同期します。本repoを原本として `skills/` を編集し、install → verify の順で反映します。`sync-from-local.ps1` による逆同期は使いません。
commit / push は依頼がある場合に行います。

2026-09-05に全22スキルを監査し、4件を退役、18件を維持・軽量化しました。[全件の判断と検証範囲](docs/astra-skill-audit.md)。新スキルは追加していません。

## ルール索引

- 適用の考え方: [docs/user-rules-guide.md](docs/user-rules-guide.md)
- タスク別の組み合わせ: [docs/rule-index.md](docs/rule-index.md)
- Astra の運用・モデル選択: [docs/model-routing.md](docs/model-routing.md)
- エージェント検証の高速化: [docs/fast-agent-test-loop.md](docs/fast-agent-test-loop.md)

## 注意

- **Cursor User Rules**（Settings）は Git 連携されません。`user-rules/` を編集したら Settings へ手動反映してください。
- **Cursor 同梱 skills**（`~/.cursor/skills-cursor/`）はこの repo に含めません。
