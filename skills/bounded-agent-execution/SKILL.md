---
name: bounded-agent-execution
description: >-
  Enforce hard limits on agent loops: max steps, token/cost budgets, wall-clock
  timeouts, and no-progress detection before runaway execution. Use when
  designing or debugging agent harnesses, runaway tool loops, or production
  guardrails—not for outer Ralph orchestration (use ralph-loop) or prompt
  quality tuning (use empirical-prompt-tuning).
disable-model-invocation: false
---

# Bounded Agent Execution

Agents that decide when to stop can loop indefinitely. **Bounded execution** adds harness-level caps the model cannot override: step limits, budgets, timeouts, and progress checks. Pattern catalog: [Step Budget](https://github.com/agentpatternscatalog/patterns/blob/main/patterns/step-budget.md); architecture context: [arxiv 2602.10479](https://arxiv.org/html/2602.10479v1).

## When to use

- Designing or reviewing an agent loop (ReAct, plan-execute, tool-calling harness).
- Production incidents: runaway cost, infinite retries, identical tool calls.
- User asks for guardrails, circuit breakers, or max-iteration policy.
- Before shipping any autonomous tool that mutates data or spends API credits.

Skip when:

- Outer multi-iteration product loop → `ralph-loop` + `templates/loop-orchestration/`.
- Prompt ambiguity causing wrong behavior → `empirical-prompt-tuning`.
- Context window management only → `context-engineering`.

## Control layers (apply in harness, not in prompt)

| Control | What it limits | Typical default (tune per task) |
|---------|----------------|----------------------------------|
| **Max steps** | Tool calls or loop iterations | 10–20 focused; 50 research; hard ceiling |
| **Token / cost budget** | Cumulative spend per run | 5–10× expected task cost |
| **Wall-clock timeout** | Total elapsed time | 60–120s user-facing; higher for batch |
| **No-progress detector** | Stalled plan or repeated identical calls | Same tool+args ≥3 or unchanged summary N steps |
| **Partial result on cap** | User experience when stopped | Return best partial + explicit cap reason |

Caps must be enforced **outside** the model (loop counter, middleware, decorator)—never "please stop after 20 steps" in the system prompt alone.

## Workflow (mandatory order)

1. **Classify task** — Focused (classify, summarize) vs agentic (research, multi-file edit). Set caps accordingly.
2. **Define caps** — At minimum: `max_steps`. Add cost/timeout for production; add no-progress for tool-heavy agents.
3. **Implement enforcement** — Increment counter per iteration; check **before** each model or tool call.
4. **Define on-cap behavior** — Return partial output, escalate to human, or fail closed. Log which cap fired.
5. **Verify** — Run a stuck scenario (bad prompt or flaky tool); confirm harness stops before unbounded spend.

## Guard ordering (recommended)

Check cheap O(1) guards first:

1. Max steps / timeout
2. Cost budget
3. No-progress / semantic loop (hash of tool name + args)
4. Policy gates (human approval for destructive tools)

## Anti-patterns

| Anti-pattern | Risk | Fix |
|--------------|------|-----|
| Model decides when to stop | Unbounded loops | Hard `max_steps` in harness |
| Retry without cap | 3 layers × 4 retries → 64 calls | `max_retries_total` across chain |
| Only post-hoc dashboards | Damage already done | Enforce before tool executes |
| Same cap for all tasks | Research starved or chat overruns | Task-class presets |

## Report template (user-facing, Japanese)

```markdown
## Bounded Execution

- **タスク分類**: focused | agentic
- **設定**: max_steps=…, budget=…, timeout=…, no-progress=…
- **cap 時の挙動**: …
- **検証**: …（スタック再現 + 停止確認 OK/NG）
```

## Reference

- [reference.md](reference.md) — sources, preset table, boundaries
- [references/skill-memory.md](references/skill-memory.md) — operational notes from use
