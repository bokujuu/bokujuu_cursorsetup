# Bounded Agent Execution — Reference

## Primary sources

| Source | URL | Takeaway |
|--------|-----|----------|
| Agent Patterns Catalog — Step Budget | https://github.com/agentpatternscatalog/patterns/blob/main/patterns/step-budget.md | Hard iteration cap; partial result on limit |
| arxiv 2602.10479 — Agentic AI Software Architecture | https://arxiv.org/html/2602.10479v1 | Bounded loops, circuit breakers, idempotent tools |
| promtable — AI agents 2026 reference | https://promtable.com/guides/ai-agents-2026 | Budget caps, no-progress detector, eval discipline |
| Augment Code — Agentic Design Patterns 2026 | https://www.augmentcode.com/guides/agentic-design-patterns | Bounded Execution / Circuit Breaker as production pattern |

## Preset table (starting points)

| Task class | max_steps | timeout | notes |
|------------|-----------|---------|-------|
| Classify / summarize / answer | 10–20 | 60s | Tight; escalate if cap hit |
| Code edit in one repo | 30–50 | 120s | Add no-progress on identical file reads |
| Research / multi-source | 50–100 | 300s+ | Pair with `context-engineering` compress |
| Autonomous pipeline | ≤200 | per-stage | Rethink architecture if higher needed |

## Implementation checklist

- [ ] Counter increments on every loop iteration (or tool call—pick one, document it).
- [ ] Check runs before model call and before side-effecting tools.
- [ ] Cap hit returns structured status (`reason: max_steps`, partial output).
- [ ] Logs include run id, step count, cap name, timestamp.
- [ ] Destructive tools behind human approval regardless of caps.

## Skill boundaries

| Skill | Scope |
|-------|--------|
| `bounded-agent-execution` | Harness limits and stop conditions |
| `ralph-loop` | Outer PRD/orchestration iterations (`MAX_ITERATIONS` in templates) |
| `anti-human-bottleneck` | When to ask human vs act autonomously |
| `context-engineering` | Token/window management inside a bounded run |

## Related

- [context-engineering](../context-engineering/SKILL.md) — reduce wasted steps via better context
- [templates/loop-orchestration/](../../templates/loop-orchestration/) — outer loop `MAX_ITERATIONS`
