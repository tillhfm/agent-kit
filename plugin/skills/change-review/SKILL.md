---
name: change-review
description: Review a change in a fresh session for correctness, against the repository's CONVENTIONS.md and against the work item it implements, as three separate verdicts. Use on a branch, a range of commits or a pull request before finishing an item.
---

# Change review

Run in a completely fresh session, preferably on a different provider than the builder. Read only.
Never edit the checkout, and treat the author's claims as unverified.

Answer three questions separately:

- **Correctness**: does the changed code work for every reachable input and state?
- **Standards**: does the diff follow `agent-kit` rules and the repository's `CONVENTIONS.md`?
- **Item**: does the diff implement the work item completely, with nothing missing or extra?

## Setup

1. Verify the base ref resolves and the diff is non-empty: `git diff <base>...HEAD` and
   `git log <base>..HEAD --oneline`.
2. Read the tracker item from the pull request or brief. Without an item, skip the Item verdict and
   say so.
3. Review all three axes yourself when running as a `ship` reviewer or on a small diff. On a large
   standalone review, you may give each axis to a separate read-only subagent with a pointer-only
   brief (diff command, commit list and its reference doc).

## Axes

- **Correctness**: report concrete bugs (wrong condition, missed case, swallowed error, race,
  leaked resource, data loss, trust-boundary flaw) with file, line, input or state and failure mode.
  Read surrounding code as needed. Never report unverified guesses.
- **Standards**: cite broken written rules. Skip checks the build already enforces. Call out design
  smells only as judgment calls (duplication, misleading names, speculative abstractions). Check
  `github-flow` commit and pull request rules. Apply `wording` (with cold read) to changed
  user-facing text and `ui-guidelines.md` beside this skill to changed UI code (`CONVENTIONS.md`
  and `DESIGN.md` win on conflict).
- **Item**: quote the item line for every missing, partial, wrong or unrequested change.

## Result

Output three short lists (**Correctness**, **Standards**, **Item**), graded **blocking**,
**should fix** or **minor**, followed by one closing line naming the worst finding of each list.
On a re-check round, receive only the fix diff and prior open findings, and mark each finding
addressed or open. When the review is for the session's own work, fix the findings before finishing
the item. When it is someone else's pull request, post them as a review.
