# Character System and Identity Contract — Clover & Bruno Stories
**Status**: LOCKED FINAL 2026-10-29
**Channel**: Clover & Bruno Stories @cloverandbruno
**Replaces**: previous financial drama prototype 10 human performer bible — ABANDONED

## 1. Architecture

Clover & Bruno uses a repertory animal cast: 2 core anchors (Clover + Bruno) + 3 family anchors (Rosa, Fin, Pip) + 2 street recurring (Mimi, Tico). All photoreal anthropomorphic, same visual engine.

Sources of truth:

| Source | Authority |
|---|---|
| `CAST.md` | Registry, co-appearance DEFAULTS (Clover usually with a parent, Bruno usually with Pip), 70/15/15, pairing matrix |
| `characters/CAST-XXX_*.md` | Immutable performer identity, fur, face, body, voice, age, wardrobe lock |
| Episode `story/characters.md` | Selected cast for this episode, lead declaration (Clover or Bruno), story objective |
| Episode `visual/character-assets.json` | Hash-bound local reference snapshot |
| `KEY_CHARACTER_PROMPTS.md` | Muse Image prompt syntax and compilation |

## 2. What is globally locked

For every master cast member, preserve verbatim:

- cast ID and master-card version
- species, breed hint, fur color/pattern, eye color
- structural facial anchors: muzzle shape, ear shape, eye size/placement
- playing age band: Clover 6y kitten / Bruno 70y retired dog
- body frame, height impression, tail, paws
- voice timbre: Clover soft polite kitten, Bruno old raspy grumpy 70y
- wardrobe signature: Clover soft orange onesie, Rosa warm apron, Fin blue shirt, Bruno burnt-orange cardigan + glasses-on-a-chain, Pip puppy bandana
- identity portrait; full-body and six-panel sheet are optional additions (see §7)
- core personality: Clover polite gentle, Bruno arrogant outside soft inside never says yes first time

## 3. What an episode may change

- story objective, wish, chore, money problem
- relationship momentary tension (Clover asks, Bruno says no)
- wardrobe variant inside approved range (same colors, different task outfit)
- temporary condition: tired, dusty from chores, slightly wet
- scene blocking, expression intensity, posture
- location: kitchen, porch, street, shop, park — story-defined

An episode must state each change as overlay. Silence = master default.

## 4. Anchor exception — LOCKED

- CAST-001 Clover remains Clover, polite young kitten lead. Never arrogant, never rude. Always appears with at least one parent (Rosa or Fin), ideally both.
- CAST-004 Bruno remains Bruno, 70y retired dog, arrogant attitude outside, soft gentle inside. Core gag locked: **never says yes in one attempt**. First line always No with scoff/complaint, second line reluctant soft yes + helps anyway.
- Anchors are never recast into other species or age.

## 5. Repertory boundaries

- one role per performer per episode
- Clover never solo without parents
- Bruno usually with Pip — a default, not a quota
- no more than 3 characters on screen in Shorts, even Duo episodes
- no more than 6 in Long-form
- no age transformation beyond master range (Bruno must stay 70y old look)
- no changing species as costume
- no reuse of signature prop as if it belonged globally (e.g., Clover's bike belongs to Clover only)

## 6. Episode-local creation rule

Create new performer when:

- story needs animal not in 7 (e.g., parrot, vet) and none of 7 fits
- all suitable performers violate max character count
- using familiar face would break Clover-always-with-parents or Bruno-never-yes-first
- character likely to recur needs stable identity

New performers are episode-local by default. Promotion requires complete card, approved assets, version, owner sign-off.

## 7. Reference-pack standard — LOCKED for photoreal unified engine

Each master performer requires one canonical reference image (item 1). Items 2
and 3 are optional additions a performer may accumulate over time; per
`pipeline/stages/04b-characters.md`, one canonical reference image already
satisfies 04b — a six-panel/four-panel turnaround pack is not required, and
its absence is not a gap:

1. neutral head-and-shoulders identity portrait — photoreal anthropomorphic (required)
2. full-body neutral wardrobe reference — same lighting (optional)
3. six-panel sheet: front, three-quarter, profile, composed sitting, action (holding object), full figure (optional)
4. voice reference 3-5 sec: Clover polite "Please, thank you", Bruno grumpy "No... sigh fine"
5. asset manifest with paths, dimensions, hashes, approval status

Old per-character engine split is abandoned. **Locked: LTX-2.5 image-to-video is the single unified engine for all 7 performers** — the split is gone; Clover, Rosa, Fin, Bruno, Pip, Mimi and Tico all render through the same path, from an approved frame-0 still generated against that performer's locked reference sheet.

## 8. Episode selection snapshot

Episode `story/characters.md` references master ID + version + lead declaration. Before generation, selected master cards and approved assets are copied into episode reference package and hash-bound. This preserves reproducibility.

Snapshot is verbatim. Episode overlays live beside it and never edit snapshot.

## 9. Dramatic character requirements — LOCKED for cozy family

Every episode character must receive:

1. visible objective (Clover wants bike fixed, Bruno wants quiet porch)
2. private soft desire (Bruno wants to help but pride)
3. point of no return (Bruno said no first, now must follow through)
4. strongest polite/grumpy defense (Clover "I understand", Bruno "I'm retired, not your repairman")
5. contradiction (Bruno helps anyway)
6. human cost or kindness (small chore done, thank you)
7. public mask (Bruno arrogant)
8. physical tell (Bruno sigh, crosses arms; Clover tilts head, soft eyes)

## 10. Generation prohibitions

- No human celebrity likeness.
- No blending two master faces into new identity (no Clover+Bruno hybrid).
- No silent change to stable anchors (Clover must stay polite, Bruno must stay 70y).
- No generated paragraphs on documents that should be unreadable.
- No identity correction by face replacement when clean rerender possible.
- No master asset approved until it passes front, three-quarter, profile, and mobile-size face checks + voice check for Bruno's never-yes-first line.
- No real animal abuse or scary lighting.
