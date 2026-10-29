# Visual style contract

## Reference style string

Use this complete style description for each new Muse Image environment
reference, then add the scene-specific geometry and supported process state:

> Photorealistic cinematic scientific visualization with a restrained
> exploration-film aesthetic. Believable material texture, controlled
> directional light, clear subject separation and readable depth. Practical
> ivory-and-orange equipment with restrained cyan navigation accents.
> Biological tissue, industrial materials and technological structures each
> retain their own documented geometry and material character. Use enough
> depth of field to show the causal action clearly. Compose around one
> observable process event with a quiet background. The fictional explorer
> remains visually distinct from the factual mechanism.

This is also `channel.json` → `render.style_echo`'s source string (with an added explicit photoreal lock — see that field's note). Keep the two in agreement if either changes.

## Inside means inside (owner rule, 2026-10-29)

An episode about the inside of something shows the **interior** of that thing, with the Explorer physically in it. It never substitutes an
outside view of a digital model for the journey.

- **"Inside your brain"** is the brain's interior at the scale where the process happens: the structures that really make it up (neurons,
  glial cells, vessels, fluid). **"Inside your stomach"** is the stomach: gastric folds, mucus, acid. The same holds for a material, a
  machine or a device: the camera is in its interior, not looking at a model of it.
- **Not allowed as the main view of an inside clip:** a whole-body transparent or X-ray figure, a hologram or wireframe body, glowing organs
  floating in an outline, a labelled anatomy diagram, a medical-infographic look. A caption saying "this is your brain" over such a view does
  not make it the inside.
- **Orientation, and the locator exception (owner: "can be integrated if needed").** Where the viewer needs to know where the organ or part
  sits, the story may show **an outside view of the body or object to locate it**, for example the whole body with the brain's position
  marked. This is a brief locator, used only when the story needs it, never the journey itself, and it is a separate clip from every
  inside clip. By default the outside "you" clip, the narration and a Remotion label do the orienting.
- Each inside clip's frame-0 still shows the named interior, built at 04c as a scene plate of its own. The structures in it come from the
  visualization ledger. The "scale, colour and visibility are simplified" disclosure still applies.
- **Checks.** 04a records the interior each scene is set in and whether it is a locator. The 04f2 vision gate asks the neutral question "is the
  camera inside the named place, or looking at a model of it from outside?" before it sees any claim. 05a repeats it on the rendered clip.

## Explorer identity and voice lock

When the Explorer is visible, the orange pressure suit and white helmet use a continuous uniform black-mirror visor panel of opaque black ceramic glass. Its exterior stays smooth, unbroken, reflective, and visually featureless for the full clip. The capsule canopy may be clear; it remains visually distinct from the Explorer helmet visor.

**Voice rule (owner decision 2026-10-29, after the LTX EP001 pilot; confirmed channel-wide 2026-10-29).** The Explorer's face is never revealed. The visor is never raised, turned transparent, opened or removed. No face, eyes, lips or mouth are ever visible.

The Explorer **does speak**, but only as a **background voice-over**, never as lip-synced on-screen speech:
- The Explorer may be visible while their line plays. The on-screen body performs the line through **body gestures only**: a lean, a head or helmet turn, pointing toward the process without touching it, an open-palm questioning hand, a small brace.
- Give the Explorer lines only in clips where the Explorer is visible, placed before Control's line, with a non-overlapping handoff.
- Control remains an off-screen radio voice.

**Prompt wording.** Whenever a prompt says the Explorer speaks, says or talks, the video model tries to reveal the face or soften the visor to show lips. Write every Explorer line with the proven helmet-radio pattern:

> The Explorer, seated in the capsule behind the canopy, holds still, watching the bottle, the dark visor unchanged, as the Explorer's voice comes over the helmet radio, in a curious, concise adult voice: "…"

- **The body holds still and keeps watching while the line plays.** Gestures belong in the speech-free moments before or after the line, never during it.
- **The voice arrives through a device, the helmet radio.** Always add the same voice description ("a curious, concise adult voice") so the voice stays consistent across clips.
- **Never write that the Explorer speaks, says, talks, asks, replies, answers or narrates, and never mention the Explorer's mouth, lips, face or "closed-mouthed".** When the Explorer is silent, write it as the visor ("the dark visor unchanged" or "sealed").
- **Never copy the script's labels into prompt prose.** The script's "Explorer (background voice-over)" label and its visible-action notes are authoring notes only.
- `pipeline/LTX_I2V_CONTRACT.md` §4 holds the LTX rules for dialogue clips.

*Why:* in LTX EP001, every clip that asked the Explorer to speak turned the visor transparent and rendered a face, a different face each time, while the helmet-radio pattern held. Keep an Explorer-voice clip in each episode's 04h pilot as a regression check.

## Explorer costume lock (from the next LTX episode, adopted 2026-10-29)

These details are locked from `locked-references/characters/` (CAST-001), and **every prompt showing the Explorer restates them positively**:
- the orange pressure suit with dark-grey panels, **plain dark-grey shoulder panels** and grey harness straps;
- the square grey chest unit with a round lens and a glowing cyan light strip;
- the smooth white dome helmet with a **round cyan side light** and an opaque black-mirror visor.

*Why:* a video model can insert an unplanned cut to an Explorer close-up, and without the restatement it redraws a generic astronaut. The sibling profile saw a stars-and-stripes shoulder patch, a chest emblem and a ribbed helmet band that way (two published clips). The render negative list carries the drift terms (`channel.json` → `render.negative_prompt_additions`). Close-ups are zoom-checked at 05a. Full rules: `STORY_ENGINE.md` §8.

The recurring outside **"you" figure** (CAST-002, locked in `locked-references/characters/`) gets the same treatment (`STORY_ENGINE.md` §9): plain, unbranded wardrobe, restated in every prompt.

## Scientific visualization is an illustration

A convincing render is not a measurement, microscopic recording or simulation.
Document enhanced visibility, false color, changed scale, time compression,
cutaways and schematic molecular views in the episode visualization ledger.
Use edit transitions or labels to indicate a change of magnification rather
than silently mixing molecules, cells and macroscopic machines at one scale.

## Readability

- Design an initial state before the main action, not a finished result.
- Establish a visible gap before contact, a destination for movement, and a
  stable final state after the change.
- Give the main process the frame. The capsule can be outside a detail shot.
- Keep fluid scenes visibly immersed; avoid an air-filled cave appearance.
  Haze and overlapping particles must not obscure the action.
- Restrict background motion to present, identified entities.
- Use restrained non-graphic biological imagery.
- Add labels and captions in editing rather than asking the video model to spell them — LTX-2.5 does not receive on-screen-text requests on this channel (`channel.json` → `render.on_screen_text`).
- Respect the active aspect ratio from channel.json at image creation.

## Continuity

Save the approved reference, scale convention, lighting direction and process
state. Same-location close-ups retain the same injury/object, illumination
and material identity. First-frame conditioning comes from the approved
frame-0 still (`04f2`, `pipeline/MUSE_FRAME0_CONTRACT.md`) — the LTX-2.5 prompt
animates and reveals that state, it does not redesign it.
