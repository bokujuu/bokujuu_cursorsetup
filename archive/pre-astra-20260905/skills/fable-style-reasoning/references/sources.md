# fable-style-reasoning — sources and layer structure

## Layer definitions

| Layer | Meaning | Adoption criteria |
|-------|---------|-------------------|
| **Backbone A** | Core epistemic rules | Anthropic **official** Fable 5 (2026-06-09) only |
| **Backbone B** | Agent action rules on the same release-notes page | Official Opus 4.7–4.8 excerpts; must not contradict A |
| **Supplement** | Procedural workflow | Non-official; must not contradict backbone |
| **Reference** | Unverified extracted patterns | Patterns only — no body copy |

Light mode uses backbone only (Read [official-excerpts.md](official-excerpts.md)).

---

## Backbone A — Anthropic official (Fable 5, 2026-06-09)

| Source | Reflected in skill |
|--------|-------------------|
| [System Prompts — Claude Fable 5](https://platform.claude.com/docs/en/release-notes/system-prompts) | Self-check implied artifacts, good epistemology, steady correction, knowledge cutoff / verify-before-claim |

Verbatim passages: [official-excerpts.md](official-excerpts.md) § A1–A4.

---

## Backbone B — Release-notes series supplement

| Source | Reflected in skill |
|--------|-------------------|
| Same page — Opus 4.7 (2026-04-16) | `acting_vs_clarifying`, `capability_check` |
| Same page — Opus 4.8 (2026-05-28) | `tool_discovery` (SKILL.md before files/code) |

Verbatim passages: [official-excerpts.md](official-excerpts.md) § B1–B3.

**Not in Fable 5 (2026-06-09):** B1–B3 are series supplements, not mislabeled as Fable-only.

---

## Supplement — community practice

| Source | Reflected in skill |
|--------|-------------------|
| [shotatykr — Fable skill sketch](https://x.com/shotatykr/status/2074035238116769851) | Phase 0–4, three principles, four self-checks, five-point whole verify |
| [shotatykr — verbalizing procedure](https://x.com/shotatykr/status/2074148603619348887) | Motivation for proceduralizing |

---

## Reference — unofficial (unverified)

| Source | Treatment |
|--------|-----------|
| [CL4R1T4S / CLAUDE-FABLE-5.md](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md) | Patterns only if consistent with backbone |
| [ayautomate — leak commentary](https://www.ayautomate.com/blog/claude-fable-5-system-prompt-leak) | Design lessons only |

---

## Runtime target

Primary: **Cursor IDE / Cloud Agent** (Grok or Composer). Tool names in SKILL.md map to Cursor tools (`Read`, `Shell`, `GetMcpTools`, `Task`, etc.), not Claude Code `view` / `tool_search`. Model routing: [docs/model-routing.md](../../../docs/model-routing.md).

## Related skills

| Skill | Relationship |
|-------|----------------|
| `abstract-source-patterns` | Layering and placement decisions |
| `agent-handoff-recovery` | Post-drift recovery and subagent synthesis |
| `repo-agent-bootstrap` | AGENTS template references this skill |

## Global suitability

- Generic agent reasoning with official epistemology as backbone. Slug `fable-style-reasoning` (not Anthropic-official).
