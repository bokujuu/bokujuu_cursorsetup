---
name: agent-loop-guardrails
description: >-
  Design explicit stop conditions and budgets for autonomous agent loops—max
  steps, token/wall-clock caps, no-progress detection, and safe escalation.
  Use when building or reviewing Ralph-style loops, tool-calling agents, or
  long-running automations—not for inner-loop autonomy (anti-human-bottleneck)
  or recovery after drift (agent-handoff-recovery).
disable-model-invocation: false
---

# Agent Loop Guardrails

Autonomous loops need **hard stop conditions** the model cannot override. Without them, agents spin, burn tokens, or act unsafely. Synthesized from [2026 agent production patterns](https://promtable.com/guides/ai-agents-2026).

## When to use

- Designing or reviewing an outer loop (`ralph-loop`, cron automation, tool-calling agent).
- Agent runs exceed expected steps/time without finishing.
- Same plan/summary repeats across iterations (stuck loop).
- Production readiness review before enabling unattended execution.

Do **not** use when:

- Recovering from wrong-track work mid-session → `agent-handoff-recovery`.
- Deciding whether to ask the human inside a single run → `anti-human-bottleneck` (opposite default: keep going).
- Evaluating prompt wording quality → `empirical-prompt-tuning`.

## Minimal loop model

```
observe state → choose action → execute tool → observe result → repeat until STOP
```

Guardrails define **STOP** and **escalate** — not the model.

## Stop conditions (implement ≥2)

| Guardrail | Typical threshold | On fire |
|-----------|-------------------|---------|
| **Max-step cap** | 15–30 iterations | Stop; return partial + reason |
| **Token budget** | Per-run or per-day cap | Stop; log spend |
| **Wall-clock budget** | e.g. 10–30 min user-facing | Stop; save checkpoint |
| **No-progress detector** | Same plan hash or summary N times | Escalate or stop |
| **Confidence threshold** | Self-score below floor | Escalate to human |
| **Verify gate** | Tests/lint not green | Do not mark story done (see `ralph-loop`) |

The model must **not** be the only authority for continuation.

## Workflow (design or review)

1. **Inventory loop** — Where does the loop start/end? What counts as one step?
2. **Pick guardrails** — At minimum: max-step + one progress signal + verify gate if code changes.
3. **Define escalation** — What artifact does the human get? (status block, diff, last N tool results)
4. **Wire enforcement** — Orchestrator/script enforces caps; do not rely on prompt alone.
5. **Log stops** — Record which guardrail fired (debugging stuck loops).
6. **Eval hook** — On prompt/tool change, rerun a small golden set; alarm on regression.

## No-progress detector (pattern)

Track a hash of `(plan_summary, open_todos, last_tool)` each step. If unchanged for **3** consecutive steps:

1. Stop implementation.
2. Emit status block (see `agent-handoff-recovery`).
3. Either switch strategy once, or escalate.

## Complements `ralph-loop`

| Layer | Skill | Role |
|-------|-------|------|
| Outer loop | `ralph-loop` | Run until PRD items pass verify |
| Stop safety | `agent-loop-guardrails` | Caps and stuck detection |
| Inner run | `anti-human-bottleneck` | Don't pause for routine approval |

Ralph's "tests decide done" is a **verify gate** guardrail. Add step/token caps for unattended runs.

## Red flags

| Rationalization | Reality |
|-----------------|---------|
| "The model will know when to stop" | Models over-continue; hard caps required |
| "Unlimited steps = more thorough" | Infinite loops and cost blowups |
| "We'll add guardrails after prod" | First stuck run becomes an incident |
| "One big prompt lists all stop rules" | Orchestrator must enforce; prompts are hints only |

## Verification

```bash
# Loop kit templates ship with orchestration scripts
test -f templates/loop-orchestration/ralph.sh
python3 scripts/verify_loop_kit.py
```

## Reference

- [references/sources.md](references/sources.md) — primary sources
- [references/skill-memory.md](references/skill-memory.md) — operational notes
