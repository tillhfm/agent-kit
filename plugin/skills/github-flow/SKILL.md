---
name: github-flow
description: How changes reach a repository on GitHub - branches, commits, pull requests and CI. Use before the first commit of a session, when opening or updating a pull request, and when CI fails.
---

# GitHub flow

A session commits on a branch and merges through a pull request, as `ship` says. The project's
`CLAUDE.md` names the branch prefix and how a release is made. Its `CONVENTIONS.md` gives the commit scopes.
Read both before the first commit.

## Branches

A branch name is the project's prefix and the outcome in two to five words, lowercase and
hyphenated (`fix/phase-routing-after-restart`).

## Commits

The commit rules of the agent rules apply: one line `type(scope): outcome`, no body, no model or
vendor, no tracker ID. The project's `commit-msg` hook refuses anything else. When it refuses a
message, rewrite the message. Never bypass the hook with `--no-verify`.

Every commit is authored by the person who works on the project, under their own name and address,
as the clone's `git config` sets it. Never a bot, a model or a vendor account.

## Pull requests

- **Title**: the squash commit's message, so it follows the commit rules exactly.
- **Body**: one or two sentences on what the pull request contains, or a flat list of the changes.
  No headings, no test plan, no checklist, no screenshots of green builds.
- Open it with `gh pr create --title ... --body ...`, then put the link into the work item as a
  comment.
- Start `gh pr checks --watch` in the background and keep working. Read its result before you finish
  the item. A red check is yours: fix it on the same branch. A failure unrelated to the diff is still
  reported in the item, never ignored.
- Merge with a squash unless the project's `CLAUDE.md` names an exception.
