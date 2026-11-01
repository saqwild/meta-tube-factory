# EP001 final package QA (07)

Signed off 2026-10-29 after the owner's watched approval of the
captioned master at 06a.

## Re-verified at this gate (not trusted from stage 06)

- Keyword set: 14 ordered phrases in metadata/package.md, exact
  primary phrase `how bread rises` first, same ordered set in the
  Tags section, mirrored into metadata/upload.json (`tags`) and
  metadata/upload-sheet.md. Count inside the 10-15 band.
- Thumbnail brief: full primary and alternate Muse Image prompts,
  exact typography/font/color/layout/output specs, and a reference
  manifest whose four still hashes were checked against disk at 06.
  Every referenced asset exists at its stable path.
- Delivered thumbnails: metadata/thumbnail-concept1.png and
  thumbnail-alternate.png, both 1280x720 PNG under 2 MB. Concept 1
  was viewed at full size and at the 120 px mobile preview:
  FROM DOUGH TO LOAF and the three process states stay legible,
  bottom-right duration-overlay corner clear. It matches the brief.
- Consistency across the package: episode health reports 12 clips
  consistent across 7 sources, 50 recorded hashes still matching on
  disk, 2 final MP4s 16:9 with audio and sane duration. Metadata
  validator OVERALL PASS (re-run at this gate). LTX strict validator
  PASS 12/12. Muse Voice Transcribe audio audit PASS 12/12.
- Assembly: captioned master 236.50 s; chapters and Problems
  timecodes measured from it; clean and captioned masters plus the
  SRT track are hashed in metadata/upload.json.

## Known warnings, accepted with reasons

- Episode health: OVERALL WARN (0 fail, 5 warn). All five warnings
  are review-freshness notices: an approved stage's deliverable
  changed after its approval. Each change was a later, separately
  gated revision (owner QA still/prompt fixes, SC01 cloth fix,
  package timecode measurement), recorded in qa/pilot-qa.md and the
  stage notes - not silent drift.
- Two schema-conformance repairs were made at this gate so health
  could pass its schema checks: _context/blocking.json and
  _context/frame0-requirements.json gained the required
  schema_version/episode_id/channel_slug fields, and blocking
  positions written as center-left/center-right (10 places) were
  normalized to the schema's left/right vocabulary, preserving the
  side in every case. No geometry changed.
- No teaser/Short was produced: the owner replaced the askyt
  assembly with a local ffmpeg cut for this hackathon sample, and
  the deliverable is the full captioned master. Recorded as an
  accepted deviation in postprod/postprod-config.json.

**STAGE VERDICT: PASS**
