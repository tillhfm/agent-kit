---
name: retro
description: Conduct a data-driven multi-session retrospective over agent logs, git history, tracker state, and steering files to improve the agentic environment and produce a comparable baseline snapshot. Use when reviewing recent agent performance or planning workflow and tooling improvements.
---

# Retro

Improve the agentic environment (checks, tooling, tracker, orchestration, steering files) instead
of patching individual code bugs. Order fixes by leverage: automated checks before navigation
pointers before written rules, and prune no-ops.

## Phase 1: Frame

Confirm scope with the owner in one short question round when not already stated:

- Time window (default: 14 days, or since the last `baseline-*.json`).
- Target repositories, hosts and agent harnesses to include.
- Whether the session stops at the report and plan or also applies immediate quick wins.

## Phase 2: Two-stage data collection

Never dump raw logs into an LLM context.

1. **Deterministic extractor (main session only):** Write and run one read-only extractor script
   inside a dedicated scratch folder to collect all raw summaries:
   - Local and remote session transcripts: separate pure human prompts from automated briefs,
     exclude 0-turn stubs, classify true `rate_limit`, `billing_error` and `api_error` separately
     from `compact_boundary`, and count `root_turn` or `countsForRun: true` failures separately
     from non-fatal shell exit codes.
   - Git history on `origin/main` (commits by type, releases, reverts) separately from local
     branches, worktrees and scratch leftovers.
   - Tracker metrics: CLI latency, payload sizes, open or stalled items, and direct owner
     participation versus agent transcriptions.
   - Current steering-file byte load and provider compaction settings across all active harnesses.
2. **Parallel thematic analysis (optional above 200 MB of logs):** Spawn read-only subagents that
   read only the extracted scratch files (never live MCP calls, remote SSH or paths outside the
   scratch folder that can block on permissions). Give each subagent its own scratch subfolder and
   one axis:
   - Prompts, recurring reminders and steering no-ops.
   - Limits, compactions, aborts, orchestration and filesystem hygiene.
   - Tracker workflow, review flow and state deadlocks.
   - Automated checks, tool economy and review-round churn.

## Phase 3: Insights (interactive)

Present a concise retro board in chat (with a comparison chart when trends or prior baselines
exist):

- **Glad**: measurable wins to keep unchanged.
- **Mad / Sad**: top 5 to 6 systemic clusters ordered by leverage, backed by exact counts and
  concrete timelines.
- **Prior baseline delta**: compare every key metric against the previous `baseline-*.json`.
- Include bold structural options (including replacing tools or workflows) alongside incremental
  fixes.

## Phase 4: Decide and stage

Turn accepted insights into a prioritized, staged action plan ordered by leverage:

1. Deterministic checks, CLI fixes, leases and hooks.
2. Navigation pointers and deletion of bloated or no-op rules.
3. Written standards (genuine judgment calls only).
4. Hardware, hosting or multi-provider routing updates.

## Phase 5: Close and meta-retro

1. Save `retro-report.md` and `baseline-YYYY-MM-DD.json` (with target metrics for the next retro)
   in a durable, non-committed folder (or tracker page, without quoting the owner).
2. Run a short **Meta-retro** on the retro itself (extraction blind spots, false positives, session
   length) and update this skill when a systemic flaw appeared.
3. Hand off implementation blocks to fresh sessions with a 5 to 8 line pointer-only brief
   referencing `retro-report.md`.
