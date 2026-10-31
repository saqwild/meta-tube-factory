# EP001 still gate (04f2)

Generator: Muse Image (muse-image-1.0) via tools/meta_models.py image
--out, one still per clip, settled frame-0 state only. Stills are
renders/stills/SC01.png .. SC12.png, true PNG, 2016x1152.

## Gate method

Binary presence first (cast count = 1 per clip, touched objects present,
environment matches the locked ENV string), then identity against the
04b masters, then the performable-first-action question per clip.

## Findings

- SC01 PASS: one adult at the counter, linen cloth held, dough ball in
  the glass bowl at rest. First action (cloth lifts) performable.
- SC02 PASS (regenerated): tall adult proportions matching the master,
  blank sleeve patches, capsule at rest behind. One recorded deviation:
  visor renders gold reflective instead of the master's black opaque;
  face remains fully hidden. Logged in
  _context/frame0-still-facts.json and carried to 04f3 re-anchoring.
- SC03-SC11 PASS (regenerated set): one Explorer per clip, adult
  proportions, blank patches, foam/oven environments per locked strings,
  mouth/visor closed state, hands as blocked. First Explorer batch
  (chibi proportions, sleeve emblem) was rejected and regenerated;
  rejected variants were overwritten by the corrected generation.
- SC12 PASS: one adult, cooled loaf on the wooden board, one slice cut,
  crumb face visible. First action (slicing) performable.

## Verdict

All 12 stills approved for 04f3 re-anchoring. Visor tint deviation is
the single recorded still-vs-prompt override (LTXV-D055 guard armed).

## Owner QA revision (2026-10-29)

Owner rejected first corrected set: SC01/SC12 used a wrong human face instead of the CAST-002 master, SC06 showed the Explorer face. All 12 stills regenerated with CAST-002 identity text (short curly dark hair, navy hoodie) and opaque black full-face visor wording. SC01 and SC06 viewed after regeneration: PASS. Verdict remains PASS for 04f3.

## Owner QA revision 3 (2026-10-29) - SC01 CAST-002 reference-anchored

Owner flagged that the packaged SC01 still showed a different adult, not the CAST-002 master, because text identity alone did not anchor the face. SC01 was regenerated with the actual EP001-CAST002-sheet.png attached as a reference image through the new Muse Image reference path (tools/meta_models.py image_edit, Responses API input_image). Candidates v1-v3 are kept in qa/candidates/; v3 was promoted to renders/stills/SC01.png at 2016x1152 true PNG by _scripts/2026-10-29-promote-sc01-cast002.py. Viewed after promotion: exactly one adult matching CAST-002 (short tight curly dark hair, medium-brown skin, round face, plain navy hoodie, grey trousers), linen cloth held clear of the bowl, risen dough fully uncovered, capsule descending above the bowl, clean hands. First action (cloth lift) performable. SC01 PASS. All other stills unchanged; verdict remains PASS for 04f3.

## Owner QA revision 4 (2026-10-29) - SC01 single cloth

Owner: identity fine, but the still read as two cloths in two hands. Check confirmed a leak at both layers. The still showed the linen cloth held in both hands plus a second folded cloth on the counter, while frame0-requirements.json and 6-image-prompts.md both specify one cloth held in one hand. Edited via image_edit with the CAST-002 sheet and the current still attached (_scripts/2026-10-29-sc01-single-cloth-edit.py), candidate qa/candidates/SC01-cloth-v1.png viewed: exactly one linen cloth, held in one hand at the adult's side, other hand empty resting on the counter edge, counter beside the bowl bare, dough fully uncovered, identity unchanged. Promoted to renders/stills/SC01.png (2016x1152 true PNG). SC01 PASS. The matching video-prompt leak (GLOBAL describing the dough as under the cloth) is fixed at 04f3 in the same pass.
