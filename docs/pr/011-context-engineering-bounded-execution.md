# PR: context-engineering + bounded-agent-execution

## Summary

- グローバル skill `context-engineering`（write / select / compress / isolate）
- グローバル skill `bounded-agent-execution`（max steps / budget / no-progress）
- MANIFEST / rule-index / skill-lifecycle reference 更新

## 調査した概念

### 1. Context Engineering

- **概要**: エージェント軌跡の各ステップでコンテキスト窓に何を入れるかを設計する横断的 discipline。
- **出典**:
  - https://rlancemartin.github.io/2025/06/23/context_engineering/
  - https://www.langchain.com/blog/context-engineering-for-agents
  - https://github.com/langchain-ai/context_engineering

### 2. Bounded Agent Execution（Step Budget / Circuit Breaker）

- **概要**: モデル任せの停止判断に頼らず、ハーネス側でステップ数・コスト・無進捗を強制上限する。
- **出典**:
  - https://github.com/agentpatternscatalog/patterns/blob/main/patterns/step-budget.md
  - https://arxiv.org/html/2602.10479v1
  - https://promtable.com/guides/ai-agents-2026

## 重複チェック

| 概念 | 検索キー | user-rules/ | skills/ | 判定 |
|------|----------|-------------|---------|------|
| Context Engineering | `context engineering`, `write select compress`, `context window` | ヒットなし | ヒットなし（`ralph-loop` の context window 言及のみ、別概念） | **新規 skill** |
| Bounded Execution | `bounded`, `max steps`, `step budget`, `circuit breaker` | ヒットなし | ヒットなし（`loop-orchestration` の `MAX_ITERATIONS` は外側ループ） | **新規 skill** |
| Trajectory evaluation | `trajectory`, `golden test` | ヒットなし | `empirical-prompt-tuning` がプロンプト品質評価をカバー | **今回は不採用**（別軸） |

skill 化判断: `skill-lifecycle` lifecycle loop に従い、横断的手順 + 判断を伴うため global skill 新規。`retrospective-codify` 分類表では「複数ステップの手順や判断を伴う」→ skill。

## 採用理由

- 2025–2026 に横断的に定着した用語・パターンで、ライブラリ固有ではない。
- 既存 skill（`ralph-loop`, `empirical-prompt-tuning`, `implement-with-practices`）と境界を description で明示。
- 1 回の追加は 2 概念に抑制（肥大化回避）。

## Test plan

- [ ] `bash scripts/install.sh` 後 `~/.codex/skills/context-engineering/SKILL.md` が存在
- [ ] 同上で `bounded-agent-execution/SKILL.md` が存在
- [ ] `python3 temp/validate_new_skills.py` が exit 0
- [ ] `python3 scripts/verify_repo_setup.py` が exit 0
- [ ] [docs/rule-index.md](../rule-index.md) から新 skill に辿れる

## マージ後

1. `git pull` → `bash scripts/install.sh`（または `.\scripts\install.ps1`）
2. エージェント設計タスクで `context-engineering` / `bounded-agent-execution` を参照
