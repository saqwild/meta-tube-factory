# QA checklist

## Story and source review

- One clear question and supported takeaway.
- All central claim IDs and visualization conventions resolve to sources.
- Fictional guide distinguished from factual process.
- No unsupported timing, manufacturer universality or healing claims.
- Any escalated review needs resolved, with the actual reviewer scope recorded.

## Reference review

- Same Explorer, capsule geometry, scale convention and lighting.
- Model has not rendered an open-air cave for an immersed setting.
- The image shows the initial state needed for the action.
- Main objects are readable at delivery size.
- Sparse foreground for a precise contact test; no decorative clutter.

## Motion review

Check the actual event through time, not just overall motion:
- APPROACH: the moving entity starts visibly separate from its destination.
- CONTACT: it reaches the intended surface without teleporting.
- HOLD: it stays attached while independent background motion continues.
- SPREAD/TRANSFORM: the visible form genuinely changes if the script claims it.
- Already attached objects remain anchored; no unexplained growth or relocation.
- Counts and identity agree across adjacent shots.
- Final state supports the actual narration.

Record failure when contact or spreading is unclear. A beautiful image is
not sufficient. Do not invent extra particles, repair beams or autonomous
behavior to make an invisible mechanism look dramatic.

## Automated prompt and still gates

Before any pilot or batch render, every compiled clip prompt must pass
`tools/ltx_prompt_validator.py` against `pipeline/ltx_prompt_validator.md` /
`pipeline/LTX_I2V_CONTRACT.md`, and every frame-0 still must pass its
`04f2-frame0-stills` gate (`tools/image_agent_packet.py`, `LTXV-S006` binding
check, the neutral-dimensions-then-judge vision-gate method — never show the
vision model the claim it is confirming). A failure is corrected at the
prompt, the still, or `_context/blocking.json` (the geometry authority — see
`TECHNICAL_PIPELINE.md`), never patched with extra prompt words alone.

This channel has no LTX-style `ltx_contract_gate.py` — the equivalent
deterministic checks are `blocking.json` (geometry, decided once at `04d`)
plus `LTXV-S001`/`S002`/`S006` (frame-0 requirement binding) and the frame-0
vision gate's performable-first-action question. Post-render semantic review
still checks generative failures such as object mutation, invented speech or
implausible motion; those cannot be proven from prompt syntax alone.

## Representative LTX pilot — 04h

Human-watch the pilot subset marked in `render-manifest.json` against every
check in `pipeline/stages/04h-ltx-pilot-qa.md`: beat adherence (the named
action actually happened, in its beat's place — not aggregate motion or file
size), frame-0 fidelity, dialogue accuracy, speaker binding/lip sync,
identity/cast count, prop interaction, environment/camera stability, audio,
and artifact-freedom. Do not manufacture dense dialogue or multiple visible
characters simply for QA coverage. Never certify these from silent frame
samples.

Record the pilot verdicts in `qa/ltx-pilot-qa.json`
(`pipeline/schemas/ltx-pilot-qa.schema.json`). Because this is this channel's
first LTX-2.5 render, also record any measured finding that settles one of
this channel's own **[C]**-graded open questions (the dual-voice
`spoken_word_band`, and whether the `calibration_note` render settings
carried from signed-anyway hold here) — promote to **[B]** only from measured
evidence, never impression.

## Final package

Check actual final runtime/aspect ratio against the active profile, narration
against visible mechanism, source/disclosure text, clean audio edits, caption
legibility and final human sign-off. An agent's sampled-frame review must be
identified as such; no invented watched/listened verdict.

## Story-engine checks (from the next LTX episode, `STORY_ENGINE.md`)

- **05 ingest:** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8). Hits that match a clip's declared cut are expected; every other hit is listed for review.
- **05a:** zoom-check every Explorer or "you" close-up against the locked reference: helmet cyan side light, grey chest unit with cyan strip, plain dark-grey shoulder panels, opaque visor. Call a patch a flag only when it is unambiguous at full resolution.
- **04f2 and 05a, "inside means inside":** for every inside clip ask, before showing any claim, "is the camera inside the named place, or looking at a model of it from outside?" An outside view of a digital or see-through body model fails unless the scene is a declared locator clip.
- **05a / 04h:** check for dead stretches (a visible change about every 5 s) and confirm each clip's beats happen.
- **03b:** the arc lands (hook, struggle, climax ≈45%, objection ≈55%, practical, callback), narration is second person, and the master metaphor is set up and paid off.
