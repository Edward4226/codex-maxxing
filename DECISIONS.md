# DECISIONS — codex-maxxing optimization log

Substantive editorial calls made during P0 optimization. One entry per decision: what we found, what we did, why. The originality CI (`scripts/check_originality.py`) is the mechanical gate; this file records the human judgments that aren't reducible to n-gram overlap.

---

## 2026-05-25 — T1: primitive mapping audit vs. the original article

### Methodology

1. Fetched Jason Liu's original article (`https://jxnl.co/writing/2026/05/10/codex-maxxing/`) and extracted plain text (15.8 KB, 129 logical lines).
2. Catalogued every primitive Jason names — both via H2 sections and via the inline definition-card boxes scattered through the prose.
3. Audited `AGENTS.md` / `CLAUDE.md` / `skills/**/*.md` section by section against that catalogue.
4. Result: 7 deviations, three buckets — (A) Jason has it, we missed; (B) Jason has it, we narrowed or broadened; (C) structural.

### Source primitive inventory (from full read)

Jason names these concepts explicitly, either as an H2 section or in an italicised inline definition card:

1. **Compaction** — definition card; called the first thing that changed his behavior, inside the Durable threads section
2. **Durable threads** — H2 section
3. **Voice input** — H2 section
4. **Steering** — H2 section + definition card
5. **Shared memory** — definition card inside Memory section (used "memory as files" descriptively in the same section)
6. **Computer/Browser use** — H2 section; `$browser` / `@chrome` / `@computer`
7. **Connectors** — paragraph inside Computer/Browser; `$slack` / `$gmail` / `$calendar`
8. **Skills** — paragraph inside Computer/Browser; Skill Creator, Skill Installer, the Hatch Pet example
9. **Remote control** — H2 section; specifically about driving a running Codex task from mobile
10. **Heartbeats** — H2 section + definition card
11. **Goals** — H2 section + definition card
12. **Side panel** — H2 section, three sub-jobs (inspect / operate / review)

The upstream SPEC §5.2 mapping collapsed Compaction into Durable threads, and folded Connectors + Skills into a single "tool tiering" line. The 9-primitive table in our README inherited that compression. This audit unpacks it.

### Findings & decisions

#### A1. Compaction was buried as a sub-clause

- **Source**: Definition card; introduced as the first behavior-changing thing in the Durable threads section; framed as the operation that makes long-lived threads sustainable at all.
- **Before**: Sub-clause inside the "Pin long-lived threads" bullet in Operating loop defaults.
- **After**: Leads the Operating loop section as its own primary bullet ("Compaction first.").
- **Why**: A reader skimming the file would now actually notice compaction as a thing to do. Without it, durable threads collapse under their own weight — the original makes that causal link explicit, so we should too.

#### A2. Connectors was treated as a sub-point of Tool tiering

- **Source**: Connectors paragraph; framed as the agent's reach into systems where work shows up before it becomes code (chat, mail, calendar).
- **Before**: `$slack` / `$gmail` / `$calendar` mentioned in the closing line of Tool tiering, framed as "alternatives to `@computer`".
- **After**: A new section between Tool tiering and the new Skills section. Tool tiering is about *access level*; Connectors is about *which systems you can reach into at all* — different axes.
- **Why**: Framing connectors as merely a faster `@computer` misses the source's point — connectors reach into systems with their own state and workflows that wouldn't be addressed by GUI control at all.

#### A3. Skills primitive was missing entirely

- **Source**: Skills paragraph; the recurring idea is packaging a one-off useful workflow so the agent can repeat it without being retaught.
- **Before**: No section in AGENTS.md. CLAUDE.md's "Companion skills" closing block is about *this repo's three skills*, not about the skill primitive in general.
- **After**: New section "Reusable workflows (Skills)" with three bullets: when to package, what shape (trigger / procedure / outputs), and a pointer to the three companion skills as worked examples.
- **Why**: This is one of the higher-leverage ideas in the source (one-shot win → repeatable behavior). Leaving it out of an executable distillation is a meaningful gap.

#### B4. "Side panel" was narrowed to "prefer HTML output"

- **Source**: Side panel has three jobs — inspect artifacts, operate web surfaces, review changes. HTML is one practical tool inside "operate web surfaces" alongside Storybook, Remotion Studio, Slidev, Streamlit.
- **Before**: "Output: prefer interactive artifacts" — only the HTML-output angle.
- **After**: Renamed to "Inspectable surfaces (side panel)" and broadened to capture inspect + operate + review. HTML remains the lightest default; heavier alternatives are named for the workloads they fit.
- **Why**: The old heading reads like a stylistic preference. The primitive is about *where* the work lives, not what format it's in.

#### B5. "Remote control" was renamed to "Long tasks: pausable, resumable, remote-friendly" — broadened past its meaning

- **Source**: Remote control is specifically about controlling a Codex task running on the home machine from a phone — preserving momentum across physical contexts.
- **Before**: A general checkpointing rule ("design tasks expected to run >5 minutes to survive interrupts").
- **After**: Renamed to "Remote control (intervene from another device)" and restated around explicit decision points + a short visible action queue, with pausability as means rather than end.
- **Why**: Generic checkpointing is engineering hygiene any agent should do regardless of this methodology. The primitive's actual content — designing tasks so a phone touch can move them forward at the right beat — got lost.

#### B6. "Memory as files" vs. "Shared memory"

- **Source**: The primitive's formal definition-card name is "Shared memory"; the article uses "memory as files" descriptively elsewhere in the same section.
- **Before**: "Memory as files" as the section title.
- **After**: Keep "Memory as files" — it's both an authorial phrase from the source and more concrete than "Shared memory". Add a parenthetical "(a.k.a. shared memory)" to the heading so anyone searching for the primitive-card name lands here.
- **Why**: Naming preference, not a substantive deviation; recorded so the reasoning is auditable later.

#### C7. Section ordering compressed the source's first three sections into one

- **Source order**: durable threads / voice / steering / memory / computer-browser / remote control / heartbeats / goals / side panel.
- **Before**: First three folded into "Operating loop defaults"; remote control demoted to after goals (now position §7); side panel demoted to "Output" at the end.
- **After**: Keep the folding of the first three (the original's intro paragraph itself groups them as the "operating loop" — this is a faithful product abstraction). Restore source ordering for everything that follows: memory → tools → connectors → skills → remote control → heartbeats → goals → inspectable surfaces.
- **Why**: Section order is pedagogy. The source's order builds upward from foundations. Our previous order had remote control appearing *after* goals, which broke the build-up.

### Skills audit

- **`verified-goal/SKILL.md`** — used the 7-word phrase "ambition without verification is just a wish" without quotation marks or attribution. Fixed: wrapped in a proper blockquote with credit line. (The 7-word phrase is under the originality CI's 15-token threshold so the script doesn't flag it, but proper attribution is the editorial right answer.)
- **`chief-of-staff-heartbeat/SKILL.md`** — clean. The label "Chief of Staff" overlaps with an example name from the source but is used here only as a thread role, not a copied passage; the worked example (blog comments) is original.
- **`memory-as-files/SKILL.md`** — clean. The vault structure has the same shape as the source's (TODO + people/ + projects/ + notes/, omits the source's `agent/`), but a directory layout is not a copyrightable expression. Worked example (Sara/Marcus handover) is original.

After T1 edits, `python3 scripts/check_originality.py` returns OK at HEAD of `optimize-content`.

### Side-by-side: what each section looks like before vs. after

| Section | Source | Before | After |
|---|---|---|---|
| Operating loop | §1 + §2 + §3, compaction inside §1 | 3 bullets, compaction buried | 4 bullets, compaction first |
| Memory | §4 (Shared memory card) | "Memory as files" | "Memory as files (a.k.a. shared memory)" |
| Tool tiering | §5 (Computer / Browser) | "Tool tiering" — kept | unchanged here (T2 window verifies the `$browser`/`@chrome`/`@computer` syntax) |
| Connectors | inside §5 | last line of Tool tiering | **new** dedicated section |
| Skills | inside §5 | absent | **new**: "Reusable workflows (Skills)" |
| Remote control | §6 | "Long tasks: pausable…" (broadened) | "Remote control (intervene from another device)" |
| Heartbeats | §7 | unchanged | unchanged |
| Goals | §8 | "Verified goals" | "Verified goals" — unchanged content, repositioned |
| Side panel | §9 | "Output: prefer interactive artifacts" (narrowed) | "Inspectable surfaces (side panel)" |

---

## Pending

- **T2** — verify `$browser` / `@chrome` / `@computer` / `$slack` etc. against the real Codex CLI; outcome may further edit AGENTS.md Tool tiering.
- **T4** — README rewrite: sync the primitive table to the new section list above; add the originality badge already landed on `main`.
- **T5** — `gh repo edit` for topics + description.
- **README originality scope** — the current `check_originality.py` does not scan `README.md`. The README has the highest reader traffic and is also the most likely place for slips. Recommend adding it to `DIRECT_TARGETS` once T4's rewrite stabilises; deferring the decision to that window.
