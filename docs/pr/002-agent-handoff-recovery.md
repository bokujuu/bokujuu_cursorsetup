# PR: agent-handoff-recovery（指示ずれ・引き継ぎ回復）

## Summary

- グローバル skill `agent-handoff-recovery` を追加（Plan/SoT/verify の折り返し）
- 任意の Cursor Hooks（`handoff-stop-check.py`）と `install.ps1` 連携
- 層 B 用 `user-rule-agent-handoff-recovery.md` と設計ドキュメント

## 背景

マルチセッション・サブエージェント・曖昧な指示で、実装は進むが期待とずれることがある。プロジェクトごとの `AGENTS.md` だけでは横断パターンを拾いにくい。

## Test plan

- [ ] `.\scripts\install.ps1` 後、`%USERPROFILE%\.codex\skills\agent-handoff-recovery\SKILL.md` が存在
- [ ] `python hooks/handoff-stop-check.py stop` に stdin で `{"cwd":"<repo-with-open-plan-todos>"}` を渡し、`followup_message` が返る（PowerShell では `python -c` + subprocess 推奨）
- [ ] Cursor 再起動後 Settings → Hooks に `hooks.json` が表示される（新規インストール時）
- [ ] 新チャットで「期待と違う」→ skill が読まれ状況整理ブロックが出ること（任意）

## マージ後

1. `git pull` → `.\scripts\install.ps1`
2. 既存 `hooks.json` がある場合は [hooks/README.md](../../hooks/README.md) に従いマージ
3. 各プロジェクトに必要なら `.cursor/handoff-recovery.local.md` を追加
