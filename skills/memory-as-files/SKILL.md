---
name: memory-as-files
description: Use this skill when the user wants persistent, cross-session, reviewable memory for an ongoing project, set of people, or domain knowledge. It initializes a versioned file vault (TODO.md + people/ + projects/ + notes/), defines maintenance rules so memory stays current at natural beats, and treats the vault's git diff as the periodic memory-review surface.
---

# memory-as-files

Chat history is volatile, lossy, and hidden. **A file vault is permanent, searchable, and diffable.** This skill turns "things you should remember about my work" into a small, structured, git-tracked folder.

## When to use this skill

Use it when:
- The user works across many sessions on the same project or people
- "Remember that..." / "Don't forget..." comes up repeatedly
- The user wants the host to onboard a future session with the same context
- A handoff to a teammate or another agent is anticipated

Do **not** use it for ephemeral session state — use TaskList for that.

## What it produces: the vault scaffold

```
memory/
├── TODO.md                      # open loops; one line per item with status
├── people/
│   └── <name>.md                # what I know about each person
├── projects/
│   └── <name>.md                # context per project (goal, status, blockers)
└── notes/
    └── <topic>.md               # domain knowledge worth keeping
```

The vault lives at the project root (default) or `~/memory/` (cross-project). It gets committed to git so changes are reviewable.

## Maintenance rules — the actual "skill"

The vault is only useful if it stays current. Update at these natural beats:

| Trigger | Update |
|---|---|
| User mentions a new person (role, ownership, contact) | `people/<name>.md` |
| Project status changes (milestone, blocker, decision) | `projects/<name>.md` |
| User closes an open loop | strike or move the line in `TODO.md` |
| User shares non-trivial domain knowledge | append to `notes/<topic>.md` |
| Session end / weekly review | commit; review the diff |

Updates are **append-mostly**: don't overwrite history without recording it. Past wrongness is sometimes useful context.

## Procedure

1. If `memory/` doesn't exist, run the scaffold (create directories + empty
   stub files with one-line headers).
2. On every meaningful learning, find the right file and update it in one place.
3. At session end, commit with a descriptive message:
   `memory: <what changed and why>`.
4. Suggest a weekly diff review:
   `git log --since="1 week ago" memory/` then `git diff HEAD~5 memory/`.

## Anti-patterns this skill blocks

- ❌ Writing memory updates into the chat without persisting to the vault.
- ❌ One giant `memory.md` — you can't `grep` it usefully when it's 5000 lines.
- ❌ Storing secrets (API keys, passwords, tokens) in the vault — even private
  repos leak. Use a secret manager.
- ❌ Memory the user doesn't know about — always announce updates:
  "I added <X> to `projects/<Y>.md`."

## Why files (not a database, not chat history)

- **Portable** — works across hosts (Claude / Codex / Cursor / a human teammate).
- **Diffable** — git diff *is* the memory review surface.
- **Greppable** — `rg "person-name" memory/` finds everything in one shot.
- **Boring** — no service to set up, no schema to migrate, no SaaS to outlast.

## Worked example (original — not lifted from any source)

Mid-session, the user says: "By the way, Sara is taking over the data pipeline from Marcus next week."

This skill triggers:

1. Update `people/sara.md`: append "owns data pipeline (from 2026-06-01, succeeding Marcus)."
2. Update `people/marcus.md`: append "handed data pipeline to Sara on 2026-06-01."
3. Update `projects/data-pipeline.md`: change owner line.
4. Announce in chat: "Updated `people/{sara,marcus}.md` and `projects/data-pipeline.md` with the handover."
