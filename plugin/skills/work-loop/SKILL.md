---
name: work-loop
description: "Work the tracker's frontier without the owner: each line in a fresh subagent with ship or ship-for-review, as many at once as the host's load allows, until no line is left. Use when the owner starts an unattended run, usually through /goal."
---

# Work loop

Start with:

```
/goal Run the work-loop skill until it reports that no item is left for an agent.
```

Keep no durable state in chat. Read the tracker and git on every step. If a compaction occurs while
subagents are still running, reload this skill to finish collecting them, then end cleanly once
running subagents finish so a fresh loop session takes any remaining frontier.

## A step

1. **Read state.** Run `frontier` and `list --state in-progress`. Never take over an `in-progress`
   item held by another session. Name any that remain in the final message.
2. **Pick.** Start every eligible `frontier` line in order that does not overlap another running
   subagent's files, keeps at most one subagent changing the running system, and respects host load
   caps. Start an area `report` or next iteration only when no subagent works in that area.
3. **Dispatch.** Send each line to a fresh subagent (in its own git worktree when building) with a
   **pointer-only brief of 5 to 8 lines**:
   - Line 1: `<item-id>` (or one-sentence goal for area reports).
   - Line 2: Skill (`ship` or `ship-for-review`, as `work-loop` subagent).
   - Line 3: Deviations or constraints not in the ticket (omit if none).
   - Line 4: Worktree path, build isolation flag if needed, and dedicated scratch folder.
   - Line 5: Required final status line: `DONE`, `PARKED: <reason>`, `QUESTION: <options, rec first>`,
     or `BLOCKED: <reason>`.

   Never copy ticket text, repeat rules from `agent-kit` or `CLAUDE.md`, or explain standard paths.

   Select models using the flexible tiers in the agent rules (frontier or worker coding models at
   `medium` for building and planning, lighter or fast models for bounded reports or docs, and a
   different provider for `change-review`). Follow the project guide when dispatching to other
   harnesses or hosts. External workers count as subagents toward all concurrency and load limits.
4. **Handle results.** Verify tracker state and git merge yourself. Treat the status line as a
   claim.
   - `DONE` or `PARKED`: line complete.
   - `QUESTION`: apply the recommended option, record a ruling on the sub-item, and dispatch a
     fresh subagent to resume. Park the sub-item instead if the action deletes data, exceeds live
     system rules or cannot be undone.
   - `BLOCKED`: ensure the sub-item is parked with the reason.
5. **Repeat** until `frontier` is empty and no subagent runs.

## Ending

Finish when `frontier` is empty and all subagents have exited. Report each area's final state and
state that no item remains for an agent. Never merge, fix or review in the loop session itself,
never ask the owner, and stop build daemons once the last subagent finishes when the project guide
calls for it.
