---
name: setup
description: Set a project up for the agent-kit, or bring it level with the kit's current templates - oxfmt and oxlint configuration, the format hook's .agent-kit.json, the commit-msg hook, the plugin in .claude/settings.json, and DESIGN.md with its design-tokens test for a Tailwind interface. Use when a project starts using the kit, or when asked to compare a project with the kit.
---

# Setup

The kit's templates are in `${CLAUDE_PLUGIN_ROOT}/templates`. A project holds its own copies, and
nothing compares them automatically. This skill copies them the first time and compares them on
request.

## Files

| Template | Project file | Fill in |
| --- | --- | --- |
| `oxfmtrc.json` | `.oxfmtrc.json` | `ignorePatterns` and the `$schema` path for the project's layout |
| `oxlintrc.json` | `.oxlintrc.json` | the plugins the stack uses, `env`, overrides |
| `agent-kit.json` | `.agent-kit.json` | `tracker` (`local`, or `plane` for a project tracked in Plane), the commands as the project runs them, `path` for a private Node |
| `commit-msg` | `.githooks/commit-msg` | `tracker=` with the pattern of the project's tracker IDs. A pull request check runs it on the title, and with `--names-only` on the body |
| `DESIGN.md` | `DESIGN.md` | everything in angle brackets. Spacing and Surfaces are the kit's: a project fills in the token names and adds its own lines at the end of each |
| `design-tokens.test.ts` | a folder the project's test runner reads, such as `tests/` | `SOURCE` relative to that folder, `THEME` and `EXEMPT`: the lines above the kit's part |

A project without TypeScript takes no oxc files. Only a project with a Tailwind interface takes the
design files. Its build runs `design-tokens.test.ts` with its other tests. A project without Java drops the `*.java`
entry. A Java entry needs `palantir-java-format` in `gradle/libs.versions.toml`.

`.agent-kit.json` maps file patterns to a `format` and a `lint` command. The hook runs the first
entry whose pattern matches the edited file, from the folder of `.agent-kit.json`, with `{file}` as
the file's absolute path and `{kit}` as the plugin's folder. A pattern without `/` matches the file
name, one with `/` the path below that folder. `path` lists folders, globs allowed, that come first on
`PATH`. Both commands must work on a single file in under a few seconds.

## A new project

1. Copy each template that applies and fill in the project's values.
2. Run each `format` and `lint` command of `.agent-kit.json` on one file of its kind and show that it
   works.
3. Set `git config core.hooksPath .githooks` and show that a two-line commit message is refused.
   On GitHub, a squash merge takes the pull request title and an empty message
   (`gh api -X PATCH repos/<owner>/<repo> -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=BLANK`),
   or the squash commit gets a body that the hook refuses.
4. Add the marketplace and the plugin to `.claude/settings.json`. The desktop app starts every
   session with `DISABLE_AUTOUPDATER`, which turns plugin auto-update off unless
   `FORCE_AUTOUPDATE_PLUGINS` is set, so the project sets it:

   ```json
   {
     "env": { "FORCE_AUTOUPDATE_PLUGINS": "1" },
     "extraKnownMarketplaces": {
       "agent-kit": { "source": { "source": "github", "repo": "tillhfm/agent-kit" }, "autoUpdate": true }
     },
     "enabledPlugins": { "agent-kit@agent-kit": true }
   }
   ```

5. Write a `CLAUDE.md` that holds only what is true for this project. A line that is true in every
   project belongs in the kit's `rules.md`.

## Comparing with the kit

Show the diff between each template and its project file. Take every change of the kit into the
project, except a deviation that the project's `CONVENTIONS.md` lists with its reason. Ask in the
chat about a difference that is neither a kit change nor a listed deviation.
