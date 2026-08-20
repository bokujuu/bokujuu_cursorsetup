# PR: capture-external-intelligence（机／書庫への知見化）

## Summary

- グローバル skill `capture-external-intelligence` を追加（knowledge-base が書庫、cursorsetup は手順）
- Hook `knowledge-capture-nudge.py`（`sessionStart` 注入、`stop` は未コミット Markdown 時）
- 過去セッションは [ctxrs/ctx](https://github.com/ctxrs/ctx) を優先

## 背景

常時 `AGENTS.md` を伸ばすと入口が重い。Decision-OS の「小さな机」と、既存の knowledge-base 分離（`github-knowledge-limits`）を、発火する skill / hook にする。旧 `retrospective-codify` は退役済みで、先に書庫・昇格は後、に置き換える。

## Test plan

- [ ] `.\scripts\install.ps1` 後、`%USERPROFILE%\.codex\skills\capture-external-intelligence\SKILL.md` がある
- [ ] `python scripts\verify_repo_setup.py` が exit 0
- [ ] `echo {} | python hooks/knowledge-capture-nudge.py sessionStart` が `additional_context` を返す
- [ ] 既存 `hooks.json` がある環境では [hooks/README.md](../../hooks/README.md) で `sessionStart` をマージ
- [ ] Cursor 再起動後 Settings → Hooks にエントリが見える
