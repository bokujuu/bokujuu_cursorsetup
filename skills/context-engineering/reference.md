# Context Engineering — Reference

## Utilization and budgets

- Treat **60–80%** of the advertised window as a practical ceiling; reserve headroom for unexpected tool output.
- Track **context utilization** in long loops: message count, largest tool payloads, compaction events.
- **Compaction trigger**: many products auto-compact near 90–95% window fill; plan external state before relying on summarization alone.

## Write — external state patterns

| Artifact | Use for |
|----------|---------|
| `progress.txt` / `NOTES.md` | Learnings, blockers, next step |
| `prd.json` / task JSON | Pass/fail per story (pairs with `ralph-loop`) |
| Git history | Durable code truth; fresh agent reads diff/log |
| Filesystem | Large intermediate results the model reads on demand |

**Append-only** notes reduce cache invalidation and replay complexity.

## Select — retrieval patterns

- **Agent-controlled retrieval**: model invokes search/read tools when needed vs pre-injecting every turn.
- **Tool RAG**: embed tool descriptions; fetch top-k tools per task to reduce overlap confusion.
- **Post-retrieval filter**: score or truncate chunks before adding to context.

## Compress — summarization patterns

- **Rolling summary**: keep running summary + last N raw turns.
- **Anchored summary**: preserve objective, open tasks, and pointers (paths, URLs, SHAs) to full data.
- **Trim vs summarize**: hard-drop stale tool output when safe; use LLM summary when semantic fidelity matters.

## Isolate — architecture patterns

- **Sub-agents**: researcher / implementer / reviewer with separate windows.
- **Phased tool availability**: avoid adding/removing tools mid-iteration when it confuses the model; prefer masking or phase gates ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
- **Multi-agent parallel exploration**: for analysis where breadth beats single-thread coherence ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## Evaluation metrics (production-oriented)

| Metric | What it tells you |
|--------|-------------------|
| Context utilization rate | How close to limits before failure |
| Retrieval precision | Useful chunks / injected chunks |
| Post-compaction task success | Whether compression preserved signal |
| Tokens per successful task | Cost vs outcome |

Iterate: baseline on real sessions → fix highest-cost segment → re-measure.

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Unbounded tool output in context | Buries instructions; triggers truncation |
| Summarize without external pointers | Irreversible loss of audit trail |
| Maxing out context every turn | No room for tool spikes; brittle |
| Dynamic tool set every iteration | Model confusion; cache miss |
| "Better prompt" only | Does not scale past one window |

## Related skills

- `harness-engineering` — outer loop, verification gates, stateless iterations
- `ralph-loop` — PRD + progress files + test-driven completion
- `cursor-session-doc` — post-hoc session analysis
