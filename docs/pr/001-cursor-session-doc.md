# PR: Cursor 向け session-doc スキルへ置き換え

## Summary

- `codex-session-doc`（Codex SQLite ログ用）を廃止し、`cursor-session-doc`（Cursor `agent-transcripts/*.jsonl` 用）を追加
- 抽出スクリプト `skills/cursor-session-doc/scripts/extract_session_context.py` を同梱
- PR 練習用に `.github/PULL_REQUEST_TEMPLATE.md` を追加

## 背景

Cursor の過去チャットを thread / session ID だけで引き継ぎたい場合、Codex のログ DB ではなく `%USERPROFILE%\.cursor\projects\...\agent-transcripts\` の jsonl を読む必要がある。

## Test plan

- [ ] 既知の session ID で抽出:

```powershell
cd C:\CursorPJs\bokujuu_cursorsetup
python skills/cursor-session-doc/scripts/extract_session_context.py `
  --session-id 8c0e4ff5-d570-46d1-82ee-c5103a76736e `
  --workspace-slug c-Users-dsakiyama-Documents-Obsidian-Vault `
  --format markdown
```

- [ ] `found: true` かつ `touched_files` / `tool_timeline` が空でないこと
- [ ] マージ後: `.\scripts\install.ps1` で `%USERPROFILE%\.codex\skills\cursor-session-doc` にコピーされること

## マージ後（利用者）

1. `git pull origin main`
2. `.\scripts\install.ps1`
3. 新チャットで「session ID を SESSION_DOC にまとめて」と依頼し、skill が読み込まれることを確認
