---
name: explained-from-within-story-writer
description: Write the source-backed, retention-aware story package for Explained From Within at stage 03a. It adapts the local youtube-scriptwriting craft workflow to factual-process Micro-Journeys. It does not write LTX-2.5 prompts.
---

# Explained From Within story writer

Use this skill only when `channel_slug: inside-the-process` is at
`03a-writer`. It is the sole story writer for that channel. It produces
`story/characters.md` and `story/script.md`; it never writes image briefs,
shot plans, LTX prompts, render manifests, metadata, or uploads.

`../youtube-scriptwriting/SKILL.md` is the retained general craft foundation.
Use its `assets/script-template.md` and `references/hooks.md`,
`references/structures.md`, `references/retention.md`, and `references/editing.md`
as craft libraries. This skill is the controlling channel adaptation whenever
the generic guidance conflicts with the evidence, compliance, runtime, audio,
or originality requirements below.

## Authority order

Read and apply in this order:

1. this skill;
2. `../../pipeline/stages/03a-writer.md` and
   `../../pipeline/youtube_benchmark.md`;
3. `../../channel_profiles/inside-the-process/channel.json` for all numbers;
4. `../../channel_profiles/inside-the-process/bible/EPISODE_SPEC.md`,
   `SCRIPT_BRIEF.md`, `SCRIPT_CRAFT.md`, `CAST.md`, `CHARACTER_BIBLE.md`, and
   `SCIENCE_AND_SOURCING.md`;
5. the current episode's owner-approved `story/coverage-map.json`
   (`../../pipeline/process_coverage.md`), `story/premise.md`,
   `research-notes.md`, `sources.md`, `compliance.md`, and validated
   `youtube-benchmark.md`;
6. the local generic craft skill and its companion guides.

The approved claim ledger and compliance clearance are factual authority. The
coverage map is **scope** authority: it says what the episode must answer, and
no craft consideration removes an item from it. The topic-market brief and
generic craft skill are storytelling references only; neither can introduce a
claim, number, visual convention, process variation, or title promise — and
neither can drop a coverage item. Where the generic skill says to skip a
low-surprise fact ("Below 50 = Skip"), that never applies to a MUST coverage
item on this channel.

## Required workflow

### 1. Establish the foundation

Write, at the start of `story/script.md`:

- one original logline;
- one viewer takeaway supported by the approved scope;
- the target viewer and one primary feeling (normally curiosity or controlled
  awe, never fear manufactured from an ordinary process);
- one core promise that the episode can visibly and factually deliver;
- the primary viewer question and the representative process boundary.

Use the topic-market brief only to test whether the audience promise is clear,
the current format is understood, and the channel has a distinct original
value. Do not copy a competitor's phrasing, order, scene, chapter label,
thumbnail, factory framing, music, CTA, or factual assertion.

### 2. Place every coverage item, then rank for emphasis

Start from `story/coverage-map.json`, not from what is most interesting:

1. **Every in-scope MUST item gets at least one beat**, built from its
   `claim_ids` (supported or qualified claims only). This is not negotiable
   and not ranked — an essential, unsurprising step ("it starts as sand")
   appears exactly like a surprising one.
2. **Every out-of-scope MUST item's `disclosure`** is written into a line of
   dialogue verbatim, at the point where the gap would otherwise be noticed.
3. **Only then rank for emphasis.** Use the generic skill's surprise method to
   decide how much *time* each beat gets — one clip for the expected step,
   several for the counter-intuitive one — never whether it appears. OPTIONAL
   items are included in ranked order while runtime allows.

There is no fixed beat count; the coverage map decides. For each beat record
its coverage item IDs, claim IDs, visualization ID where applicable, and the
misconception, question, or visible state-change it resolves. After drafting
the table, write each item's beat-table row numbers into its `script_rows`.

*Why:* EP001 kept only beats that were "both causally necessary and likely to
change understanding". Raw materials are necessary but unsurprising, so they
failed the *and* — and the episode reached its stills before anyone noticed it
never showed what glass is made of.

An unresolved claim blocks the draft. Return it to research/sourcing instead
of inventing a satisfying explanation.

### 3. Make the causal outline before dialogue

Build the channel structure, rather than a generic listicle:

1. familiar object/event and specific viewer question;
2. conceptual entry with required fictional, scale, time, cutaway, or
   visibility disclosure;
3. baseline — **what it is made of and where it starts** — and the constraint
   that must be solved. For a made thing, the true raw/original starting
   substances and, if it has parts, what each part is and does (a battery's
   cathode, anode, electrolyte and separator before any of them is made); for a
   biological process, the anatomy involved and its resting state; for a
   natural or system process, the ingredients or source. Never an
   already-transformed intermediate state ("molten glass"). If a general
   viewer would reasonably ask "what is this made of / what are its parts,
   before any of this happens?", it is answered on screen, not left as
   "implied, not shown". The only exception is an origin the coverage map puts
   out of scope — and then its disclosure is spoken on screen;
4. distinct causal stages, each using `state A → interaction → state B → why
   it matters`;
5. a supported misconception correction or comparison;
6. stable result at the evidence-supported scope;
7. return to the familiar outside-world object/event;
8. one optional original next-question bridge.

The familiar trigger must be visible immediately, the question must be clear
within 30 seconds, and the inside-view promise must arrive by 45 seconds.
Every 30–60 seconds, earn attention with a new causal question, material
state, comparison, supported correction, or visible transformation. Do not
use a countdown, invented emergency, worker peril, generic factory spectacle,
or a rehook that repeats the same claim.

### 4. Snapshot cast and draft the table

Create `story/characters.md` from the registry, including only roles the
script actually uses. The Explorer observes and asks concise questions;
audio-only Control explains one cause or limit at a time. Neither directs the
process or claims unsupported authority. Per the channel voice rule
(`VISUAL_STYLE_CONTRACT.md`):
- Explorer words are a voice over the helmet radio, never lip-synced, and the
  face is never revealed.
- Give the Explorer lines only in rows where the Explorer is visible, and place
  them before Control's line in that row.
- In the visible action, the Explorer holds still, watching, while its line
  plays. Name any body gesture for the moment before or after the line.

From the next LTX episode, the story follows `channel_profiles/inside-the-process/bible/STORY_ENGINE.md`:
confirm `story/story-definition.md` first, write Control's narration to "you", place the arc by share
of runtime, stage the master metaphor as an inside place the Explorer enters, and keep practical
sections to explanation. The recurring outside "you" figure (CAST-002) appears only in outside rows.

Write `story/script.md` as a scene/beat table with at least:

| # | Time | Duration | Story question / payoff | Visible action and before → after state | Coverage IDs | Claim IDs | Visualization IDs | Explorer words | Control words | Native dialogue window | Diegetic soundscape | Non-diegetic music | Spoken-word estimate |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---:|

`#` is the row number that `coverage-map.json` → `script_rows` points at, and
`Claim IDs` must carry the item's claims on that row — both are read by
`tools/coverage_validator.py`.

Use exact approved dialogue words and explicit native-LTX-2.5 dialogue
windows. Keep dialogue, diegetic soundscape, and non-diegetic music separate.
Leave real observation space before/after lines. No spoken claim may exceed
what the visible action and source ledger support.

The active channel profile requires a 540–660 second finished landscape
episode with roughly 1,000–1,200 spoken words (`channel.json` → `format`).
Plan for later 20-second source clips by giving each future unit one primary
causal action with a readable initial state and a stable changed state — the
duration is fixed 20 seconds in this repo (not the 15 seconds this channel
uses under its sibling LTX profile); do not write LTX prompt prose in
this stage.

### 5. Apply the full craft audit

Before handoff, record a concise `## Writer self-audit` in `story/script.md`:

- **Expectation/payoff:** the hook, intended title concept, opening visual and
  ending visibly deliver the same promise.
- **Story flow:** every beat advances the one causal journey; delete tangents
  and repeated factory imagery.
- **Comprehension:** use plain active English, define a technical term when it
  becomes visible, and restate a difficult causal idea more simply when needed.
- **Retention:** check the opening, 30–60 second rehooks, set-up/payoff loops,
  pattern interrupts, and the next-question bridge.
- **Evidence and visuals:** every factual beat maps to approved claim and
  visualization IDs; all qualifications and synthetic-visualization
  disclosures remain intact.
- **Completeness:** every in-scope MUST item in `coverage-map.json` has
  `script_rows` pointing at beat-table rows that cite its claims, and every
  out-of-scope MUST item's disclosure is spoken verbatim;
  `tools/coverage_validator.py --stage 03a-writer` passes.
- **Raw origin and composition:** the baseline (outline step 3) is the true
  starting substance — and, for a made thing, its parts and their roles; for a
  biological process, the anatomy — not an already-transformed intermediate
  state, unless the coverage map puts it out of scope with an on-screen
  disclosure.
- **Audio and production:** dialogue has exact words/windows, speakers are
  correct, silence has a visual purpose, and each future source clip can carry
  one primary action within the channel's `spoken_word_band`.
- **Clip cuts:** each 20-second clip renders its own audio, so a row's dialogue
  must divide into its clips at *sentence ends or speaker changes*, with every
  clip inside `spoken_word_band`. Being in band on average is not enough: EP001
  revision 9 was, yet 9 of its 15 rows could only be cut mid-phrase. Write each
  clip's worth of dialogue as whole sentences that describe that clip's shot.
  `tools/clip_split_check.py` checks this, and it runs inside the 03a coverage
  check. A comma or dash cut passes, but it is reported; prefer a full stop.
- **Runtime and originality:** total duration and spoken words meet the active
  profile; no competitor wording, sequence, branded treatment, or copied
  material enters the draft. The topic-market brief has not prescribed the
  script's emotional arc, CTA, visual treatment or scene order.

## Hard boundaries

- Do not copy or store full third-party transcripts.
- Do not treat a topic-market brief, generic script guide, AI answer, title, thumbnail,
  or manufacturer video as factual evidence.
- Do not use unsupported universal timing, temperature, strength, safety,
  scale, factory-access, or machine-design claims.
- Do not create a visible Control character, extra passengers, a second role
  for one performer, or an Explorer who touches or operates the process.
- Do not add a second narration, post-production score, or dialogue source.
  The approved words, process audio, ambience, and music are authored for
  native LTX-2.5 generation later.
- Do not advance the episode, perform the independent `03b-script-review`,
  lock the script, or start visual production.
- Do not reuse the sibling LTX profile's already-produced episode premise,
  script, or dialogue as source material for this profile's episode — this is
  a fresh production, not a re-render of that episode.

## Handoff

The stage is ready for independent review only when
`python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage 03a-writer --emit-review`
passes (it re-runs the benchmark validator too) and both `story/characters.md`
and `story/script.md` contain the required material. An item that cannot be
placed within the runtime goes back to the owner — reopen `01b` to rescope it
with a disclosure — never quietly dropped or demoted here (the validator fails
on a demoted or scoped-out locked item). `03b-script-review` is a different session/actor and may
return the script here for revision. The later
`local_skills/ltx-production-writer/SKILL.md` (04f/04f3) and
`local_skills/frame0-still-writer/SKILL.md` (04f2) remain the sole writers for
LTX-2.5 clip prompts and frame-0 stills.
