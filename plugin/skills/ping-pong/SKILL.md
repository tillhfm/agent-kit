---
name: ping-pong
description: Orchestrate alternating fresh build and strict review rounds across providers, starting from a read-only audit and blueprint. Use for iterative quality work on web interfaces, in-game visuals, or backend and architecture improvements, either on one area or across a whole system.
---

# Ping-pong

The session acts as a thin orchestrator. It does not edit repository code or perform reviews itself.
Each phase runs in a fresh subagent with a dedicated scratch folder and a pointer-only brief. Pair
builder and reviewer across different providers whenever available, following the project's model
guide.

## 1. Scope and modes

Pick the mode before starting:

- **Focused (`area`, default)**: improves one screen, module, subsystem or workflow from audit
  through alternating build and review rounds to a finished branch.
- **Broad (`system`)**: audits a whole application or architecture first (structure, navigation,
  shared concepts, cross-area boundaries or systemic bottlenecks) and returns a consolidated
  blueprint for owner approval before any build starts.

Track the effort in an isolated tracker area and sub-item (or the existing item named in the
request). Record each round's outcome and rulings there. Weight the planned phases once and report
progress in percent as rounds complete.

## 2. Round 0: Audit and blueprint

Start a fresh, read-only reviewer on the strongest reasoning or frontier model available (`high`
effort when supported). Pass the target scope, relevant design or architecture docs (`DESIGN.md`,
`CONVENTIONS.md`, domain specs) and any owner hypothesis to evaluate critically.

Require three outputs:

1. A direct diagnosis of the main flaws in the current state.
2. Clear architectural or design decisions with trade-offs.
3. A concrete, prioritized Round 1 implementation specification ready for a fresh builder.

In **broad (`system`)** mode, stop after Round 0. Present the blueprint (shared structural changes
plus a prioritized list of follow-up areas) to the owner for approval before starting any build.

## 3. Alternating build and review rounds

Alternate build and review rounds on one feature branch until the quality bar is met. Do not stop
after an arbitrary round count while rounds still deliver meaningful improvements.

- **Build round**: start a fresh builder in an isolated worktree on the feature branch (reusing the
  same branch across rounds). Pass only the Round 1 blueprint or the open findings from the latest
  review. The builder implements the changes, runs tests, local pre-PR checks and direct proof,
  opens a draft pull request in Round 1 and pushes updates in later rounds.
- **Strict review round**: start a fresh, read-only reviewer on a different provider than the
  builder. Pass only the base ref, diff command, target scope, relevant project docs and prior probe
  scripts, never the builder's reasoning. The reviewer inspects the code and probes the running
  system directly, then returns concrete findings graded **blocking**, **high impact** or **minor**
  with exact locations and reproduction steps.

## 4. Domain rules

Every review round verifies the running change directly rather than reading the diff alone.

### UI and UX work

Apply these criteria in Round 0 and every review round for web, desktop or admin interfaces:

- **User guidance and task flow**: judge whether a user immediately sees what to do next, where they
  are, and what happens on each action. Cut unnecessary chrome, deep nesting and avoidable page
  scroll so the primary workspace carries the screen.
- **Cognitive load and interaction friction**: minimize clicks, modal hops and hidden disclosures on
  frequent tasks. Prefer direct manipulation where it fits, keep related controls visible together,
  and support keyboard flow, undo or safe recovery on destructive edits.
- **States and feedback**: verify empty, loading, error, saving and validation states. Blocking
  issues must surface clearly and guide the user directly to the affected field or control.
- **Visual hierarchy and consistency**: check against `DESIGN.md` (tokens, contrast, spacing,
  typography, alignment) and `wording` (short, plain user-facing text). Check layouts across
  viewports (mobile, tablet, desktop) for overflow, clipping or unintended scroll.
- **Interactive Playwright probing**: run real user journeys against the live interface (clicks,
  typing, drag and drop, keyboard focus, resize and edge cases). Save reusable probe scripts in the
  scratch folder so later review rounds repeat the same scenarios.

### In-game and visual surfaces

For visual surfaces outside the browser (such as Minecraft menus, HUDs, dialogs or resource packs),
inspect live or rendered states, timing, readability, text wrapping, contrast and interaction edge
cases against the project's visual and wording rules.

### Backend, APIs and architecture

For technical work, probe the running code with focused test harnesses, contract checks, failure and
concurrency cases or benchmarks. Verify data integrity, error handling, trust boundaries, API
ergonomics and clean module boundaries.

### Stepwise visual protocol

Follow this protocol whenever a review inspects screenshots or rendered images:

1. Start with a code overview and automated DOM or state assertions.
2. Load screenshots in small batches of at most 2 to 3 images per step.
3. Write findings to a scratch file immediately after each batch before taking or reading the next.
4. Never load dozens of images into one context window, because compaction erases visual detail.
5. Save reusable probe scripts in the scratch folder so later review rounds repeat the same checks.

## 5. Stopping and handoff

Stop the loop when any of these holds:

- The reviewer reports no **blocking** or **high impact** findings.
- Two consecutive rounds stall or oscillate on the same issue without meaningful improvement.
- The request sets an explicit round cap and that cap is reached.
- A product or architectural trade-off needs an owner decision. Pause and ask in chat with numbered
  decisions and lettered options.

Finish cleanly once the loop ends:

1. Run a final `change-review` on the branch to check code correctness, standards and scope.
2. Collect evidence for the owner where relevant (before and after screenshots across viewports and
   a short Playwright video for UI work, or probe and benchmark outputs for backend work).
3. Default ending: mark the pull request ready for review and leave it open for the owner without
   merging.
4. Optional ending: when the request explicitly asks to merge, finish through `ship` or
   `ship-for-review` once the merge gate passes.
