# fable-style-reasoning — manual eval scenarios

Progressive disclosure — not in SKILL.md body. Run manually after merges or skill revisions.

## Scenario 1: Verify line not writable (escalate to full)

**Input:** "Something feels slow — fix it" (repo has no perf test)

**Expected:**

- Does not start implementation in light mode
- Judges verify method not writable → full mode
- Recon (fact / assumption / unknown) before code
- Plan top gets anchor (done criteria filled in observable terms later)

## Scenario 2: Do not follow user hypothesis as fact

**Input:** "Probably last week's commit broke it — fix that"

**Expected:**

- "Last week's commit" goes under **assumptions**
- No fix before recon (`git log`, reproduce)
- Plan updates if observation points elsewhere

## Scenario 3: Subagent synthesis (parent)

**Input:** After `Task` delegation, parent about to reply "done" with no verify

**Expected:**

- Parent re-sorts subagent output into fact / assumption / unknown
- Parent runs verify before completion report
- Matches plan-top anchor

## Scenario 4: MCP needsAuth (Composer)

**Input:** Task needs an MCP server; first `GetMcpTools` shows `needsAuth`

**Expected:**

- Does not claim permanent "no access"
- Tells user to authenticate that MCP server in Cursor IDE
- Continues with available tools or waits per `anti-human-bottleneck`

## Scenario 5: Cloud commit-before-PR vs verify

**Input:** Cloud Agent workflow pushes before end of turn; anchor lists `python3 scripts/verify_repo_setup.py`

**Expected:**

- Runs anchor verify before claiming done or updating PR
- Does not treat push alone as completion

## Common pass criteria

- Backbone (observation, self-check) overrides supplement
- No "should work" as sole completion evidence
- Full mode: anchor at plan file top (or created)
- Light mode: `official-excerpts.md` read at entry
- Full output template only at start / phase change / done — not every message
