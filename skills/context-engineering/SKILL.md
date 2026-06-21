---
name: context-engineering
description: >-
  Design and maintain what enters an agent's context window across a trajectory:
  write, select, compress, and isolate strategies. Use when long agent runs hit
  context limits, tool overload, stale history, or quality drops mid-session—not
  for one-off prompt wording (use empirical-prompt-tuning) or library-specific
  retrieval setup (use implement-with-practices).
disable-model-invocation: false
---

# Context Engineering

**Context engineering** is the discipline of filling the context window with the right information at each step of an agent's trajectory—not just writing a better initial prompt. Framework: [Lance Martin, Context Engineering for Agents](https://rlancemartin.github.io/2025/06/23/context_engineering/) (write / select / compress / isolate).

## When to use

- Agent runs exceed ~70% of the context window or trigger auto-compaction.
- Too many tools confuse tool selection; descriptions overlap.
- Long multi-turn sessions lose early decisions or hallucinate missing state.
- Designing a new agent harness, sub-agent split, or memory tiers.
- User asks how to manage context, memory, or token budget across steps.

Skip when:

- One-shot prompt quality only → `empirical-prompt-tuning`.
- Framework-specific RAG/MCP wiring only → `implement-with-practices`.
- Trivial single-turn Q&A with no tools.

## Four strategies (mandatory mental model)

| Strategy | Meaning | Typical tactic |
|----------|---------|----------------|
| **Write** | Persist outside the window | Scratchpad file, state object, DB, session notes |
| **Select** | Pull in only what is needed now | RAG over docs/tools, just-in-time retrieval |
| **Compress** | Shrink what stays in-window | Summarize trajectory, trim tool outputs, mask observations |
| **Isolate** | Split context across boundaries | Sub-agents, state schema fields, sandbox per tool |

At each design decision, name which bucket(s) apply. Mix strategies; do not rely on a single "bigger window."

## Workflow (mandatory order)

1. **Measure pressure** — Estimate tokens: system + tools + history + latest tool outputs. Note which bucket is failing (overflow, wrong tools, stale facts, cross-talk).
2. **Pick strategy** — Use the table above. Prefer the lightest fix (select before compress; isolate only when roles are distinct).
3. **Apply one change** — One strategy per iteration (e.g. add summarization *or* tool RAG, not both at once).
4. **Verify** — Re-run a representative task; confirm quality, step count, and peak context use improved or held.
5. **Record** — Note what was written where (paths, state keys) so the next session can select it.

## Decision shortcuts

- **Tool overload** → Select (semantic tool retrieval) or Isolate (sub-agent with subset).
- **Repeated verbose tool JSON** → Compress (summarize or replace with pointer to written artifact).
- **Sub-task needs clean slate** → Isolate (delegate to sub-agent with fresh window).
- **Facts must survive compaction** → Write (external store) + Select (retrieve on demand).

## Anti-patterns

| Anti-pattern | Why it fails | Prefer |
|--------------|--------------|--------|
| Monolithic system prompt grows forever | Brevity bias; critical detail evicted | Write + Select |
| Full-history rewrite in one pass | Context collapse; information loss | Incremental delta updates to stored notes |
| All tools always visible | Wrong tool picks, wasted tokens | Select or Isolate |
| Never compact | Hits hard limit; sudden quality cliff | Compress on a schedule (e.g. >85% window) |

## Report template (user-facing, Japanese)

```markdown
## Context Engineering

- **圧力の原因**: write | select | compress | isolate（複数可）
- **採用策**: …（1 文）
- **成果物**: …（パス / state キー / 圧縮タイミング）
- **検証**: …（タスク + OK/NG）
```

## Reference

- [reference.md](reference.md) — sources, tactic catalog, boundaries
- [references/skill-memory.md](references/skill-memory.md) — operational notes from use
