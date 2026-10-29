# Character Prompt Compilation Standard — Clover & Bruno Stories
**Status**: LOCKED FINAL 2026-10-29
**Channel**: Clover & Bruno Stories @cloverandbruno
**Replaces**: previous prototype painterly graphic-novel anchor — ABANDONED

## 1. Photoreal cozy family style anchor — LOCKED

Copy this style anchor verbatim into every master portrait, full-body, sheet and episode character-reference prompt:

```
Photoreal anthropomorphic cozy family, ultra realistic fur, natural cat and dog anatomy with human-like posture, warm daylight, soft natural skin-fur texture, readable gentle eyes, consistent face geometry, warm cream #FFF6E3 and soft wood #D8B589 lighting, shallow depth of field, not cartoon, not painterly graphic-novel, not dark navy tribunal.
```

Old anchor abandoned: Cinematic painterly graphic-novel realism with ink-navy and aged-brass is ABANDONED for this channel.

## 2. Master-card authority

Individual character prompts live in characters/CAST-XXX_*.md. This file defines only how those prompts are compiled and used.

For selected master performer, copy verbatim:

- structural facial anchors: muzzle shape, ear shape, eye size/placement, fur color/pattern, tail
- master portrait prompt with wardrobe signature (Clover soft orange onesie, Bruno burnt-orange cardigan + glasses-on-a-chain + gray fur 70y, Rosa warm apron, Fin blue shirt, Pip puppy bandana)
- voice lock: Clover soft polite kitten, Bruno old raspy grumpy 70y retired
- core personality lock: Clover always polite gentle, Bruno arrogant outside soft inside never says yes first time
- reference asset paths and approved hashes

Append episode role overlays only after locked master content.

## 3. Muse Image / Photoreal reference sequence — LOCKED

1. Generate and approve neutral portrait from master portrait prompt with style anchor above.
2. Use approved portrait as image 1 for full-body prompt (same fur, same wardrobe signature).
3. Use portrait image 1 and full-body image 2 for six-panel character sheet: front, three-quarter, profile, composed sitting, action holding object, full figure.
4. Add labels and readable text in post; generated sheets use clean unmarked panels, no text.
5. Record all selected files in asset manifest with hashes.
6. Unified engine: the same photoreal engine for all 7 characters. The old per-character split is ABANDONED.

Muse Image prompts use positive descriptions. Describe clean text-free background, natural paws, unobstructed eyes, unbranded wardrobe, warm home/porch.

## 4. Episode role-overlay block — cat & dog family

Append this filled block to master prompt:

```
EPISODE ROLE OVERLAY
Story character name: [[NAME - must stay Clover/Bruno/etc]]
Type: [[A Duo 70% / B Clover Only 15% / C Bruno Only 15%]]
Lead: [[Clover or Bruno]]
Co-appearance check: [[Clover+Rosa+Fin / Bruno+Pip]]
Occupation/function: [[e.g., polite kitten asking help / 70y retired dog on porch]]
Relationship moment: [[e.g., Clover asks Bruno to fix bike]]
Wardrobe variation: [[must stay inside signature colors - orange onesie / burnt-orange cardigan + glasses-on-a-chain]]
Current condition: [[e.g., slightly dusty, tired, holding shopping bag]]
Public mask: [[Clover polite / Bruno arrogant grumpy]]
Private soft desire: [[Bruno wants to help but pride]]
Physical tell: [[Bruno arms crossed on No, sigh + uncross on soft yes / Clover tilts head soft eyes]]
The performer retains exact master face, fur, body frame, playing age, tail, wardrobe signature and voice.
Bruno never says yes on first attempt - first line must be No with attitude.
Clover always polite even after No.
```

## 5. Clip prompt contract

There is no sectioned prompt format. A clip prompt is one continuous chronological paragraph of
prose, with no subject labels and no timing syntax. Identity is not carried by the clip prompt
at all: it is carried by the approved frame-0 still, which was itself generated against that
performer's locked reference sheet in `characters/reference_sheets/`.

The binding authority is `pipeline/LTX_I2V_CONTRACT.md`. What this channel adds on top of it,
and must appear in every clip that carries them:

- the chore or errand the scene is actually about, visible as prop business;
- Clover's polite register, and Bruno's first answer as No with attitude before any soft yes;
- the sound bed named for this world — tap drip, porch creak, bag rustle, birdsong — in the
  `Acoustic environment:` sentence, never a bare "room tone";
- warm acoustic guitar or soft piano only, and only where a wish, a soft yes or a payoff lands.

## 5a. Character anchor compiler — cat & dog

Compile a speaking character's clip-prompt anchor short, because the still already carries face,
fur, build and wardrobe:

```
[[FIRST NAME]], [[ONE SHORT IDENTIFYING PHRASE]], [[CURRENT WARDROBE]]
```

Never paste a full identity string into a clip prompt — a full re-description competes with the
conditioning frame instead of reinforcing it. The traits below stay in the STILL prompt and in
the blocking spec, which is where they belong.

## 6. Subject-definition compiler — cat & dog

Compile speaking character as:

```
<Subject 1> (S1) is story character Clover, performed by CAST-001 version 2.0.0 and defined by approved portrait, full-body and character-sheet references. Preserve exactly: polite young kitten, soft orange onesie, big gentle eyes, cream and wood lighting. In this episode, <Subject 1> wears [[WARDROBE variation orange onesie]] and performs with [[CURRENT CONDITION]] while asking Bruno politely.
```

Bruno example:

```
<Subject 2> (S2) is story character Bruno, performed by CAST-004 version 2.0.0 and defined by approved portrait, full-body and sheet references. Preserve exactly: 70-year-old retired dog, graying fur, burnt-orange cardigan, tortoiseshell reading glasses on a bronze chain resting at his chest, grumpy arrogant outside soft inside, never says yes first time. In this episode, <Subject 2> wears the burnt-orange cardigan and glasses-on-a-chain and performs with arms crossed on first No, sigh + soft eyes on reluctant yes.
```

If voice reference exists:

```
<Audio 1> is voice-timbre reference for <Subject 1> (S1), preserving soft polite kitten voice without copying unrelated dialogue.
<Audio 2> is voice-timbre reference for <Subject 2> (S2), preserving old raspy grumpy 70y retired dog voice, slow, slight scoff on No.
```

## 7. Retention-analysis compiler

```
<Subject 1> (appears in Shot 1, Shot 2): fully_preserved - approved master face, fur pattern, playing age, orange onesie, body frame remain consistent while expression changes (polite request, gentle disappointment, thank you).
<Subject 2> (appears in Shot 1, Shot 2): fully_preserved - approved master face 70y gray fur, burnt-orange cardigan and glasses-on-a-chain, body frame remain consistent while expression changes from grumpy No (arms crossed) to soft reluctant yes (sigh, uncross, soft eyes).
<Audio 1>: reference - target performance follows approved soft polite kitten timbre.
<Audio 2>: reference - target performance follows approved old raspy grumpy timbre, first line No with attitude, second line reluctant soft yes.
```

## 8. Speaking-character rules — LOCKED for polite vs grumpy

- Speaking referenced character written <Subject N> (Sx)
- Dialogue written inside <d>[English] ...</d>
- Reuse same (Sx) for speaker through clip
- Do not assign speaker ID to silent reaction (e.g., Pip listening, Rosa background)
- Do not place dialogue inside overall_soundscape or non_diegetic_music
- Split lines that cannot be performed naturally inside shot duration
- Bruno first line in any episode where he appears must be No with attitude / scoff / complaint
- Bruno second line must be sigh + reluctant soft yes + action helping
- Clover lines always polite: "Please...", "Thank you...", "Okay..."
- Pip is loyal to Bruno; his position in any given episode is a story choice

## 9. Reference limits — cat & dog

- Use smallest reference set that preserves identity and shot
- Maximum configured reference images: 9
- Preferred character references per ordinary dialogue shot: portrait or sheet + one wardrobe/full-body
- Maximum characters in frame: Shorts 2-3 (even Duo), Longs up to 6
- Preferred speaking cast per episode: Shorts 2-3, Longs 3-4; configured maximum: Shorts 3, Longs 6
- Always include wardrobe signature reference to prevent drift: Clover orange onesie, Bruno burnt-orange cardigan + glasses-on-a-chain

## 10. Validation — cat & dog

- [ ] Cast ID and version exist in CAST.md 2.0.0 (Clover & Bruno)
- [ ] Episode selection file pins source-card hash + Type (A/B/C) + Lead (Clover/Bruno) + co-appearance check
- [ ] Structural anchors copied verbatim and in order (fur, muzzle, ears, eyes)
- [ ] Story name and role overlay clearly separated from master identity
- [ ] Character and voice reference labels stable
- [ ] Episode wardrobe stays inside signature colors (orange onesie / burnt-orange cardigan + glasses-on-a-chain)
- [ ] Face, fur, playing age, tail, body frame, voice have not drifted
- [ ] Bruno never-yes-first checked: first line No, second line reluctant yes
- [ ] Clover always-polite checked
- [ ] Master asset text and logos clean and unbranded, warm cozy lighting
