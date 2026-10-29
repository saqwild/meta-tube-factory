# Muse Image Frame-0 Still Contract

The binding authority for **frame-0 still generation** — the one image each LTX-2.5 clip is
conditioned on. Stage `04f2` obeys this file.

There are two different image jobs in this pipeline and they must not be confused:

| | **reference sheets** (`04b`/`04c`) | **frame-0 stills** (`04f2`) |
|---|---|---|
| purpose | lock a character's / place's identity | be the literal first frame of a clip |
| count | a handful per episode, reused | **one per clip** — this is the "x images" |
| reused across episodes | yes, promoted on second use | no, episode-local |
| feeds | Muse Image `--ref-asset` identity lock | LTX's i2v conditioning input |
| may show motion | n/a (turnarounds, plates) | **never** — a settled state only |

A reference sheet is a *persistent guide*. A frame-0 still is *the contract*. Generating one
when you needed the other is the most expensive mistake available at this stage.

---

## 0. Authority hierarchy (highest wins on conflict)

1. **This file + [`LTX_I2V_CONTRACT.md`](LTX_I2V_CONTRACT.md)** — the i2v / frame-0 / hard-safety
   discipline a generic image guide cannot know.
2. **The channel's own visual-style contract** in its reference bible — palette, lighting,
   photoreal-vs-stylised. Muse Image default aesthetic never overrides a channel's locked style.
3. **Google's official Muse Image prompting guide** — the model's own rules.
4. **The `muse-image` / `muse-image` skills** — technique only, never authority.

**Philosophy: layered risk reduction, not automated correctness.** No image model fills every
gap. Every safeguard shaves risk; a **human or vision gate holds the final call**, and the
model's own judgement of its own output is a filter, never the last word.

---

## 1. The still is derived from the clip prompt, not the other way round

This is the inversion that makes the pipeline work, and it is the reason `04f` (clip prompt
draft) runs **before** `04f2` (stills).

> **Every prop the clip's action touches must already exist in the still. i2v never invents
> objects.**

So stage `04f` emits, per clip, a **frame-0 requirement block** — and this stage's prompt is a
projection of that block, not a fresh creative act:

```
clip:            SC07
touched_objects: [ the mud-caked trowel, the overturned watering can, the garden fence ]
characters:      [ BRUNO, PIP ]
frame0_state:
  BRUNO: pos=LEFT  facing=camera-left-three-quarter  gaze=at Pip
         pose=standing at the fence, one paw resting on the post
         expression=guarded  mouth=closed  hands=empty
  PIP:   pos=RIGHT facing=camera  gaze=up at Bruno
         pose=seated in the mud beside the overturned watering can
         expression=hopeful  mouth=closed  hands=empty
props_at_rest:
  the mud-caked trowel: lying flat in the garden bed, blade half-buried
  the overturned watering can: on its side, spout pointing camera-right
first_action_performable_from_this_frame: yes — Bruno reaches for the trowel
end_state_of_previous_clip: matches (SC06 end_state)
```

Every field traces to `_context/blocking.json` (stage `04d`). **This stage does not decide
position, facing, gaze, pose, expression or prop state** — it projects them into prose. If a
blocking entry looks wrong once you are staring at the actual staging, **flag it back to
`04d`**; never silently override it in the prompt.

---

## 2. Prompt anatomy — Google's structure, i2v-constrained

Google's formula is **Subject + Action + Location/Context + Composition + Style**. Adopt it
with one hard override:

> **"Action" becomes the settled FRAME-0 STATE, never mid-motion.** Anything the clip must
> *perform* is written as a state the still already shows.

Three structured paragraphs, plus a lock sentence:

**0. Cast-count lock — before anything else.**
"The complete visible cast contains exactly N anthropomorphic characters: <names>." N and the
names come straight from the blocking entry's visible characters. A cheap, direct guard
against an invented background character.

**1. Setting.** `<shot type>` first, then the **full environment string verbatim**. Muse Image is
stateless between calls — it does not remember a prior scene's environment, so copy the whole
locked string every single time. Never write "the same locked kitchen as before". Props appear
at their exact resting state, and each prop's permanent identifying detail is restated
**verbatim, the same wording every scene**, so it reads as the same object each time.

**2. Characters.** Short anchor per character + **On the LEFT / On the RIGHT** (caps) for 2+
characters + pose-with-purpose + gaze + `expression` as its own explicit field, all projected
from blocking. Only characters marked visible are drawn. State each character's **frame-0
mouth state explicitly — every character, not just the speaker** ("mouth closed and relaxed at
frame zero"). An already-mid-word mouth is legal only for a deliberate cold-open/reveal peak
and must be stated as a deliberate exception.

**3. Composition + mood + style.** Light direction, depth of field, and a **rich mood line** —
then the style token, and a positive anatomy reinforcement line.

---

## 3. What flips on Muse Image versus a FLUX-era still prompt

| rule | on Muse Image |
|---|---|
| frame-0 = state not transition; props at rest; hands empty; name the first/last subject; one pose per character | **INHERIT — model-agnostic.** These are the i2v contract, not a FLUX quirk. |
| positive framing, no negation | **INHERIT — Google confirms** ("empty street", not "no cars"). |
| **"empty \<place\>"** | **RECOMMENDED affirmative**, not a risk. The old caution was CLIP-specific; Meta example uses it. |
| materiality with specifics | **INHERIT** — "denim overalls with rolled cuffs", never "overalls"; "navy tweed", never "suit". |
| **mood / atmosphere / colour-grade / film-stock language** | **FLIPPED — allowed and encouraged.** Muse Image interprets emotional and aesthetic language into light and composition. FLUX banned this; Muse Image wants it. Write the mood line richly. |
| narrate, don't keyword-list | **INHERIT — Google confirms** ("a list of keywords won't cut it"). Full sentences. |
| separate negative-prompt node | **DOES NOT EXIST.** Muse Image has no negative channel at all. Every exclusion folds into affirmative description — which is also why the positive anatomy line is the *only* place a paw/hand-anatomy safeguard can live. |
| ownership labels ("Mrs. X's yard") | **DROP** — name the visible place ("a cottage front yard"). A model cannot render ownership; the proper noun is dead tokens at best and summons an unwanted extra character at worst. |
| multi-reference identity (up to 14 refs) | **NEW capability** — this is the identity lock, see §4. |
| semantic masking / inpaint edit | **NEW capability** — fix one detail without a full re-roll, see §6. |
| explicit "anthropomorphic animal" for any animal character or crowd | **INHERIT — non-negotiable.** A bare species word renders as a human. |

---

## 4. Identity — the `[[TAG]]` → reference-asset lock

Each `[[TAG]]` on the prompt's tag line resolves to a **named reference asset** — the sheet
produced at `04b`. The named asset **is** the identity lock; the prose carries only a short
anchor ("Bruno, the elderly bulldog-mastiff mix"), never the full identity string.

- **Exact-match naming.** `[[BRUNO]]` needs an asset named exactly `BRUNO`. Ambiguous matches
  **abort, never guess.**
- **Deliberately sheet-less tags** — one-off background figures (`[[CROWD]]`, `[[VILLAGER]]`)
  are described in prose only, always as explicit anthropomorphic animals. Check the episode's
  cast map before treating a missing asset as an error.
- **Derivatives condition on the existing locked reference**, never on a fresh text
  re-description. Muse Image identity lock across many generations is looser than a dedicated
  character workflow — re-deriving from a prior *image* is the only reliable anti-drift move.
- **Cast drift is a first-class QA check at every gate**, not an afterthought. It is the one
  failure this whole approach must not reintroduce.

---

## 5. The generate-N-select loop — never skip the final gate

1. **Author the structured spec** from the frame-0 requirement block (§1) — LEFT/RIGHT
   positions, contact, containment, placement, states. Machine-checkable, before prose.
2. **Generate N variants** (default 4) at 16:9.
3. **Binary-presence pass** — cast count, props present, colours, one-of-each. The model is
   strong here; trust it.
4. **FINAL GATE on the keep, before any clip render.** The *relational* details — which paw,
   gaze direction, physical contact, identity-versus-reference — are the contamination-prone
   zone, and a model's self-report on those is weak. Verify with the validated three-step
   method (**neutral dimensions → text-only judge → any-FALSE fails**) or a human glance.
   **Never show the vision model the claim you want confirmed** — it will fabricate an
   observation that matches any claim it can see.
   A false PASS costs a 20-second clip render plus everything downstream. A false FAIL costs
   one glance.
5. **Do not delete the other variants until the keep passes step 4.** They are the cheap
   fallback; auto-deleting on a contaminable verdict turns a subtly-wrong keep into a full
   re-roll.

The gate's last question is the important one: **"is the clip's first action performable from
this frozen instant?"** If not, the still is wrong — re-roll the still, do not reword the clip.

---

## 6. Edit, don't re-roll

When a still is right *except one thing* — a paw position, a gaze — use semantic masking /
inpaint: *"keep everything exactly the same except \<the one detail\>."* Near-misses become
one-edit fixes instead of four fresh generations.

**Honest gap, stated rather than papered over:** there is no precise-pose lever on any current
image model. Pose control is a *stack* — reference the pose, narrate the state clearly,
generate N, inpaint the near-miss. Each layer shaves risk; none removes it.

---

## Output naming — this matters mechanically

The render app matches each still to its clip by the **scene number that prefixes the filename
stem**. Name stills `SC01.png`, `SC02.png`, … — matching the clip id — so the match is
unambiguous (`SC07` → prefix `SC` + `07` → clip 7). A name without a recognised scene prefix
(`bruno_v2.png`) is skipped, and a second file for the same number (`SC07_v2.png` beside
`SC07.png`) makes that clip ambiguous — either way the clip does not render as intended.

---

## Forbidden

- Baked motion in a still — frame-0 is a settled state only.
- Any object the clip's action touches that is absent from the still.
- A bare species word for an animal character or crowd (renders as a human — safety floor).
- Shorthand for a previously "locked" environment — restate the full string every call.
- Ownership labels as scenery.
- Auto-deleting variants before the final gate passes.
- Showing a vision gate the claim it is meant to verify.
- Duration, aspect ratio, fps or resolution in the prompt text — set them at generation.
