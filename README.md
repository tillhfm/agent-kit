# agent-kit

A Claude Code plugin marketplace with one plugin, `agent-kit`: the agent rules every project shares.

- `plugin/rules.md` holds the shared rules. A SessionStart and a SubagentStart hook put it into the
  context of every session and every subagent.
- `plugin/hooks/format.py` formats and lints each file an agent edits, with the commands of the
  project's `.agent-kit.json`. It writes into the context only when it changed the file or found
  something.
- `plugin/skills` holds `setup`, `fix`, `change-review`, `github-flow`, and the workflow skills
  `ship`, `ship-for-review`, `work-loop` and `plan-work`.
- `plugin/scripts/tracker` is the local tracker: work items as Markdown files under
  `~/.agent-kit/<repository>/`, for a project that `.agent-kit.json` sets to `"tracker": "local"`.
- `plugin/templates` holds the files `setup` copies into a project.
- `plugin/scripts/palantir-java-format` runs the native palantir-java-format of the project's
  version catalog.

A project enables the plugin in its `.claude/settings.json`, as the `setup` skill shows. It follows
`main`: the plugin has no `version`, so every commit is a new one. An interactive session in a
project that sets `FORCE_AUTOUPDATE_PLUGINS`, as `setup` does, fetches it in the background within
ten minutes of its first message, with the git credentials the machine stores, and the next session
runs it. A change that must reach the next session at once is fetched by hand from the project's
folder: `claude plugin marketplace update agent-kit` and `claude plugin update agent-kit@agent-kit
--scope project`.

Run the tests with `python3 -m unittest discover -s tests`.

The kit is under the MIT license in `LICENSE`. The rules on the smallest complete change follow the
ponytail skill by Dietrich Gebert (MIT, `plugin/ponytail-LICENSE`). `ship` and `ship-for-review`
adapt the full-send and full-stop skills of t3dotgg/tstack by Theo Browne (MIT,
`plugin/skills/ship/tstack-LICENSE`). `change-review` carries a pinned copy of
vercel-labs/web-interface-guidelines (MIT, `plugin/skills/change-review/ui-guidelines-LICENSE`). The
`DESIGN.md` template follows the shape of `.interface-design/system.md` from Dammyjay93/interface-design
(MIT, `plugin/templates/interface-design-LICENSE`).
