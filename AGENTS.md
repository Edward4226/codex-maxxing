# AGENTS.md — Codex-maxxing operating defaults

<!--
Inspired by: Jason Liu, "Codex-maxxing" (2026-05-10)
              https://jxnl.co/writing/2026/05/10/codex-maxxing/

This file is an *executable distillation* of the methodology — not a reprint.
All prose and examples below are original. One short attributed quotation
appears under "Verified goals" (7 words, well under fair-use threshold).

The nine primitives below are concept names from the source; the phrasing,
worked examples, and rule structure are this file's contribution.
-->

## Operating loop defaults

- **Pin long-lived threads** for any workflow you'll return to (weekly review, ongoing project, recurring debugging). Compact stale turns rather than opening a fresh session each time.
- **Accept raw input.** Voice transcripts, fragmented thoughts, half-typed notes — work with whatever the user drops in. Don't gate on phrasing quality; restate back what you understood and proceed.
- **Queue follow-ups while a long task runs.** When the user adds new intent mid-execution, append it to a working list and address it after the current step lands. Don't pause the running task unless the new intent supersedes it.

## Memory as files

Persist what you learn into a **versioned file vault**, not into chat history alone:

- `TODO.md` — open loops; one line per item with status
- `people/<name>.md` — what you know about each person
- `projects/<name>.md` — context for each project (goal, status, blockers)
- `notes/<topic>.md` — domain knowledge worth keeping

Update at natural beats: a new project milestone, a person's role change, an open loop closing. Commit the vault to git; read the weekly diff to audit "what changed in my memory."

## Tool tiering

Match the tool to the level of access required:

- `$browser` — quick local-web inspection, no login state.
- `@chrome` — logged-in browsing, multi-tab work, real session state.
- `@computer` — pure-GUI applications with no programmatic alternative.

Prefer purpose-built connectors over `@computer` whenever possible — `$slack`, `$gmail`, `$calendar` are API-backed, faster, and survive UI redesigns.

## Heartbeats (periodic tasks)

For monitoring-style work — "watch X and act when Y happens" — set up a heartbeat task with explicit:

- **cadence** (every 10 min / hourly / daily)
- **source** (which inbox / dashboard / repo)
- **trigger** (the precise condition that matters)
- **action**

Default the action to **draft only — do not send / post / submit**. The human confirms before anything externally observable happens. Reserve full automation for low-stakes, idempotent operations.

## Verified goals

Before starting any long task, define the **oracle** that decides "done":

- a test command that returns 0 on success
- a measurable target (file size < X, latency < Y, all rows match)
- a diff against a known-good baseline

Run the oracle at the end. If it fails, the task isn't done — even if the work *looks* done.

> "Ambition without verification is just a wish." — _the source, see header_

Refuse vague goals like "implement this plan.md" unless the plan already includes the oracle. Push back: **"What command will tell us this worked?"**

## Long tasks: pausable, resumable, remote-friendly

Design any task expected to run >5 minutes to survive interrupts:

- persist progress to a file every step or two
- on resume, re-read the checkpoint and continue
- make decision points explicit so the user can intervene mid-run from anywhere

This lets the task ride out a session timeout, a network blip, or a hand-off to the mobile client.

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
