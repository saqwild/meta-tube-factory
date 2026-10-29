# LTX-2.5 i2v Prompt Contract

The binding authority for every clip prompt this pipeline produces. Stage `04f`, `04f3` and
every gate obey this file; it outranks any skill's generic advice, including the global
`ltx25-prompting` skill, which is a **syntax conformance checker that runs after
compilation** and never drafts, enhances, paraphrases, or rewrites.

Evidence and provenance for every rule below: [`research/LTX25_PROMPTING_RESEARCH.md`](research/LTX25_PROMPTING_RESEARCH.md).
Each rule is graded:

- **[A]** vendor-confirmed (docs.ltx.io / the LTX-2.5 model card, retrieved 2026-10-29)
- **[B]** render-validated on a sibling pipeline under LTX-2.3, model-agnostic in nature
- **[C]** `[2.3-RETEST]` — an LTX-2.3-era number kept as the safe default, **unproven on 2.5**

EP001 (signed-anyway) rendered a full 29-clip LTX-2.5 batch on 2026-10-29 — that promoted
`img_compression` and the base-pass cfg figures to **[B]** (see §6 q4). Every other **[C]**
here is still unproven on 2.5. Do not upgrade a **[C]** to fact without a real render; do not
silently loosen one without evidence either.

---

## The one principle

**In i2v the image is the contract; the prompt is only the delta.**

The approved frame-0 still fixes the opening state — who is present, where they stand, what
they hold, what the room contains, how it is lit. The prompt's job is to describe what
happens *forward from* that instant. A failure gets fixed at the layer it lives in — the
still, the conditioning, the render config, or the gate — **never by adding words to the
prompt.**

Everything else in this file follows from that.

---

## Scope and format

**One prompt per clip.** The clip is the generation unit for both channels: a fixed **20
seconds** at 24 fps, 16:9. Duration, fps, aspect and resolution live in the render graph.

**Owner-locked PromptRelay-style beat packet.** Every channel uses the exact model-facing
syntax below, selected as `render.prompt_format: prompt_relay_beats_v1` in its profile:

```
GLOBAL:: Continue from the still. <full approved frame-zero scene and style anchor>. Low motion.
BEAT:: 24 :: <first performable character action and Ambient (slow, subtle): clause>
BEAT:: <frames> :: <one speaker's action, voice binding and quoted line>
BEAT:: <frames> :: <next speaker's action, voice binding and quoted line>
BEAT:: 120 :: <camera movement and Acoustic environment: clause>
```

`GLOBAL::` is not an old graph node and the current LTX-2.5 workflow does not execute the
labels as deterministic clock control. The labels are the **owner-locked model-facing pacing
convention**, retained because its 20-second LTX-2.5 render outperformed the regular-prose
alternative in this production (carried over from the `vidgen-codex-ltx` sibling, owner
decision 2026-10-29). This is local empirical evidence, not a vendor timing claim. The
validator requires one `GLOBAL::` line, one or more `BEAT:: <positive integer> ::` lines, and
a total of **481 frames** (24 fps × 20 seconds plus the conditioning frame). Do not put
seconds, timestamps or timing prose inside a beat — timing lives only in the frame labels.

The global intentionally carries the full static scene: characters, wardrobe, placement,
environment, recurring props, lighting and style. That is the reference anchor needed to keep
the approved frame zero intact. Each beat then names only the next controlled performance,
prop interaction or camera action. `Low motion.` is the approved global motion constraint, not
a suppression error.

**Length.** S1 and S2 set **no vendor word ceiling**; the former ~200-word ceiling was an
LTX-2-era sibling-pipeline import and is **retired 2026-10-29, not softened.** The only length
check is the 450-word `LTXV-D004` runaway/bloat tripwire: inspect for repeated inventory or
duration filler, but never trim a load-bearing identity, audio or camera anchor merely to fit a
number. A full three-hander beat packet normally lands around **260–340 words, and that is
expected, not a warning**.

**Single take is the i2v default.** LTX-2.5 can cut between shots inside one prompt, but the
vendor guidance is explicit that i2v from a first frame should prefer one continuous take
unless you *intend* to leave the conditioning frame behind. **[A]** A cut is allowed only when
the clip genuinely needs a new framing — and then you must name the transition in prose,
re-establish shot scale / identity / light, and state whether dialogue, music and ambience
continue across it. **Never use a cut to escape a frame-0 contradiction.**

**Naming the transition, if one is genuinely declared.** Pick the word for what actually
happens on screen, not a default — each names a different cut and reads differently to the
model:

| transition | when | example phrasing |
|---|---|---|
| hard cut | abrupt, most common | "A hard cut transitions to…" |
| match cut | the new shot echoes the old composition | "A match cut connects…" |
| dissolve | a gradual blend, time passing | "The image dissolves into…" |
| jump cut | a temporal leap within the same scene | "A jump cut leaps to…" |
| fade | through black/white | "The scene fades to black, then reveals…" |

No episode in this pipeline has used a declared cut yet (every clip so far is single
continuous take) — this table is here for the day one genuinely needs it, not a signal to
start using cuts. `LTXV-D050`/`D051` still gate: an *undeclared* cut fails, and a declared
cut's count and audio-continuity statement must match the prose.

**No numeric camera specification.** "The camera pans 45 degrees at 2°/second" reads as a
literal on-screen token, not a motion instruction — LTX-2.5 takes natural-language camera
description only ("a slow arc around the subject", not a measured angle or rate). Enforced by
`LTXV-D053`, adopted 2026-10-29 from the `ltx-2-5-prompter` reference skill's pitfall list
(the one item from it this pipeline didn't already cover) — cross-checked against every
existing clip in this pipeline (zero prior instances) before enabling it as a hard rule.

---

## Required elements, in beat order

1. **`GLOBAL::`** starts `Continue from the still.` and describes the full approved
   frame-zero composition: identity/wardrobe, environment/lighting, fixed props, and style.
   It ends `Low motion.`
2. **The 24-frame opening beat** begins with the first performable character action and carries
   `Ambient (slow, subtle):` as its distinct visual-motion clause. **[B]**
3. **Dialogue beats** stay chronological. Each quoted line is attached to that speaker's visible
   action and first-use voice signature; non-speaking characters stay explicitly mouth-closed.
   Order beats by chronology; chronological connectives ("Initially…", "A moment later…") still
   help inside a long dialogue beat.
4. **The final beat** (120 frames by default; a channel may set `render.closing_beat_frames`, and
   inside-the-process uses 72, measured at its first pilot [B]: the beat is speech-free, so a 120-frame
   tail left a mean 5.4 s of silence in every clip) carries a motivated camera movement and `Acoustic environment:`
   naming room tone, a scene-specific ambient sound, the subjects' own foley, and "clear close
   dialogue front and center". Ambient motion and acoustic sound remain separate clauses. **[B]**
   **Speech finishes early, so the final beat must carry a visible action, not a static hold [B].**
   Measured at inside-the-process EP001's second pilot (2026-10-29; 8 clips, 39–40 words each): delivery pace
   varied from 2.20 to 3.30 words/s from clip to clip, so speech ended 1.0–6.6 s before the clip did (typically
   about 4.5 s). The owner judged each tail by what played over it. A static push-in read as "dialog short", and
   SC30, where the Explorer walked to the capsule and boarded, read as "the best in term of dialog" with a
   4.7 s tail. So the closing beat names a real, continuing action by the subject (a walk, a turn, a prop
   settling, a machine cycling), running to the end. Do not answer the tail by raising the word count across
   the board: at the slowest measured pace, 40 words already used 18.2 s of 20.
   **A character who is off-screen at frame 0 never enters the frame inside the clip** (validator `LTXV-S003`).
   With no identity in frame 0, i2v invents a new person: EP001 SC29's "the Explorer leans back into frame"
   rendered a stranger with a visible face. Who is on screen changes across a cut, which `LTXV-S004` allows.
   **When no one is in frame 0, the picture text names no one [B].** The root cause of the stranger renders
   (EP001 SC13/SC15/SC29, 2026-10-29) was every off-screen reference, not just the re-entry line. "The
   Explorer, just out of frame, listens…" in the anchor and "the Explorer … just out of frame" in the tail
   both told the model a person stood beside the view, and when the camera moved it revealed people. So in a
   no-one-visible clip:
   - The anchor states the emptiness positively ("The view is empty and unattended").
   - The final beat ends on what the frame shows.
   - A character who speaks is an audio-only voice, in the same form as a narrator: "An off-screen voice
     (VOICE-002 Explorer, over the helmet radio, audio-only) speaks, <visible action>…".

   `LTXV-D040`/`LTXV-D041` invert for these clips: they require a named character only when one is visible,
   and fail if one is named when none is. Negative prompts cannot guard against this, because they act only in
   the cfg-1.2 base pass (the refine pass that reaches the output runs at cfg 1.0).
   *Also for the next episode:* write environment locks positively ("an empty, unattended hall"), never
   "no people". A negation in positive text summons the thing it negates.
   **Narration of a change lands on the clip that shows its result.** A state change happens across a cut
   (i2v keeps frame 0's shape), so a line that describes the change ("the air blows the glass outward") must
   play over the clip whose frame 0 already shows the result. The clip before it narrates the setup. Owner note
   on EP001 SC12 (2026-10-29): the narration said the air blows the glass outward, but no impact was visible,
   because the gob correctly held its shape until the cut to SC13. This is a script-stage (`03a`) alignment rule.
5. **A concise style echo** closes the `GLOBAL::` line (before `Low motion.`), verbatim from
   `channel.json → render.style_echo`.

### Anchor, do not inventory
The `GLOBAL::` line carries the full static composition as a reliable reference anchor: all
visible characters and wardrobe, named location features, recurring props, light and style. It
must match the approved still and may never contradict it. The later beats add only the
controlled delta, so a prop never drifts simply because the global forgot its position. Use
the character's first name + a short anchor ("Bruno, the elderly bulldog-mastiff mix"), never
the full identity string — the still already carries fur, eyes, markings and wardrobe.

### Camera movement is a decision, not a default
A settle tail with both character and camera locked reads as a dead freeze-frame. Pick the
movement the scene actually calls for; state how the subject looks *after* the move so the
model can complete it. **[A]**

| Movement | Use when the scene is… |
|---|---|
| Dolly in / out | building intimacy (push in) or releasing/revealing space (pull out) |
| Truck / pan / slide | revealing something beside the subject, or adding parallax to a wide shot |
| Crane / jib / pedestal | emphasising scale or height, or introducing a character entering frame |
| Handheld | urgency or physical exertion — rarely right for a calm domestic register |

If nothing implies a type, default to a slow subtle dolly rather than a locked camera. Never
put a camera movement and a quoted line in the same sentence.

---

## Dialogue and sound

**Fold dialogue into the action. Never use a labelled block.** A `Spoken dialogue:` header
followed by quoted lines reads to the model like a caption track and triggers burned-in
subtitles. **[B]** Weave each line into the speaker's visible action instead:

> …he pauses, paw still on the trowel, and grumbles, gruff but wavering, in a steady gravelly
> American English elder voice: "In my day, dogs didn't need rescuing." A beat later, watching
> Pip shiver in the mud, his ears droop and he mutters: "…Oh, fine. Just for tonight."

- Dialogue goes **in quotation marks**; state language/accent where it matters. **[A]**
- **Voice signature inline on the speaker's first line only** — verbatim from the character
  map, including "American English" and the timbre tail. Never a separate voice preamble, and
  never abbreviated to "gruff, old". Later lines get bare name + action.
- **Every line carries the speaker's visible action** ("his paw tightening on the trowel
  handle"). "Bruno says, resigned: '…'" is not enough. **[B]**
- **Every clip names a continuing ambient sound.** A clip with no stated sound bed invites
  native audio to invent dialogue to fill the silence. Keep it present through the settle
  tail — never true silence. **[B]**
- **Qualify ambience by place** — "warm *garden* room tone", not a bare "room tone".
- **Avoid "background activity" / "distant voices"** — they make the model render people.
  Use room tone plus a specific named ambient life sound. **[B]**
- **Narration**, if a channel permits it at all, is *"a warm, dry off-screen background
  voice-over, not synced to any on-screen character: '…'"* — never the word "Narrator".

### Multi-character mouth discipline
Anywhere 2+ characters are on screen, near every dialogue line: **[B]**

1. Name the speaker as the only one whose mouth moves for that line.
2. Give every non-speaking on-screen character an explicit closed-mouth clause ("Pip watches
   quietly, mouth closed").
3. Let the speaker's mouth return to rest after the line ("After speaking, Bruno's mouth
   closes naturally").

A reaction clause alone is not enough. This is the cheap mitigation for the wrong-character's-
mouth-moving failure class; it is not optional polish.

Non-speaking characters get a **reaction, not silence-by-omission** — a short reaction clause
or an explicit stay-in-place anchor. An unaccounted-for on-screen character has nothing
pinning it, and the model can animate the wrong face.

---

## Affirmative only — never negate in the positive

**The model renders the tokens it sees.** It does not process "no". Every one of these
backfires by naming the thing you are excluding: "no new characters", "no morphing", "no one
moves toward", and above all:

> ⚠ **Never end a prompt with "No added captions, subtitles or overlay text."** That clause
> **causes** burned-in subtitles at the render layer. **[B]**

Describe exactly who and what IS in the scene. Text suppression, duplicate suppression and
every other exclusion live **only in the negative prompt** — LTX-2.5 has a real negative
channel, so there is no excuse to smuggle exclusions into the positive. **[A]**

Diegetic signage that genuinely belongs in the scene is simply described, and renders fine.

---

## Frame-0 state rules

These are the i2v contract itself. They are model-agnostic — they describe what a single
conditioning frame can and cannot imply.

- **Continue forward from frame-0.** Never contradict the still's pose, orientation or
  blocking. Never re-enact an arrival, discovery, placement or break the still already
  shows as complete. **[B]**
- **State, not transition.** If the still shows a door already open, the clip cannot knock and
  open it. A *closed* door plus opens-in-clip is a legal start-state transition and is fine.
  The illegal shape is: still declares the END state, clip performs the transition into it.
- **Props at their resting state, hands empty.** If a prop will be "placed", the still shows
  it already placed and the hand empty — a prop seeded mid-placement lingers or duplicates in
  the clip. **[B]**
- **Every object the action touches must already exist in the still.** i2v does not invent
  props. This is what `04f`'s frame-0 requirement block exists to guarantee — see
  [`MUSE_FRAME0_CONTRACT.md`](MUSE_FRAME0_CONTRACT.md).
- **This extends to objects named only in `Ambient (slow, subtle):` or `Acoustic environment:`,
  not just objects a character touches.** `LTXV-S002` only checks `touched_objects` against
  the still, so a concrete object invented purely for atmosphere slips past validation —
  render-confirmed on EP001 SC03: "a sheet of paper near Jonah's elbow lifts one corner and
  settles" named a prop absent from the approved still, and i2v resolved it by morphing the
  one real object already in that hand (his pen) into paper and back for the span of the beat.
  A generic particulate or sound with no fixed shape ("dust drifts", "a low ventilation hush")
  is fine; a concrete noun is not, unless it is the same object already declared for that clip
  under a different word (e.g. "the paper" referring to that clip's own established form/
  letter/document) or a recurring environmental fixture already visible in the still (the
  lamp, a wall panel, a corridor-light spill). **[B]**
- **Author the opening clause AFTER the still is approved**, describing what the still
  actually shows. A pre-still guess routinely contradicts the render. This is why prompt
  authoring is split across `04f` (draft) and `04f3` (final). **[B]**
- **A reflection or mirror tell must be written as a motionless, already-turned STATE.** i2v
  cannot desync a reflection's timing. **[B]**

---

## Prose grammar — LTX is a literal reader

- **One clear action per clause, with a connective between actions.** "she holds a beat
  withdraws" has no boundary; "she holds a beat, then withdraws" is two clearly sequenced
  clauses. Don't stack more than 2–3 distinct actions in a sentence — start a new sentence
  instead of adding a fourth comma clause.
- **Concrete photographable verbs only.** No idioms ("catches her eye" → a literal grab), no
  grasp-verbs for non-grasping ("holds there"), no formal/abstract verbs ("withdraws" →
  "drifts back"), no referential phrases ("the way it came" — name the path). Test: could a
  camera operator film the sentence without asking a question?
- **Emotion through physical cues, never abstract labels.** "sad" and "confused" are not
  filmable; drooping ears and a slow head-tilt are. **[A]**
- **Name concrete, specific props** ("a small stuffed toy rabbit", never "a small toy") and
  reuse the *exact same name* every time the object recurs — the model has nothing to be
  consistent with otherwise. **[B]**
- **Duration-filler with no other content is still weak** ("a long beat" as the entire
  clause). A connective paired with a real action is good ("a moment later, she reaches for
  the dial").
- **The `GLOBAL::` line and the last `BEAT::` must name a character as grammatical subject.**
  A scenery-only anchor or closing beat spawns extra characters or drifts the camera off the
  subject. **[B]**
- **Never a bare species or role word for background figures** where an anthropomorphic
  character is intended — "neighbours", "kids", "adults" render as photoreal humans. State
  "anthropomorphic animal" explicitly. This is a hard safety floor on any channel that
  declares one.

---

## Productive tail

Dialogue ends before the clip does. **Never end on a frozen held pose** — the model fills dead
air by repeating the last line. **[B]** Close with a continuation action that:

- uses **only in-frame elements** and stays in frame;
- keeps the named ambient sound present (never true silence);
- carries an **affirmative stay-in-place clause** for any character who must remain visible
  ("stays rooted at her spot, toy resting in her paws"), not merely their emotional reaction —
  otherwise they drift out of frame. **[B]**

---

## Forbidden

- Any prompt format other than the owner-locked `GLOBAL::` / `BEAT:: <frames> ::` packet, a
  beat frame total other than 481, or seconds/timestamps/timing prose inside a beat.
- Duration, fps, aspect ratio, resolution or the model name in the prompt text.
- Any negation or text-suppression clause in the positive prompt.
- A labelled `Spoken dialogue:` block or a separate voice preamble.
- Any blanket motion-suppression token beyond the mandated `Low motion.` that closes the
  `GLOBAL::` line (`minimal motion`, `static scene`, `still frame`). Inside a beat, describe
  the exact plausible motion instead.
- A full room or full-appearance inventory, or any contradiction of the approved still.
- Inventing an object, prop or character that the still, the blocking spec and the prior clip
  all fail to establish.
- Requesting on-screen text, titles, labels or logos — spelling is not guaranteed across
  frames; those are a post-production pass. **[A]**
- Internal planning jargon, pipeline meta, or audience-facing meta lines inside the prompt.
- Bench / podium / head-of-table geometry that puts a speaking character's back to the lens.
  Facing is always described **relative to the camera**, never relative to another character.

---

## Semantic preflight

Before a clip prompt is accepted:

1. Every visible character, focal prop and fixed environment resolves to a row in
   `_context/blocking.json` (stage `04d`) — the single geometry authority both the clip prompt
   and the still prompt project from. Conflicting upstream phrasing **stops compilation and
   gets reported**, never silently resolved by picking one reading.
2. A continuing entity's opening state equals the preceding clip's `end_state`.
3. Every object the clip's action touches appears in that clip's frame-0 requirement block.
4. `python tools/ltx_prompt_validator.py --channel <slug> --episode EPxxx` reports zero
   `LTXV-*` errors. The validator **reports only** — it never auto-fixes, and a failure
   returns the clip to the writer.
5. The global `ltx25-prompting` skill's conformance read, run last, as a read-only check.

## Stop condition

A clip prompt is done when it is one `GLOBAL::` continuation anchor on the still's real
approved pixels (ending `Low motion.`) plus `BEAT:: <frames> ::` lines totalling 481 that move
forward through named actions and folded dialogue, name both an ambient-motion clause (in the
24-frame opening beat) and an acoustic-environment clause (in the final 120-frame beat), state
a motivated camera movement, end on a productive tail that names a character, contain no
negation and no loose timing prose, and pass the validator with zero errors.
