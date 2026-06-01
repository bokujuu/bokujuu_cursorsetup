---
name: codex-session-doc
description: Reconstruct and document a Codex Desktop or Codex CLI session from a session or thread ID by mining local Codex log databases and the current workspace state. Use when a prompt includes a session ID or thread ID and asks to summarize, document, archive, hand off, or explain what happened in that past session, especially when the original transcript is not attached.
---

# Codex Session Doc

Run `scripts/extract_session_context.py` first. Treat its output as `OBSERVED`. Add `INFERRED` only after reading the current workspace files that the session touched.

## Workflow

1. Extract session context.

```bash
python <CODEX_HOME>/skills/codex-session-doc/scripts/extract_session_context.py --thread-id <THREAD_ID> --format markdown
```

Use `--format json` when another script or agent will consume the result.
If `CODEX_HOME` is unset, resolve it to the local Codex home directory first, typically `~/.codex` or `%USERPROFILE%\\.codex`.

2. Read the workspace state that survives after the session.

- Run `git status --short`.
- Read the repository `AGENTS.md`.
- Read `README.md` if it exists.
- Read the files listed in `TOUCHED_FILES` from the extracted context.

3. Separate facts from inference.

- `OBSERVED`: tool calls, touched files, update-plan steps, validation commands, timestamps.
- `INFERRED`: conclusion, rationale, intended architecture, remaining gaps.
- `UNKNOWN`: anything not recoverable from logs or current files.

4. Write the handoff document.

- Prefer a machine-oriented markdown structure.
- Do not try to reconstruct a verbatim transcript.
- Do not claim user intent unless it is directly supported by logs or surviving files.
- If evidence is incomplete, say so explicitly in `UNKNOWN`.

## Output Contract

Use this shape unless the user specifies another schema:

```markdown
# SESSION_DOC

## OBSERVED
- thread_id: ...
- time_window: ...
- tool_summary: ...
- touched_files: ...
- validation: ...

## INFERRED
- conclusion: ...
- implemented_changes: ...
- verification_result: ...
- residual_gaps: ...

## UNKNOWN
- missing_prompt_text: true|false
- missing_final_reply: true|false
- ambiguous_points: ...
```

Compactness is preferred over prose. Human readability is optional.

## Extraction Rules

- Prefer the local Codex logs over memory or guesswork.
- Use `apply_patch` operations as the source of truth for file edits.
- Use `shell_command` calls to identify installs, builds, benchmarks, smoke tests, and inspections.
- Use `update_plan` calls to recover the intended phase structure.
- Use current repository files to infer the final conclusion when the logs do not contain the final assistant message.

## Failure Modes

- If the thread ID is not present in local logs, report that the session is not recoverable from this machine.
- If logs exist but are sparse, produce a partial document with explicit `UNKNOWN`.
- If the workspace changed after the session, state that the conclusion is reconstructed from current files and may include post-session drift.
