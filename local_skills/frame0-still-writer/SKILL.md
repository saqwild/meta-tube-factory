---
name: frame0-still-writer
description: >
  The sole writer for stage 04f2. Turns each clip's frame-0 requirement block (from 04f) into
  one Muse Image image prompt — the literal first frame that clip is conditioned on.
  Frame-0 is a settled STATE, never mid-motion; every object the clip's action touches must
  appear in it. Drives the generate-N-select loop and the still gate.
scope: vidgen-ltx, both channels
authority: pipeline/MUSE_FRAME0_CONTRACT.md
---

# Frame-0 still writer (Muse Image)

## The job in one line

**The clip prompt already exists. Your job is to build the frame it starts from.**

This is the inversion that makes i2v work. You are not designing a shot — `04d` did that. You
are not deciding what happens — `04f` did that. You are rendering the single frozen instant
from which `04f`'s action is physically performable, containing every object that action
touches.

If you find yourself making a creative choice, you have lost the thread. Go and find the field
in `blocking.json` or the frame-0 requirement block that should have decided it.

## Read before writing

1. [`pipeline/MUSE_FRAME0_CONTRACT.md`](../../pipeline/MUSE_FRAME0_CONTRACT.md) — the binding
   rules for this stage.
2. [`pipeline/LTX_I2V_CONTRACT.md`](../../pipeline/LTX_I2V_CONTRACT.md) § *Frame-0 state rules*
   — why these constraints exist downstream.
3. `episodes/<slug>/<EPID>/_context/frame0-requirements.json` — **your input**, one block per clip,
   written by `04f`.
4. `_context/blocking.json` — the geometry authority the block projects from.
5. `visual/references/manifest.md` — which reference sheet each `[[TAG]]` resolves to.
6. The channel's visual-style contract in its reference bible — the locked style language, to
   be copied verbatim, not paraphrased.

## Two image jobs — do not confuse them

| | reference sheets (`04b`/`04c`) | **frame-0 stills (this stage)** |
|---|---|---|
| what it is | a persistent identity/place guide | the literal first frame of one clip |
| how many | a handful per episode | **one per clip** |
| shows motion | n/a | **never** — a settled state only |
| reused | across episodes, on promotion | never |

You consume reference sheets as `--ref-asset` identity locks. You produce frame-0 stills.

## Prompt anatomy — Google's structure, i2v-constrained

Google's formula is **Subject + Action + Location/Context + Composition + Style**, with one
hard override: **"Action" becomes the settled frame-0 STATE, never mid-motion.**

Write it as a lock sentence plus three narrated paragraphs. Full sentences throughout — Google
is explicit that a keyword list won't cut it.

**0 — Cast-count lock, before anything else.**
> The complete visible cast contains exactly 2 anthropomorphic characters: Bruno and Pip.

N and the names come straight from the block's `characters`. A cheap, direct guard against an
invented background figure.

**1 — Setting.** Shot type **first**, then the **full environment string verbatim**. Muse Image is
stateless between calls — it remembers nothing from the previous scene. Copy the whole locked
string every single time; never write "the same kitchen as before". Each prop appears at its
exact `props_at_rest` state, and each prop's permanent identifying detail is restated
**verbatim, the same wording in every scene it appears**, so it reads as the same object.

**2 — Characters.** Per character, projected from `frame0_state`:
- short anchor only ("Bruno, the elderly bulldog-mastiff mix") — never the full identity
  string, which the reference asset already carries;
- **On the LEFT / On the RIGHT** in caps for 2+ characters, from `pos`;
- pose-with-purpose from `pose`, gaze from `gaze`, facing from `facing`;
- **`expression` as its own explicit clause**, not folded into the pose;
- **mouth state stated explicitly for every character, not just the speaker** — "mouth closed
  and relaxed at frame zero" is the default. An already-mid-word mouth is legal only for a
  deliberate cold-open peak, and must be written as a stated exception;
- `hands` — an empty hand is stated as empty.

**3 — Composition, mood, style.** Light direction, depth of field, then a **rich mood line**
(see below), the channel's style token, and a positive anatomy reinforcement line.

## What flips versus a FLUX-era still prompt

**Mood, atmosphere and colour-grade language are now encouraged.** This is the single biggest
change. Muse Image interprets emotional and aesthetic language into light and composition — "a
tender, picture-book warmth, soft golden light and a cozy homey grade" is a feature here. FLUX
banned exactly this. Write the mood line richly.

**Muse Image has no negative channel at all.** Every exclusion folds into affirmative description.
"An empty garden, Bruno the only figure in frame" — never "no birds". Note that
"empty \<place\>" is the *recommended* affirmative on Muse Image, not a risk; Meta example
uses it. This is also why the **positive anatomy line is the only place a paw/hand-anatomy
safeguard can live** — there is no negative node to put it in.

**Materiality with specifics.** "Denim overalls with rolled cuffs", never "overalls". "Navy
tweed", never "suit".

**No ownership labels as scenery.** "A cottage front yard", never "Mrs. Bramblewood's yard".
A model cannot render ownership; the proper noun is dead tokens at best, and at worst it
summons the owner as an extra character.

**Explicit "anthropomorphic animal" for every animal character and every crowd.** A bare
species or collective word renders as a photoreal human. Non-negotiable on any channel with a
declared safety floor.

## Identity — `[[TAG]]` to reference asset

Line 1 of each block is the tag line. Each `[[TAG]]` resolves to a named reference asset from
`04b`, matched **exactly**. Ambiguous matches abort — never guess.

- The named asset **is** the identity lock. The prose carries a short anchor only.
- A derivative (new outfit, new pose) conditions on the **existing locked reference image**,
  never a fresh text re-description. Muse Image identity lock across many generations is looser
  than a dedicated character workflow; re-deriving from a prior image is the only reliable
  anti-drift move.
- Deliberately sheet-less tags — one-off background figures — are described in prose only, and
  always as explicit anthropomorphic animals. Check the cast map before treating a missing
  asset as an error.

**Cast drift is a first-class check at every gate.** It is the one failure this whole approach
must not reintroduce.

## Output format

`episodes/<slug>/<EPID>/prompts/6-image-prompts.md`, one block per clip:

```
## SC07 | pose: <one-line echo of the frame-0 pose from the requirement block>
[[BRUNO]] [[PIP]]
<the prompt: lock sentence + three paragraphs, ending with the style token>
```

The `pose:` note **echoes** the requirement block — this stage does not invent it.

**`SC07` is the clip id from `frame0-requirements.json` (`SC01`…`SC08`), and it must match.** A still authored
against the wrong clip conditions the wrong generation, and the batch renders successfully and
looks entirely plausible. `LTXV-S006` checks this binding, along with three things that follow
from it: every `touched_objects` entry appears in the prompt, every character in the clip's
`frame0_state` is actually described, and no motion verb has crept into a settled state.

Note that the header line and the `[[TAG]]` line are **packet metadata the image model never
sees**. They are stripped before those checks run — a character named only in the pose note or
only as a reference tag has been bound for identity but staged nowhere, which is precisely the
failure worth catching.

## Then build the agent packet — required, run last

```bash
python tools/image_agent_packet.py --channel <slug> --episode <EPID>
```

This writes `prompts/6-image-agent-packet.md`, pairing each clip's **verbatim** prompt with that
clip's own validation rules: the staging claims the prompt already makes turned into checks,
plus its `touched_objects` and the performable-first-action question.

Hand that one file to whoever generates the stills. They generate, self-check the *result*
against the embedded conditions, correct (inpaint one detail, or re-roll), finalise, and only
then move to the next clip. Regenerate the packet whenever a still prompt is amended — it is
derived, like any other derived artifact.

The sequencing is the whole point: without it, the first time anyone sees "here is exactly what
this image must show" is *after* a render has been spent.

### Filenames matter mechanically

Approved stills are named for their clip id — `SC01.png`, `SC02.png`, … The render app matches
each still to its clip by the **scene number that prefixes the filename stem** (`SC07` → clip
7); a name without that prefix (`bruno_v2.png`) is skipped, and a second file for the same
number makes the clip ambiguous. Rename before the still leaves this stage.

## The generate-N-select loop — never skip step 4

1. **Author the structured spec** from the frame-0 requirement block — LEFT/RIGHT, contact,
   containment, placement, states — before any prose.
2. **Generate N variants** (default 4) at 16:9.
3. **Binary-presence pass.** Cast count, props present, colours, one-of-each. The model is
   strong here; trust it.
4. **FINAL GATE on the keep, before any clip render.** The relational details — which paw,
   gaze direction, physical contact, identity-versus-reference — are the contamination-prone
   zone, and a model's self-report on those is weak.
5. **Do not delete the other variants until the keep passes step 4.**

### How to run the gate without contaminating it

**Never show the vision model the claim you want confirmed.** It will fabricate an observation
that matches any claim it can see. The validated three-step method:

1. Ask for **neutral dimensions** — "how many characters are in frame, where is each one's
   gaze directed, what is each character's left paw touching" — with no expected answer in the
   prompt.
2. Hand the **text answers only** to a separate judge alongside the checklist.
3. **Any FALSE fails.** No aggregate scoring, no "mostly right".

The gate's last question is the one that matters:

> **Is the clip's first action performable from this frozen instant?**

If not, the still is wrong. **Re-roll the still — do not reword the clip.** A false PASS costs
a 20-second clip render plus everything downstream; a false FAIL costs one glance.

## Edit, don't re-roll

When a still is right *except one thing* — a paw position, a gaze — use semantic masking:
*"keep everything exactly the same except \<the one detail\>."* Near-misses become one-edit
fixes instead of four fresh generations.

**Honest gap:** there is no precise-pose lever on any current image model. Pose control is a
stack — reference the pose, narrate the state clearly, generate N, inpaint the near-miss. Each
layer shaves risk; none removes it. Say so rather than promising precision the model cannot
deliver.

## Stage gate

Per clip, before it advances:

- `[[TAG]]` present and resolving for every visible character; short anchors only.
- Cast-count lock sentence present, N matching the requirement block.
- Full environment string restated verbatim; every prop at its declared resting state with its
  permanent detail verbatim.
- **Frame-0 STATE only — no motion verbs anywhere.** Hands stated empty where empty.
- Explicit mouth state for every character.
- `expression` present as its own clause per character.
- Affirmative throughout — no negation (Muse Image has no negative channel to catch it).
- Mood line present; style token appended; positive anatomy line present.
- No ownership labels; explicit "anthropomorphic animal" for any crowd.
- **Every `touched_objects` entry visible in the prompt.**
- The rendered still passes the gate above, including the performable-first-action question.

## Forbidden

- Baked motion in a still — frame-0 is a settled state only.
- Any object the clip's action touches that is absent from the still.
- Shorthand for a previously "locked" environment.
- Deciding position, facing, gaze, pose, expression or prop state yourself — flag it back to
  `04d` instead.
- Auto-deleting variants before the final gate passes.
- Showing a vision gate the claim it is meant to verify.
- Duration, aspect ratio, fps or resolution in the prompt text.
- Mixing this generator with any other image model inside one episode.
