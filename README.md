# codex-maxxing 🎯

[![originality](https://github.com/Edward4226/codex-maxxing/actions/workflows/originality.yml/badge.svg)](https://github.com/Edward4226/codex-maxxing/actions/workflows/originality.yml)

> Two `cp` commands and your Codex or Claude Code session inherits Jason Liu's [《Codex-maxxing》](https://jxnl.co/writing/2026/05/10/codex-maxxing/) operating loop — compaction, durable threads, file-vault memory, heartbeats, verified goals, inspectable artifacts — as defaults the agent actually follows.

**Executable rules, not a reprint.** Every sentence in this repo is original; the originality CI rejects any 15-token overlap with the source article on every push.

## 60-second install

```bash
# Drop into a project (Codex / Claude Code pick these up automatically):
cp AGENTS.md  /path/to/project/AGENTS.md
cp CLAUDE.md  /path/to/project/CLAUDE.md

# Or install globally so every session inherits the defaults:
cp AGENTS.md  ~/.codex/AGENTS.md
cp CLAUDE.md  ~/.claude/CLAUDE.md

# Optional: three companion skills covering the heaviest primitives
cp -r skills/* ~/.codex/skills/    # for Codex
cp -r skills/* ~/.claude/skills/   # for Claude Code
```

Open a fresh session in that project and the rules are in effect.

## What changes (before / after)

| Scenario | Without these drop-ins | With them |
|---|---|---|
| *"Rebuild the search backend to be faster."* | Agent starts coding; declares done when the work *looks* done | Agent first writes a goal card with an oracle (e.g. `make bench-search-p50`); runs the oracle at the end to decide *done* |
| *"Make this nicer."* | Agent iterates on cosmetics immediately | Agent pushes back — *"What command will tell us this worked?"* — before any edit |
| Long thread getting expensive | History keeps growing; cost climbs unchecked | Compaction is a first-class routine, not a last-resort cleanup |
| User mentions a new person mid-conversation | Stored in volatile chat context; lost next session | Persisted to `people/<name>.md` in the file vault, committed to git |
| *"Watch X and ping me when Y happens."* | Agent writes a one-shot script | Heartbeat skill produces cadence + source + trigger + **draft-only** action, scheduled by the host |
| Output that benefits from interaction | Plain-Markdown blob | Single-file `index.html` (or Storybook / Slidev / Streamlit when heavier) — reviewable in place |

These are reproducible: open a session in a project with `AGENTS.md` (or `CLAUDE.md`) installed, ask the agent any prompt on the left, and observe the behavior on the right.

## Primitive map

Jason names twelve primitives across nine sections. Each becomes an executable rule (and, for the three heaviest, a full Skill):

| # | Source primitive | Our rule | Companion skill |
|---|---|---|---|
| 1 | Compaction | Operating loop — *Compaction first* | |
| 2 | Durable threads | Operating loop — *Pin threads to important workstreams* | |
| 3 | Voice input | Operating loop — *Accept raw input* | |
| 4 | Steering | Operating loop — *Steer mid-run* | |
| 5 | Shared memory | Memory as files | `memory-as-files` |
| 6 | Computer / Browser use | Tool tiering | |
| 7 | Connectors | Connectors *(new section)* | |
| 8 | Skills | Reusable workflows | |
| 9 | Remote control | Remote control | |
| 10 | Heartbeats | Heartbeats | `chief-of-staff-heartbeat` |
| 11 | Goals | Verified goals | `verified-goal` |
| 12 | Side panel | Inspectable surfaces | |

Full rules in [`AGENTS.md`](./AGENTS.md) (Codex) and [`CLAUDE.md`](./CLAUDE.md) (Claude Code). Every editorial call — what we kept, what we re-framed, what we deliberately left out — is recorded in [`DECISIONS.md`](./DECISIONS.md).

## Codex vs Claude Code

Where the two tools genuinely differ, each gets its own best fit rather than a watered-down common denominator:

| Capability | Codex | Claude Code |
|---|---|---|
| Local-web inspection | `$browser` plugin | Bundled browser / fetch tools |
| Logged-in browser control | `@chrome` plugin | Chrome MCP server |
| Native-GUI control | `@computer` plugin | `computer-use` MCP |
| External-service connectors | `$gmail` / `$github` / `$notion` / `$figma` (curated); more via `codex plugin marketplace` | MCP servers (Slack / GitHub / Notion / Linear / Gmail / …) |
| Scheduled work | Heartbeats | `CronCreate` or the `schedule` skill |
| Agent-rule file location | `~/.codex/AGENTS.md` or `<project>/AGENTS.md` | `~/.claude/CLAUDE.md` or `<project>/CLAUDE.md` |
| Thread compaction | Automatic at token threshold | `/compact` slash command |

Capabilities without an equivalent (e.g. Codex's `Appshots` macOS Command-Command screenshot affordance) are omitted from the rules rather than hard-translated.

## Companion skills

Three skills covering the primitives that pay off most when packaged as a contract rather than a paragraph of prose:

- **`verified-goal`** — interview-style goal capture; produces a goal card with an oracle (test command / measurable target / diff baseline) and runs it at the end to decide *done*.
- **`chief-of-staff-heartbeat`** — cadence-based monitor scaffold (cadence + source + trigger + **draft-only** action). The human always confirms before anything externally observable happens.
- **`memory-as-files`** — initializes a versioned file vault (`TODO.md` + `people/` + `projects/` + `notes/`), with maintenance rules so memory updates at natural beats and the git diff becomes the periodic memory review surface.

All three pass the [`skillcli`](https://github.com/Edward4226/skillcli) control plane's quality gate (`skillcli verify`) at 100/100, including its safety scan — they're the dogfood proving the gate works on third-party skills.

## Why a separate repo

This started inside [`Edward4226/skillcli`](https://github.com/Edward4226/skillcli) as its Phase 5 "distillation ticket". Spinning it out:

- lets you install just the rules + skills without taking the whole control plane,
- lets `skillcli verify` audit this repo as an independent third-party drop-in,
- gives the distillation room to grow on its own cadence (more primitives, translations, additional hosts).

## Originality CI

`scripts/check_originality.py` (standard-library Python, no dependencies) tokenises the source article and rejects any 15-token overlap against `AGENTS.md`, `CLAUDE.md`, `README.md`, and every `skills/**/*.md` file. Concept names (`durable threads`, `heartbeats`, `compaction`, `side panel`) are short enough that they never trigger; the single whitelisted seven-word quotation under *Verified goals* clears it too.

The check runs on every push and pull request via GitHub Actions — see the badge at the top.

## License & attribution

MIT. The methodology and observations distilled here are Jason Liu's, linked at the top; this repo is an *executable distillation* (re-expression as rules + skills), not a reprint, and is unaffiliated with the author or OpenAI. The rule structure, phrasing, worked examples, and skill contracts in this repo are MIT-licensed for any use, including commercial.
