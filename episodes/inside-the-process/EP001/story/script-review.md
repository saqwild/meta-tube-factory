# EP001 script review — 03b (independent, recorded run)

Reviewer: independent 03b session (not the 03a writer). Scope: `story/script.md`
(12 rows) against `story/sources.md` (CLM-1–CLM-12), `story/coverage-map.json`
(COV01–COV08), `story/characters.md`, `story/premise.md`, `story/compliance.md`,
`story/story-definition.md`, `story/youtube-benchmark.md`,
`channel_profiles/inside-the-process/channel.json`, `bible/STORY_ENGINE.md`, and
`local_skills/explained-from-within-story-writer/SKILL.md`. This review does not
approve or lock the script; the owner gate at 03b remains the owner's.

## Method note on the blind test

The stage asks for a blind naive-viewer test written before reading the script.
In this recorded run the delegated read list presented the script in the same
batch as the premise, so a genuinely blind pass was not possible and none is
claimed. Instead: (a) the questions below were written as a naive-viewer check
and are marked post-read, not blind; and (b) they were cross-checked against
the six `naive_viewer_questions` already locked in `coverage-map.json` before
03a, which serve as the independent pre-script record.

Naive-viewer questions (post-read check) and where the script answers them:

| # | Question a curious 14-year-old would ask | Answered? | Beat |
|---|---|---|---|
| 1 | What is bread actually made of, and where do flour, yeast and salt come from? | Yes | Row 2 (COV02); wheat origin declared out of scope in row 1 (COV08) |
| 2 | Why does the dough get bigger if nothing is added — who makes the gas? | Yes | Rows 4–5 (COV04, CLM-1/CLM-3) |
| 3 | Why knead if the yeast does the work? | Yes | Row 3 (COV03, CLM-2) |
| 4 | What are the holes in bread, and is the yeast still alive when we eat it? | Yes | Rows 5, 10, 12 (COV01/COV06, CLM-3/CLM-7) |
| 5 | Why does it rise again in the oven, then stop? | Yes | Rows 8–9 (COV04/COV05, CLM-4) |
| 6 | How do bakers know it is cooked through, and why wait to slice? | Yes | Row 11 (COV06/COV07, CLM-8) |
| 7 | Does squashing it for shaping undo the rise, and does warmth matter? | Yes | Rows 6–7 (COV03/COV05, CLM-11/CLM-6) |

No naive-viewer question a general viewer needs is left unanswered, and the
only out-of-scope item (COV08, wheat growing/milling) carries its disclosure
spoken in row 1: "The flour began as wheat in a field long before it reached
this bowl" (coverage-map disclosure text, capitalised at sentence start).

## Mechanical checks (read-only, as run in this review)

Run exactly as delegated — no `--emit-review`, no stage completion:

```
python tools/coverage_validator.py --channel inside-the-process --episode EP001 --stage 03a-writer
coverage check (03a-writer) -- inside-the-process / EP001: PASS

python tools/clip_split_check.py --channel inside-the-process --episode EP001
  row 1 OK [40] … row 12 OK [39]  (all 12 rows in band)
clip split check -- inside-the-process / EP001: PASS (12/12 rows split cleanly)
```

Both exit 0. Spoken-word estimates (38–42 per row) match the channel band
`render.spoken_word_band` [38, 42] in `channel.json`; every row's dialogue
splits at sentence/speaker boundaries.

## Claim-by-beat check (every beat vs approved claims and QUALIFIED limits)

| Row | Claims cited | Finding |
|---|---|---|
| 1 | CLM-6 | Hook + COV08 disclosure only; no unsupported fact. Fictional-guide and magnified-scale disclosure spoken ("fictional guide, at magnified scale"). |
| 2 | CLM-1, CLM-9, CLM-10 | Flour/water/living dormant yeast/salt and each role as ledgered; salt "slows it slightly while tightening the net" stays inside CLM-9. No quantity claim. |
| 3 | CLM-2 | Kneading → long elastic gluten strands that trap gas; "without it, every bubble would simply escape" matches CLM-2's dense-bread limit. |
| 4 | CLM-1 | Yeast feeds on flour sugars, breathes out CO₂; ethanol (CLM-1) is omitted, not contradicted. |
| 5 | CLM-1, CLM-3 | QUALIFIED honoured: "Millions of tiny bubbles" is used as the ledger's permitted image, not a measured count for this loaf (script header and self-audit restate this). Shared stretch = visible rise, as CLM-3 bounds it. |
| 6 | CLM-2, CLM-11 | QUALIFIED honoured: only oversized bubbles pressed out, smaller ones redistributed, surface tensioned; described for this loaf, not as universal technique. |
| 7 | CLM-6 | Warmth/cool pace and flavour-over-time trade-off, no universal timing promised — inside CLM-6 variability. |
| 8 | CLM-4 | Oven spring: trapped gas expands, yeast's last minutes of activity before heat death; no temperature numbers asserted. |
| 9 | CLM-4, CLM-5 | QUALIFIED honoured: starch "swelled and locked", crust "browns and crispens" — qualitative only, no spoken 65–82 °C / >140 °C figures, per the recorded deviation. |
| 10 | CLM-7 | Objection beat: yeast killed by heat as the loaf bakes, gradual-death wording as CLM-7's limit requires. Initial-rise vs finished-bread state is kept distinct (rows 9–10). |
| 11 | CLM-8 | QUALIFIED honoured: colour, hollow sound, set crumb as cues; no single universal internal-temperature number; early slicing → gummy crumb, cooling finishes set. |
| 12 | CLM-3, CLM-8 | Callback: bubbles as yeast's retained breaths, soft crumb / firm crust roles (COV01); "wrapped tonight, it firms slowly as it rests" is a hedged staling image consistent with CLM-12's variability, with no storage guarantee. |

No beat exceeds its cited claim, no QUALIFIED claim is stated as measured or
universal, no unsupported timing/temperature/safety claim appears, and no claim
in the ledger is UNRESOLVED. Narration and visible action agree in every row
(each row is one before → after state change).

## Coverage completeness

All seven in-scope MUST items land on the rows declared in `coverage-map.json`:
COV01 rows 9, 12; COV02 row 2; COV03 rows 3, 6; COV04 rows 4, 5, 8; COV05 rows
7, 9; COV06 rows 10, 11; COV07 rows 11, 12 — matching the script's self-audit
list exactly. COV08 (out of scope) is disclosed verbatim in row 1. The baseline
is the true starting substances (flour, water, yeast, salt and their roles,
row 2), not an already-transformed intermediate.

## Voice, cast and story-engine checks

- Cast: only CAST-001 (Explorer), VOICE-001 (Control), CAST-002 (outside "you"
  figure), per `characters.md` and `channel.json`; one figure per frame;
  Control never visualised; Explorer observes/asks and never touches or
  operates the process; the "you" figure appears only in outside rows 1 and 12
  and never shares a frame with the Explorer.
- Explorer lines are helmet-radio voice-over, appear only in rows 2–11 where
  the Explorer is visible, and precede Control's line in each row. Control
  speaks to "you" throughout (rows 1, 3–7, 9, 12 explicitly; no lecture voice,
  one cause or limit at a time).
- Master metaphor: foam city / gluten scaffolding (VIS-02), entered by the
  Explorer, paid off at rows 8–10 as the city locks solid and in row 12's slice.
  Every spoken metaphor is in the visualization ledger: foam-city/scaffolding
  (VIS-02), bubbles inflating (VIS-03), oven lock (VIS-04), crust/steam (VIS-05),
  workers/breathers, engine, colour-as-receipt, patience-as-ingredient (VIS-07),
  plus disclosure/time-compression cards (VIS-06, VIS-08).
- Objection (row 10) precedes the practical section (row 11), and row 11 is
  explanation (doneness cues, why cooling matters), not instruction — no recipe
  steps, quantities, or how-to directions.
- Demo-grid deviation is recorded in the script header, not silent: on the
  12-clip process-ordered grid the climax (rows 8–9) and objection (row 10) land
  later than STORY_ENGINE's 43–50% / 53–58% targets because proofing must
  precede the oven; outside rows are 1 and 12 (17%) with surface portions in
  rows 9 and 11; the master metaphor is seeded at row 3; COV05 is answered
  qualitatively without spoken temperatures. This matches the premise's
  owner-decided 240 s demo (12 × 20 s) in place of the 540–660 s long form.
- Writer self-audit is present and complete (expectation/payoff, flow,
  comprehension, retention, evidence/visuals, completeness, raw origin, audio,
  clip cuts, runtime/originality, revision record R1–R7). No LTX prompt prose,
  no benchmark wording/structure/CTA copied, no sibling-profile episode reused.

## Verdict

Cleared at 03b review. This is a reviewer verdict only; it does not approve or
lock the script — the owner gate decides.

**VERDICT: PASS**
