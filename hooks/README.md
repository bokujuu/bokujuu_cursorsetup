# Cursor Hooks（任意）

`handoff-stop-check.py` はセッション終了時・サブエージェント完了時に、Plan todo の未整合や親エージェントの未統合を検知して follow-up を差し込みます。

## インストール

Windows では `scripts/install.ps1` が以下を実行します:

1. `hooks/handoff-stop-check.py` → `%USERPROFILE%\.cursor\hooks\`
2. `hooks/hooks.template.json` を展開して `%USERPROFILE%\.cursor\hooks.json` を生成（**既存がある場合は手動マージ**）

インストール後 **Cursor を再起動**し、Settings → **Hooks** で読み込みを確認してください。

## 手動マージ

既に `hooks.json` がある場合、`hooks.template.json` の `subagentStop` / `stop` エントリだけをコピーし、`{{HOOKS_DIR}}` を `%USERPROFILE%\.cursor\hooks` の実パスに置換してください。

## 関連 skill

- `skills/agent-handoff-recovery/` — エージェントが読む回復ワークフロー
- `docs/hooks-handoff-recovery.md` — 設計メモ
