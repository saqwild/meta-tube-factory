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
