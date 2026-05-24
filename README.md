# codex-maxxing 🎯

> Drop-in **AGENTS.md** (for Codex) and **CLAUDE.md** (for Claude Code) + three companion skills, distilled from Jason Liu's [《Codex-maxxing》](https://jxnl.co/writing/2026/05/10/codex-maxxing/) (2026-05-10).
>
> **Executable rules, not a reprint.** Original prose, original example prompts. The links and credits go to Jason; everything else is rewritten from scratch into agent-actionable form.

## One-line framework

> _"Ambition without verification is just a wish."_ — Goals primitive (single short quotation under fair-use threshold)

## 60-second install

```bash
# For Codex
cp AGENTS.md ~/.codex/AGENTS.md

# For Claude Code
cp CLAUDE.md ~/.claude/CLAUDE.md

# Optional: 3 companion skills (verified-goal / chief-of-staff-heartbeat / memory-as-files)
cp -r skills/* ~/.claude/skills/
```

🚧 **WIP** — initial scaffold pushed; content lands in subsequent commits.

## What this distills

Jason's nine primitives (durable threads / voice input / steering / memory-as-files / computer-browser-use / remote-control / heartbeats / goals-with-verification / side-panel) → rewritten as **executable rules** an agent can follow:

| # | Primitive | Rewritten as |
|---|---|---|
| 1 | Durable threads | Working-loop rule: pin long threads, periodic compaction |
| 2 | Voice input | Working-loop rule: accept raw/voice input, don't gate on phrasing |
| 3 | Steering | Working-loop rule: queue next intents while long task runs |
| 4 | Memory as files | **skill: `memory-as-files`** (file vault, git diff = memory review) |
| 5 | Computer/browser use | Tooling rule: tier between local-web / logged-in browser / pure-GUI |
| 6 | Remote control | Working-loop rule: design long tasks to be pausable/resumable |
| 7 | Heartbeats | **skill: `chief-of-staff-heartbeat`** (cadence + monitor + draft-only) |
| 8 | Goals (with verification) | **skill: `verified-goal`** (goal card + oracle test + run-to-verify) |
| 9 | Side panel | Output rule: prefer interactive `index.html` artifacts over plain Markdown |

## Codex vs Claude differences

When the two tools genuinely differ, this repo gives each their best fit instead of a watered-down common denominator:

| Concept | Codex | Claude Code |
|---|---|---|
| Persistent memory primitive | `memories.md` + AGENTS.md | `CLAUDE.md` + memory files |
| Browser/web access | `$browser` / `@chrome` syntax | Browser tools / MCP |
| Pure GUI control | `@computer` | Computer use |
| Long-task scheduling | Heartbeats (cron-like) | Scheduled tasks / hooks |

Differences without equivalents (e.g., Codex pets) are omitted, not hard-translated.

## Why a separate repo

This started as part of [Edward4226/skillcli](https://github.com/Edward4226/skillcli)'s "Phase 5 ticket". Spinning it out lets it be installed without taking the whole control plane—and lets the control plane's quality gate verify it as a third-party drop-in.

## License

MIT. Original work is © Jason Liu (linked above); this rewrite is © the contributors of this repo and licensed permissively for any use.
