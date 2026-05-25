# AGENTS.md — Codex-maxxing operating defaults

<!--
Inspired by: Jason Liu, "Codex-maxxing" (2026-05-10)
              https://jxnl.co/writing/2026/05/10/codex-maxxing/

This file is an *executable distillation* of the methodology — not a reprint.
All prose and worked examples below are original. One short attributed
quotation appears under "Verified goals" (7 words, well under the
fair-use threshold and the only literal sentence retained from the source).

Jason's primitive names ("durable threads", "compaction", "heartbeats",
"shared memory", "side panel", etc.) are concept labels and are used as
such; the rule structure, phrasing, and worked examples are this file's
contribution.
-->

## Operating loop defaults

- **Compaction first.** Long threads only stay workable if you keep compressing stale turns — boil down old exchanges into shorter summaries so the conversation continues without re-paying for every prior message. Treat it as routine, not last-resort cleanup; without it, durable threads collapse under their own weight.
- **Pin threads to important workstreams.** Weekly review, an active project, a recurring debugging surface — these get their own long-lived thread you return to. Don't open a fresh session for work you'll touch again.
- **Accept raw input.** Voice transcripts, fragmented thoughts, half-typed notes — work with whatever the user drops in. Don't gate on phrasing quality; restate what you understood, then proceed.
- **Steer mid-run.** When the user adds new intent while a long task is executing, append it to a working queue and address it after the current step lands. Pause the running task only if the new intent overrides it.

## Memory as files (a.k.a. shared memory)

Persist what you learn into a **versioned file vault**, not into chat history alone:

- `TODO.md` — open loops; one line per item with status
- `people/<name>.md` — what you know about each person
- `projects/<name>.md` — context for each project (goal, status, blockers)
- `notes/<topic>.md` — domain knowledge worth keeping
- `agent/` — instructions you want every future thread on this vault to pick up

Update at natural beats: a milestone, a role change, an open loop closing. Commit the vault to git; read the weekly diff to audit *what changed in your memory*. The vault is portable across hosts (Codex / Claude Code / a human teammate); chat history is not.

## Tool tiering

Match the tool to the level of access required:

- `$browser` — quick local-web inspection, no login state.
- `@chrome` — logged-in browsing, multi-tab work, real session state.
- `@computer` — pure-GUI applications with no programmatic alternative.

These three are plugins from the `openai-bundled` marketplace (verified on Codex CLI 0.130.0); manage with `codex plugin marketplace`.

## Connectors (extend reach to where work happens)

Connectors plug the agent into systems where work actually shows up *before* it becomes code: chat, mail, calendar, ticket trackers, docs. They're API-backed (faster, more reliable, survive UI redesigns) and they don't require taking over your screen the way `@computer` does. Prefer a connector whenever one exists for the system you need to touch — `$gmail`, `$github`, `$notion`, `$figma` ship as curated OpenAI plugins; for `$slack`, `$calendar`, and others, check `codex plugin marketplace` for available sources.

## Reusable workflows (Skills)

When you find yourself re-explaining the same workflow on each new thread, package it as a Skill so future threads can load it on their own. A Skill is a small file with three required parts:

- **Trigger** — phrased as *"use this when the user wants to X"*, not a feature list. If the trigger isn't an *if*-clause the host won't auto-load the skill at the right moment.
- **Procedure** — the steps a fresh session needs to follow.
- **Outputs** — what artifacts the skill produces.

Three working skills ship with this repo (`verified-goal`, `chief-of-staff-heartbeat`, `memory-as-files`); install them under `~/.codex/skills/` to see the pattern concretely.

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

## Remote control (intervene from another device)

Long tasks should let you drop attention and pick it back up from anywhere — desk, laptop, phone. Design for that:

- persist state to a file at each non-trivial step so any session can resume the run
- surface decision points as explicit prompts, never hidden behind a default
- keep the next-action queue short and visible so anyone with thread access (you on a different device, a teammate, a future session) can read it and act

Pausability is the means; the point is that the work survives your changing physical context, not just a session timeout.

## Inspectable surfaces (side panel)

Produce work in surfaces that can be read, annotated, and operated without leaving the loop — not static documents you scroll past once:

- a single-file `index.html` is the lightest default (no server, no build chain)
- heavier choices when the workload calls for it: Storybook for UI components, Remotion Studio for animation, Slidev for slides, Streamlit for data apps
- prefer the interactive form whenever a reviewer will want to point at a thing and say "change this"

Markdown is fine for pure narrative. The principle: keep the artifact alive in a surface where review and action sit together.

---

## Anti-patterns (don't do these)

- ❌ **Long-task pause** that loses state on restart — always checkpoint to disk.
- ❌ **Implicit goal** ("make this nicer") — convert to an oracle first.
- ❌ **Auto-send** anything to humans without a draft step.
- ❌ **One big SKILL.md** spanning many unrelated topics — split per concern.
- ❌ **Memory in chat** that doesn't get persisted to a file before session ends.
- ❌ **Skipping compaction** on long threads — they degrade faster than the cost it would have saved.
