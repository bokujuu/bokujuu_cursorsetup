---
name: implement-with-practices
description: "Best-practice-first implementation for features that depend on specific libraries, APIs, or frameworks. Use when Codex needs to implement with a technology, search repository and primary-source practices first, and capture successful trial-and-error as a repo-local draft skill."
---

# Implement With Practices

Search the current repository for reusable practices before writing code. If no suitable practice exists, use small reversible experiments, then record successful patterns as a repo-local draft skill.

## Workflow

1. Inspect `AGENTS.md`, `.codex/practice-registry.json`, and `.codex/skills/` for existing local practices.
2. For external libraries, frameworks, or APIs, prefer official docs and primary sources over secondary articles.
3. Before implementation, summarize the adopted practice in terms of why to use it, what to avoid, and how to verify it.
4. Only when practice coverage is insufficient, run small experiments with explicit hypotheses, verification commands, and rollback boundaries.
5. If the implementation succeeds and is reusable, scaffold a repo-local draft skill and register it in `.codex/practice-registry.json`.

## Deterministic Tools

- `python <CODEX_HOME>/skills/implement-with-practices/scripts/scaffold_local_skill.py --target <repo> --slug <library-pattern> ...`
- `python <CODEX_HOME>/skills/implement-with-practices/scripts/validate_local_skill.py --target <repo> [--slug <library-pattern>]`
- `python <CODEX_HOME>/skills/implement-with-practices/scripts/promote_local_skill.py --target <repo> --slug <library-pattern>`

## Local Repo Contract

- Store draft and approved local skills under `.codex/skills/<topic-slug>/`.
- Store the registry at `.codex/practice-registry.json` with `draft` and `approved` statuses only.
- Do not edit repository `AGENTS.md` automatically; promotion generates an append snippet instead.

## References

- See `references/overview.md` for the intended operating model.
- See `references/local-practice-format.md` for the repo-local skill and registry format.
