# 同梱マニフェスト

最終同期の想定元（ローカル）。`scripts/sync-from-local.ps1` で再取得できます（Windows・rulemaintenance 利用時）。

## user-rules/

| ファイル | 同期元（sync 利用時） |
|----------|------------------------|
| `user-rule-*.md` (10件) | `C:\CursorPJs\rulemaintenance\user-rule-*.md` |

**正の編集場所**: 本リポジトリを正とする場合は `user-rules/` を直接編集。

## skills/（グローバル・自作のみ）

| スキル | 備考 |
|--------|------|
| `anti-human-bottleneck` | sync 時は `%USERPROFILE%\.codex\skills\` から |
| `cursor-session-doc` | Cursor `agent-transcripts/*.jsonl` 用（本 repo 内で管理） |
| `empirical-prompt-tuning` | 同上 |
| `implement-with-practices` | 同上 |
| `ralph-loop` | 同上 |
| `retrospective-codify` | 同上 |
| `web-research-resolve` | 旧 `.cursor/commands/websearch-resolve` を skill 化 |

## docs/

| ファイル | 内容 |
|----------|------|
| `rule-index.md` | タスク別ルール参照 |
| `user-rules-guide.md` | Settings への貼り方（2 層運用） |
| `migration-from-legacy.md` | 旧 `.cursor/` からの移行 |
| `pr/` | PR 設計メモ |

## mcp/

| ファイル | 内容 |
|----------|------|
| `mcp.template.json` | 最小構成の雛形 |
| `mcp.optional.json` | playwright / serena（任意） |
| `README.md` | 適用手順・セキュリティ注意 |

## 意図的に含めないもの

| 対象 | 理由 |
|------|------|
| `%USERPROFILE%\.cursor\skills-cursor\` | Cursor 製品同梱。Cursor が自動同期 |
| `%USERPROFILE%\.codex\skills\.system\` | Codex 同梱 |
| 各プロジェクトの `.cursor/skills/` | リポジトリローカル |
| Obsidian Vault の commands | ワークスペース専用 |
| 旧 `.cursor/commands` / `mcp_enhanced.json` / `step_snapshot.py` | 廃止（移行表: `docs/migration-from-legacy.md`） |
| `codex-primary-runtime`（空ディレクトリ） | 中身なしのため同梱しない |
