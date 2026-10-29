# EP001 script review — FINAL independent 03b review (verification-only follow-up)

- Episode: inside-the-process EP001 "How Bread Rises: Inside the Dough"
- Reviewer: independent 03b final reviewer (did not author 03a script)
- Inputs read: `pipeline/stages/03b-script-review.md`,
  `episodes/inside-the-process/EP001/story/script.md`,
  `episodes/inside-the-process/EP001/story/sources.md`,
  `episodes/inside-the-process/EP001/story/coverage-map.json`,
  `episodes/inside-the-process/EP001/story/script-review.md` (prior REVISE, R1–R7),
  `episodes/inside-the-process/EP001/story/premise.md`,
  `episodes/inside-the-process/EP001/story/compliance.md`
- Scope of this round: verification-only per the 03b follow-up rule in
  `pipeline/stages/03b-script-review.md`. Only the previously open items
  named for this round were checked — R1, R4, R5, R6 — each as described,
  inside its cited claim's Limits, with no new factual or clip-boundary
  defect introduced in the edited text. No whole-script re-read for new
  advisories, no re-run of the blind naive-viewer test.
- Reviewer actions: read-only validator runs only (exact commands in §5).
  No `--emit-review`, no edit to `script.md`/`sources.md`, no
  `preflight complete`, no approval. The 03b owner gate stands for the
  owner to decide; this file is a verdict, not a completion.

## Overall verdict

**CLEARED**

All four checked items (R1, R4, R5, R6) are applied as described and stay
inside their claims' Limits. Both mechanical checks PASS (§5). The
non-blocking notes in §6 do not change the verdict.

---

## 1. R1 — ingredient origins and roles in row 2 (CLM-9 / CLM-10)

**CLEARED.**

Row 2 Control dialogue (script.md row 2):

> "Flour from milled grain, water, living yeast from its dry packet, and
> mined salt. Water wakes the dormant yeast, flour feeds it, and salt
> slows it slightly while tightening the net to come."

Check against the ledger in `sources.md` and `coverage-map.json` COV02
(claim_ids CLM-1, CLM-9, CLM-10; script_rows ["2"]; row 2 cites
CLM-1, CLM-9, CLM-10):

- Origins/identity for all four ingredients are now spoken in row 2, as
  R1 required: flour from milled grain, water named as its own
  ingredient, living yeast from its dry packet, mined salt. This closes
  the prior gap (yeast only as a name, salt only as the unsourced
  metaphor "keep its work honest", no origins).
- Yeast identity and activation stay inside CLM-10 (SUPPORTED: living
  single-celled organism, sold dry and dormant, warm water/dough
  reactivates it): "living yeast from its dry packet" and "Water wakes
  the dormant yeast" are faithful paraphrases. "Flour feeds it" stays
  inside CLM-1 (yeast ferments dough sugars / feeds on sugars in flour).
- Salt's role stays inside CLM-9 (SUPPORTED: slows fermentation
  slightly, tightens the gluten network): "salt slows it slightly while
  tightening the net to come" tracks the claim almost word for word,
  including the "slightly" hedge CLM-9's limits require. No quantity
  claim is made, honouring CLM-9's recipe-variability limit.
- No wording exceeds the claims: no strain, medical, probiotic, or
  universal-quantity claim is introduced.

## 2. R4 — crumb / crust / bubble jobs together on a mapped row (row 12), plus storage

**CLEARED.**

Row 12 is a mapped COV01 row (`coverage-map.json` COV01 script_rows
["9", "12"]) and is also mapped to COV07 (script_rows ["11", "12"]).
Its Control dialogue states all three jobs together, in one beat, as
R4 required:

> "Every bubble in that slice is a breath the yeast left behind: the
> soft crumb holds them, the firm crust protects them. Wrapped
> tonight, it firms slowly as it rests."

- Bubble job: the retained yeast breath held in the slice — restates
  CLM-3 qualitatively with no bubble count, inside CLM-3's QUALIFIED
  limits (the pattern the prior review held up as safe).
- Crumb job: "the soft crumb holds them". Crust job: "the firm crust
  protects them". The three parts of COV01's question ("what does each
  part — crumb, crust, bubbles — do?") are now answered together on a
  mapped row, closing the prior defect (substance stranded on
  unmapped row 9, never stated together).
- Storage (the missing third of COV07, previously never mentioned) is
  now spoken on the same mapped row: "Wrapped tonight, it firms slowly
  as it rests." This stays inside CLM-12 (QUALIFIED: crumb firms
  further as starch recrystallizes over hours to days; rate varies, no
  guarantee promised) — "firms slowly" is the qualitative form CLM-12's
  limits allow, and no storage guarantee is made.
- Self-audit consistency: the script's completeness list (COV01 rows
  9, 12; COV07 rows 11, 12) now matches what is actually on screen for
  the checked items, including the storage beat.

## 3. R5 — every spoken metaphor logged (VIS-07) and time card (VIS-08)

**CLEARED.**

`sources.md` visualization ledger now carries both entries the prior
review found missing:

- VIS-07 logs the spoken metaphors as metaphor, with mechanism wording
  kept literal in the same lines: "Yeast as workers/breathers, rise as
  engine, colour as receipt, patience as ingredient (spoken
  metaphors)" (CLM-1, CLM-10). Each named metaphor is present in the
  dialogue exactly where logged:
  - engine — row 4 Control: "That is our engine."
  - workers — row 7 Explorer: "The workers are at it again, slower now."
  - receipt — row 9 Control: "The colour is the receipt."
  - patience — row 11 Control: "Patience is an ingredient here."
  The foam-city / scaffolding metaphor remains logged separately under
  VIS-02, so no spoken metaphor in the checked rows is unlogged.
- VIS-08 logs the time-compression card the prior review found missing
  (VIS-06 alone covered only the COV08 disclosure): "Time-compression
  card: hours of fermentation shown in seconds", a post-produced text
  card with the exact planned line "Hours of rising, shown here in
  seconds." Row 1 plans it explicitly — visible action "post card
  planned (VIS-08)", Visualization IDs VIS-06, VIS-08 — and the writer
  self-audit now correctly attributes the time-compression disclosure
  to VIS-08 instead of claiming it is in the dialogue or under VIS-06.

## 4. R6 — header deviation covering late arc, outside share, metaphor seeding, COV05

**CLEARED.**

The script header now records an explicit, owner-approved demo-grid
deviation instead of passing silently as "at its targets" (script.md,
"Demo-grid deviation" paragraph). It covers all four points R6 named:

- Late arc: "the climax and objection land later than the 43-50% /
  53-58% targets because proofing must precede the oven" — the
  process-order reason is stated, not hidden.
- Outside share: "Outside rows are 1 and 12 (17%); rows 9 and 11 carry
  surface/outside portions, keeping inside share at target" — the
  below-target fully-outside count and the partial-outside rows are
  both declared.
- Metaphor seeding: the deviation "also covers the master metaphor
  being seeded at row 3 (scaffolding) rather than in the hook".
- COV05 qualitative-only: "conditions (COV05) being answered
  qualitatively without spoken temperatures, per CLM-5/CLM-6
  variability" — matching the QUALIFIED limits of CLM-5 and the
  kitchen-variability limit of CLM-6, and matching what rows 7 and 9
  actually speak.

The deviation is labelled owner-approved at 03b revision and recorded
in the script itself, which is the form R6 allowed ("record an explicit
owner-agreed demo-grid deviation in the script header"). The objection
(row 10) still precedes the practical section (row 11), as required.

## 5. Mechanical checks (re-run by this reviewer, read-only)

Exact commands run, no `--emit-review`:

```
python tools/coverage_validator.py --channel inside-the-process --episode EP001 --stage 03a-writer
coverage check (03a-writer) -- inside-the-process / EP001: PASS
```

```
python tools/clip_split_check.py --channel inside-the-process --episode EP001
  row   1  OK   [40]
  row   2  OK   [41]
  row   3  OK   [42]
  row   4  OK   [40]
  row   5  OK   [41]
  row   6  OK   [41]
  row   7  OK   [38]
  row   8  OK   [41]
  row   9  OK   [42]
  row  10  OK   [39]
  row  11  OK   [40]
  row  12  OK   [39]
clip split check -- inside-the-process / EP001: PASS (12/12 rows split cleanly)
```

Both PASS with the revised dialogue. All 12 rows sit inside the
channel spoken-word band (38–42); the beat table's own estimates now
agree with the tool counts on the checked rows (row 2: 41, row 12: 39).
No new clip-boundary defect was introduced by the R1/R4/R5/R6 edits.

## 6. Non-blocking notes (noticed in passing; do not change the verdict)

Per the follow-up rule, these are listed for the record only:

- N1. Row 12 speaks the CLM-12 storage beat ("Wrapped tonight, it firms
  slowly as it rests") but its Claim IDs cell cites CLM-3 and CLM-8
  only. The claim exists in the ledger and is bound to COV01/COV07 in
  `coverage-map.json`, and the validator passes, but adding CLM-12 to
  row 12's citations at the next touch would make the row
  self-documenting.
- N2. Row 9 is listed under COV01 in `coverage-map.json`
  (script_rows ["9", "12"]) but its Coverage IDs cell in the beat table
  shows COV05 only. Row 12 alone now delivers COV01's jobs together,
  so coverage is substantively met either way.
- N3. "Mined salt" in row 2 states this loaf's salt origin; CLM-9
  supports salt's role, not a universal salt origin. Read as a
  loaf-specific ingredient choice it is unobjectionable, but it has no
  dedicated ledger claim if a later stage wants to cite one.

## Stop condition

CLEARED at the verification level of this follow-up round. The reviewer
has not run `preflight complete`, has not approved the 03b owner gate,
and has not locked the script. Whether the episode advances is the
owner's decision at the gate.

**VERDICT: PASS**
