# LTX prompt validator — rule catalog

Companion to [`../tools/ltx_prompt_validator.py`](../tools/ltx_prompt_validator.py). Every rule
ID the validator can emit is listed here with what it catches and why it exists. The module
raises if it ever emits an ID that is not declared in its own `IMPLEMENTED_RULE_IDS`, so this
catalog and the code cannot silently drift apart.

## Purpose and boundary

The validator is a **deterministic reporter**. It never rewrites, enhances, paraphrases or
"fixes" a prompt. A failure returns the clip to `local_skills/ltx-production-writer`; it does
not get patched at the gate.

It also does not replace judgement. It catches the mechanical, regex-shaped failures — retired
syntax, missing required clauses, negation, timing markers, a cast mismatch. It cannot tell you
whether a clip is any good, whether the acting reads, or whether the still actually shows what
the prompt claims. Those are the human/vision gates at `04f2` and `04h`.

## Draft vs. strict

The CLI runs in two modes. **Draft** (default) runs every check the inputs on disk allow and
reports, per clip, which rules it could **not** check (`skipped_rule_ids`) because an input was
absent — no `blocking.json` entry, no `frame0-requirements` block, no still, no
`voice-signatures.json`, no `render.spoken_word_band`. A draft run can `PASS` with inputs
missing; its emitted review is stamped `mode: "draft"`.

**Strict** (`--strict`, mandatory at `04f3`) additionally requires every clip to have a
`blocking.json` entry, a `frame0-requirements` block **and** a still — any gap `FAIL`s that
clip. Its review is stamped `mode: "strict"`, and `pipeline/stage-gates.json` accepts **only**
a strict `PASS` to clear the `04f3` completion gate. A rule that was never checked is not a
rule that passed: `checked_rule_ids` lists only what actually ran, and
`checked ∪ skipped == IMPLEMENTED_RULE_IDS` always.

## Tiers

- **error** — blocks the clip. The prompt does not advance to `04g`.
- **warning** — reported and recorded, does not block. Used where the underlying rule is a
  `[C]` `[2.3-RETEST]` house limit rather than a vendor fact, or where the check is
  intrinsically fuzzy.

## Authority precedence

`LTX_I2V_CONTRACT.md` > this catalog > the code. If the code disagrees with the contract, the
code is wrong. If a rule turns out to be wrong, change the contract first and say why — a
validator rule is never edited to make a failing prompt pass.

---

## Format and owner-locked beat syntax

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D001` | error | The prompt is not the owner-locked PromptRelay-style packet — first line is not `GLOBAL::`, more than one `GLOBAL::`, a non-`GLOBAL::`/`BEAT::` line, or no valid `BEAT::` blocks. Format is `render.prompt_format == "prompt_relay_beats_v1"`: one `GLOBAL:: Continue from the still. … Low motion.` line plus `BEAT:: <positive integer frames> :: <text>` lines. |
| `LTXV-D002` | error | A malformed `BEAT::` line, a non-positive frame count, a beat frame total other than **481** (24 fps × 20 s + 1 conditioning frame), **or** loose timing prose inside a beat — `(3.0s)`, `00:05.200`, "at 5 seconds", "second 4". Timing lives only in the `BEAT:: <frames>` labels; inside a beat, order events with chronological connectives. |
| `LTXV-D003` | error | Render configuration in prompt text — fps, aspect ratio, pixel dimensions, megapixels, "1080p", "~20 second clip", the model name. These live in the graph; in the prompt they are dead weight and a misleading token. |
| `LTXV-D004` | warning | Prompt is past the **runaway tripwire** (`max_words`, default 450). **Not a ceiling** — LTX-2.5 has no vendor word limit and the Gemma encoder is built for long prompts. This fires only on genuinely bloated prompts; the fix is to cut a repeated room inventory or duration filler, **never** a load-bearing identity, audio or camera anchor. A dense three-hander normally runs 260–330 words and does not trip this. |
| `LTXV-D005` | warning | A non-dialogue clip outside the 4–8 sentence single-take band. Skipped for beat-packet prompts (the `BEAT::` structure is the length control) and for dialogue clips. |

## Positive-only discipline

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D010` | error | Negation in the positive prompt — "no captions", "no new characters", "never", "do not", "without adding", "avoid …ing". The model renders the tokens it sees; a suppression clause **summons** the thing it names. Quoted dialogue is exempt (a character may say "don't"). Suppression belongs in the negative prompt only. |
| `LTXV-D011` | error | A blanket motion-suppression token inside the packet — `minimal motion`, `static scene`, `still frame`. The mandated `Low motion.` that closes the `GLOBAL::` line is **exempt** (it is the approved global motion constraint). Inside a beat, describe the exact plausible motion instead. |
| `LTXV-D012` | error | A request for on-screen text, captions, title cards, lower thirds or watermarks. Spelling is not guaranteed across frames — those are a post-production pass. |
| `LTXV-D013` | error | Internal pipeline jargon leaking into model-facing text — `blocking.json`, "stage 04", "render package", `[[TAG]]`, `[STYLE]`. |

## Required clauses

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D020` | error | Missing the `Ambient (slow, subtle):` visual-motion sentence. This is genuinely new information the video adds — the still is frozen — so it is never covered by the don't-restate-the-still rule and never dropped for brevity. |
| `LTXV-D021` | error | Missing the `Acoustic environment:` sound sentence. A clip that names no continuing sound bed invites native audio to invent dialogue to fill silence. |
| `LTXV-D022` | error | Ambient motion and acoustic environment merged into one sentence. Visual motion and sound are two separate clauses. |
| `LTXV-D023` | error | A clip with dialogue that omits the mix note "clear close dialogue front and center". |
| `LTXV-D024` | error | No camera movement stated anywhere. A locked camera over a settled character reads as a dead freeze-frame. Detection is two-tier: an unambiguous camera noun (dolly, crane, jib, push in, …) stands alone; an ambiguous movement verb (pan, slide, track, follow) must sit beside a camera subject — otherwise "Bruno's paw slides along the rail" would count as a dolly. |
| `LTXV-D025` | error | Camera movement sharing a sentence with a quoted line. They are two separate clauses. |

## Dialogue

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D030` | error | A labelled dialogue block (`Spoken dialogue:`, `Dialogue:`, `Voice-over:` at line start). A dialogue header reads to the model like a caption track and triggers burned-in subtitles. Fold each line into the speaker's action. |
| `LTXV-D031` | error | A quoted line with no visible action attached to its speaker in the carrying clause. "Bruno says, resigned: '…'" is not enough. |
| `LTXV-D032` | error | A speaking character whose declared voice signature never appears. The inline first-use tag is the only voice definition — there is no separate preamble. |
| `LTXV-D033` | error | A voice signature stated more than once. Inline on the first line only; later lines get bare name + action. |
| `LTXV-D034` | error | Spoken word count outside the channel's declared band. The band comes from `channel.json`, not from this file. |
| `LTXV-D035` | error | The literal word "Narrator", which binds a voice to nothing visible. Describe an off-screen background voice-over instead. |
| `LTXV-D036` | error | 2+ visible characters with dialogue and no explicit closed-mouth clause. This is the mitigation for the wrong-character's-mouth-moving failure class; a reaction clause alone does not satisfy it. |

## Subject and prose

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D040` | error | The `GLOBAL::` line does not name a character as its subject. A scenery-only anchor spawns extra characters or drifts the camera off the subject. (Falls back to the first sentence only if the prompt failed to parse as a relay.) |
| `LTXV-D041` | error | The last `BEAT::` — the explicit productive tail — does not name a character. Its `Acoustic environment:` clause stays part of that same timed beat, so nothing has to be guessed around; the style echo lives on the `GLOBAL::` line and is out of scope here. |
| `LTXV-D042` | error | An unqualified collective noun ("neighbours", "kids", "adults", "crowd") on a channel that declares anthropomorphic characters. A bare collective renders as photoreal humans — a hard-safety-floor violation. Only fires when `anthropomorphic_channel` is set. |
| `LTXV-D043` | error | An idiom or abstract verb LTX reads literally — "catches her eye", "withdraws", "holds there", "breaks into a smile". Curated list; **grows only by escalation from a real render failure**, never speculatively. |
| `LTXV-D044` | warning | Duration filler with no filmable content ("a long beat", "for a while" as an entire clause). A connective paired with a real action is fine and expected. |

## Multi-shot

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D050` | error | Cut language in a clip declared single-take. i2v defaults to one continuous take; an unmarked cut is either a mistake or an undeclared multi-shot. |
| `LTXV-D051` | error | A declared cut whose count disagrees with the prose, or which never states whether music, dialogue and ambience continue across it. |

## Unquoted speech risk

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D052` | error | A speech verb (`says`/`asks`/`answers`/`replies`/`announces`/`whispers`/`shouts`/`exclaims`/`states`/`remarks`/`calls out`) sitting in a `GLOBAL::` or `BEAT::` segment with **no quoted line anywhere in that same segment**. Found live 2026-10-29 (clover-and-paws EP001 SC13, then SC09/SC02): a `BEAT::` written as narrative shorthand — "Pip tips his head back and says Bruno always says Paw Street looks after its own" — is never meant as literal dialogue, but every render passes through `app-vidgen-dist`'s `compile_relay_style_prompt()`, which flattens `GLOBAL::`/`BEAT::` into plain chronological prose (LTX-2.5's Gemma encoder has no native concept of those markers). Once flattened, the unquoted clause reads to the model as an actual line — it gets vocalized, then the real quoted dialogue repeats it moments later, wasting a full GPU render. `tells?`/`told` is deliberately excluded: "the way he was told" is a common, safe past-tense idiom, not a live speech assertion, and was the one false positive found validating this rule against a real 29-clip episode. Fix: rewrite the segment as physical/atmospheric description only, no speech verb — never reword the real quoted line to compensate. |
| `LTXV-D053` | error | A numeric camera-motion spec — a bare degree figure (`45 degrees`, `45°`) or a rate (`2°/sec`, `2 fps`, `per second`) — anywhere in the prose. LTX-2.5 has no numeric camera control; a measured angle or rate reads as a literal on-screen token, not a motion instruction. Adopted 2026-10-29 from the `ltx-2-5-prompter` reference skill's pitfall list — the one gap in its 11 pitfalls this pipeline didn't already cover on its own. No prior instance in this pipeline; cross-checked against the full clover-and-paws EP001 episode (zero hits) before enabling. |
| `LTXV-D054` | error | A ground/terrain word (`grass`/`lawn`/`meadow`/`gravel`/`sand`/`pavement`/`sidewalk`/`asphalt`) in a clip's prose that doesn't appear in the locked description of any environment/prop plate the clip is tagged with. Requires the optional `_context/environment-locks.json` sidecar (04c) — an episode without one skips this rule rather than failing. Caught live 2026-10-29 (clover-and-paws EP001 SC06/SC14): both inherited "grass" from the original script (03a/03b), written before the environment was visually locked at 04c to a bare wooden porch deck; nothing before this rule cross-checked a clip's incidental scene-setting words against the plate that got locked *after* the script. `dirt` is deliberately excluded — it's legitimately ambiguous here (a wardrobe stain, not always a ground claim) and was the one plausible false positive found scoping the rule. Proven against the exact original bug text (fires) and its fix (clears) before being enabled. |

## Still-grounding regression

D054 catches a prose claim contradicted by the *locked world* (the environment plate). This
group catches a different failure: a prose claim contradicted by the *actual approved pixel*
of a specific clip's still, after a real deviation between the still-prompt's ask and the
rendered still was already found and hand-corrected once (identity/wardrobe/pose drift a
generation model introduces even from a correct prompt — glasses rendering on-face instead of
on-chain, a pose settling further than asked). No amount of static text-checking against the
locked world can catch this class; it can only be caught by looking at the pixel, which the
04f2/04f3 still-gate review already does once, by hand, per clip. This rule doesn't replace
that look — it just stops a later prompt rebuild from silently losing what it found.

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D055` | error | A clip's prose matches the `contradicting_pattern` of a fact recorded in the optional `_context/frame0-still-facts.json` sidecar — i.e. it has reverted to a phrasing that a confirmed real observation of the *approved* still already overrode. Each fact is hand-recorded, one at a time, only after a real still-vs-prompt deviation was directly confirmed against the rendered pixel (never guessed): e.g. clover-and-paws EP001 SC02/SC09, where Bruno's glasses render worn on his face rather than on the locked chain, and SC28, where the still shows him fully settled rather than the "perched forward" the still-prompt asked for. The 04f3 builder already sources these corrected clauses by hand (`build_clover_04f.py`'s `BRUNO_CUE_ON_FACE` and `STILL_STATES["SC28"]` overrides); this rule turns "a reopen/rebuild silently drops one of those overrides" from a defect only caught by re-eyeballing every pixel again into a hard validator failure. An episode with no sidecar, or a clip with no fact records, skips silently — this is a regression guard on a finding already made, not a substitute for the still-gate review itself. Added 2026-10-29, proven against both known facts: fires when the recorded override is reverted, clears on the real current text. |

## Within-clip prop-state continuity

Unlike D054/D055 (prose vs. the locked world / the approved pixel), this rule catches a
contradiction entirely internal to one clip's own beat sequence — no sidecar, no still, just
`blocking.json`'s own `props[]` list and the clip's own `BEAT::` text.

| ID | Tier | Catches |
|---|---|---|
| `LTXV-D056` | error | A prop from `blocking.json`'s `props[]` is already described as set at rest in an earlier `BEAT::`, then reappears "in his/her paws" in a *later* `BEAT::` of the same clip with no pickup verb (`picks up`/`reaches for`/`retrieves`/`lifts`/`grabs`) between the two. Caught live 2026-10-29 (clover-and-paws EP001 SC06): the opening beat had Fin "set the wrench down"; his speaking beat two lines later re-described it as "in his paws" and had him "set the wrench down" a second time — an invisible re-grab the model had to invent between beats. On the actual render it filled that gap by having Fin hold the *flashlight* instead (a nearby prop the owner had separately removed from the still, unrelated to this bug) — a vivid demonstration that an unresolved state contradiction in the prose becomes visible, unpredictable prop confusion on screen, not a harmless no-op. Fix: write the later beat from the object's *current* rested state, never re-copy an earlier draft's holding language; if the object genuinely gets picked back up, say so explicitly and the rule clears. A clip with no `blocking.json` props (or none for this clip) skips silently. Added 2026-10-29, proven against the exact original SC06 bug text: fires on the unfixed beat, clears on the corrected one and on an explicit-pickup rewrite. |

## State and continuity

These take structured input, not just prose: the clip's **frame-0 requirement block** from
`04f`, `_context/blocking.json` from `04d`, and the still prompt from `04f2`.

`LTXV-S002` and `LTXV-S006` are the two halves of the same guarantee — that a clip and its still
agree about what exists in frame. Run both; either alone leaves the other direction unchecked.

| ID | Tier | Catches |
|---|---|---|
| `LTXV-S001` | error | An incomplete frame-0 requirement block — a missing field, a character state missing `pos`/`facing`/`gaze`/`pose`/`expression`/`mouth`/`hands`, an unstated mouth state, or `first_action_performable` not asserted true. |
| `LTXV-S002` | error | An object the action touches with no frame-0 resting state, or declared touched but never named in the clip prose. **i2v never invents objects** — this is the rule the whole `04f` → `04f2` ordering exists to enforce. |
| `LTXV-S003` | error | The clip's cast disagrees with `blocking.json`. |
| `LTXV-S004` | error | A continuing entity whose opening `pos`/`pose`/`hands` conflicts with the previous clip's `end_state`, or which declares continuity from a clip that is not its immediate predecessor. |
| `LTXV-S005` | error | The still already shows the completed end state while the clip performs the transition into it — door already open + knocks; lamp lit + strikes a match; seated + sits down; broken + breaks; held + picks up; placed + places. **High precision by design:** a *closed* door plus opens-in-clip is a legal start-state transition and passes. |
| `LTXV-S006` | error | The **still prompt** is bound to the wrong clip, has no `## SC<NN>` header at all, omits an object its clip's action touches, omits a character from the clip's frame-0 state, or bakes a motion verb into what must be a settled state. `LTXV-S002` checks the clip prose against its own requirement block; this is the other half. Without it a still can be authored against the wrong clip, or omit something the clip reaches for, and nothing catches it until a render has been spent. The `## SC<NN> | pose:` header line and `[[TAG]]` tokens are stripped before the prose checks — a character present only as a reference tag binds identity but stages nothing, which is exactly the defect worth catching. |

---

## Enforcement

Stage `04f3` runs the validator over every clip and writes
`_context/ltx-prompt-review.json` (schema `schemas/ltx-prompt-review.schema.json`) recording which
rule IDs were checked and their pass/warn/fail status. **A clip with any error does not
advance.** `04g` refuses to build a render package from a review file containing a FAIL.

## Adding a rule

A new rule is added only when a **real render failure** or a **real vendor statement**
justifies it — never on speculation. Add it in this order:

1. Write the finding into `LTX_I2V_CONTRACT.md` with its evidence grade **[A]/[B]/[C]**.
2. Add the ID to this catalog with what it catches and why.
3. Add it to `IMPLEMENTED_RULE_IDS` and implement it.
4. Add a test to `tests/test_ltx_prompt_validator.py` that fails without the implementation —
   both a positive case (it fires on the defect) and, where the rule is at all fuzzy, a
   negative case (it does *not* fire on the legitimate near-miss).

Step 4 is not optional. `LTXV-D024` and `LTXV-D041` both shipped with false positives on
ordinary prose that only the negative test cases exposed.
