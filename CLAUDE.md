# CLAUDE.md — Codex-maxxing operating defaults (Claude Code edition)

<!--
Inspired by: Jason Liu, "Codex-maxxing" (2026-05-10)
              https://jxnl.co/writing/2026/05/10/codex-maxxing/

Executable distillation of the methodology — not a reprint. All prose
and examples below are original. One short attributed quotation appears
under "Verified goals".

Semantically equivalent to AGENTS.md in this repo; adapted for Claude
Code idioms (slash-commands, MCP connectors, skills, hooks). Where Codex
and Claude Code differ meaningfully, this file picks Claude Code's best
fit rather than the lowest common denominator.
-->

## Operating loop defaults

- **Pin long-lived sessions** for any workflow you'll return to. Use `/compact` on stale turns rather than spinning up a fresh session each time.
- **Accept raw input.** Voice transcripts, fragmented thoughts, copy-pasted notes — work with whatever the user drops in. Restate what you understood, then proceed.
- **Queue follow-ups while a long task runs.** When the user adds intent mid-execution, append to TaskList and address after the current step lands. Don't pause unless the new intent overrides.

## Memory as files

Persist what you learn into a **versioned file vault**, not just into the conversation:

- `TODO.md` — open loops; one line per item with status
- `people/<name>.md` — what you know about each person
- `projects/<name>.md` — per-project context (goal, status, blockers)
- `notes/<topic>.md` — domain knowledge worth keeping

Update at natural beats. Commit the vault to git; read the weekly diff to audit memory.

> Claude Code's built-in memory mechanism complements this — use it for *session-bound* hints and the file vault for *cross-session, cross-tool* knowledge. The vault is more portable.

## Tool tiering

For external reach, match the tool to the access level:

- **Read-only web** — use Claude Code's bundled browser/fetch for quick inspection.
- **Logged-in multi-tab work** — use the Chrome MCP server (if connected).
- **Pure-GUI native apps** — use `computer-use` as a last resort; prefer MCP alternatives where they exist.

Prefer purpose-built MCP connectors (Slack / GitHub / Notion / Linear / Gmail / Calendar) over computer-use — they're faster, more reliable, and the user authorizes them once.

## Scheduled work (Claude Code's heartbeat equivalent)

For monitoring-style tasks — "watch X and act when Y happens" — use `CronCreate` (or the schedule skill) with explicit:

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

## Long tasks: pausable & resumable

Design tasks expected to run >5 minutes to survive interrupts:

- persist progress to a file every step or two
- on resume, re-read the checkpoint and continue
- make decision points explicit so the user can intervene mid-run

This lets a task ride out a session timeout, an interrupt, or a switch between Claude Code CLI / Desktop / Web.

## Output: prefer interactive artifacts

Prefer **single-file interactive `index.html` artifacts** over plain Markdown when the output benefits from inspection or controls — charts, filters, drill-down, forms. Use inline CSS + vanilla JS + a CDN lib if needed. Avoid build chains.

For pure narrative, Markdown is fine.

---

## Anti-patterns (don't do these)

- ❌ **Long-task pause** that loses state on restart — always checkpoint.
- ❌ **Implicit goal** ("make this nicer") — convert to an oracle first.
- ❌ **Auto-send** anything to humans without a draft step.
- ❌ **One big SKILL.md** spanning many unrelated topics — split per concern.
- ❌ **Memory in chat** that doesn't get persisted to a file before session ends.

## Companion skills

This repo also ships three opt-in skills that turn three of the heaviest primitives into reusable behaviors:

- `verified-goal` — interview-style goal capture + oracle definition
- `chief-of-staff-heartbeat` — cadence-based monitor scaffold (draft-only by default)
- `memory-as-files` — file-vault initializer + maintenance rules

Install with:

```bash
cp -r skills/* ~/.claude/skills/
```
