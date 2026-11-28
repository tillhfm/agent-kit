---
name: ship
description: "Take one line of the tracker's frontier to its end: a sub-item through branch, proof, fresh cross-provider review, pull requests, merge gate and merge to its report, a ready area item to its next iteration, or a due area to its report. Use when a session picks up work whose result a check can prove, and as the base that ship-for-review and work-loop build on."
---

# Ship

Own one `frontier` line to its end without an orchestrating session. Stop only for "Blocked".

## 1. Start

1. Read the item (`show`, including comments) and its parent area item. Area decisions bind the
   sub-item. Handover comments describe prior progress.
2. Dispatch by line kind:
   - `report`: write the area report (see "Area report").
   - `ready` area item with sub-items: turn owner or pre-review comments after the last report into
     the next iteration (`plan-work`: decisions into area, brief into a `ready` sub-item, parked
     sub-items re-readied or folded, open details recorded as rulings), then continue with the new
     sub-item.
   - Sub-item or flat item: continue below.
3. Choose the ending. Use `ship` when a check proves the result. Use `ship-for-review` when the
   brief says "Ends with a review." or requires human judgment.
4. Run `claim <item>` unless resuming an already `in-progress` item.
5. Branch from freshly fetched `origin/<default>` (`github-flow`), or locally if no remote exists.
6. Run the project's checks on touched modules before editing. Note pre-existing failures in the
   sub-item.

With `atelier`, read the Task and its Area with `atelier --json task <id>` and
`atelier --json area <id>`. The runner's lease replaces `claim`. Use the worktree and
`atelier/<task>` branch the runner assigns instead of creating or renaming a branch.

A sub-item may span several pull requests. Each pull request gets its own branch and runs sections
2 to 6 while the sub-item stays `in-progress`.

## 2. Change

Make the smallest complete change for the brief. Follow `fix` for bugs and `github-flow` for
commits. Run the project's local pre-PR check (such as `bin/pre-pr`) when available.

## 3. Proof

Observe the result yourself in a fresh run after the last edit. Cover every diff change directly:

- Failing reproduction now passes.
- Local CI checks pass on all touched modules.
- New logic with branches, loops, parsers, money or security has one focused red-then-green test.
- UI or runtime changes are observed live where they run. Mocked tests do not prove them.

Verify every subagent claim against the diff and your own run. If nothing can prove the change,
stop under "Blocked".

## 4. Review

- **Atelier owns review dispatch:** Atelier dispatches the reviewer after the builder opens the
  pull request. The builder starts no reviewer and chooses no review model. The runner chooses
  same-builder or fresh-builder rework and supplies the findings to fix.
- **Fresh cross-provider reviewer (`plane` and `local`):** Every review round uses a completely
  fresh session running `change-review`, preferably on a different provider than the builder. Use
  the project guide's cross-provider dispatch mechanism when available, or fall back to a fresh
  subagent on the current provider. Pass a pointer-only brief: base ref, diff command, item ID or
  brief, and nothing of the builder's reasoning. The reviewer never edits the checkout.
- **Triage every finding against the code:**
  - *Blocking or should fix*: fix minimally and re-run proof.
  - *Minor or out of scope*: decline in one line with reason in the report. File any discovered bug
    as a tracker item immediately.
  - *Wrong*: dismiss with code evidence.
- **Fresh builder from round 2 (`plane` and `local`):** The original builder fixes simple findings
  from round 1 itself. From round 2 onward, on architectural findings, or once context exceeds 180k
  tokens, the `ship` session starts a fresh builder subagent with a pointer-only brief naming only
  the branch or worktree, the diff command and the open findings.
- **At most 3 rounds (`plane` and `local`):** Each re-check uses a fresh reviewer receiving only the
  fix diff and open findings. After round 3, on a second dispute, or after two failed attempts on
  the same finding, record a ruling or escalate under "Blocked" instead of patching again.

## 5. Pull request

Rebase onto the latest default branch, push and open the pull request (`github-flow`). Add one line
to the body stating how the change was proved. Watch CI checks without `sleep` and fix every red
check with fresh proof before pushing again.

With `atelier`, push the assigned branch and open the pull request as the runner's brief says.
Atelier watches the checks and owns the later review rounds.

## 6. Merge gate

Never merge under `atelier`. Atelier owns the merge gate and the serialized merge.

Merge only when all hold on the latest commit:

- Proof covers every change in the diff.
- Every required check is green.
- Every review finding is fixed or dismissed with a written reason.
- No human review requests changes.
- Branch is up to date and mergeable.

Use `github-flow`'s merge method. Never use `--admin`, disable rules or pass `--no-verify`. Without
a remote, merge locally after checks and delete the branch.

## 7. Report

With `atelier`, post the proof with `atelier --json comment --type task --id <task> --body -`.
Post each ruling with `atelier --json comment --type task --id <task> --kind ruling --body -`.
Answer with the runner's output schema, including the pull request URL and assigned branch. Do not
run `finish` or `set`.

For `plane` and `local`, run `finish <sub-item> --done -` once the brief is met:

- **What changed**: one or two sentences plus pull requests or merge commits.
- **Proof**: what ran and the decisive observed line.
- **Rulings**: one line per ruling (`Ruling: <decision>, because <reason>. If wrong: <cost>.`).
- **Found**: out-of-scope bugs or work with their created item IDs (omit if none).
- **For the owner**: items to look at, decide or do, with locations (omit if none).

Write the area report next if `finish` says it is due, except under `work-loop` where the loop
gates area reports through its pre-review first. A flat item needing owner input ends with an
area report instead of `--done`.

If stopping early (including after one compaction), post a handover comment with what is done and
remaining, and run `set <sub-item> --state ready`. Under `atelier`, answer with the runner's
`escalate` status instead of running `set`.

## Area report

Due when an area is `in-progress` with no `ready` or `in-progress` sub-items. Read the area and all
sub-items finished or parked since the last report:

1. Rewrite the area description with current outcome, dated decisions and open questions.
2. Attach any unattached files the owner needs to inspect.
3. Run `finish <area> --review -` with non-empty sections in this order:
   - **To look at**: question and where to look.
   - **To decide**: numbered open decisions with lettered options `[a-z]`, recommended first, with
     plain context and linked parked items.
   - **To do by hand**: human-only steps (device, real client, external service, release).
   - **Rulings**: rulings that change what the owner receives.
   - **Done**: one line per sub-item with pull requests.
   - **Next**: one line per queued `idea` sub-item.

Include no proofs, logs or session reports. With the `local` tracker, post the report in chat too.
With `atelier`, the delivery packaging phase replaces this section. Do not finish an Area manually.

## 8. The next item

In an interactive session with `start_session`, offer the first `frontier` line with `initiation`
set to `offer`, a title naming the item and a 5 to 8 line pointer-only brief telling it to run
`ship`. With an empty frontier, say so instead. Skip this step under `work-loop` or `atelier`.

## Rulings

Record autonomous decisions as `Ruling: <decision>, because <reason>. If wrong: <cost>.`.

## Blocked

Stop and ask only when:

- no method can prove the change,
- the merge gate cannot pass and you cannot fix it,
- the next step deletes data, exceeds project rules on a live system or edits outside the repo,
- the goal is ambiguous in a way that changes the result,
- another pull request obsoletes this one.

Finish independent parts of the brief first. Interactive sessions ask with `AskUserQuestion`.
Without an answer, leave the pull request open, add the question to the area, post a handover
comment and park with `set <sub-item> --state idea`. Under `work-loop`, return `QUESTION:` or
`BLOCKED:` to the loop. For unreachable environments (device, account, host), claim, park with what
remains and why, and list it under **To do by hand**. Write the area report if parking leaves no
active sub-item, except under `work-loop`.

Under `atelier`, do not use `AskUserQuestion` or `set`. Post a handover comment and answer with
`status: "escalate"` and the reason in the runner's output schema.
