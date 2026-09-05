---
name: ralph-loop
description: "Use when planning or running long-running, multi-task work; when the user mentions PRD, task list completion, or autonomous agent loops. Describes the Ralph pattern: run the agent repeatedly until all PRD items are complete, with fresh context per iteration and state in git and progress.txt."
disable-model-invocation: false
metadata:
  version: 1.1.0
  source: "https://nyosegawa.github.io/posts/claude-code-verify-command/"
  note: "Content aligned with the article 'Agentワークフローで人間がボトルネックにならないためのSkill設計' (逆瀬川). Ralph loop = outer loop (fresh context, durable state, observable verify)."
---

# Ralph Loop

*This skill is derived from and aligned with the article [Agentワークフローで人間がボトルネックにならないためのSkill設計](https://nyosegawa.github.io/posts/claude-code-verify-command/) (逆瀬川).*

Ralph is an **outer agent loop** that runs the agent repeatedly until all PRD (Product Requirements Document) items are complete. Each iteration is a **fresh instance with clean context**. Memory persists via **git history**, `progress.txt`, and `prd.json` (or equivalent durable files).

## Role

Ralph の責務は次に限定する。

- fresh context で反復する
- state を git / progress / PRD 等に保存する
- observable な検証条件で各項目を閉じる
- all-pass で停止する

外部操作・commit・push・deploy の可否は、User Rules、リポジトリ固有ルール、ユーザー依頼に従う。Ralph を有効化しただけでは、それらを自動許可しない。

## How it works (summary)

1. **PRD** → task list（例: `prd.json`）with user stories and `passes` status.
2. **Each iteration**: New agent instance; picks highest-priority story where `passes: false`; implements it; runs checks (typecheck, tests); if OK and commit が依頼または明確な承認の範囲内なら commit; marks story `passes: true`; appends learnings to `progress.txt`.
3. **Stop when** all stories have `passes: true`（完了判定は tests/checks などの観測可能な条件。人間のステップ承認は完了条件にしない）。

Critical: **Completion is decided by tests/checks, not by narrative claims.** Run until verification passes.

## Key ideas

- **Small tasks**: Each PRD item should fit in one context window. Split “build the whole dashboard” into many small stories.
- **Feedback loops**: Typecheck, tests, CI must be green. Ralph relies on these to know when a story is done.
- **AGENTS.md**: Update with learnings after iterations so future runs (and humans) see patterns and gotchas.
- **Human involvement**: 問題発見・方針・承認境界の操作。各ステップの儀式的な承認待ちはしない。ただし push / deploy / 破壊的操作は依頼またはルールに従う。

## Faceted prompting (optional)

When implement and review should **not share one bloated prompt**, split each iteration into facets (persona, policy, knowledge, instruction, output-contract). Kit: [templates/loop-orchestration/facets/](../../templates/loop-orchestration/facets/). Design: [docs/pr/004-qa-faceted-adoption.md](../../docs/pr/004-qa-faceted-adoption.md). Origin: [TAKT faceted prompting](https://github.com/nrslib/takt).

## References

- **Article (origin)**: [Agentワークフローで人間がボトルネックにならないためのSkill設計](https://nyosegawa.github.io/posts/claude-code-verify-command/) (逆瀬川) — Ralph as outer loop; source for this skill.
- **Ralph (snarktank)**: [github.com/snarktank/ralph](https://github.com/snarktank/ralph) — Loop implementation, PRD skill, `ralph.sh`, `prd.json`, `progress.txt`.
- **Ralph pattern (Geoffrey Huntley)**: [ghuntley.com/ralph](https://ghuntley.com/ralph/) / [ghuntley.com/loop](https://ghuntley.com/loop/) — Original “everything is a ralph loop” idea; human for problem-finding, not routine step approval.
- **Matthew Berman**: [Why 'Ralph' Agents Are Upending How We Code](https://www.wisdomai.com/insights/matthew_berman/ralph-loop-autonomous-agents-ai-coding-context-window-ffdd1834) — Completion decided by tests, not by agent narrative.
