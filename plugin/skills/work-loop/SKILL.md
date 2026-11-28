---
name: work-loop
description: "Work the tracker's frontier without the owner: each line in a fresh subagent with ship or ship-for-review, gated by an independent pre-review before any area enters review, as many at once as the host's load allows, until no line is left. Use when the owner starts an unattended run, usually through /goal."
---

# Work loop

Start with:

```
/goal Run the work-loop skill until it reports that no item is left for an agent.
```

Keep no durable state in chat. Read the tracker and git on every step. If a compaction occurs while
subagents are still running, reload this skill to finish collecting them, then end cleanly once
running subagents finish so a fresh loop session takes any remaining frontier.

With `atelier`, the Atelier runner is the work loop. Use `atelier --json frontier` and
`atelier --json task list` only to inspect state. Start no subagents, claim no Tasks and dispatch
no work. The steps below apply only to `plane` and `local`.

## A step

1. **Read state.** Run `frontier` and `list --state in-progress`. Never take over an `in-progress`
   item held by another session. Name any that remain in the final message.
2. **Pick.** Start every eligible `frontier` line in order that does not overlap another running
   subagent's files, keeps at most one subagent changing the running system, and respects host load
   caps. Start an area `report` or next iteration only when no subagent works in that area.
3. **Dispatch.**
   - For a `report` line, run **Pre-review gate** before dispatching the area report.
   - For a `ready` sub-item, a `ready` area, or an area that passed the pre-review gate, send the
     line to a fresh subagent (in its own git worktree when building) with a **pointer-only brief
     of 5 to 8 lines**:
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

## Pre-review gate

Under `work-loop`, subagents finish or park their sub-item and stop without running
`finish <area> --review -`, so every due area report passes this gate.

Before any area moves to `review` for the owner, dispatch one fresh, independent, read-only
reviewer subagent on `claude-fable-5-2` at `high` effort (falling back to the strongest available
frontier reviewer only if `claude-fable-5-2` is unavailable). Give it a dedicated scratch folder
and a pointer-only brief naming the area item and its scratch path. Never run this review in the
loop session or in a builder session.

The reviewer inspects the area item, its recorded decisions, every sub-item completed or parked
since the last report, and every attached screenshot, video or artifact directly. For video
attachments, it extracts PNG frames with `ffmpeg` into its scratch folder to inspect motion, timing
and UI transitions, and crops small visual details when needed. It never decides from ticket text
alone.

The reviewer applies a strict end-user polish standard:

- Every claimed change and prior review finding has current visual or direct proof.
- Spacing, alignment, margins, layout across viewports or GUI scales, animation smoothness,
  contrast, wording and UX look polished and ready for real users.
- Any visible defect, unpolished detail, outdated attachment or missing current proof fails the
  check.

The reviewer returns `READY` or `NEEDS_WORK` with concrete itemized findings and missing proof:

- **`READY`**: dispatch a fresh `ship` subagent to write the area report and run
  `finish <area> --review -`.
- **`NEEDS_WORK`**: keep the area out of `review`. Post the reviewer's concrete findings and
  required proof as a dated review comment on the area item, run `set <area> --state ready`, and
  continue the loop so the next step plans and builds the rework iteration.

Run at most 2 pre-review rework rounds per area in one loop run. Stop rework early if two
consecutive pre-review rounds report the same unresolved defect or only human-only checks remain.
When capped or blocked on human-only checks, dispatch the area report with
`finish <area> --review -` and list the remaining pre-review findings under **To look at** or
**To decide**.

## Ending

Finish when `frontier` is empty and all subagents have exited. Report each area's final state and
state that no item remains for an agent. Never merge, fix or review in the loop session itself,
never ask the owner, and stop build daemons once the last subagent finishes when the project guide
calls for it.
