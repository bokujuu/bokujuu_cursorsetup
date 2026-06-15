# PR: loop-orchestration キット（汎用ループ + エージェント基盤）

## Summary

- `templates/loop-orchestration/` — `ralph.ps1`, `ralph.mjs`, `run-once.ps1`, PROMPT/ROADMAP テンプレ
- `docs/loop-engineering.md` — 4層スタック、**SDK 安定優先（Tier A–F）**、モデル `composer-2.5`
- `scripts/verify_loop_kit.py`, `scripts/sdk-smoke.ps1` — 同梱検証と SDK スモーク
- `skills/ralph-loop/references/operational-guide.md` — `repo-agent-bootstrap` 接続手順
- MANIFEST / rule-index 更新

**PR 本文全文**: [temp/pr-body-loop-orchestration.md](../../temp/pr-body-loop-orchestration.md)

## 背景

- Obsidian Vault PoC: `/loop`, `cursor-agent -p`, `ralph.ps1` 3反復を検証済み
- **SDK 方針**: 安定して流せる経路のみキット化 — **Tier 2 F（TypeScript `@cursor/sdk`）を Windows SDK 第一候補**、Python 同期 `Client` は禁止
- `repo-agent-bootstrap` とセットで汎用ループ + エージェント基盤を提供

## 推奨スタック（要約）

| Tier | ID | 方式 |
|------|-----|------|
| 1 | A | CLI `ralph.ps1`（デフォルト） |
| 2 | F | `@cursor/sdk` TypeScript `ralph.mjs` |
| 2 | B | Python `AsyncClient` |
| 3 | C | 手動 Bridge |
| 4 | D | WSL `ralph.sh`（任意） |
| 5 | E | upstream 修正 |

## Test plan

- [ ] `python scripts/verify_loop_kit.py` 通過
- [ ] `templates/loop-orchestration/run-once.ps1`（`composer-2.5`）成功
- [ ] `ralph.ps1 -MaxIterations 2` で `loop-journal.txt` 更新
- [ ] `node templates/loop-orchestration/ralph.mjs`（`MAX_ITERATIONS=1`）— TS SDK
- [ ] `scripts/sdk-smoke.ps1`（任意、API キー要）

## マージ後

1. `git pull` → `.\scripts\install.ps1`
2. 対象 repo に `templates/loop-orchestration/` をコピー → `repo-agent-bootstrap` で基盤整備
3. `run-once.ps1` スモーク → `ralph.ps1` または `ralph.mjs`
