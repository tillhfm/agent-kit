---
name: change-review
description: Review a change for correctness, against the repository's CONVENTIONS.md and against the work item it implements, as three separate verdicts. Use before finishing an item that changed code, on a pull request, or when asked for a review of a branch or a range of commits.
---

# Change review

Three questions, answered separately, because a change can pass one and fail another:

- **Correctness**: does the changed code do what it claims, in every case it reaches?
- **Standards**: does the diff follow the agent-kit rules and the repository's `CONVENTIONS.md`?
- **Item**: does the diff do what the work item asked, nothing missing and nothing extra?

The reviewer only reads. It does not edit the checkout, and it treats the author's report and
reasons as claims to check, not as facts.

## Setup

Pin the base: the pull request's base branch, or the commit that was named. Check it resolves and
the diff is not empty before anything else: `git diff <base>...HEAD` and
`git log <base>..HEAD --oneline`.

Find the item: the pull request's link, or the item this session claimed, read from the tracker.
No item means no Item verdict. Say so rather than inventing a spec.

For a small diff, review the axes yourself, one after the other. For a large one, give each axis
to one subagent with the diff command, the commit list and its source (the rules and
`CONVENTIONS.md`, or the item's text), so none colours the other. A reviewer that is itself a
subagent of `ship` reviews all three axes alone.

## Correctness

Report each place where the changed code fails for an input or a state it reaches: a wrong
condition, a missed case, an error swallowed, a race, a resource left open, data lost, a security
hole at a trust boundary. Each finding names the file and line, the input or state, and what goes
wrong. Read the code around the diff where the change depends on it. A guess without that case is
not a finding.

## Standards

Report each place the diff breaks a written rule, citing the rule. Skip what the build already
enforces: the project's check on the touched code is the proof for that. Beyond the written rules,
name design smells only as judgement calls ("possibly feature envy"): duplicated logic, a
misleading name, parameters that always travel together, a speculative abstraction, one change
scattered over many files. A written rule always wins over a smell.

Also check what `github-flow` requires of the commits and the pull request text.

A diff that changes UI code is also checked against `ui-guidelines.md` beside this skill, a pinned
copy of the Web Interface Guidelines. A rule of the project's `CONVENTIONS.md` or `DESIGN.md` wins
over it.

## Item

Report what the item asked that is missing or partial, what the diff does that nobody asked
for, and what looks done but wrong. Quote the item's line for each.

## Result

Three short lists under **Correctness**, **Standards** and **Item**, not merged and not re-ranked.
Each finding carries a grade: **blocking**, **should fix** or **minor**. One closing line names the
worst finding of each list. When the review is the session's own work, fix the findings
before finishing the item. When it is someone else's pull request, post them as a review.
