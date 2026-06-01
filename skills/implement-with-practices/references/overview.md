# Implement With Practices Overview

This home skill helps Codex implement with an explicit practice-first workflow.

## Operating Rules

- Search the current repository for local practices before inventing a new pattern.
- Prefer official documentation and primary sources when external technology is involved.
- Use small reversible experiments only when existing guidance is insufficient.
- Record successful experiments as repo-local draft skills instead of silently relying on memory.

## Deterministic Outputs

- `.codex/practice-registry.json` records the local practice inventory.
- `.codex/skills/<topic-slug>/` stores repo-local skills.
- `.codex/practice-snippets/<topic-slug>.md` stores append-only AGENTS snippets generated on promotion.
