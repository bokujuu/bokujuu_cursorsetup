# PR: 素早くテストを回す — 非対話検証ループ

## Summary

- 考え方 SoT [docs/fast-agent-test-loop.md](../fast-agent-test-loop.md) を追加
- グローバル skill `non-interactive-hang`（実測キャリブレーション + 秒単位 watchdog 自己検証）
- リポ展開用テンプレ `templates/project-ci/non-interactive-hang/` と `verify_non_interactive_hang_kit.py`

着想元: `excel-approval-platform-customer-registration` での pause ハング対策。本 PR は **実装のコピーではなく「速く verify を回す設計思想」** を汎用化する。

## 背景

エージェントは Shell で `.bat` や COM verify を回すが、失敗時 `pause` やモーダルで無期限待ちになり、1 回の verify がセッションを占有する。人間運用（失敗時 pause）は維持したまま、エージェント側だけ **予防 → 実測 timeout → 秒テスト** の三層で回数を増やす。

## Test plan

- [ ] `python scripts/verify_non_interactive_hang_kit.py` → exit 0、`[SUMMARY] OK=3 FAIL=0`
- [ ] `python scripts/verify_repo_setup.py --repo-only` → exit 0
- [ ] `.\scripts\install.ps1` 後 `~/.codex/skills/non-interactive-hang/SKILL.md` が存在
- [ ] [docs/rule-index.md](../rule-index.md) にタスク行が追加されている

## マージ後

1. `git pull` → `.\scripts\install.ps1`
2. 各アプリリポへ `templates/project-ci/non-interactive-hang/` を `scripts/ci/` にコピーし presets を編集
3. `AGENTS.md` にエージェント向け一行を追記
