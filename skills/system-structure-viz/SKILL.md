---
name: system-structure-viz
description: >-
  Produce or update architecture and dependency visuals when modules change,
  refactoring, or onboarding needs a shared mental model. Chooses Tier 1
  (Mermaid in docs), Tier 2 (Cursor canvas for session analysis), or Tier 3
  (static HTML site from template)—not for one-line fixes or library-specific
  implementation (use implement-with-practices).
disable-model-invocation: false
---

# System Structure Visualization

Keep **structure visible** as the codebase evolves. Pick the lightest tier that fits audience and longevity. Context: [GianMattya on visualization vs docs-only](https://x.com/GianMattya/status/2062294853464265004); Tier 3 aligns with dedicated browseable views for non-developers.

## When to use

- New top-level module, package, or service boundary.
- Refactor that changes imports or public APIs.
- Onboarding: "explain how this repo is organized".
- User asks for dependency map, architecture diagram, or structure overview.

Skip when:

- Change is trivial (rename variable, single-file bugfix).
- User asked for a deliverable in another tool only (e.g. Datadog dashboard).

## Tier selection

| Tier | Choose when | Output |
|------|-------------|--------|
| **1** | Small/medium repo, dev-only audience, Git-friendly docs | `docs/architecture.md` with Mermaid ([template](../../templates/structure-viz/architecture.md)) |
| **2** | Interactive exploration, review, metrics in one session | Read Cursor bundled `canvas` skill at `%USERPROFILE%\.cursor\skills-cursor\canvas\SKILL.md`; write `.canvas.tsx` per that skill |
| **3** | Team-wide, long-lived, non-developers need browse | Copy [templates/structure-viz/site/](../../templates/structure-viz/site/) to e.g. `docs/structure-viz/` |

Default: start at **Tier 1**; escalate only when the user or audience requires it.

## Workflow (mandatory order)

1. **Inventory** — Map layout and dependencies (see [reference.md](reference.md)).
2. **Choose tier** — Apply table above; state choice in the reply.
3. **Draw** — Module/layer diagram + optional dependency graph (keep diagrams ≤2 per file unless user asks more).
4. **Place artifact** — Tier 1: create or update `docs/architecture.md`. Tier 2: canvas path per canvas skill. Tier 3: copy template site and open locally. commit / push / PR はユーザー依頼またはリポジトリ固有ルールに従う（成果物作成と Git commit は分離する）。
5. **Update rule** — If Tier 1 or 3 exists, refresh when: top-level dir added, public API changed, major dependency swapped.

## Diagram conventions

- Use `flowchart` or `graph` with camelCase or underscored node IDs (no spaces in node IDs).
- Label edges with relationship: `imports`, `calls`, `deploys_to`.
- Note generated date and scope in a one-line caption under each diagram.

## Report template (user-facing, Japanese)

```markdown
## 構造可視化

- **Tier**: 1 | 2 | 3
- **成果物**: …（パスまたは canvas 名）
- **更新トリガー**: …（該当する場合）
- **次**: …（実装継続 / 図の追記）
```

## Reference

- [reference.md](reference.md) — collection commands, tier detail
- [templates/structure-viz/](../../templates/structure-viz/) — Tier 1 and 3 scaffolds
