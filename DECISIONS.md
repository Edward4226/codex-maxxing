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

- **Source**: Side panel has two H3 sub-sections — Inspect artifacts and Operate web surfaces. HTML is one practical tool inside Operate alongside Storybook, Remotion Studio, Slidev, Streamlit.
- **Before**: "Output: prefer interactive artifacts" — only the HTML-output angle.
- **After**: Renamed to "Inspectable surfaces (side panel)" and broadened to capture both inspect and operate. HTML remains the lightest default; heavier alternatives are named for the workloads they fit.
- **Why**: The old heading reads like a stylistic preference. The primitive is about *where* the work lives, not what format it's in.
- **Correction (2026-05-27)**: The first version of this entry claimed three sub-sections including "review changes"; a re-fetch confirms the source has only the two H3s listed above. The AGENTS.md prose ("read, annotated, and operated") was unaffected — it maps cleanly onto inspect + operate. See the 2026-05-27 audit entry below.

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

---

## 2026-05-25 — T2: Codex CLI plugin syntax verification

### Methodology

- Probed local Codex CLI 0.130.0 installation (installed at `/Users/edward/.npm-global/bin/codex`, package `@openai/codex@0.130.0`).
- Read `~/.codex/config.toml` for plugin registrations.
- Listed locally cached plugins under `~/.codex/plugins/cache/`.
- Cross-referenced against the syntax used in the source article.

### Findings — these are REAL plugin invocation tokens

Marketplace inventory on this machine:

| Marketplace | Plugins present locally |
|---|---|
| `openai-bundled` | `browser`, `chrome`, `computer-use`, `latex` |
| `openai-curated` | `figma`, `github`, `gmail`, `notion` |
| `openai-primary-runtime` | `documents`, `presentations`, `spreadsheets` |
| custom (git) | `goalnight` |

Direct mapping to syntax used in the source:

- `$browser` → `browser@openai-bundled` (confirmed enabled in `~/.codex/config.toml`)
- `@chrome` → `chrome@openai-bundled` (confirmed)
- `@computer` → `computer-use@openai-bundled` (confirmed; runs `Codex Computer Use.app`)
- `$gmail` → `gmail@openai-curated` (confirmed)
- `$github`, `$notion`, `$figma` — curated plugins (also confirmed enabled in config)
- `$slack`, `$calendar` — not present in this machine's local cache. They match the curated-connector pattern and are likely installable via the marketplace, but not literally verified by this audit.

### Implications

**The syntax already in AGENTS.md is correct — these tokens are not the source author's prompt shorthand, they are literal Codex plugin invocations.** No retraction needed.

Two surgical additions help a reader who installs the file:

1. A one-sentence pointer under Tool tiering: these are real plugins from `openai-bundled`, managed via `codex plugin marketplace`.
2. Connectors paragraph rewritten to name the curated connectors actually shipped (`$gmail`/`$github`/`$notion`/`$figma`) and redirect to `codex plugin marketplace` for the rest.

### Out of scope (deliberately not documented)

- **`$` vs `@` prefix distinction** — undocumented in the CLI help and not cleanly partitioned by marketplace (both `$browser` and `@chrome` sit in `openai-bundled`). A plausible read is "`@` drives a live environment, `$` reads or connects to a service," but this is unverified. Stating it would risk getting it wrong; we leave the prefix as Jason used it and let readers learn the convention from the official docs.
- **`Appshots`** (the macOS Command-Command "send frontmost window to thread" affordance) — a desktop-app UI feature, not a CLI plugin and not an agent behavior. Omitted from AGENTS.md by design.
- **`openai-primary-runtime`** plugins (`documents`/`presentations`/`spreadsheets`) — these power the side panel's artifact rendering. The Inspectable surfaces section already covers them generically; no syntax change.

---

---

## 2026-05-25 — T4: README rewrite + extend originality CI to README

### Methodology

- Audited the old README against the handoff's T4 brief (one-line hook → 60-second install → before/after → primitive map → why-separate → license).
- Validated the install command by reading current Codex / Claude Code conventions: project-level `AGENTS.md` / `CLAUDE.md` are picked up automatically; user-level globals at `~/.codex/AGENTS.md` / `~/.claude/CLAUDE.md` work the same way.
- Drafted six before/after rows, each traceable to a specific rule in `AGENTS.md` or a specific worked example in one of the three skills.

### Decisions

1. **Lead with the action, not the description.** The new hook ("Two `cp` commands and your session inherits…") names the operating-loop primitives explicitly and tells the reader what they get in exchange for two commands. The old hook ("Drop-in AGENTS.md…") read like documentation; the new one reads like an offer.

2. **Before/after rows are reproducible.** Every row is a real prompt the reader can paste into a session that has this file installed. The "after" column is derivable from a specific rule (e.g. *"What command will tell us this worked?"* is a literal line in the Verified goals section). No fabricated stats, no testimonials.

3. **Primitive map shows all twelve primitives, not just nine.** The old README inherited the SPEC's 9-primitive compression; the new map matches `DECISIONS.md`'s 12-primitive inventory and flags the three primitives that get a full Skill.

4. **Codex vs Claude table now reflects the T2 verification.** The old row "Browser/web access — `$browser` / `@chrome` syntax" was correct but unverified at the time; the new rows split it into local-web inspection / logged-in browser control / native-GUI control with the specific plugin names that T2 confirmed.

5. **Extended `scripts/check_originality.py` to scan `README.md`.** The READMD has the highest reader traffic and is the most likely place a future contributor copies a sentence verbatim while paraphrasing the agent files. Locking it in CI is the smallest possible enforcement; previously deferred in this DECISIONS doc, now resolved.

### Out of scope (deferred to later phases)

- **Demo GIF / asciinema** (handoff P1 T6) — can be added without restructuring once the README baseline is stable.
- **Comparison table vs alternative repos** ("Why not awesome-claude-code-rules?") (handoff P1 T8).
- **Chinese translation of the README** (handoff P2).

---

## 2026-05-27 — Round 2: re-audit + corrections

A second pass against the source article, focused on (a) confirming the
Round-1 primitive audit on the actual prose rather than DECISIONS' summary
of it, and (b) probing the Codex CLI directly rather than inferring from
config files. Three corrections landed plus one optional clarification.

### Methodology

1. Re-fetched the source article with prompts narrowed to specific section
   structures (Heartbeats H3s, Side panel H3s, H2 order from Memory
   onwards) — i.e. queries Round 1's general fetch hadn't covered.
2. Probed Codex CLI 0.130.0 directly: `codex plugin --help`,
   `codex plugin marketplace --help`, and each leaf subcommand. Read
   `~/.codex/config.toml`'s `[plugins."*"]` blocks rather than treating
   the cache directory as a proxy for "enabled".
3. Walked AGENTS.md / CLAUDE.md section by section against the verified
   source structure.

### Findings & decisions

#### D1. Section order in AGENTS.md / CLAUDE.md violated the source (and Round 1's stated target)

- **Source H2 order from Memory onwards**: Memory → Computer/Browser →
  Remote control → Heartbeats → Goals → Side panel.
- **Round 1 (C7) stated target**: memory → tools → connectors → skills →
  **remote control → heartbeats → goals** → inspectable surfaces.
- **Actual file order pre-Round-2**: ... → skills → heartbeats → verified
  goals → **remote control** → inspectable surfaces. Remote control had
  drifted to sit *after* Goals, breaking the source's build-up.
- **Decision**: Move the Remote control section to sit between Reusable
  workflows (Skills) and Heartbeats in both AGENTS.md and CLAUDE.md.
- **Why**: This is the source's actual pedagogy — designing tasks for
  remote intervention is named before the heartbeat mechanism that often
  triggers such interventions. Restoring the order is no-cost (same
  paragraphs, no rewording).
- **Commit**: `f90ac92`.

#### D2. AGENTS.md pointed readers at a CLI command that doesn't search

- **Verified behaviour**: `codex plugin marketplace` accepts only `add`,
  `upgrade`, `remove` — there is no `list`, `search`, or registry index.
  `add` takes a concrete source spec (owner/repo[@ref], Git URL, or local
  directory). The cache directory `~/.codex/plugins/cache/{openai-bundled,
  openai-curated, ...}` is populated *after* a marketplace is added; it is
  not a discovery surface.
- **Before**: Connectors section ended with "for `$slack`, `$calendar`,
  and others, check `codex plugin marketplace` for available sources".
  Running that command returns help text, not sources.
- **After**: "for `$slack`, `$calendar`, and others, see Codex's plugin
  docs — additional marketplaces are installed via
  `codex plugin marketplace add <source>` (the CLI itself only exposes
  `add` / `upgrade` / `remove`, not a search index)".
- **Why red line was tested**: the project rule forbids strong "Codex
  supports X" claims absent verification, and prefers "see codex docs"
  fallback when CLI behaviour is ambiguous. The new wording satisfies
  both: it points at the docs *and* names the one CLI invocation that is
  verified, while explicitly disclaiming the absence of a search index.
- **Commit**: `28f0511`.

#### D3. Round 1 entry B4 listed three Side-panel sub-sections; the source has two

- **Verified structure**: Side panel H2 has exactly two H3 sub-sections —
  "Inspect artifacts" and "Operate web surfaces". The phrase "review
  changes" used in the original B4 entry does not appear as an H3.
- **AGENTS.md prose was unaffected**: "read, annotated, and operated" maps
  cleanly onto the two real sub-sections (read ⊆ inspect; operated =
  operate; annotated is the *output* of inspecting, not a third
  sub-section). No prose change needed.
- **Decision**: Correct the B4 entry inline (now reflects two H3s) and
  add a dated correction note pointing back here.
- **Commit**: `84738ad` (part of the DECISIONS update; this very entry).

#### D4. (Optional clarification) "Memories" as a platform feature was not disambiguated from the vault

- **Source distinction**: Jason's Memory section names two separate
  things — Codex's first-party `Settings > Personalization > Memories`
  (cross-thread assistant preferences) plus the opt-in Chronicle
  preview, *and* the vault approach he uses (per-project file store).
- **Before**: The AGENTS.md Memory section described only the vault. A
  reader skimming could believe the rules were about Codex's built-in
  Memories. (CLAUDE.md already drew the equivalent line against Claude
  Code's `/remember` + project-level memory in its existing
  blockquote — no change there.)
- **After**: Add a single blockquote to the AGENTS.md Memory section
  naming Memories and Chronicle, and stating that the vault is
  per-project, diff-reviewable, and portable across hosts.
- **Why marked optional**: This wasn't a structural deviation; the rules
  themselves were correct as written. The footnote prevents reader
  confusion without changing what the rules require.
- **Commit**: `84738ad`.

### What was checked and found *clean*

- The three companion skills (`verified-goal`, `chief-of-staff-heartbeat`,
  `memory-as-files`) were re-read against the source's worked examples
  (Chief of Staff thread, Monitor for feedback, Get a refund, Rich-to-Rust
  port). All in-skill examples remain original: search backend / p50
  latency (verified-goal), blog comment questions (heartbeat), Sara/Marcus
  pipeline handover (memory). No new edits needed.
- The Heartbeats H2 in the source contains three H3 worked examples
  (Chief of Staff, Monitor for feedback, Get a refund). Our AGENTS.md
  Heartbeats section keeps the *primitive* (cadence + source + trigger +
  action; draft-only default) without lifting any of those three example
  contexts — exactly the right line to hold.
- Originality CI ran clean after every commit in this round (six files
  against 2754 source 15-grams, no overlap).

### Out of scope (still deferred)

- Verifying the prompt-time recognition of `$browser` / `@chrome` /
  `@computer` inside a real Codex session — i.e. typing the literal
  tokens into a prompt and confirming the agent dispatches the
  corresponding plugin. The plugin-enabled status is verified at the
  config level; recognition at the prompt level remains a level deeper
  than this audit reached. AGENTS.md does not assert that level of
  verification (no "Codex confirmed to support `$browser` in prompts"
  phrasing) so the file stays inside the project's truth boundary.
- CLAUDE.md line 38's specific path claim about
  `~/.claude/projects/<project>/memory/` — directory presence verified
  on this machine, but the structure inside (whether a `MEMORY.md`
  literally exists) was not exhaustively checked. Out of scope for a
  *Codex*-focused audit; flagged for whoever does a parallel Claude Code
  audit.

---

## Pending

- **T5** — `gh repo edit` for topics + description.
- **Open PR** for `optimize-content` and coordinate merge order with the (now-landed) `add-originality-ci`.
