# 同梱マニフェスト

最終同期の想定元（ローカル）。`scripts/sync-from-local.ps1` で再取得できます。

## user-rules/

| ファイル | 同期元 |
|----------|--------|
| `user-rule-*.md` (10件) | `C:\CursorPJs\rulemaintenance\user-rule-*.md` |

## skills/（グローバル・自作のみ）

| スキル | 同期元 |
|--------|--------|
| `anti-human-bottleneck` | `%USERPROFILE%\.codex\skills\anti-human-bottleneck` |
| `codex-session-doc` | `%USERPROFILE%\.codex\skills\codex-session-doc` |
| `empirical-prompt-tuning` | `%USERPROFILE%\.codex\skills\empirical-prompt-tuning` |
| `implement-with-practices` | `%USERPROFILE%\.codex\skills\implement-with-practices` |
| `ralph-loop` | `%USERPROFILE%\.codex\skills\ralph-loop` |
| `retrospective-codify` | `%USERPROFILE%\.codex\skills\retrospective-codify` |

## 意図的に含めないもの

| 対象 | 理由 |
|------|------|
| `%USERPROFILE%\.cursor\skills-cursor\` | Cursor 製品同梱。Cursor が自動同期 |
| `%USERPROFILE%\.codex\skills\.system\` | Codex 同梱 |
| 各プロジェクトの `.cursor/skills/` | リポジトリローカル |
| Obsidian Vault の commands | ワークスペース専用 |
| 旧 `bokujuu_cursorsetup` の MCP・commands | 廃止 |
| `codex-primary-runtime`（空ディレクトリ） | 中身なしのため同梱しない |

## docs/

| ファイル | 同期元 |
|----------|--------|
| `rule-index.md` | `C:\CursorPJs\rulemaintenance\docs\rule-index.md` |
