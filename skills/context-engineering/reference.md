# Context Engineering — Reference

## Primary sources

| Source | URL | Takeaway |
|--------|-----|----------|
| Lance Martin — Context Engineering for Agents | https://rlancemartin.github.io/2025/06/23/context_engineering/ | write / select / compress / isolate taxonomy |
| LangChain — Context Engineering for Agents | https://www.langchain.com/blog/context-engineering-for-agents | Same four buckets; harness design notes |
| LangChain notebooks | https://github.com/langchain-ai/context_engineering | Runnable examples per strategy |
| Karpathy on context engineering (2025) | https://x.com/karpathy/status/1937902205765607626 | Term adoption; context as first-class design surface |

## Tactic catalog (by strategy)

### Write

- Session scratchpad (`notes.md`, `PROGRESS.md`, structured state file).
- Structured agent state (fields not passed to LLM until needed).
- Long tool outputs saved to disk; context holds path + short summary only.

### Select

- RAG over documentation or prior decisions.
- Semantic retrieval over tool descriptions (subset per task).
- Just-in-time fetch of API schemas or config.

### Compress

- Trajectory summarization after N turns or at window threshold (e.g. Claude Code auto-compact).
- Hierarchical summarization: recent turns verbatim, older turns summarized.
- Observation masking: replace large tool payloads with one-line digest + pointer.

### Isolate

- Sub-agents with separate windows and narrow tool sets (separation of concerns).
- State schema: isolate tool results in fields until a node needs them.
- Sandboxed execution environments with persisted side-channel state.

## Skill boundaries

| Skill | Scope |
|-------|--------|
| `context-engineering` | Cross-cutting context window design |
| `empirical-prompt-tuning` | Prompt/skill text quality via blind executor |
| `implement-with-practices` | Stack-specific retrieval, MCP, framework APIs |
| `bounded-agent-execution` | Hard caps on steps, cost, loops (complementary) |
| `ralph-loop` | Outer orchestration loop; keep inner tasks context-sized |

## Related

- [bounded-agent-execution](../bounded-agent-execution/SKILL.md) — stop runaway loops before context is wasted on no-progress steps
