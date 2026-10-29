# EP001 script review — 03b-script-review (independent)

- Episode: inside-the-process EP001 "How Bread Rises: Inside the Dough"
- Reviewer: independent 03b reviewer (did not author 03a script)
- Inputs read: `pipeline/stages/03b-script-review.md`,
  `story/script.md`, `story/characters.md`, `story/coverage-map.json`,
  `story/sources.md`, `story/compliance.md`, `story/premise.md`,
  `story/story-definition.md`, `story/youtube-benchmark.md`,
  `story/research-notes.md` (supporting only, not factual authority),
  `channel_profiles/inside-the-process/channel.json`,
  `bible/EPISODE_SPEC.md`, `bible/SCRIPT_CRAFT.md`,
  `bible/STORY_ENGINE.md`,
  `local_skills/explained-from-within-story-writer/SKILL.md`
- Factual authority applied: `story/sources.md` claim ledger only.
  Research notes and benchmark do not authorise script facts.
- Reviewer actions: read-only validator runs only. No `--emit-review`,
  no `preflight complete`, no edit to `script.md`. Owner gate stands.

## Overall verdict

**REVISE (BLOCKED — returns to 03a-writer)**

Mechanical checks pass, but substantive claim-support, coverage and
story-engine checks below fail. Do not lock this draft. Required
revisions R1–R7 are listed at the end with script rows. This review
does not approve the episode past the 03b owner gate.

---

## 1. Blind naive-viewer test (done FIRST)

Per the 03b contract, the following questions were written from only
the premise viewer question — "Why does bread dough rise, and what
actually happens inside it in the oven?" — before `script.md` or
`coverage-map.json` was opened. Recorded exactly as written:

1. What is dough actually made of — just flour and water, or is there more in it?
2. What is yeast — is it alive, and what does it eat?
3. Where does the gas that puffs dough up come from, and why doesn't it just escape?
4. Why do you have to knead dough — can't you just mix it and leave it?
5. Why does dough need to rest/rise twice, and why do bakers punch it down?
6. What happens in the oven — why does it rise even more at first, then stop and turn brown and crusty?
7. Why is the inside soft and full of holes but the outside hard?

Answered / unanswered after reading the script:

| # | Result | Beat evidence |
|---|---|---|
| 1 | PARTIAL — counts as unanswered for salt | Row 2 names flour, water, yeast, salt and gives flour/water roles, but salt's role is the unsourced metaphor "keep its work honest" and no origin is given for water, yeast or salt. COV02 asks what each is and where each comes from. See R1. |
| 2 | PARTIAL | Row 4 answers what yeast eats (sugars → carbon dioxide) and row 10 answers that baking kills it, so "alive" is only implied. The script never states in dialogue that yeast is a living organism, what kind of thing it is, or that it arrives dry/dormant as a sourced fact. A 14-year-old's direct "is it alive?" deserves a direct sourced line. See R1. |
| 3 | ANSWERED | Row 4 (yeast → CO₂ bubbles), row 3 (net traps gas; without it gas escapes), row 5 (many bubbles stretch net = rise). |
| 4 | ANSWERED | Row 3: kneading pulls flour proteins into elastic strands; without the net bubbles escape. Supported by CLM-2. |
| 5 | PARTIAL | Row 6 covers shaping/pressing and row 7 covers the second rise, but the script never explains in sourced terms why there are two rises or what pressing does to the gas. Row 6's shaping claims have no ledger claim. See R3. |
| 6 | ANSWERED (with wording caveats) | Row 8 oven spring, row 9 set/browning/steam. Caveats on "every bubble at once" and "works furiously" in §3. |
| 7 | PARTIAL | Row 9 (crust browns and crispens, starch locks foam) + row 12 (bubbles in slice) imply the contrast, but no beat states why the interior stays soft while the surface dries/browns, and COV01's crumb/crust jobs are not delivered on their mapped row. See R4. |

Contract rule: an unanswered question a general viewer needs is a
`REVISE` unless the coverage map declares it out of scope with an
on-screen disclosure. Q1 (salt), Q2 (yeast identity) and Q7
(crumb-vs-crust) are in scope (COV02/COV01) with no such disclosure.
This alone requires REVISE.

## 2. Mechanical checks (re-run by this reviewer, read-only)

Command run exactly as instructed (03a stage, no emit):

```
python tools/coverage_validator.py --channel inside-the-process --episode EP001 --stage 03a-writer
coverage check (03a-writer) -- inside-the-process / EP001: PASS
```

```
python tools/clip_split_check.py --channel inside-the-process --episode EP001
  row   1  OK   [40]
  row   2  OK   [39]
  row   3  OK   [42]
  row   4  OK   [40]
  row   5  OK   [40]
  row   6  OK   [41]
  row   7  OK   [38]
  row   8  OK   [41]
  row   9  OK   [42]
  row  10  OK   [39]
  row  11  OK   [40]
  row  12  OK   [38]
clip split check -- inside-the-process / EP001: PASS (12/12 rows split cleanly)
```

- Coverage validator (03a): **PASS**. All MUST items have `script_rows`
  citing their claim IDs; COV08 disclosure string is found in
  `script.md` (validator normalises case, so sentence-initial "The"
  passes). Mechanical PASS does not settle substantive coverage —
  see §4.
- Clip split: **PASS 12/12**. Every row's counted words (38–42) sit
  inside `channel.json` `render.spoken_word_band` [38, 42] and split
  at sentence/speaker boundaries.
- Note: the beat table's own "Spoken-word estimate" column disagrees
  with the tool count on most rows (e.g. row 3 table 40 vs tool 42;
  row 6 table 39 vs tool 41; row 9 table 38 vs tool 42). All values
  remain in band, so this is advisory A1, not a failure — but the
  table should be corrected to the tool counts at revision so 04d
  inherits true numbers.

## 3. Claim support — every beat against the ledger

Ledger statuses: CLM-1, CLM-2, CLM-4, CLM-6, CLM-7 SUPPORTED;
CLM-3, CLM-5, CLM-8 QUALIFIED. No UNRESOLVED claims. Findings are
about script wording exceeding or missing those bounds.

| Row | Claim IDs cited | Verdict | Evidence |
|---|---|---|---|
| 1 | CLM-6 | PASS with note | Hook + COV08 disclosure + fictional-guide/magnified-scale disclosure. No warmth/speed claim is actually spoken, so the CLM-6 citation is decorative. Harmless, but citations should mean the row uses the claim. |
| 2 | CLM-1 | **FAIL — R1** | "the water wakes the dry yeast" (hydration/activation) and "the salt will keep its work honest" (salt moderating fermentation) appear in no ledger claim. CLM-1 covers only fermentation → CO₂ + ethanol. Both lines trace to `research-notes.md` COV02, which states facts must still clear 02a — they did not. Salt has no claim anywhere in the ledger. |
| 3 | CLM-2 | PASS | Kneading → elastic strands/net → traps gas restates CLM-2. "every bubble we meet would simply escape" is stronger than the ledger's "gas escapes and bread stays dense" but is a fair paraphrase of the without-net limit. Watch absolutes per `SCRIPT_CRAFT.md` Accuracy language. |
| 4 | CLM-1 | PASS with omission note | Feeds on sugars, breathes out CO₂, bubble caught by net: supported. Ethanol (in CLM-1, "largely bakes off") is never mentioned anywhere in the script. Omission is not a false claim; advisory A2. "That is our engine" is an unlogged metaphor — see §6. |
| 5 | CLM-1, CLM-3 | **FAIL — R2** | Core mechanism supported (bubbles inflate stretching net = rise). But dialogue says "Thousands of bubbles are inflating at once." CLM-3 QUALIFIED limits require bubble-count language to be "millions of tiny bubbles" as an image, not a count. "Thousands" is a different, unmeasured count and contradicts the script header's own claim that the surprise beat was "restated without a measured bubble count, per CLM-3 QUALIFIED limits." |
| 6 | CLM-2 | **FAIL — R3** | Shaping claims — "Only its biggest, weakest bubbles", "Shaping evens the foam and tensions the surface, so the second rise builds a loaf shape instead of a spreading puddle" — have no ledger support. CLM-2 is about kneading developing gluten; no claim covers degassing, redistribution, or surface tension. |
| 7 | CLM-6 | PASS | Warmth sets pace, cold slows, time/flavour trade: within CLM-6. "much of the flavour quietly builds" is qualitative and allowed. "The workers are at it again" (Explorer) uses the yeast-as-workers metaphor, which is not in the visualization ledger — see §6. |
| 8 | CLM-4 | PASS with caveats | Oven spring + expansion + imminent set: supported. Caveats: "Heat expands every trapped bubble at once" (absolute "every/at once"; CLM-4 also includes water vapour, unmentioned — omission only) and "the yeast works furiously for a few last minutes" (activity-rate colour; ledger says only that heat kills yeast). Trim absolutes at revision. |
| 9 | CLM-4, CLM-5 | PASS | Starch swelled/locked foam (gelatinization in plain words), crust browns/crispens: supported. No temperatures are spoken, so CLM-5's QUALIFIED "about" requirement is satisfied by omission. Maillard is never named — acceptable plain-language choice. |
| 10 | CLM-7 | PASS | Objection row. "The heat killed the yeast as the loaf baked" matches CLM-7's prescribed gradual-death wording. Correctly placed before the practical row. |
| 11 | CLM-8 | PASS on claims | Colour, hollow sound, set crumb, gummy-if-early, cooling finishes set: all inside CLM-8. No universal temperature number is given, honouring CLM-8 QUALIFIED limits. Coverage gap on storage is §4, not a claim failure. |
| 12 | CLM-3, CLM-8 | PASS on claims | Callback: bubbles as yeast's retained breath held by the kneaded net restates CLM-3 qualitatively with no count. Good — this is the CLM-3-safe pattern row 5 should follow. |

No script wording invents temperatures, timings, safety guarantees,
brands, medical claims, or factory access. `compliance.md` CLEARED
gates 1–10 and the hard floor (no real person/brand, no footage
claimed as real, no insignia, no alcohol/smoking) are not violated
by any dialogue or visible action in this draft.

## 4. Coverage completeness (substantive, beyond the validator)

Mechanical mapping is complete (validator PASS), but four items are
not substantively answered on screen:

- **COV01 (composition) — PARTIAL (R4).** Mapped only to row 12.
  Row 12 says bubbles are held breath in a slice. It does not say
  what crumb and crust each are/do. Row 9 carries the crust/crumb
  substance but is not a COV01 row. The coverage question ("what
  does each part — crumb, crust, bubbles — do?") and naive question
  ("what are the holes, are they safe?") need the crumb/crust/bubble
  jobs stated together, with safety picked up from row 10.
- **COV02 (raw materials) — FAIL (R1).** Question asks what flour,
  water, yeast and salt are and where each comes from. Row 2 gives
  flour's cargo (starch/protein) and water's job in unsourced form,
  yeast only as a name, salt only as a metaphor, and origins for
  none (flour's wheat origin is the COV08 disclosure in row 1, not
  a COV02 answer). Either source the missing roles/origins at 02a
  and speak them, or return to the owner to rescope COV02 — a MUST
  item may not be quietly thinned at 03a (`explained-from-within`
  skill §2).
- **COV05 (conditions) — PARTIAL (advisory, folded into R4 note).**
  Rows 7 + 9 answer warmth/pace and oven-set qualitatively. No step
  gets a time or heat scale ("what time, warmth and oven heat does
  each step need, and why?"). Given CLM-5/CLM-6 variability limits,
  qualitative-plus-"about" wording is defensible for a 4-minute
  demo, but the writer self-audit should say so explicitly rather
  than claim full completeness.
- **COV07 (product in use) — FAIL (R4).** Question: "How does the
  finished loaf get sliced, stored and eaten?" Rows 11–12 cover
  sliced and eaten (final bite). **Stored is never mentioned.**
  Research-notes COV07 explicitly reserved storage/staling for 02a
  confirmation; no storage claim was ledgered, so the script
  silently dropped a third of a MUST question. Source it or rescope
  with the owner; do not leave the validator's PASS to imply it is
  covered.
- **COV03, COV04, COV06 — PASS substantively** (rows 3/6, 4/5/8,
  10/11), subject to R3 fixing row 6's sourcing.
- **COV08 (out of scope) — PASS.** Disclosure "the flour began as
  wheat in a field long before it reached this bowl" is spoken in
  row 1 Control dialogue (sentence-initial capital only). Verbatim
  requirement met; validator confirms.

Writer self-audit completeness claim ("COV01 rows 12; COV02 row 2;
… COV08 disclosure spoken verbatim in row 1") is mechanically true
and substantively overstated for COV01/COV02/COV07. Revise the audit
with the script.

## 5. Dialogue, clip-split fitness, voice rules

- **Clip fitness: PASS.** 12 rows × 20 s = 240 s demo runtime as
  authorised in `premise.md` (owner decision 2026-10-29; channel
  long-form 540–660 s does not apply to this demo sample). One
  primary state change per row; dialogue in whole sentences;
  `clip_split_check.py` PASS 12/12 in band 38–42 (see §2).
- **Explorer helmet-radio only when visible: PASS.** Explorer speaks
  only in rows 2–11, all inside rows where the Explorer viewpoint is
  present, each placed before Control's line in the row. No Explorer
  line in outside rows 1 or 12. `characters.md` correctly records
  helmet-radio only, visor never transparent, face never revealed.
  No clip asks the Explorer to speak on screen or mentions mouth/lips.
- **Control never visualised: PASS.** No visible action shows
  Control; VOICE-001 is audio-only in `characters.md` and the table.
- **One figure in frame / CAST-002 separation: PASS with note.**
  Outside rows 1 and 12 carry only the "you" figure; inside rows
  carry only the Explorer. Note for 04d: rows 9 and 11 each plan an
  inside→surface/outside transition inside one 20 s clip. That will
  need a declared cut under `STORY_ENGINE.md` §7 / LTX contract or a
  split of the visible action — flag it now so it is not discovered
  at 04f. Row 11 must also keep the Explorer out of the outside
  tap/slice portion.
- **Second-person Control narration: PARTIAL.** Control addresses
  "you/your" in rows 1, 3, 4, 5, 6, 10, 12, but rows 2, 7, 8 and 9
  have no second-person address at all and row 11 speaks of "your
  baker" in third person. `STORY_ENGINE.md` §4 requires speaking to
  "you" throughout. Advisory A3 — restore the anchor in those rows
  without breaking the word band.
- **No LTX prompt prose at this stage: PASS.** Visible-action cells
  are beat descriptions; no `GLOBAL::`/`BEAT::` or render language.
- **No extra speakers/roles: PASS.** Two voices only
  (`channel.json` maximum_speaking_characters: 2).

## 6. Story craft, story engine, originality

- **Causal chain: PASS.** Mixing → kneading/net → fermentation →
  rise → shaping → proof → oven spring → set → objection → doneness/
  cooling → slice. Each row opens a new causal question; set-up/
  payoff pairs (net/catch 3→5, patience 7→11, solid city 9→10)
  land. No tangents, no countdown, no invented peril. Plain active
  English; "oven spring" is defined as it appears.
- **Terminology note (advisory A4).** Spoken dialogue never uses the
  words "gluten", "fermentation" or "gelatinization" — it teaches
  the mechanisms in plain words (proteins/strands/net; feeding/
  breathing; starch swelled/locked). That is good comprehension
  craft, but the self-audit's claim that terms are "defined when
  they first become visible" should be reworded: the episode teaches
  the concepts without naming two of the three terms a viewer will
  meet on a flour bag or recipe. Consider naming "gluten" once at
  row 3 where the net becomes visible.
- **Master metaphor: PASS with timing note.** Foam city is set up
  (scaffolding row 3, city named row 5), entered by the Explorer,
  and paid off as it locks solid with the Explorer inside (rows
  8–10: braced in the city, city stops, finished city). However
  `STORY_ENGINE.md` §3 puts master-metaphor introduction in the
  hook (0–7%); row 1 introduces no metaphor. First scaffolding
  language arrives at row 3 (~17%). Acceptable for the demo grid,
  but name it as a deliberate deviation or seed the city in row 1
  at revision. See R6.
- **Every metaphor in the visualization ledger: FAIL (R5).**
  Ledger logs foam-city/scaffolding/balloons (VIS-02). Dialogue
  adds unlogged metaphors: "That is our engine" (row 4), yeast as
  "workers" (row 7), "Patience is an ingredient" (row 11),
  "The colour is the receipt" (row 9). The 03b contract requires
  every metaphor to appear in the ledger. Log them at 02a or cut/
  reword them.
- **Time-compression disclosure: FAIL (R5).** VIS-03/VIS-04 record
  hours compressed into seconds, and `story-definition.md` promises
  on-screen disclosure. No dialogue discloses time compression;
  row 1 discloses only fictional guide + magnified scale. The
  self-audit's "time-compression disclosures are in the dialogue or
  planned in post (VIS-06)" is incorrect — VIS-06 is the COV08 card
  only. Add a spoken or explicitly planned post disclosure.
- **Arc placement vs `STORY_ENGINE.md` §3: FAIL (R6).** Percentages
  are the rule and scale to 12 clips. Script: climax (oven spring/
  set, rows 8–9) at 58–75% vs target 43–50%; objection (row 10) at
  75% vs target 53–58%; practical (row 11) at 83% vs target 70–85%
  (inside, at the edge); no distinct caveats/"what we simplified"
  beat at 88–95%; callback (row 12) at 92–100% vs 95–100%.
  Objection-before-practical order is correct. The process order
  constrains this (the oven cannot precede proofing), so the fix
  is either a documented demo-grid deviation agreed with the owner
  or a restructure that moves the payoff earlier — it may not pass
  silently as "at its targets."
- **Outside share: FAIL (R6).** Fully outside rows: 1 and 12 =
  2/12 ≈ 17%, below the ~20–25% (6–8 of 32) target in
  `STORY_ENGINE.md` §§1/3. Rows 9/11 contain partial outside views;
  if those count, say so explicitly in the revision and keep the
  inside share at 75–80%. As tabled, the episode is more inside-
  heavy than the engine allows.
- **Surprise beat: PARTIAL.** Intended surprise (many bubbles /
  early oven rise) is present in rows 5 and 8 before the callback,
  but row 5's wording is blocked by R2 and no beat is marked as the
  Shorts lead in the script itself. Fix with R2.
- **Practical = explanation, not instruction: PASS.** Row 11
  explains doneness cues and why cooling matters; it does not give
  a bake recipe, temperatures to follow, or steps to perform.
  `STORY_ENGINE.md` §11 satisfied for a Materials episode.
- **Originality vs benchmark: PASS.** No benchmark title, opening
  line, dialogue, thumbnail, music or CTA is copied. The
  ingredients→kneading→gas order is the process itself, not B01/
  B02/B03 structure; B02's dry-packet framing is not reproduced as
  wording (row 2's activation line fails on sourcing, R1, not on
  copying). The closing question ("what should we travel inside
  next?") is original to this channel's premise. Benchmark was
  used only for audience promise/format signal, as required.
- **Writer self-audit present: PASS in form, overstated in two
  claims** (completeness, time-compression disclosure — see §4/§6).
  Causal/audience/payoff self-audit is otherwise present as the
  skill requires: expectation/payoff, flow, comprehension,
  retention, evidence/visuals, raw origin (row 2 true starting
  substances), audio/production, clip cuts, runtime/originality.
- **Characters snapshot: PASS.** Drawn from the registry, no
  invented cast, audio-only roles included, voice notes correctly
  marked as not identity locks.
- **Sibling-episode reuse: PASS.** Fresh bread topic; no platelet/
  glass/concrete/sleep material reused. Muse drafting is recorded
  in the script (Muse Wonder narration drafting, 2026-10-29) per
  the hackathon overlay.

## 7. Required revisions (REVISE — all must clear before re-review)

| ID | Rows | Required fix |
|---|---|---|
| R1 | 2 | Source or remove "water wakes the dry yeast" and "salt will keep its work honest." Add ledger claims at 02a for hydration/activation and salt's role (with limits), plus yeast identity ("living" organism, dry/dormant arrival) and the COV02 origins the coverage question demands — or take COV02 back to the owner for rescope. Do not promote `research-notes.md` text directly into dialogue. |
| R2 | 5 | Bring bubble-count wording inside CLM-3 QUALIFIED limits: use the ledger's "millions of tiny bubbles" as an image, not a count (the row 12 pattern), or delete the number. Correct the script header/self-audit claim that no count is used. |
| R3 | 6 | Source the shaping/degassing beat (redistribution of large bubbles, surface tension, shape-holding) with a new/extended ledger claim, or cut dialogue to what CLM-2 supports. Row 6 currently explains COV03's second half on no claim. |
| R4 | 9, 11, 12 (+ audit) | Deliver COV01 and COV07 substantively: state crumb/crust/bubble jobs together (reteach on the mapped rows or remap `script_rows` honestly), and either source-and-speak storage (COV07) or rescope it with the owner. Update the self-audit completeness paragraph to match what is actually on screen, including COV05's qualitative-only conditions. |
| R5 | 1, 4, 7, 9, 11 | Log every spoken metaphor in the visualization ledger (engine, workers, patience-as-ingredient, colour-as-receipt) or remove/reword them; add the missing time-compression disclosure (spoken line or explicitly planned post card — VIS-06 alone does not cover it) and correct the self-audit sentence that claims it exists. |
| R6 | 1, 8–12 (grid) | Reconcile the arc with `STORY_ENGINE.md` §3/§4: either restructure toward climax ≈43–50%, objection ≈53–58%, a real caveats beat at 88–95%, and outside share ≈20–25% within the 38–42 word band, or record an explicit owner-agreed demo-grid deviation in the script header (including the late metaphor seeding in row 3 vs hook target). Silent non-compliance is not an option. |
| R7 | 2–12 (re-check) | After R1–R6 edits, re-run `python tools/coverage_validator.py --channel inside-the-process --episode EP001 --stage 03a-writer` and `python tools/clip_split_check.py --channel inside-the-process --episode EP001`; both must still PASS with the revised dialogue in band. Follow-up 03b round will be verification-only per the stage contract unless rows are added/removed/reordered or claims re-scoped (R1/R3/R4 may trigger a full re-review — flag which when returning). |

## 8. Advisories (non-blocking; fix opportunistically in the same pass)

- A1. Correct the beat table's spoken-word estimates to the
  `clip_split_check.py` counts (rows 2, 3, 5, 6, 8, 9, 11 differ by
  1–4 words).
- A2. Consider one sourced sentence on ethanol baking off (CLM-1)
  and steam/water vapour in oven spring (CLM-4) if the word band
  allows; current omissions are honest but leave two ledger facts
  unused.
- A3. Restore second-person "you" address in Control lines at rows
  2, 7, 8, 9 and fix row 11's third-person "your baker."
- A4. Name "gluten" once at row 3 where the net becomes visible, or
  amend the self-audit terminology claim.
- A5. Trim absolutes: row 8 "every trapped bubble at once", row 3
  "every bubble … would simply escape" (`SCRIPT_CRAFT.md` accuracy
  language: prefer "can/helps" where evidence is a range).
- A6. Drop decorative claim citations that the row does not use
  (row 1 / CLM-6) so the validator's citation check stays meaningful.
- A7. For 04d: resolve the inside→outside transitions planned inside
  rows 9 and 11 (declared cut vs split) before prompt drafting.

## Stop condition

REVISE returns EP001 to `03a-writer`. The reviewer has not run
`preflight complete`, has not approved the owner gate, and has not
locked the script. Re-review follows the stage contract's follow-up
rule (verification-only unless the revision is substantial).
