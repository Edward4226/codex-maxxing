---
name: verified-goal
description: Use this skill when the user gives a long, multi-step, or open-ended task without specifying how completion will be verified. It produces a goal card with an explicit oracle (test command, measurable criterion, or diff against baseline) and runs the oracle at the end to decide "done" objectively.
---

# verified-goal

Most long tasks fail not because they're hard but because "done" was never defined. This skill captures the goal as a small structured doc, locks in the **verification** up front, and runs it at the end.

## When to use this skill

Use it when:
- The user describes a task that will take >5 minutes
- The success criterion is implicit or vague ("make it better")
- Multiple plausible interpretations of "done" exist

Do **not** use it for trivial work (one-liners, single-file edits).

## What it produces: the goal card

A small `goal.md` (or section appended to an existing one):

```
## Goal: <one-line statement>
## Why it matters: <one line — drives prioritization>
## Oracle (how we'll know it's done):
  - <test command that returns 0 on success>          OR
  - <measurable criterion: "p95 latency < 200 ms">    OR
  - <diff target: "matches snapshot baseline 2026-05">
## Out of scope:
  - <things the user might assume but shouldn't be done here>
## Risks / unknowns:
  - <things that might force re-scoping>
```

## Procedure

1. Reflect the user's stated goal back in one sentence. Confirm.
2. Ask: **"What command or measurement will tell us this worked?"**
   If the user can't answer, propose 2–3 options based on the work shape
   (test command, baseline diff, manual checklist).
3. Write the goal card to the project root or `notes/goals/`.
4. Execute the task as usual.
5. **At the end**: run the oracle. If it fails, the task is **not done**.
   Report what failed and propose next steps.

## Anti-patterns this skill blocks

- ❌ "Just implement this plan.md" — vague goal, no oracle. Ask for an oracle line first.
- ❌ "Make this prettier / cleaner / better" — subjective. Convert to specific
  (linting warnings clear, visual diff against attached screenshots, etc).
- ❌ Skipping the oracle run at the end because "the work looks done."
  The oracle exists precisely because looks-done lies.

## Worked example (original — not lifted from any source)

User: "Rebuild the search backend to be faster."

After this skill:

```
## Goal: Rebuild search backend so the median query is faster
## Why it matters: Users abandon search after 1s; we're at 1.3s today
## Oracle:
  - p50 query latency < 600 ms on the production replay set
    (cmd: `make bench-search-p50` → must print "OK")
## Out of scope:
  - UI changes; ranking changes; multi-language tokenization
## Risks:
  - The replay set may not represent worst-case multi-tenant load
```

Then build. Then `make bench-search-p50`. Then declare done — or not.

## Why this matters

The framework principle: ambition without verification is just a wish.
Define how you'll measure success **before** you start.
