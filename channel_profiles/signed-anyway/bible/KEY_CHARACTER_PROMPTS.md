# Character Prompt Compilation Standard

## 1. Painterly graphic-novel style anchor

Copy this style anchor verbatim into every master portrait, full-body, sheet and episode character-reference prompt:

```text
Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry.
```

## 2. Master-card authority

Individual character prompts live in `characters/CAST-XXX_*.md`. This file defines only how those prompts are compiled and used.

For a selected master performer, copy verbatim:

- structural facial anchors;
- master portrait prompt;
- voice lock;
- reference-sheet identity clause;
- reference asset paths and approved hashes.

Append episode role overlays only after the locked master content.

## 3. FLUX reference sequence

1. Generate and approve the neutral portrait from the master portrait prompt.
2. Use that approved portrait as image 1 for the full-body prompt.
3. Use portrait image 1 and full-body image 2 for the six-panel character sheet.
4. Add labels and readable text in post; generated sheets use clean unmarked panels.
5. Record all selected files in the asset manifest.

FLUX prompts use positive descriptions. Describe a clean text-free background, natural hands, unobstructed eyes and unbranded wardrobe instead of a negative-prompt list.

## 4. Episode role-overlay block

Append this filled block to the master prompt:

```text
EPISODE ROLE OVERLAY
Story character name: [[NAME]]
Occupation/function: [[ROLE]]
Relationship: [[RELATIONSHIP]]
Wardrobe variation: [[WARDROBE]]
Current condition: [[CONDITION]]
Public mask: [[MASK]]
Pressure tell: [[TELL]]
The performer retains the exact master face, body frame, playing age, hair identity and voice.
```

## 5. Clip prompt contract

There is no sectioned prompt format. A clip prompt is one continuous
chronological paragraph of prose, with no subject labels and no timing syntax.

Identity is not carried by the clip prompt at all: it is carried by the
approved frame-0 still, which was itself generated against this character's
locked reference sheet. The clip prompt names the character by first name plus
a short anchor and moves forward from that frame.

The binding authority is `pipeline/LTX_I2V_CONTRACT.md`.

## 6. Character anchor compiler

Compile a speaking character's clip-prompt anchor as:

```text
[[FIRST NAME]], [[ONE SHORT IDENTIFYING PHRASE]], [[CURRENT WARDROBE]]
```

Short, deliberately. The still already carries face, build, playing age and
wardrobe. Never paste the full identity string into a clip prompt - a full
re-description competes with the conditioning frame instead of reinforcing it.

The voice signature is stated **inline on the character's first spoken line
only**, verbatim from the master card, and never repeated afterwards:

```text
in a [[VERBATIM VOICE LOCK]] voice: "[[LINE]]"
```

If a voice reference exists:

```text
<Audio 1> is the voice-timbre reference for <Subject 1> (S1), preserving [[VERBATIM VOICE LOCK]] without copying unrelated source dialogue.
```

## 7. Retention-analysis compiler

```text
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - the approved master face, playing age, hair identity, body frame and episode wardrobe remain consistent while expression and posture change according to the scene.
<Audio 1>: reference - the target performance follows the approved timbre, cadence and accent baseline without copying the original signal.
```

## 8. Speaking-character rules

- A speaking referenced character is written `<Subject N> (Sx)`.
- Dialogue is written inside `<d>[English] ...</d>`.
- Reuse the same `(Sx)` for that speaker through the clip.
- Do not assign a speaker ID to a silent reaction.
- Do not place dialogue inside `overall_soundscape` or `non_diegetic_music`.
- Split lines that cannot be performed naturally inside the shot duration.

## 9. Reference limits

- Use the smallest reference set that clearly preserves identity and the shot.
- Maximum configured reference images: nine.
- Preferred character references per ordinary dialogue shot: portrait or sheet plus one wardrobe/full-body reference.
- Maximum characters in frame: two.
- Preferred speaking cast per episode: three to four; configured maximum: five.

## 10. Validation

- [ ] Cast ID and version exist in `CAST.md`.
- [ ] Episode selection file pins the source-card hash.
- [ ] Structural anchors are copied verbatim and in order.
- [ ] Story name and role overlay are clearly separated from master identity.
- [ ] Character and voice reference labels remain stable.
- [ ] Episode wardrobe stays inside the master role boundaries.
- [ ] Face, hair, playing age, body frame and voice have not drifted.
- [ ] Master asset text and logos are clean and unbranded.
