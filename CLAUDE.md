# CLAUDE.md — Codex-maxxing operating defaults (Claude Code edition)

<!--
Inspired by: Jason Liu, "Codex-maxxing" (2026-05-10)
              https://jxnl.co/writing/2026/05/10/codex-maxxing/

Executable distillation of the methodology — not a reprint. All prose and
worked examples below are original. One short attributed quotation appears
under "Verified goals" (7 words, the only literal sentence retained from
the source).

Semantically equivalent to AGENTS.md in this repo; adapted for Claude Code
idioms — slash commands, MCP servers, skills, hooks, scheduled tasks.
Where Codex and Claude Code differ meaningfully (the Codex `$browser` /
`@chrome` / `@computer` syntax has no exact equivalent here), this file
picks Claude Code's best fit rather than the lowest common denominator.
-->

## Operating loop defaults

- **Compaction first.** Long-running sessions only stay workable if you compact stale turns — use `/compact` so the conversation continues without re-paying for every prior message. Make it routine, not last-resort cleanup; without it, durable sessions collapse under their own weight.
- **Pin sessions to important workstreams.** Weekly review, an active project, a recurring debugging surface — each gets its own session you return to instead of starting fresh every time.
- **Accept raw input.** Voice transcripts, fragmented thoughts, copy-pasted notes — work with whatever the user drops in. Restate what you understood, then proceed.
- **Steer mid-run.** When the user adds intent during a long task, append it to TaskList and address it after the current step lands. Don't pause unless the new intent overrides the running one.

## Memory as files (a.k.a. shared memory)

Persist what you learn into a **versioned file vault**, not just into the conversation:

- `TODO.md` — open loops; one line per item with status
- `people/<name>.md` — what you know about each person
- `projects/<name>.md` — per-project context (goal, status, blockers)
- `notes/<topic>.md` — domain knowledge worth keeping
- `agent/` — instructions every future session on this vault should pick up

Update at natural beats. Commit the vault to git; read the weekly diff to audit memory. The vault is portable across hosts (Claude Code / Codex / a human teammate); chat history is not.

> Claude Code's built-in `~/.claude/memory/` directory complements this — use it for *session-bound* hints; use the file vault for *cross-session, cross-tool* knowledge that should outlive any single host.

## Tool tiering

For external reach, match the tool to the access level:

- **Read-only web** — Claude Code's bundled browser / fetch for quick inspection.
- **Logged-in multi-tab work** — Chrome MCP server (if connected).
- **Pure-GUI native apps** — `computer-use` as a last resort; prefer an MCP alternative whenever one exists.

## Connectors (extend reach to where work happens)

Plug into the systems where work shows up *before* it becomes code: chat, mail, calendar, ticket trackers, docs. MCP connectors (Slack / GitHub / Notion / Linear / Gmail / Calendar / Drive) are API-backed, faster than driving a GUI, and they survive app redesigns. Prefer a connector whenever one exists for the system you need to touch — the user authorises them once and they keep working.

## Reusable workflows (Skills)

When the same workflow recurs across sessions — same intent, same shape, different inputs — package it as a Skill instead of re-explaining. A Skill is a small file with three required parts:

- **Trigger** — phrased as *"use this when the user wants to X"*, not a feature list. If the trigger isn't an *if*-clause Claude Code won't auto-load the skill at the right moment.
- **Procedure** — the steps a fresh session needs to follow.
- **Outputs** — what artifacts the skill produces.

Three working skills ship with this repo (`verified-goal`, `chief-of-staff-heartbeat`, `memory-as-files`); install them under `~/.claude/skills/` for concrete patterns.

## Scheduled work (Claude Code's heartbeat equivalent)

For monitoring-style tasks — "watch X and act when Y happens" — use `CronCreate` (or the `schedule` skill) with explicit:

- **cadence**
- **source** (which inbox / dashboard / repo)
- **trigger condition**
- **action**

Default the action to **draft only — do not send / post / submit**. The user confirms before anything externally observable happens. Reserve full automation for low-stakes, idempotent operations.

## Verified goals

Before any long task, define the **oracle** that decides "done":

- a test command that returns 0
- a measurable target (file size, latency, row match)
- a diff against a known-good baseline

Run the oracle at the end. If it fails, the task isn't done — even if the work *looks* done.

> "Ambition without verification is just a wish." — _the source, see header_

Refuse vague goals like "implement this plan.md" unless the plan already includes the oracle. Push back: **"What command will tell us this worked?"**

## Remote control (intervene from another device)

Long tasks should let you drop attention and pick it back up from anywhere — Claude Code CLI / Desktop / Web. Design for that:

- persist progress to a file at each non-trivial step so any session can resume
- surface decision points as explicit prompts, never hidden behind a default
- keep the next-action queue short and visible so anyone with thread access can read it and act

Pausability is the means; the point is that the work survives your changing physical context, not just a session timeout.

## Inspectable surfaces (side panel)

Produce work in surfaces that can be read, annotated, and operated without leaving the loop — not static documents:

- a single-file `index.html` is the lightest default (no server, no build chain)
- heavier choices when the workload calls for it: Storybook for UI components, Remotion Studio for animation, Slidev for slides, Streamlit for data apps
- prefer the interactive form whenever the reviewer will want to point at a thing and say "change this"

Markdown is fine for pure narrative. The principle: keep the artifact alive in a surface where review and action sit together.

---

## Anti-patterns (don't do these)

- ❌ **Long-task pause** that loses state on restart — always checkpoint.
- ❌ **Implicit goal** ("make this nicer") — convert to an oracle first.
- ❌ **Auto-send** anything to humans without a draft step.
- ❌ **One big SKILL.md** spanning many unrelated topics — split per concern.
- ❌ **Memory in chat** that doesn't get persisted before session ends.
- ❌ **Skipping compaction** on long sessions — they degrade faster than the cost it would have saved.
