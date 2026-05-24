---
name: chief-of-staff-heartbeat
description: Use this skill when the user wants periodic, lightweight monitoring of a source (an inbox, dashboard, repository, or feed) and conditional action when a defined trigger fires. It produces a heartbeat task configuration with explicit cadence, source, trigger, and action, and defaults the action to draft-only so the human confirms before anything externally observable happens.
---

# chief-of-staff-heartbeat

For monitoring-style work — *"watch X, tell me when Y happens, then draft Z"* — this skill produces a heartbeat configuration the host can schedule. Default behavior is **draft-only**: the user confirms before any external send/post/submit.

## When to use this skill

Use it when the user says any of:
- "Keep an eye on X"
- "Let me know when Y happens"
- "Every <interval> check Z"
- "I want to react quickly to changes in W"

Do **not** use it for one-off checks ("what's the latest in X?"). A plain tool call is fine for those.

## What it produces: the heartbeat card

```yaml
heartbeat:
  name: <short id>
  cadence: <cron or "every Nm" / "every Nh" / "daily HH:MM TZ">
  source:
    type: <email | slack | dashboard | repo | rss | api>
    location: <URL / path / channel / inbox label>
  trigger:
    when: <plain-language condition the heartbeat checks>
    confidence_floor: <0..1, optional — only fire if heuristic >= this>
  action:
    mode: draft       # draft | notify | send (default = draft)
    target: <where the draft goes — usually a file or DM to the user>
    template: |
      <draft template referencing the trigger details>
  guardrails:
    rate_limit: <max fires per day or hour>
    cooldown: <minimum gap between fires>
```

## Procedure

1. Clarify the four required fields: **cadence, source, trigger, action.**
2. **Negotiate the action mode.** Default `draft`. Only escalate to `notify`
   if the user explicitly wants the host to ping them. Only escalate to `send`
   if the action is low-stakes AND idempotent AND the user explicitly opts in.
3. Add sensible guardrails (rate limit + cooldown) so a misfiring trigger
   doesn't flood the user.
4. Register the heartbeat with the host's scheduler:
   - **Claude Code**: `CronCreate` (or the `schedule` skill).
   - **Codex**: native heartbeat mechanism.
5. Tell the user how to disable it (`CronDelete <name>` or equivalent).

## Anti-patterns this skill blocks

- ❌ "Send me a summary every hour" with `mode: send` and no rate limit —
  one misfire becomes spam.
- ❌ "Auto-reply to anything matching X" — auto-send to humans without a
  draft step; bypass.
- ❌ Heartbeats that fire on every cadence regardless of trigger — that's
  just a cron job, not a heartbeat.
- ❌ A trigger condition that's a fuzzy judgment ("if it looks important")
  with no measurable definition.

## Worked example (original — not lifted from any source)

User: "Watch the blog for new comments that ask actual questions, and draft replies."

```yaml
heartbeat:
  name: blog-comment-questions
  cadence: every 30m
  source:
    type: api
    location: https://example.com/api/comments?since=cursor
  trigger:
    when: a new comment contains "?" and is >20 chars and not from a known spammer
  action:
    mode: draft
    target: notes/comment-queue.md
    template: |
      ### {{ comment.author }} on "{{ comment.post }}"
      > {{ comment.text }}
      Suggested reply: {{ generated_reply }}
  guardrails:
    rate_limit: 10/day
    cooldown: 15m
```

The heartbeat drops drafts into a single file; the human reviews and posts when convenient. No comments get auto-published.
