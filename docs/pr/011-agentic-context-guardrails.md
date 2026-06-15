# PR: agentic-context-engineering + agent-loop-guardrails

## Summary

- グローバル skill `agentic-context-engineering`（ACE: 増分 delta 更新でプレイブックを進化）
- グローバル skill `agent-loop-guardrails`（エージェントループの停止条件・予算・無進捗検知）
- MANIFEST / rule-index 更新

## 調査した概念・出典

### 1. Agentic Context Engineering (ACE)

| 項目 | 内容 |
|------|------|
| 概念 | コンテキストを「縮めるプロンプト」ではなく **進化するプレイブック** として扱い、Generator / Reflector / Curator の役割分離で **増分 delta 更新**（add/edit/remove by id）のみ許可する |
| 出典 | [arxiv 2510.04618](https://arxiv.org/html/2510.04618), [ace-agent/ace](https://github.com/ace-agent/ace), [Agent Patterns Catalog](https://www.agentpatternscatalog.org/patterns/agentic-context-engineering-playbook/) |
| 重複チェック | `rg` on `user-rules/` + `skills/`: `context collapse`, `brevity bias`, `ACE`, `playbook` → **ヒットなし**。`skill-memory` の追記運用はあるが ACE の役割分離・全面書き換え禁止は未収録 |
| 採用理由 | 2025 後半〜2026 に横断的に引用される汎用パターン。`skill-lifecycle` / `retrospective-codify` と補完関係で重複しない |

### 2. Agent loop guardrails（停止条件・予算）

| 項目 | 内容 |
|------|------|
| 概念 | 自律ループに **max-step / token・wall-clock 予算 / 無進捗検知 / verify gate** を実装し、モデル任せの継続を禁止する |
| 出典 | [AI agents in 2026](https://promtable.com/guides/ai-agents-2026), [Leanware agent architecture](https://leanware.co/insights/ai-agent-architecture-concepts-components-best-practices) |
| 重複チェック | `rg`: `stop condition`, `max-step`, `token budget`, `guardrail` → **ヒットなし**。`ralph-loop` は verify による完了判定のみ。`anti-human-bottleneck` は「止まるな」側 |
| 採用理由 | 無人ループ（Ralph / cron automation）の本番化で共通の必須設計。ライブラリ非依存 |

### 検討したが今回見送った概念

| 概念 | 理由 |
|------|------|
| Agent trajectory eval suite | `empirical-prompt-tuning` がプロンプト品質評価を既にカバー。本番トラジェクトリ eval は別 skill 化の余地あり（次回候補） |
| Planner-executor split | フレームワーク実装寄り。guardrails skill に軽く言及済み |

## 分類（retrospective-codify 判定表）

| 概念 | 判定 | 出力先 |
|------|------|--------|
| ACE | 複数ステップ・判断を伴う | 新規 skill `agentic-context-engineering` |
| Loop guardrails | 複数ステップ・判断を伴う | 新規 skill `agent-loop-guardrails` |

practice-registry は **repo-local** 向けのため、グローバル skill 追加のみでは未登録（`skill-lifecycle` 手順に準拠）。

## Test plan

- [ ] `bash scripts/install.sh` 後 `~/.codex/skills/agentic-context-engineering/SKILL.md` が存在
- [ ] 同上 `agent-loop-guardrails/SKILL.md`
- [ ] `python3 temp/validate_new_skills.py` が PASS
- [ ] `python3 scripts/verify_loop_kit.py`（guardrails の検証コマンド）
- [ ] [docs/rule-index.md](../rule-index.md) から両 skill に辿れる

## マージ後

1. `git pull` → `bash scripts/install.sh`（または Windows: `.\scripts\install.ps1`）
2. ループ設計時は `ralph-loop` + `agent-loop-guardrails` を併用
3. skill-memory / AGENTS.md の改訂時は `agentic-context-engineering` の delta 原則に従う
