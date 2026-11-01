# EP001 pilot QA (04h, in progress)

Pilot clips: SC01, SC02, SC05, SC08, SC12. No verdict is final until
the owner has watched each clip; frame grabs below support, never
replace, that viewing.

## SC01 - s01_20261031222018.mp4 - FAIL (owner + frame check)

- Spec check: 20.04 s, 1344x768, 24 fps, native audio present. PASS.
- Finding (owner, confirmed on frames f1/f3/f5 in qa/frames-s01/):
  the clip starts with the dough uncovered (matching the still), then
  drapes the cloth over the bowl - the reverse of the scripted lift.
  Mid and end frames show the dough dome visible through/above the
  cloth: the bread is neither fully covered nor uncovered.
- Root cause layer: prompt delta, not the still. Beat 1 said "The cloth
  lifts slowly" without stating direction or end state; the model chose
  covering. Fix at 04f3 for SC01 only: state the adult lifts the cloth
  clear of the bowl, holds it aside, dough fully uncovered at end.
- Action: re-render SC01 only after the prompt fix. Do not re-roll the
  still; SC01 still is correct (uncovered dough, cloth in hand).

## Remaining pilots

SC02, SC05, SC08, SC12: awaiting owner viewing and verdicts.

## SC02, SC03, SC04 - owner viewed 2026-10-29

- Verdict: PASS (owner watched; clips look fine).
- Post note for 06a assembly: trim dead-silence tails on rendered clips during postproduction. This is an assembly trim, not a re-render: keep each clip's dialogue and productive tail action, cut only trailing silent frames, and record per-clip trim ranges in the assembly notes at 06a.

- SC05 (s05 render): owner viewed 2026-10-29 - PASS. Dead-silence tail trim at 06a if present, as with SC02-SC04.

- SC06 (s06 render): owner viewed 2026-10-29 - PASS. Dead-silence tail trim at 06a if present.

## Owner overall review (2026-10-29) - process-focus revision

- Overall: dialogue feels short with dead tails (trim at 06a); too many clips end on the Explorer. Show the tech/process, not the presenter.
- SC01 REVISE: capsule now descends into the risen dough (transition into the interior); cloth beat already fixed. Note: dough doubling is proofing warmth, not oven heat - oven spring stays SC08.
- SC02 PASS, SC03 PASS (owner).
- SC04 REVISE still: yeast/bubble macro, Explorer small at edge.
- SC05 REVISE still: stretched net fills frame.
- SC06 REVISE (agent review): Explorer hands were gripping strands - violates never-touch rule; regenerated hands empty at sides, process wide.
- SC07 REVISE still: slow proofing bubbles wide, Explorer small.
- SC08 REVISE still: expanding bubbles/dome fill frame.
- SC09 PASS (owner); more dialogue requested - spoken band is capped 38-42 words/clip by channel format, so no added lines without a format change; perceived shortness is the dead tail, fixed by 06a trims.
- SC10 REVISE still: crumb surroundings fill frame.
- SC11 REVISE still: set cooling crumb per spoken content.
- SC12 REVISE still: bread zoom, person cropped at edge.
- All revised clips: final prompt beats now end on the process, not the Explorer. Stills regenerated, strict validator PASS, manifest/package rebuilt. Awaiting owner re-render of SC01, SC04-SC08, SC10-SC12.

- SC12 still revision (owner flag): heavy wrist hair regenerated to a clean hand with short nails and minimal arm hair; viewed PASS. Package rebuilt with new SC12 hash.

- SC01 still revision 2 (owner flag): face was cropped out of frame 0, so i2v had no identity to hold. Regenerated with CAST-002 face fully visible, capsule descending; viewed PASS. Package rebuilt.

## Owner clip review, second pass (2026-10-29) - SC04, SC05, SC06

- SC04 FAIL (owner watched): the Explorer voice is female; the
  Explorer voice in the other clips is male. Root cause layer: prompt
  delta. The SC04 Explorer beat specified no voice gender. Fix at
  04f3, SC04 only: Explorer line is spoken in a calm adult male
  English voice. Re-render SC04 only.
- SC05 FAIL (owner watched): the Explorer face becomes visible in the
  rendered clip. Still check (agent viewed renders/stills/SC05.png):
  frame 0 shows the Explorer small at the lower-left edge with an
  opaque black visor, no face visible - the still is not the fault.
  Root cause layer: prompt delta / i2v drift as the tilt-up enlarges
  the figure. Fix at 04f3, SC05 only: every Explorer beat states the
  opaque black visor stays fully opaque with the face hidden, and the
  Explorer line uses the same calm adult male English voice as the
  other clips. Re-render SC05 only; if the face appears again,
  regenerate the SC05 still with a larger, clearer visor figure.
- SC06 FAIL (owner watched): the Explorer duplicates, appearing to
  come out of the bread a second time. Still check (agent viewed
  renders/stills/SC06.png): frame 0 shows exactly one Explorer at the
  right edge, hands empty, visor opaque - the still is not the fault.
  Root cause layer: prompt delta / i2v drift on the push-in. Fix at
  04f3, SC06 only: the single Explorer stays planted at the right
  edge, feet still, and does not walk, emerge, or duplicate. Re-render
  SC06 only.

- SC12 PASS (owner watched, 2026-10-29). Full 12-clip review is now
  complete. Final tally: PASS with no re-render - SC02, SC03, SC08,
  SC09, SC12. Re-render after fixes - SC01, SC04, SC05, SC06, SC07,
  SC10, SC11. Dead-silence tail trims for passing clips stay a 06a
  assembly task, not a re-render.

## Owner clip review, third pass (2026-10-29) - SC07, SC08, SC10, SC11

- SC08 PASS (owner watched).
- SC07 FAIL (owner watched): the Explorer walks over a bubble and
  disappears inside it. Still check (agent viewed SC07.png): exactly
  one Explorer, small at the left edge, visor opaque. Prompt cause:
  the dialogue beat has the tiny figure "look toward camera" and the
  camera drifts; LTX turned that into walking and lost him in the
  foam. Fix at 04f3: single Explorer stays planted in his frame-0
  spot, feet still, and stays visible in frame for the whole clip.
- SC10 FAIL (owner watched): two Explorers - one at the edge and a
  second appears suddenly. Still check (agent viewed SC10.png):
  exactly one Explorer, small at the right edge, visor opaque. Prompt
  cause: "looks around" on a tiny figure plus a drifting camera; LTX
  spawned a second figure. Fix at 04f3: single Explorer, stationary,
  same spot and size throughout.
- SC11 FAIL (owner watched): two Explorers - one standing and one
  jumps in. Still check (agent viewed SC11.png): exactly one
  Explorer, small at the left edge, visor opaque. Prompt cause:
  "looks toward camera" plus a dolly-out on a tiny figure. Fix at
  04f3: single Explorer, stationary; the dolly-out keeps him in
  frame, no second figure enters.
- Pattern across SC05, SC06, SC07, SC10, SC11: every duplication /
  disappearance happens on a process-wide still where the Explorer is
  a small edge figure, and the prompt then asks that figure for a
  head/body action or moves the camera past him. The passing clips
  (SC02, SC03, SC08, SC09) either hold the Explorer larger or keep
  him braced without a look-around action. First fix is the prompt
  stationary lock at 04f3 for all five clips. If any clip duplicates
  again on re-render, the second fix is at the still layer:
  regenerate that still with the Explorer larger, using the CAST-001
  sheet attached via image_edit, as done for SC01.
- Rewrite method for the 04f3 fixes: the still is the contract and the
  prompt is only the delta, so each fix states positively what stays
  (one Explorer, planted, same spot and size, visor opaque) instead of
  adding new actions or redescribing the frame. Wording is compiled
  under pipeline/LTX_I2V_CONTRACT.md and checked with the strict
  validator before the package is rebuilt.

## SC01 still revision 3 (owner flag: attach the reference image)

- Owner instruction: the SC01 person is not the generated CAST-002
  character because the face was not anchored; attach the actual
  CAST-002 reference sheet instead of relying on text identity.
- Method: new Muse Image reference path in tools/meta_models.py
  `image_edit` (Responses API, sheet sent as an input_image data URI,
  per meta-model-cookbook 05_muse_image/01). The earlier multipart
  /images/edits attempt was closed by the server and was replaced.
  Generation scripts kept at _scripts/2026-10-29-sc01-cast002-ref-edit*.py
  with logs beside them. Candidates kept outside renders/stills.
- Candidates: qa/candidates/SC01-ref-v1.png (fresh scene from sheet),
  SC01-ref-v2.png (three-quarter retry), SC01-ref-v3.png (v1 scene
  preserved, head-turn correction requested). v1 and v3 are visually
  the same composition.
- Validation against EP001-CAST002-sheet.png (agent viewed both):
  identity PASS - short tight curly dark hair, medium-brown skin,
  round face matching the sheet's side and front views, plain navy
  hoodie, grey trousers, exactly one person. Scene PASS - linen cloth
  held clear of the bowl, risen dough fully uncovered, ivory-and-orange
  capsule with cyan ring descending above the bowl, clean hands with
  short nails. Face criterion NEEDS REVIEW - the face is fully in
  frame and unobstructed, but in three-quarter profile looking down at
  the dough, not both-eyes toward camera; two correction attempts did
  not change the head direction.
- Resolution (owner flagged the packaged still still showed the old
  adult): candidate v3 promoted to renders/stills/SC01.png (2016x1152
  true PNG, _scripts/2026-10-29-promote-sc01-cast002.py), still gate
  updated, stage 04f2 completed. Package verification: packaged
  exports/ltx-render-package/stills/SC01.png hash matches the new
  renders/stills/SC01.png exactly.

## Prompt fixes applied (04f3, after owner full review)

- SC04: Explorer line now carries the calm adult male English voice
  signature on his first line.
- SC05: Explorer stays settled on the stretching mass with his opaque
  black full-face visor fully opaque (dialogue and Control beats);
  same male voice signature added.
- SC06, SC07, SC10, SC11: the single Explorer stays planted at his
  frame-0 edge (right: SC06, SC10; left: SC07, SC11), feet still,
  head raised for his line; same male voice signature added. All
  wording is a positive stay-delta under LTX_I2V_CONTRACT.md - no new
  actions, no negation, beat frame totals unchanged.
- Strict validator: PASS 12/12. Manifest rebuilt with the SC01
  revision-3 still hash. Render package rebuilt (12 stills paired);
  stage now sits at 04g owner gate.
- Re-render list for the owner: SC01, SC04, SC05, SC06, SC07, SC10,
  SC11. Leave SC02, SC03, SC08, SC09, SC12 renders untouched.
- 04h stays open: no verdict is recorded for the re-rendered clips
  until the owner has watched them.

## SC01 cloth check (owner re-check, 2026-10-29)

- Owner: the still read as two cloths held in two hands; re-check
  that the cloth staging is correct and the prompt is not leaking.
- Finding: leak at both layers. Still: one cloth held in both hands
  plus a second folded cloth on the counter, against the spec (one
  cloth, one hand). Video prompt: SC01 GLOBAL described the dough as
  "under a linen cloth" while the still shows it uncovered - the
  wording that invites LTX to drape the cloth back over the bowl.
- Still fix: image_edit with CAST-002 sheet + current still; exactly
  one cloth in one hand at the adult's side, other hand empty on the
  counter, counter bare, dough uncovered. Viewed PASS, promoted,
  still gate revision 4 recorded, 04f2 completed again.
- Prompt fix (04f3): GLOBAL now states the risen dough fully
  uncovered with one linen cloth held in one hand at the adult's
  side; beat 1 settles that cloth at the side and the dough stays
  uncovered. The wrong-gender "his hand" token in beat 1 is also
  gone. Strict validator PASS 12/12, manifest and render package
  rebuilt; packaged SC01 hash verified against the new still.
- Net SC01 story is now consistent at every layer: she comes back to
  the already-uncovered risen dough, cloth in hand; the cloth never
  covers the dough at frame 0 or in any beat.
- Owner confirmation (2026-10-29): SC01 confirmed and approved. The
  04g render package advances on that approval; re-rendering of the
  seven fixed clips follows, and their verdicts are recorded here
  only after the owner watches them.

## Re-render verdicts (owner watched, 2026-10-29)

- SC01 PASS (owner watched the re-render). CAST-002 identity holds,
  the single cloth stays in one hand at her side, and the dough stays
  uncovered. No re-render needed; any dead-silence tail is a 06a trim.
- SC04 PASS (owner watched the re-render). The Explorer voice is now
  male, consistent with the other clips. No re-render needed.
- SC05 PASS (owner watched the re-render). The Explorer face stays
  hidden behind the opaque visor for the whole clip. No re-render
  needed; the still-layer fallback (larger visor figure) is not
  required.
- SC06 PASS (owner watched the re-render). The single Explorer stays
  planted at the right edge; no duplication and no emergence from
  the bread. No re-render needed.
- SC10 PASS (owner watched the re-render). The single Explorer stays
  planted at the right edge; no second Explorer appears. No
  re-render needed.
- SC11 PASS (owner watched the re-render). The single Explorer stays
  planted at the left edge; no second Explorer jumps in. No
  re-render needed.
- SC07 PASS (owner watched the camera-fixed re-render, with the 04g
  approval). The camera now holds wide on the re-inflating bubbles
  and the doming surface; the Explorer stays small at the left edge.
  No re-render needed.
- All 12 clips now carry an owner-watched PASS. The five pilot clips
  (SC01, SC02, SC05, SC08, SC12) are written up per-check in
  qa/ltx-pilot-qa.json for the 04h gate.
- SC07 RE-RENDER (owner watched the re-render): the stationary fix
  held - no walking, no disappearance - but the camera focus moved
  to the Explorer instead of the bubbles and the loaf walls. Root
  cause layer: prompt delta. The final beat named the doming surface
  as the end state, but no beat held the camera wide on the bubbles
  during the dialogue, so LTX pushed in on the speaker. Fix at 04f3:
  the camera stays wide on the re-inflating bubbles during the
  Explorer and Control beats, and ends on the re-inflating bubbles
  and doming surface with the Explorer still small at the left edge.
  Re-render SC07 only.
