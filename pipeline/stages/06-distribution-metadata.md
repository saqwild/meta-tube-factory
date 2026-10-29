# 06 — distribution metadata

## Inputs

`render/render-qa.md` (all `PASS`), `channel_profiles/<slug>/channel.json` →
`youtube`/`metadata_validation`, the channel's title-formula reference,
`bible/SEO.md` (keyword families §2, title/description contracts §4-5, tags
§7, thumbnail contract §8), `bible/VISUAL_STYLE_CONTRACT.md`'s thumbnail
contract, and — if the episode has one — its `channel.json → youtube.
primary_keywords` list and `visual/references/manifest.md` (the `[[TAG]]` →
reference-asset map, for the thumbnail).

## Task

Write the title, description, tags, chapters, thumbnail brief, and
made-for-kids / altered-or-synthetic-content declarations. Three things below
are easy to get half-right — each was a real gap found and fixed on EP001,
not a hypothetical.

### 1. Keyword derivation, not just keyword tagging

Pick the episode's pillar and one primary phrase from `SEO.md` §2's keyword
families (or the channel's own `primary_keywords` list). It is not enough
for the primary phrase to show up correctly ordered in the Tags section —
`SEO.md` §5's description template requires the **hook** (the first visible
line) to use the primary phrase or its pillar's supporting vocabulary
*naturally*. Check the actual hook sentence for that vocabulary before
declaring the section done; a title/tags that are keyword-correct while the
visible description hook contains none of it is the gap that shipped on
EP001 v1 (a chosen tag, `digital inheritance story`, never reached the
description at all).

### 2. Thumbnail: a full generation prompt, not just a design spec

The thumbnail brief's spec table (plate/face/quote/number/etc., per `SEO.md`
§8) is not something an image model can render from directly. Also write the
actual Muse Image prompt, in the same anatomy `04f2` stills use
(`MUSE_FRAME0_CONTRACT.md` §2 — cast-count lock, full environment string
verbatim, character block with pose/gaze/expression/mouth, composition +
mood + style), plus:

- explicit `[[TAG]]` → reference-asset attachments (character sheet and/or
  environment plate) with **paths and SHA-256 hashes checked against the
  actual files on disk**, not copied from a doc — a stale or wrong reference
  here conditions the wrong face or set silently;
- a note on what is *not* baked into the Muse Image prompt — the quote text, the
  number and any hairline/divider are typography overlays added in post
  (exact typefaces per `VISUAL_STYLE_CONTRACT.md` are a design-tool pass, not
  something an image model spells reliably — the same reason on-screen text
  is banned from `04f2` prompts).

Write this in full for concept 1. `SEO.md` §8's A/B rule still requires a
second, materially different concept before upload — record its reference
asset(s) too, but the second prompt can be written later if concept 1
underperforms.

### 3. Chapters: check the format before adding every beat as a marker

Chapters are real, verified YouTube functionality (first timestamp `0:00`,
≥3 timestamps, ascending, ≥10s apart — YouTube's own minimum; this pipeline's
convention is ≥20s) and a genuine discoverability channel (Google Search can
surface individual chapters as "key moments"). But for narrative/reveal- or
verdict-driven formats, a standalone chapter marker sitting on the reveal or
verdict is a one-click shortcut to the payoff, which works against the
format's own engagement design (a viewer who skips straight to `Your
Verdict` never watches the argument the comment prompt depends on) and
against average view duration. Fold a trailing reveal/verdict beat into the
chapter before it (e.g. `Closing Arguments` absorbing what would have been a
separate `Your Verdict` marker) rather than giving it its own timestamp.
Tutorial/reference-format channels have no such risk and can chapter every
beat.

### 4. Problems field (Education videos)

YouTube Studio's **Problems** field lists learner questions the video answers, one per line, each starting with the
timecode where its explanation starts (for example `0:59 What raw materials is a glass bottle made from?`). For an
explainer channel it is a direct discoverability and navigation aid. Add a `## Problems (YouTube Studio → Problems
field)` section to `package.md` with a copy-ready block, and mirror it into the upload JSON and the upload sheet.
Rules:
- A question must be answered in the approved script and supported by the claim ledger. Restate the script's own story
  questions for a learner; never invent a question the episode only touches on.
- Each timecode is where the explanation *starts*: the first clip of the row that answers it, using the same maths as
  the chapters, and re-confirmed against the assembled master at `06a`.
- Leave out narrative beats (the opening hook, the Explorer's journey, the ending). *(Added 2026-10-29 at the owner's
  request, first used on inside-the-process EP001.)*

### Validate before declaring this stage done

```
python tools/metadata_validator.py --channel <slug> --episode EPxxx --emit-review
```

It parses the Title/Description sections of `package.md`, checks them against
`channel.json`'s `metadata_validation` (and relevant `youtube`) constants, and
prints PASS/FAIL per rule. It reports only — it never rewrites the package —
and it warns (`META-W001`) on any `metadata_validation` key it doesn't yet
implement, so a channel-specific constant never gets silently skipped. It
does **not** check items 1-3 above (they are judgment calls, not deterministic
constants) — verify those by re-reading the actual hook/prompt/chapter list
before signing off.

## Output

`episodes/<slug>/EPxxx/metadata/package.md`.

## Stop condition

**Owner gate.** Last checkpoint before anything is public-facing. Every
`metadata_validator.py` check passes, the description hook demonstrably uses
the chosen primary phrase or its supporting vocabulary, the thumbnail brief
includes a full concept-1 generation prompt with hash-verified reference
assets, and no chapter marker sits alone on a reveal/verdict beat in a
narrative-format episode.
