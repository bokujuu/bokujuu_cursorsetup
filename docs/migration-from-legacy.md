# 旧構成からの移行（2026/06）

PR #3 以前の **`.cursor/` 配下一式**は廃止しました。`origin/main`（user-rules + skills + `mcp/`）に寄せてください。

## ディレクトリ対応

| 旧（廃止） | 新（現行） |
|------------|------------|
| `.cursor/commands/*.md` | `skills/*/SKILL.md`（下表参照） |
| `.cursor/mcp_enhanced.json` | `mcp/mcp.template.json` + [mcp/README.md](../mcp/README.md) |
| `.cursor/MCP_README.md` / `INSTALL_GUIDE.md` / `QUICKSTART.md` | [INSTALL.md](../INSTALL.md) + `mcp/README.md` |
| `.cursor/scripts/step_snapshot.py` | 廃止（セッション引き継ぎは `cursor-session-doc` skill） |
| （なし） | `user-rules/user-rule-cursor-communication.md` |
| （なし） | `scripts/install.ps1` / `install.sh` |

## Custom Commands → Skills

| 旧 command | 新 skill / 代替 |
|------------|-----------------|
| `websearch-resolve` | `skills/web-research-resolve/` |
| `code-review` | チャットで checklist 依頼、または `implement-with-practices` |
| `code-test` | プロジェクトのテスト手順 + `AGENTS.md` |
| `onboard-new` | プロジェクト README / `AGENTS.md` |
| `step-snapshot` | `cursor-session-doc`（引き継ぎ文書） |

## MCP の変更

| 項目 | 旧 | 新 |
|------|-----|-----|
| 同梱 | `playwright` / `serena` をデフォルト同梱 | テンプレは filesystem / memory / blender。任意は `mcp/mcp.optional.json` |
| context7 | テンプレ同梱だった時期あり | **非同梱**（不要のため削除） |
| Codex | 単一 `codex` エントリ、または未同梱 | いったん Sol / Terra / Luna を同梱した。2026/11/10 に GPT-5.6 を呼ばないため雛形から外した |
| GitHub PAT | プレースホルダ表記が不統一 | `Bearer YOUR_GITHUB_PAT_HERE`（optional・`mcp.json` は gitignore） |
| filesystem ルート | `"."` | テンプレ同様。**プロジェクト絶対パスへの差し替えを推奨**（[mcp/README.md](../mcp/README.md)） |

## ローカル main が古い枝に残っている場合

```powershell
git fetch origin
git checkout main
git reset --hard origin/main
.\scripts\install.ps1
```

`73ab3e9`（move-under-dot-cursor）と `64bdfff`（全面刷新）は**履歴が分岐**しています。古い `.cursor/` 枝へのマージは不要です。

## 更新履歴

- 2026/06/01 16:30: 初版（新構成への整合ドキュメント）
- 2026/11/10 23:25: `codex-sol` / `codex-terra` / `codex-luna` を雛形とインストーラから削除
