---
name: work-loop
description: Work the tracker's frontier without the owner - each line in a fresh subagent with ship or ship-for-review, as many at once as the host's load allows - until no line is left. Use when the owner starts an unattended run, usually through /goal.
---

# Work loop

The owner starts the loop with exactly this line, so the goal is the same every time:

```
/goal Run the work-loop skill until it reports that no item is left for an agent.
```

The harness repeats the goal until the session states it is reached. After every compaction, load
this skill again before the next step. The loop keeps no state of its own: the tracker and git are
its memory, so every step starts by reading them.

## A step

1. **Read the state.** `frontier`, and `list --state in-progress`. A sub-item in `in-progress`
   belongs to one of this loop's subagents or to another session: the loop never takes it over, and
   names any that are still there in its last message.
2. **Pick.** Every line of `frontier` that can start now, in its order. A line starts when no running
   subagent holds that line, none touches the same files, and at most one subagent at a time changes
   the running system. A report or a next iteration of an area starts only when no subagent works in
   that area.
   The number of subagents has no fixed cap: the host's limits on load, which the project's guide
   names, decide when one more starts. Two sub-items of one area run at once when their files are
   apart.
3. **Dispatch.** Each line goes to a fresh subagent, in its own git worktree when it builds, with a
   brief that holds:
   - the item's ID and the instruction to follow `ship` (or `ship-for-review`) as a subagent of
     `work-loop`,
   - the worktree's path and the project's `--project-cache-dir` or similar build isolation the
     project's guide names,
   - a scratch folder of its own for every temporary file, as the rules on subagents say,
   - that it returns exactly one status as its last line: `DONE`, `PARKED: <what waits for the
     owner>`, `QUESTION: <question with options, recommended first>` or `BLOCKED: <reason>`.

   The model follows the rules on subagents: Opus for building and for writing an iteration, Sonnet
   for an area report.
4. **Handle the result.** Check the item's state and the merge in git yourself; the status line is
   a claim.
   - `DONE` or `PARKED`: the line is finished. Next step.
   - `QUESTION`: decide it with the recommended option, write it into the sub-item as a ruling (the
     format of `ship`) and send a fresh subagent with the decision, as a brief that resumes the
     sub-item. A question whose answer deletes data, touches a live system beyond the project's
     rules, or cannot be undone is not decided: the sub-item is parked with the question, as
     "Blocked" in `ship` describes.
   - `BLOCKED`: the sub-item is parked with the reason, if the subagent did not do that already.
5. **Repeat** until `frontier` is empty and no subagent runs. A `report` line that appears when an
   area's last sub-item ends is a line like any other.

## Ending

The loop is done when `frontier` prints nothing and none of its subagents runs. Every area it worked
on is then in `review` with its area report, or still has work that another session holds. The last
message names each area and how it ended, and states that no item is left for an agent.

The loop never merges, fixes or reviews itself: subagents do that, so its context stays small. It
never asks the owner. It stops the project's build daemons once the last subagent has finished,
where the project's guide says so.
