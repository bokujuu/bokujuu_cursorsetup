# PR: context-engineering + harness-engineering

## Summary

- グローバル skill `context-engineering`（Write / Select / Compress / Isolate）
- グローバル skill `harness-engineering`（init/test/review ゲート・外部状態・自己完了禁止）
- MANIFEST / rule-index 更新

## 調査した概念

### 1. Context Engineering

- **出典**: [Lance Martin (2025/06)](https://rlancemartin.github.io/2025/06/23/context_engineering/), [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Manus lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- **重複チェック**: `rg` on `user-rules/` + `skills/` → `context engineering`, `compaction`, `write.*select.*compress` 等 **ヒットなし**。`ralph-loop` は「1 context window に収める」粒度のみで本フレームワークは未収録。
- **採用理由**: 2025 以降の横断的プラクティス。プロンプト調整だけでは長時間エージェントが破綻する問題に対し、既存の `ralph-loop`（外側ループ）と正交する「窓内の情報設計」を補完する。

### 2. Harness Engineering

- **出典**: [Anthropic — Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), [LangChain — Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering), [Gen α AI field guide (2026)](https://genalphai.com/agentic-loops-and-harness-engineering/), [agents.md](https://agents.md/)
- **重複チェック**: `rg` → `harness`, `verification gate`, `self-certif` 等 **ヒットなし**。`ralph-loop` は Ralph パターン特化で、init/test/review ゲートや evaluator 分離の一般化は未記載。`non-interactive-hang` はゲートの**実行方式**（非対話）でありハーネス全体ではない。
- **採用理由**: 「エージェントが自分で完了宣言しない」実行可能ゲートは本 repo の Ralph 系資産を一般化し、`repo-agent-bootstrap` / `AGENTS.md` 運用と接続できる。

### 検討したが今回見送った概念

- **Graduated autonomy / HITL パターン**（[Cordum HITL patterns](https://cordum.io/blog/human-in-the-loop-ai-patterns)）: `anti-human-bottleneck` と方向性が対立し、別 skill として設計・レビューが必要。今回の 2 件上限のため次回候補。

## Test plan

- [ ] `bash scripts/install.sh` 後 `~/.codex/skills/context-engineering/SKILL.md` が存在
- [ ] 同上で `harness-engineering/SKILL.md` が存在
- [ ] `python3 scripts/verify_repo_setup.py` exit 0
- [ ] `python3 temp/validate_new_skills.py` exit 0
- [ ] `ralph-loop` / `anti-human-bottleneck` との役割分担を目視

## マージ後

1. `git pull` → `bash scripts/install.sh`（または `install.ps1`）
2. 長時間エージェント運用では `harness-engineering` → `ralph-loop`、コンテキスト肥大時は `context-engineering` を参照
