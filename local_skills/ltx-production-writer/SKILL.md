---
name: ltx-production-writer
description: >
  The sole writer for stages 04f (clip prompt draft) and 04f3 (final). Compiles one LTX-2.5
  owner-locked PromptRelay-style beat prompt per clip from the blocking spec, plus the frame-0
  requirement block that stage 04f2 turns into that clip's still. One `GLOBAL::` continuation
  anchor plus `BEAT:: <frames> ::` lines totalling 481; no loose timing prose, no negation in
  the positive. The global `ltx25-prompting` skill runs after this one as a read-only
  conformance check and never drafts.
scope: vidgen-ltx, both channels
authority: pipeline/LTX_I2V_CONTRACT.md
---

# LTX-2.5 production writer

## Read before writing a single word

In this order, every time:

1. [`pipeline/LTX_I2V_CONTRACT.md`](../../pipeline/LTX_I2V_CONTRACT.md) — the binding rules.
2. The active stage contract (`04f-ltx-prompt-draft.md` or `04f3-ltx-prompt-final.md`).
3. `channel_profiles/<slug>/channel.json` → `render`, `format`, `cast`, `hard_safety_floor`.
   **Numbers come from here, never from this file and never from a sibling channel.**
4. `episodes/<slug>/<EPID>/_context/blocking.json` — the geometry authority.
5. `visual/shot-plan.md`, the approved storyboard, `visual/references/manifest.md`.
6. For `04f3` only: the **approved stills** from `04f2` and their gate verdicts.

You are not the geometry author. Position, facing, gaze, pose, expression, mouth state, prop
resting state, camera movement and end state were all decided at `04d` and live in
`blocking.json`. **Project them into prose. Do not re-decide them.** If an entry looks wrong
once you are staring at the actual staging, flag it back to `04d` — never silently override it
here.

## The two-pass shape, and why it exists

i2v has a circular dependency: the prompt must match the still's real pixels, but the still
must contain every object the prompt's action touches. Resolving it by guessing in either
direction produces the two classic failures — a prompt that contradicts the render, or a clip
that reaches for a prop the still never showed.

So authoring is split, and this skill runs twice:

**Pass 1 — `04f`, before any still exists.** Write the clip's *motion, performance, dialogue,
audio and camera* from `blocking.json`. Write the opening clause **provisionally** and mark it.
Emit the **frame-0 requirement block** — the complete list of what the still must contain for
this clip to be performable at all.

**Pass 2 — `04f3`, after the stills are approved.** Rewrite the opening clause to describe what
the still **actually shows**, from the real pixels and the still gate's verdict — never the
pre-still plan carried forward unedited. Everything downstream of the opening clause usually
survives unchanged; if it doesn't, the still is wrong and goes back to `04f2` rather than the
prose bending around it.

## The template

The owner-locked packet (`render.prompt_format == "prompt_relay_beats_v1"`) has labelled
pacing fields. Their frame labels are a model-facing convention, not graph-level clock
control; they must always total **481**.

```
GLOBAL:: Continue from the still. <full approved still: characters, wardrobe, fixed props,
          environment, light> <style echo, verbatim from render.style_echo>. Low motion.
BEAT:: 24 :: <first performable character action>. Ambient (slow, subtle): <two named visual motions>.
BEAT:: <frames> :: <speaker action + first-use voice signature + quoted line>. <non-speakers mouth-closed>
BEAT:: <frames> :: <next speaker action + quoted line>. <productive tail — a character stays in frame>
BEAT:: 120 :: <camera movement>. Acoustic environment: <room tone + named ambient life + own foley>;
              clear close dialogue front and center.
```

**Always open `GLOBAL:: Continue from the still.`** It is the locked continuity anchor — in
this packet it is required, not a meta-instruction. The `GLOBAL::` line carries the full
approved static scene and ends on the channel's style echo then `Low motion.`; each later beat
names only the controlled delta. Split dialogue across as many `BEAT::` lines as there are
turns; allocate the frames so speech beats are long and the opening/closing beats stay 24 /
120. The last beat is the productive tail and must name a character.

### Worked example

> GLOBAL:: Continue from the still. Bruno, the elderly bulldog-mastiff mix in his burnt-orange
> cardigan, stands at the garden fence with Pip, the ginger puppy in his red bandana, seated in
> the mud beside him. Warm late-afternoon light rests on the fence and overturned watering can.
> Photoreal anthropomorphic cozy family look, warm daylight, cream-and-soft-wood palette. Low motion.
> BEAT:: 24 :: Bruno's paw slides along the fence rail. Ambient (slow, subtle): sunlight shifts
> across the garden bed and the carrot tops sway faintly.
> BEAT:: 169 :: Bruno's paw tightens on the trowel handle and he grumbles, gruff but wavering,
> in a steady gravelly American English elder voice: "In my day, dogs didn't need rescuing."
> Pip watches quietly, mouth closed, ears drooping.
> BEAT:: 168 :: Bruno's ears droop and he mutters: "Oh, fine. Just for tonight." After speaking,
> Bruno's mouth closes naturally and he stays rooted at the fence, one paw resting on the post.
> BEAT:: 120 :: The camera begins a slow dolly in toward Bruno and Pip. Acoustic environment: a
> light warm garden room tone with faint birdsong and the scrape of Bruno's paw on the wooden rail;
> clear close dialogue front and center.

That example passes the validator clean (24 + 169 + 168 + 120 = 481). Use its *shape*, not its content.

## The frame-0 requirement block — the handoff to `04f2`

Emitted per clip alongside the prose. This is what makes the still derivable rather than
guessed, and it is validated by `LTXV-S001`/`S002`/`S003`.

```yaml
clip: SC07
touched_objects:            # EVERY object the action makes contact with. i2v never
  - the trowel              # invents objects — if it isn't here, it isn't in the still,
  - the watering can        # and the clip cannot touch it.
characters: [BRUNO, PIP]
frame0_state:
  BRUNO: {pos: left,  facing: camera-left three-quarter, gaze: at Pip,
          pose: standing at the fence, one paw on the post, expression: guarded,
          mouth: closed, hands: empty}
  PIP:   {pos: right, facing: camera, gaze: up at Bruno,
          pose: seated in the mud, expression: hopeful,
          mouth: closed, hands: empty}
props_at_rest:
  the trowel: lying flat in the garden bed, blade half-buried
  the watering can: on its side, spout pointing camera-right
first_action_performable: true      # assert this only after actually checking
continues_from: SC06                # null unless this clip is a true continuous
                                    # hand-off from the previous one (see NOTES.md)
end_state:                          # feeds the NEXT clip's continuity check
  BRUNO: {pos: left, pose: standing at the fence, hands: empty}
  PIP:   {pos: right, pose: seated in the mud, hands: empty}
```

Two fields carry real weight and get filled honestly or not at all:

- **`touched_objects`** — walk the prose and list every object a character contacts, lifts,
  leans on, reaches for or looks directly at as a focal object. Omitting one is how a clip ends
  up reaching for a prop that was never rendered.
- **`first_action_performable`** — asserting `true` means you checked that the clip's opening
  action can physically begin from that frozen instant. It is not a formality. If a still shows
  a door already open, a clip cannot knock on it.

## Rules with teeth

Full detail in the contract; these are the ones that cause the most rework.

**No negation, ever, in the positive.** The model renders the tokens it sees. Ending with
"No added captions, subtitles or overlay text" **causes** burned-in subtitles. Every exclusion
lives in the negative prompt.

**Timing lives only in `BEAT:: <frames> ::`.** The beat frame counts must total 481. `(3.0s)`,
`00:05.200` and "at 5 seconds" are forbidden loose timing prose *inside* a beat. Chronological
connective language — "Initially…", "A moment later…", "As he finishes speaking…" — still helps
inside a long dialogue beat, but beat order is the primary performance sequence.

**Anchor, do not inventory.** Repeat only the load-bearing identity, wardrobe, location and
light anchors needed to preserve frame-0. First name plus a short anchor — the still already
carries fur, eyes, markings and wardrobe. Never contradict the still; never dump the room.

**Dialogue folds into action.** No `Spoken dialogue:` header (it reads as a caption track), no
separate voice preamble. Voice signature verbatim and inline on the speaker's first line only.
Every line carries the speaker's visible action.

**Mouth discipline with 2+ characters.** Name the speaker as the only mouth moving; give every
non-speaker an explicit closed-mouth clause; return the speaker's mouth to rest after the line.

**Productive tail.** Never end on a frozen held pose — the model fills dead air by repeating
the last line. Continuation action, in-frame elements only, ambient sound still present, and an
affirmative stay-in-place clause for anyone who must remain visible.

**Camera-relative facing only.** Never describe facing relative to another character. No bench,
podium or head-of-table geometry that puts a speaker's back to the lens.

**Concrete photographable verbs.** Could a camera operator film the sentence without asking a
question? "Catches her eye" gets you a literal grab.

**Single take is the default.** LTX-2.5 can cut inside one prompt, but the vendor guidance says
i2v from a first frame should prefer one continuous take. A cut needs the transition named, the
new shot re-established, and audio continuity stated — and is never a way to escape a frame-0
contradiction.

## Stage gate

```bash
python tools/ltx_prompt_validator.py --channel <slug> --episode EPxxx   # via 04f3's compile step
```

Zero `LTXV-*` errors before a clip advances. The validator reports; it never fixes. A failure
returns here, not to the syntax skill.

Then, and only then, run the global **`ltx25-prompting`** skill as a read-only conformance read
against the official LTX-2.5 format. It never drafts, enhances, paraphrases or rewrites. If it
disagrees with `LTX_I2V_CONTRACT.md`, the contract wins and the disagreement gets recorded — it
is a generic vendor-syntax guide and does not know this pipeline's render-validated findings.

## What this skill must not do

- Decide geometry, camera movement or end state — those are `04d`'s.
- Write the still prompt — that is `frame0-still-writer` at `04f2`.
- Finalise an opening clause before the still is approved.
- Edit `blocking.json`, another stage's artifacts, or a channel's `channel.json`.
- Add words to a prompt to fix a problem that lives in the still, the conditioning, the render
  config or the gate. **In i2v the image is the contract; the prompt is only the delta.**
