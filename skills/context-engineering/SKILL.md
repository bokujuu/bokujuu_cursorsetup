---
name: context-engineering
description: >-
  Curate what enters an agent's context window across long or multi-step work:
  write external state, select on demand, compress history, and isolate by
  sub-agent or module. Use when sessions grow long, tool outputs bloat prompts,
  or retrieval quality drops—not for one-shot prompts, library-specific APIs
  (use implement-with-practices), or outer-loop orchestration (use ralph-loop /
  harness-engineering).
disable-model-invocation: false
---

# Context Engineering

**Context engineering** is the practice of filling the context window with the smallest set of high-signal tokens at each step—not just writing better prompts. Treat the window as a finite resource (like RAM): plan what to persist, pull in, summarize, and partition.

Primary framing: **Write → Select → Compress → Isolate** ([Lance Martin](https://rlancemartin.github.io/2025/06/23/context_engineering/); [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## When to use

- Agent sessions exceed a few turns; tool outputs dominate the prompt.
- Retrieval injects noise; the model misses the actual task signal.
- Long-horizon work needs memory beyond one context window.
- User asks to reduce tokens, fix "context rot", or improve long-session coherence.

Skip when:

- Single-turn Q&A with no tools.
- Problem is missing verification or outer-loop structure → `harness-engineering` / `ralph-loop`.
- Problem is library/API usage → `implement-with-practices`.

## Four strategies (mandatory mental model)

| Strategy | Goal | Typical tactics |
|----------|------|-----------------|
| **Write** | Persist state outside the window | `progress.txt`, `NOTES.md`, structured state files, git, filesystem as scratchpad |
| **Select** | Pull in only what this step needs | Agent-triggered retrieval, tool-result filtering, RAG over tools/docs, post-retrieval scoring |
| **Compress** | Shrink history without losing goals | Rolling summarization, compaction at ~80–95% utilization, anchored summaries with pointers to raw artifacts |
| **Isolate** | Limit blast radius of context | Sub-agents with narrow scopes, separate modules per concern, mask/limit tool sets per phase |

Apply in order of diagnosis: measure utilization → pick the lightest strategy that fixes the symptom.

## Workflow

1. **Measure** — Estimate context pressure: long message list, large tool payloads, repeated failures after compaction. Target ~60–80% utilization headroom in production loops ([reference](reference.md)).
2. **Write first** — Externalize durable state (task list, decisions, file paths) before compressing. Prefer append-only notes the agent can re-read ([Manus lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
3. **Select on demand** — Prefer agent-controlled retrieval over auto-injecting every turn. Filter chunks before injection.
4. **Compress deliberately** — Summarize trajectories; keep recent actions and current objective explicit. Avoid destructive compression without pointers (URLs, file paths, commit SHAs).
5. **Isolate if needed** — Split research vs implementation vs review across sub-agents or phases; each gets a minimal context slice.
6. **Verify impact** — Re-run the failing scenario; confirm accuracy did not regress (token savings alone is not success).

## Tool and prompt hygiene

- Return **token-efficient** tool results (truncate, summarize, link to files).
- Keep **stable prefixes** (system prompt, tool defs) at the front for cache-friendly runs; avoid volatile headers (e.g. per-second timestamps) in static prefixes.
- Prefer **deterministic serialization** (stable JSON key order) when caching matters.

## Pairing with other skills

| Situation | Also use |
|-----------|----------|
| Stateless outer loop, PRD-driven iterations | `ralph-loop`, `harness-engineering` |
| Fast non-interactive verify | `non-interactive-hang` |
| Codify recurring context patterns | `retrospective-codify`, `skill-lifecycle` |

## Report template (user-facing, Japanese)

```markdown
## Context Engineering

- **症状**: …（肥大化 / 忘却 / 検索ノイズ 等）
- **採用戦略**: Write | Select | Compress | Isolate（複数可）
- **変更**: …（外部ファイル / 圧縮 / 検索条件 等）
- **検証**: …（再実行結果・精度）
- **次**: …（継続監視 / harness 側の調整）
```

## Reference

- [reference.md](reference.md) — tactics, metrics, anti-patterns
- [references/sources.md](references/sources.md) — upstream URLs
