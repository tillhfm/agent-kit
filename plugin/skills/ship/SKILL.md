---
name: ship
description: Take one line of the tracker's frontier to its end - a sub-item through branch, proof, review by a fresh subagent, pull requests, merge gate and merge to its report, a ready area item to its next iteration, a due area to its report. Use when a session picks up work whose result a check can prove, and as the base that ship-for-review and work-loop build on.
---

# Ship

The session owns the line it took from `frontier` until its end. It works without an orchestrating
session and stops only for the reasons under "Blocked". The tracker commands, the areas and the
sub-items are in the rules under "Work items".

## 1. Start

1. Read the item with `show`, its comments included, and its area item when it is a sub-item. The
   area's decisions bind the sub-item. A handover comment on the sub-item says what an earlier
   session left.
2. Find what the line asks for:
   - A `report` line: write the area report, as "Area report" below describes.
   - A `ready` area item that has sub-items: the comments after its last report are the owner's
     answer. Write the next
     iteration from them, as `plan-work` describes under "The items": the decisions into the area,
     the brief into a sub-item in `ready`, and the parked sub-items set to `ready` or folded into the
     new one. A decision the answer leaves open is a ruling. Then continue with the new sub-item.
   - A sub-item, or a flat item without sub-items: continue below.
3. Decide how it ends. It ends with the merge when a check can prove the result. It ends with the
   evidence for a look when the brief says "Ends with a review." or the result is a design, a
   proposal or wording without a checkable goal: then follow `ship-for-review`, which is this skill
   with another end.
4. `claim` the sub-item. A brief that resumes a sub-item already `in-progress`, such as a `work-loop`
   brief after a question, skips the claim.
5. Create a branch from the freshly fetched default branch, named as `github-flow` says. A
   project without a GitHub remote takes a local branch.
6. Run the project's check on the modules the sub-item will touch before any change. A check that
   already fails is noted in the sub-item, so a later failure is attributable.

A sub-item may need several pull requests. Each one takes a branch of its own (steps 5 and 6) and
runs sections 2 to 6, and the sub-item stays `in-progress` until its brief is met.

## 2. Change

The smallest change that reaches the brief's goal, as the rules define it. Fix the case the brief
names, not every case that could happen. A bug follows the `fix` skill. Commit as `github-flow`
says.

## 3. Proof

Proof is what the session observed itself, after the last change, in a run it started fresh. An
earlier run and "should pass" are not proof. The proof covers every change in the diff, with the
most direct method the change allows:

- The reproduction that failed passes.
- The checks the project's CI runs pass locally on the touched modules.
- One focused test fails without the change and passes with it, for new logic with a branch, a
  loop, a parser, money or security.
- A UI or runtime change is run and looked at where it lives: the page in a browser, the command,
  the running service. Green mocked tests do not prove it.

A subagent's report of success is checked against the diff and a run of its own, never taken as
it is. When no method can prove the change, the session cannot ship it: see "Blocked".

## 4. Review

A fresh subagent reviews the diff with `change-review`. It gets the base, the diff command, the
brief and nothing of this session's reasoning. It does not edit the checkout. Reviewers are the
only subagents a `ship` subagent may start itself.

Each finding is checked against the code before it is acted on, and graded again by the session:

- **Blocking or should fix**: fixed with the smallest change, and its proof is run again.
- **Minor or out of scope**: declined in one line with the reason, and named in the report. A bug
  among them is created as an item first, as the rules say.
- **Wrong**: dismissed with the evidence.

After a round of fixes, a fresh reviewer gets only the fix diff and the open findings, and marks
each finding addressed or open. Three rounds at most. A finding still open after the third, or
disputed twice, is a ruling of the session (see "Rulings") or a reason to block. The third failed
fix of the same finding is a sign that the design or the brief is wrong: the session says so in the
sub-item instead of a fourth patch.

## 5. Pull request

Rebase onto the latest default branch, push and open the pull request as `github-flow` says. The
body adds one line on how the change was proved. Watch the checks in the background with
`gh pr checks <pr> --watch`. A red check is the session's own to fix, with proof before each push.

## 6. Merge gate

The session merges only when all of these hold on the latest commit:

- The proof covers every change in the diff.
- Every required check is green.
- Every review finding is fixed or dismissed with a written reason.
- No human review requests changes.
- The branch is up to date with the default branch, and GitHub reports it mergeable.

Merge with the method `github-flow` names. Never with `--admin`, never by switching off a rule, and
never with `--no-verify`. A project without a GitHub remote merges the branch into the default
branch locally after the local checks, and deletes the branch.

## 7. Report

`finish <sub-item> --done` once the brief is met, with the final report as its comment:

- **What changed**: one or two sentences, and the pull requests or merge commits.
- **Proof**: what was run and what was seen, by its decisive line.
- **Rulings**: every decision the session made on its own, one line each, as below.
- **Found**: every bug or piece of work noticed outside the brief, each with the item it went into.
  Omitted when there is nothing.
- **For the owner**: what the owner has to look at, decide or do, one line each, with where to look.
  Omitted when there is nothing.

When `finish` says that the area's report is due, the session writes it next. A flat item without
an area that leaves something for the owner ends with its own area report instead of `--done`.

A session that stops before the brief is met, such as one compacted twice, writes a handover
comment with what is done and what is left, and sets the sub-item back with
`set <sub-item> --state ready`.

## Area report

An area's report is due when the area is `in-progress` and none of its sub-items is `ready` or
`in-progress`: then no agent can do more in it without the owner. The session reads the area item and
every sub-item finished or parked since the area's last report, and then:

1. Rewrites the area's description, so it states the outcome, every decision with its date and the
   questions still open.
2. Attaches to the area item every file the owner has to look at that is not attached yet.
3. Runs `finish <area> --review -` with the report. Its parts come in this order, and an empty part
   is left out:
   - **To look at**: one line per result the owner judges: the question, and where to look.
   - **To decide**: one numbered question per open decision, with its options, the recommended one
     first. A parked sub-item names the question it waits for.
   - **To do by hand**: what only a human can do, such as a check on a device or a release.
   - **Rulings**: the rulings of the iteration that change what the owner gets, one line each.
   - **Done**: one line per sub-item: what changed, and its pull requests.
   - **Next**: one line per sub-item queued in `idea`.

The report holds nothing else: no proof, no logs and no session's own report. Those stay in the
sub-items. With the `local` tracker, the report is also the session's message in the chat.

## 8. The next item

A session the owner started, in an app that offers `start_session`, ends by proposing the next
line: the first line of `frontier`, offered with `start_session`, initiation `offer`, a title that
names the item and a brief that says to take it with `ship`. The owner then starts it or declines
it with one click. With an empty frontier, the session says so instead. A `work-loop` subagent
skips this step: the loop picks the next line.

## Rulings

A decision the session makes without the owner is a ruling, written as
`Ruling: <decision>, because <reason>. If wrong: <what it costs>.`. Every ruling goes into the
sub-item's report, so the owner can overrule it.

## Blocked

The session stops and asks only when:

- no method can prove the change,
- the merge gate cannot pass and the session cannot fix that,
- the next step deletes data, touches a live system beyond the project's own rules, or changes
  something outside the repository,
- the goal is ambiguous in a way that changes the result,
- another pull request makes this one obsolete.

Before it stops, the session finishes every part of the brief that does not wait for the answer.

A session the owner started asks with `AskUserQuestion`: the sub-item, the pull request, what blocks
and the options with the recommended one first. Without an answer, it leaves the pull request
unmerged and parks the sub-item: the question goes into the area's open questions, a handover
comment on the sub-item says what is left, and `set <sub-item> --state idea` parks it. Under
`work-loop`, the subagent returns the question to the loop instead of asking.

Work out of the session's reach, such as a check on a machine, an account or a device the session
cannot use, needs no question: the session claims the sub-item, parks it with a comment that says
what remains, where and why the session cannot do it, and names it for the area report under
**To do by hand**. A `work-loop` subagent does the same and tells the loop.

A park that leaves the area without a `ready` or `in-progress` sub-item makes its report due, and the
session writes it next, as "Area report" describes.

Everything else the session decides itself, as a ruling.
