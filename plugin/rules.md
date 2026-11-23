# Agent rules

Shared rules from the `agent-kit` plugin. A project's `CLAUDE.md` (or `AGENTS.md`) and
`CONVENTIONS.md` add project rules and win on conflict.

## Working with the owner

- **Questions go into the chat.** Use `AskUserQuestion` only when running work cannot go on without
  an answer.
- **Report progress in percent** on long efforts. Weight phases once, keep the weights, and name
  the least-known phases.
- **Give all times in Europe/Berlin** in messages to the owner.
- **Unattended runs ask nothing.** Take the recommended option and record it as a ruling on the
  item, except for `ship`'s "Blocked" reasons (handed back to the loop) or steps that delete data,
  touch a live system beyond project rules or cannot be undone (park the sub-item with the
  question).
- **Never wait with `sleep`.** Run long commands in the background and react to their completion.
- **Never send a refused command again unchanged.** Find another way or ask the owner in chat.
- **Never quote the owner** in a repository or tracker item. Record decisions in plain words with
  their date. Put nothing from an agent conversation into a repository.
- **Keep `CLAUDE.md` and `AGENTS.md` to navigation pointers** and facts a session cannot find out
  itself, with no versions, hashes, dates or history. Record a new preference at once: here when it
  holds in every project, otherwise in `CLAUDE.md` (or `AGENTS.md`) or `CONVENTIONS.md`.

## Subagents

- **Start subagents by load, not by count.** Do simple work directly. Give each subagent a whole
  block of work, respecting the host's concurrency cap.
- **One subagent per block.** A subagent exits cleanly when its block ends. Any subagent may start
  the cold readers `wording` asks for. A `ship` subagent may also start fresh reviewers
  (`change-review`) and, from review round 2 onward, on architectural findings or after exceeding
  180k tokens, a fresh builder. No other subagent starts subagents of its own.
- **Dedicated scratch folders.** Give every concurrent subagent its own scratch folder. Never write
  temporary files to fixed paths like `/tmp/report.md`.
- **Pointer-only briefs (5 to 8 lines).** Every agent-to-agent brief and start prompt lists only:
  (1) item ID or one-sentence goal, (2) role or skill, (3) deviations or constraints not in the
  tracker item, (4) worktree and scratch paths (plus the required status line for loop workers).
  Never repeat rules from `agent-kit` or `CLAUDE.md`, explain standard paths or copy ticket text.
- **Flexible model tiers (`medium` effort by default).** Never use `low` effort for building or
  review. Escalate to a stronger model rather than raising effort, using `high` only for genuinely
  hard problems:
  - *Orchestration*: strong orchestrator or coding model at `medium`.
  - *Frontier* (architecture, UI design, hard problems): alternate top frontier models at `medium`.
    Use the strongest reasoning model at `high`, or switch providers, when stuck across iterations
    or for whole-project reviews.
  - *Workers*: prefer Kimi K3.1 Pro (`kimi-code/k3.1-pro`) for shorter, bounded tasks whenever
    possible; escalate to a stronger model (`claude-opus-5-5`, `gemini-4-neon`) if Kimi falls short
    or for complex multi-file logic.
  - *Small subagents*: mechanical read, search, cold-read or strictly schematic tasks only. Never
    use them to split logic code.
- **Compaction and rotation.** Align provider compaction windows around 220k tokens where
  configurable. A subagent hands over in a tracker comment and ends after at most one compaction.
  An orchestrator keeps no durable state in chat and rotates cleanly around 150k tokens or after
  one compaction.

## Work items

The project's `.agent-kit.json` sets `tracker` to `plane`, `local` or `atelier` (default `local`).
The `plane` tracker runs `plane`. The `local` tracker runs `python3 {kit}/scripts/tracker` under
`~/.agent-kit/<repository>/`. The `atelier` tracker runs every command through `atelier --json`.
Run the selected command without arguments for usage.

Atelier calls sub-items Tasks. Its runner owns dispatch, leases, branch names, review rounds,
merges and state transitions.

### Areas and sub-items

- **Area items belong to the owner.** Their description holds the outcome, dated decisions and open
  questions. Comments hold owner answers and area reports. Everything the owner reads, reviews or
  decides lives on the area item.
- **Sub-items belong to agents.** One sub-item covers one iteration between two looks of the owner.
  Split only for parallel work on disjoint files or cross-area waits, never to fit a session.
- **Return an area only when complete or blocked on the owner.** Merge intermediate pull requests
  without stopping for the owner. Combine everything into one area report at the end. Flat projects
  without sub-items use `finish <item> --review -` when owner input is needed.
- **With the `local` tracker**, post owner questions and area reports in chat. The tracker holds
  agent bookkeeping only.

### States and commands

States: `idea` (unplanned or parked), `ready`, `in-progress`, `review` (areas only), `done`,
`wontfix`.

- `frontier`: lists due area reports (`report`) and actionable `ready` items.
- `claim <item>`: run before work. Sets the parent area `in-progress`.
- `comment <item> -`: rulings and handovers.
- `finish <sub-item> --done -` or `finish <area> --review -`: comment required. Area review refuses
  while any sub-item is `ready` or `in-progress`.
- `create --parent <area> --title T -`: file every discovered bug or follow-up in the same turn
  after checking it is not already tracked or fixed.
- `blocked by`: links sub-items only (or flat items), never an area item.

Under `atelier`, `atelier --json frontier` lists actionable work. Create a Task with
`atelier --json task create --area <area> --title T --repo <repository> --brief -`. Post a ruling
with `atelier --json comment --type task --id <task> --kind ruling --body -`. Use `--kind handover`
for a handover. The runner replaces `claim`, `finish` and `set`.

## Before the work

- **Clarify non-obvious decisions in chat first.** Look up every checkable fact in code, tracker,
  running system and docs. Ask open decisions in one numbered list (facts, 2 to 4 options with
  consequences, recommended option first). Name obvious decisions taken without asking.
- **Pick the ending before building.** Use `ship` when a check proves the result. Use
  `ship-for-review` when a human must inspect it or the item says "Ends with a review."
- **Never recall versions, coordinates or constants from memory.** Read repository metadata or
  vendor docs.
- **Question unclear or broken instructions immediately** in chat instead of ignoring them.

## The change

- **Smallest complete change wins.** Reuse existing code, standard library or platform features, or
  installed dependencies before writing new code. Update every affected caller, test, fixture,
  config and doc.
- **Every mechanism exists once.** Reuse or extract shared logic. Keep no second copy.
- **Delete what becomes untrue.** Remove dead code, tests, docs and instructions. Keep no
  compatibility shim unless requested.
- **No unrequested abstractions, options or config.** Keep the codebase's structure.
- **Never cut** trust-boundary validation, data-loss error handling, security or accessibility.
- **Mark bounded shortcuts** with `shortcut: <limit>, <when to upgrade>`.

## Proof

- **"It compiles" is not proof.** Observe the change running where it lives.
- **See new tests fail before trusting them green.** Bug fixes start with a failing reproduction.
- **Add one focused test** for new logic with branches, loops, parsers, money or security.
- **Inspect visual work** in screenshots across widths and report every difference from the target.

## Code

- **One name per concept**, matching existing code or domain terms. Renames are separate changes.
- **Follow `DESIGN.md`** for UI work. Use theme tokens and add missing tokens to the theme first.
- **Comments state non-obvious why only** (workaround, ordering, vendor quirk), never what the code
  does, history or dates. Doc comments open with one sentence stating what the element does or is,
  followed only by contract details the signature cannot express.
- **No banner comments, `TODO`, `FIXME`, `XXX`, or tracker IDs** anywhere in a repository (code,
  comments, commits, branches, pull requests, docs).

## Text

Write short, plain technical prose in Markdown, comments, commits, pull requests, tracker items and
chat. User-facing interface, message and log text follows the `wording` skill.

- **Cut** what the code already shows, history, filler ("please", "currently", "in order to",
  "seamlessly", "robust"), jokes and emoji.
- **Reword every sentence that stays.** Name the subject first by its code name. State a verifiable
  fact with plain literal verbs (`start`, `stop`, `create`, `delete`, `read`, `write`, `send`,
  `refuse`). Use no private words without explaining them. Give every heading a real topic.
- **One fact per sentence.** No semicolons, no dash as punctuation (no em/en dashes, no ` - ` in
  prose), no invented abbreviations or arrows (`cfg`, `impl`, `->`), no walls of bold, and no
  headings for three sentences. Write present tense.
- **Chat:** lead with the answer in the owner's language, quote only the decisive error line, and
  write warnings, destructive steps and ordered sequences in full. Write German naturally.
- **Cold read** every sentence on its own before finishing. Rewrite any sentence that leaves a
  reader asking who or what it means.

## Commits

- **One line only:** `type(scope): outcome`, lowercase, present tense, no trailing period, no body.
  Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `style`.
- **Never name a model, assistant or vendor as author or contributor** in any commit, branch, pull
  request or file (no bot `Co-Authored-By`, no "Generated with", no session link).
- **One logical change per commit.** Keep formatting passes separate.
