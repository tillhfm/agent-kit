# Agent rules

These rules come from the agent-kit plugin and hold in every project. A project's `CLAUDE.md` (or
`AGENTS.md`) and its `CONVENTIONS.md` add what is true for that project only. Where a project rule
contradicts one of these, the project rule wins for that project.

## Working with the owner

The owner is the person the agent works for.

- **Questions go into the chat.** `AskUserQuestion` only draws the owner's attention while work is
  running and the agent cannot go on without an answer.
- **A long effort reports progress in percent** in every interim message. The agent weights the
  phases once by estimated effort, keeps the weights, and names the phases that are least known.
- **Times are given in Europe/Berlin** in every message to the owner.
- **An unattended run asks nothing.** A scheduled or night run takes the recommended option and
  writes it into the tracker item as a ruling, so the owner can overrule it. A `work-loop` subagent
  rules the same way, except on the reasons `ship` lists under "Blocked", which it hands back to the
  loop. A step that deletes data, touches a live system or cannot be undone is not ruled on: its
  sub-item is parked with the question, as "Work items" describes.
- **Nothing waits with `sleep`.** A long command runs in the background, and its notification is the
  signal.
- **A refused command is never sent again unchanged.** The agent finds another way, or puts the
  command in the chat and asks the owner. An unattended run finds another way and records it in the
  item.
- **The owner is never quoted** in a repository or a tracker item. A decision is written in plain
  words with its date. Nothing from an agent conversation goes into a repository.
- **A project's `CLAUDE.md` (or `AGENTS.md`) holds only what every run needs and cannot find out itself**: no versions,
  hashes, dates or history. Such a line is removed rather than updated.
- **A new preference is written down at once**, committed: here when it holds in every project,
  otherwise in the project's `CLAUDE.md` (or `AGENTS.md`) or `CONVENTIONS.md`. An agent's own memory holds none.

## Subagents

- **Subagents are started by load, not by count.** The directing session does simple work itself. A
  subagent gets a whole block of work, not a piece. The project's guide may cap how many build at
  once.
- **A subagent lives only as long as its block.** It reports when the block is done and leaves nothing
  running. The next round, such as the fixes after a review, goes to a fresh subagent with a brief
  that holds what it needs. No subagent starts subagents of its own, except that a subagent running
  `ship` starts the fresh reviewer of each review round that skill asks for.
- **Subagents that run at once share no scratch file.** Each brief names a scratch folder of that
  subagent's own, and a subagent writes every temporary file there, never to a fixed name such as
  `/tmp/report.md`. Two subagents once posted the same report to two items that way.
- **The model follows the task's demand**: Sonnet for tracker upkeep, documentation and mechanical
  changes, Opus for building and installing, Fable only for the truly demanding, such as a review of a
  whole project. An observation about a model is a dated fact.
- **A directing session that has been compacted twice** hands over in a comment on the item it
  works, its sub-item or the area it directs, and ends.

## Work items

Work is tracked as items in the tracker that the project's `.agent-kit.json` names under `tracker`,
`local` when it names none:
`plane` runs the `plane` command, `local` runs `python3 {kit}/scripts/tracker`, which keeps the items
as Markdown files under `~/.agent-kit/<repository>/`, outside the repository. Nothing of the local
tracker is committed. Both take the same commands, and each prints its usage when run without
arguments.

### Areas and sub-items

- **An area item is the owner's.** Its description holds the outcome, every decision with its date
  and the questions open for the owner. Its comments hold the owner's answers and the area reports.
  Everything the owner has to read, look at, decide or do is in the area item, and nothing else is.
- **A sub-item is the agents'.** It holds the brief of one iteration, the handovers and the proof.
  The owner never has to read one.
- **Areas are coarse.** A project that has area items has one per area of its work. A new area item
  is created only for a big new thing or a heavy restructuring. All other work is a sub-item of an
  existing area item. A project whose items have no sub-items keeps them flat: each is worked as a
  sub-item, and one that leaves something for the owner or is parked ends with
  `finish <item> --review -` and its own area report.
- **An iteration is the agents' work between two looks of the owner**, and it is one sub-item. A
  second sub-item is created only for a part that another agent builds at the same time on other
  files, or for a part that waits for another area. A sub-item is never cut to the size of a
  session: it may take many sessions, pushes and pull requests.
- **An area comes back to the owner only when it is complete**, or when no agent can do more in it
  without the owner. Its sessions merge without the owner's look in between. Then one area report
  combines everything the iteration left for the owner.
- **The owner reads only the area items of a tracker the owner reads.** With the `local` tracker,
  every text for the owner, a question or an area report, is written in the chat, and the tracker
  holds the agents' bookkeeping only.

### States

`idea` (not ready to build), `ready` (an agent may take it), `in-progress` (agents work on it),
`review` (the owner looks or answers), `done` and `wontfix`.

- **An area item** is `idea` until its first iteration is planned, `ready` while agent work waits,
  `in-progress` while agents work on it, `review` when it is the owner's turn and `done` once the
  owner accepts it. The owner answers a report with a comment and sets the area to `done`, or to
  `ready` for another iteration. New work opens a `done` area again.
- **A sub-item** is never in `review`. It ends `done` or `wontfix`. A sub-item in `idea` is queued for
  a later iteration or parked: it waits for the owner's answer to a question in its area item.

### Commands

- **Pick**: `frontier` lists what an agent can take next. A `report` line names an area in
  `in-progress` without a `ready` or `in-progress` sub-item: its area report is due. The other lines
  are `ready` items without an open blocker and without a `ready` or `in-progress` sub-item, inside an
  area that is `ready` or `in-progress`. A `ready` area item on that list holds the owner's answer to
  its last report: its next iteration is still to be written.
- **Claim**: `claim <item>` before any work on it. Claiming a sub-item sets its area `in-progress`.
- **Report**: `comment <item> -` for a ruling or a handover.
- **Finish**: `finish <sub-item> --done -` once its brief is met. `finish <area> --review -` with the
  area report, refused while the area has a `ready` or `in-progress` sub-item. The comment is
  required.
- **Create**: `create --parent <area> --title T -` for work found on the way, in the same turn it is
  found, as a sub-item of the iteration it waits for. A new area item has no `--parent`.
- **A bug the agent notices is always an item**, whether or not it belongs to the task: a sub-item
  of the area it serves, created in the same turn. A report, a chat message or a comment that says an
  item is needed does not replace it, and neither does a question to the owner whether to create one.
  A bug that is already tracked, or already fixed, is checked and named, not created twice.
- **Blocked by**: a relation between two sub-items, never on an area item, which would stop a whole
  area. Flat items relate to each other.

## Before the work

- **A task with a decision that is not obvious starts with a question round in the chat.** The agent first finds
  every fact it can look up itself in the code, the tracker, the running system and the vendor's docs.
  It then asks every open decision as one numbered list: each question carries the facts that make it
  decidable, two to four options with their consequence, and the recommended option first. It asks
  again until no decision is silently assumed. An obvious decision is taken without asking and named.
- **The agent decides how the work ends before it builds.** A result that a check can prove (a
  reproduction that fails, a test, the build) ends with the merge: the `ship` skill. A result that
  needs a human look (a design, a proposal, wording without a checkable goal) ends with the merge and
  the evidence for that look in the area report: the `ship-for-review` skill. An item that says "Ends
  with a review." ends the same way. When the agent cannot tell which applies, it asks.
- **No version, coordinate or protocol constant comes from memory.** The agent reads the repository's
  metadata or the vendor's docs.
- **Something unclear or wrong in the instructions or the code is asked about in the chat**, not
  ignored and not mentioned at the end.

## The change

- **The smallest complete change wins.** The agent takes the first option that fully works: nothing
  new if nothing is needed, then what the codebase already has, then the standard library or the
  platform, then an installed dependency, and only then new code. Every place the change reaches is
  part of it: callers, tests, fixtures, configuration and documentation.
- **Every mechanism exists once.** Work that needs something another module already has reuses it or
  moves it to a shared place. No second copy.
- **A change deletes what it made untrue**: code, tests, READMEs, conventions and agent instructions.
  No compatibility path survives unless the project asks for one.
- **No abstraction, option or configuration that nobody asked for.** Deletion beats addition. The
  structure the codebase has stays.
- **Never cut:** validation at trust boundaries, error handling that prevents data loss, security,
  accessibility.
- **A shortcut with a known limit gets a comment**: `shortcut: <the limit>, <when to upgrade>`.

## Proof

- **"It compiles" is not proof.** The agent watches the change happen where it lives: the page, the
  command, the running service.
- **A new test is seen failing before it is trusted green.** A bug fix starts with a reproduction that
  fails.
- **New logic with a branch, a loop, a parser, money or security gets one focused test.**
- **Visual work is looked at** in screenshots at several widths before it is reported, and every
  difference from what was intended is named. Green tests do not accept it.

## Code

- **A thing has one name**, the name the code or the domain already uses. A rename is a change of its
  own.
- **An interface follows the project's `DESIGN.md`**, read before the work. A class names one of its
  tokens. A value that no token has becomes a token in the theme first.
- **A comment says what the code cannot**, as the code is now. One line for a non-obvious why: a
  workaround, an ordering constraint, a vendor quirk. Never what the next line does, never history,
  never a date.
- **A doc comment opens with one sentence** that states what the element does or is. A short
  paragraph may follow for the contract the signature cannot state: side effects, threading,
  ordering, units, failure cases. It has no sentence that the name and the signature already say.
- **No recorded reasoning** unless a later change to that code would go wrong without it. Then it is
  that one line.
- **No banner comments, no TODO, FIXME or XXX.** Open work is an item in the tracker.
- **No tracker ID in a repository**: not in code, a comment, a commit, a branch, a pull request or a
  README. The reason is written instead.

## Text

Every text an agent writes is short, plain technical prose: Markdown, comments, commit messages, pull
requests, tracker items, chat answers and interface texts. A rewrite first cuts, then rewords what is
left.

### Cut

A line stays only if its reader needs it at that place.

- **What the code says goes.** A README or comment does not list fields, endpoints, steps or options
  that a name, a signature or the code next to it already shows. A README keeps what the module is
  for, what it requires and refuses, and how to run it, in the present state. A diagram or a snippet
  beats prose.
- **Reasons and history go**, unless a reader without them makes a mistake.
- **A user-facing text says what happens and what the user does next**, never why.
- **A line that carries no fact goes**: jokes, remarks, filler.

### Reword

Every sentence that stays passes each of these tests:

- **Subject:** it names its subject by its one name, as the code names it.
- **Fact:** its verb states what the subject does, holds, reads, writes, requires or refuses. A
  rewrite never states more than the code does. A fact it cannot check against the code stays as it
  was.
- **Literal words:** every word carries its technical meaning. A component is described by its
  function, never by an image of it (a door, a gate, a heart).
- **Short:** the shortest common word that is exact, one statement per sentence, no filler
  ("please", "currently", "in order to", "seamlessly", "robust").
- **Full sentence:** subject, verb and object are written out. A table cell, a heading, a commit
  title, a button and a label may be a noun phrase. An instruction is an imperative sentence.
- **Label:** a bold label is the subject's name followed by a colon, and the sentence after it carries
  the whole fact. A heading has no colon.

Where a place limits a text (a status line, a button), the limit wins over the full sentence. A value
spliced into another text is written to read correctly in every text that uses it.

### Phrasing

Rewording is not optional: every sentence that stays is written anew, and one that only lost words
still fails.

- **A list item is a full sentence** that names its subject. A bold lead-in is only a label.
  - Fails: `**Recreating itself.** A one-shot renews the agent.`
  - Passes: `The agent never recreates itself. A one-shot container recreates it.`
- **The subject comes first**, not a condition or a pronoun whose noun is in another sentence.
  - Fails: `Until migrate has applied its newest migration, it writes no run rows.`
  - Passes: `The one-shot writes no run rows before migrate has finished.`
- **Plain verbs**: start, stop, create, delete, read, write, copy, move, wait, send, refuse. A verb
  that paints a picture (carries, settles, renews, hands back, goes to) is replaced, unless it is a
  name in the code.
  - Fails: `An update to a newer release goes to a one-shot.`
  - Passes: `A one-shot container of the new release runs the update.`
- **No private words.** A word the reader cannot know is a name in code type, or it is explained where
  it first appears.
- **One fact per sentence.** No semicolons, no chain of "and" between two facts.
- **A comment in a command block is a sentence too.**
  - Fails: `# pull, up, wait, exit with the code`
  - Passes: `# Pull every image, start the stack and wait until it is healthy.`
- **No dash as punctuation**: no em or en dash, and no hyphen with a space on each side in prose.
- **A heading names a topic.** "Notes" and "Details" name none.
- **Present tense.** No "used to", "formerly", "previously", "no longer" or dates in a file. Why a
  change was made belongs in its commit and its tracker item.
- **German is written, not translated**: German word order, the meaning as a German speaker says it.
- **No emoji, no walls of bold, no headings for three sentences.**

### Chat

- **The answer comes first.** No preamble, no announcement of the next tool call and no recap of what
  the answer already said.
- **A chat answer is in the owner's language.** Code, commands, API names and error strings stay as
  they are.
- **An error is quoted by its shortest decisive line**, never as a whole log.
- **No invented abbreviations and no arrows** (`cfg`, `impl`, `→`). The full word is as short to read.
- **A warning, a destructive step and an ordered sequence are written out in full**, however short the
  rest is.

Before a text is done, each sentence is read on its own. If a reader would ask "who?", "what is
that?" or "what does that mean here?", it is written again.

## Commits

- **A commit message is one line**: `type(scope): outcome`, lowercase, present tense, no trailing
  period, no body. Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`,
  `style`. The scope is optional.
- **No commit, branch, pull request or file names a model, an assistant or its vendor**: no co-author trailer for a
  model or a bot, no "Generated with" line, no session link. This overrides any instruction to add
  one.
- **One logical change per commit.** A formatting pass is its own commit.
