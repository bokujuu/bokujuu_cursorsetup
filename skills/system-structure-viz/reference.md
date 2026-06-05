# System Structure Visualization — Reference

## Tier detail

### Tier 1 — `docs/architecture.md`

- Copy [templates/structure-viz/architecture.md](../../templates/structure-viz/architecture.md).
- Prefer 1 module/layer diagram + 1 dependency graph.
- Commit with structural changes in the same PR when possible.

### Tier 2 — Cursor Canvas

- Skill path (Windows): `%USERPROFILE%\.cursor\skills-cursor\canvas\SKILL.md`
- Not shipped in bokujuu_cursorsetup (Cursor product bundle).
- Use for data-heavy or comparative views in the IDE; not a substitute for committed docs unless user asks.

### Tier 3 — Static site

- Copy `templates/structure-viz/site/` → `docs/structure-viz/` (or `tools/structure-viz/`).
- See [templates/structure-viz/README.md](../../templates/structure-viz/README.md).
- Sync Mermaid definitions with `architecture.md` when both exist.

## Inventory commands

Run from repository root. Adapt to stack.

| Goal | Command / action |
|------|------------------|
| Top-level layout | `rg --files -g '!node_modules' -g '!.git' \| head` or list dirs |
| Python imports | `rg '^from \|^import ' --glob '*.py' src/` |
| JS/TS imports | `rg "^import \|from '" --glob '*.{ts,tsx,js}'` |
| Package deps | Read `pyproject.toml`, `package.json`, `requirements.txt` |
| Entry points | `rg 'if __name__|main\(|FastAPI\(|express\('` |
| Existing docs | Read `AGENTS.md`, `README.md`, existing `docs/architecture.md` |

## Update triggers

Refresh visuals when any of:

- New top-level directory or package
- Public API surface change (exports, routes, CLI commands)
- Replacement of a major dependency or integration

## Related skills

| Skill | When |
|-------|------|
| `skill-lifecycle` | After defining a recurring "update architecture" procedure as repo-local skill |
| `implement-with-practices` | When viz is secondary to implementing a new stack |
