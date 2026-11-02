---
name: plan-work
description: Turn a vague idea into the next iteration of an area item in the tracker, settled with the owner in rounds of questions until nothing is silently assumed. Use when the owner brings an idea, a feature or a change that is not ready to build, or says to plan, grill or clarify something.
---

# Plan work

The result is the next iteration of an area: its decisions in the area item and one sub-item in
`ready` that holds the brief, as the rules under "Work items" describe. A sub-item is not cut to the
size of a session. A new area item is created only for a big new thing or a heavy restructuring.

## Facts first

Anything the code, the running system, the tracker, GitHub or a vendor's docs can answer is the
agent's to look up, never a question. A version or a measured number carries its date.

## Rounds of questions

A plan is a tree of decisions: each answer opens the decisions that hang off it.

1. Collect the frontier: every open decision whose prerequisites are settled. A question whose
   answer depends on another open question waits for a later round.
2. Ask the whole frontier in the chat as one numbered list, as the rules on the question round
   describe: the facts, two to four options with their consequence, the recommended option first.
3. Read the answers as they are. A free-text answer can change the tree, add a rule or overrule an
   earlier decision. An answer that contradicts something already written (a guide, a skill, an
   item) is a question for the next round, not a silent edit.
4. Repeat until the frontier is empty.

No-brainers are decided without asking and named. A decided question is not asked again.

## A check by a stranger

Before the items are written, a fresh subagent reads only the draft items and lists the questions it
would still need answered to build them, most important first, or says that none is left. Each
question is answered from the facts or asked in the next round.

## The items

Summarise the plan in a few lines and have the owner confirm it in the chat. Then write it:

- **The area item** gets the decisions. Its description is rewritten so it states the outcome, every
  decision with its date as "Decided <date>: ...", never quoting the owner, and the questions still
  open. For a decision that rests on an assumption, one sentence on what happens if it is wrong. The
  area is set to `ready`, unless agents already work on it. A new area item takes the title of the
  area or of the big new thing.
- **The sub-item** is created with `create --parent <area> --state ready`. Its title is the
  outcome of the iteration in plain words. Its description is the brief: what to build and, where it
  is not obvious, why, "Ends with a review." when the result needs the owner's look, and one
  sentence under **Done when** that names what is observed when the iteration is finished.
- **A second sub-item** is created only for a part that another agent builds at the same time on
  other files, or for a part that waits for another area. **Blocked by** is then a relation between
  the two sub-items, never a sentence.
- **Sub-items queued for later**, such as work that waits for the owner's look at this iteration,
  stay in `idea`.

A design direction (a new `DESIGN.md`, a design proposal) ends with a review. Its session uses the
`frontend-design` skill where the project enables it.

Once the sub-item exists, offer the first line that `frontier` lists as a session of its own, as
`ship` does in its last step, so the owner can start building with one click.

## Unattended runs

They ask nothing. The rules say what they do instead.
