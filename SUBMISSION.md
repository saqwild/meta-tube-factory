# Hackathon submission — vidgen-meta

Meta Global AI Developer Hackathon. Approved project, $150 Model API credit.
All hackathon calls go through [tools/meta_models.py](/C:/pycode/vidgen-meta/tools/meta_models.py)
to `https://api.meta.ai/v1` with `MODEL_API_KEY`. Model allocation is in
[META_MAPPING.md](/C:/pycode/vidgen-meta/META_MAPPING.md).

## What it does

One pipeline (`pipeline/`) drives YouTube episodes stage by stage. Each stage
has a plain-text contract, free local validators gate every paid call, and the
episode state machine (`tools/episode_state.py`) records provenance per artifact.

No demo episode yet. All prior EP folders were removed on 2026-10-29; the first hackathon episode starts fresh as a new EP001 via python tools/preflight.py, totally on Muse models plus LTX-2.5 i2v.

## Verified 2026-10-29

- `python tools/meta_models.py config` — key present, base URL and model IDs correct.
- `python tools/meta_models.py smoke` — live `muse-spark-1.3` call returned `ok` (exit 0).
- `python tools/meta_models.py call --role creative` — live `muse-wonder-1.0` reached the API.
- `python -m unittest tests.test_meta_models` — 9 tests OK (allocation, endpoints mocked, key never printed).
- Full suite: 307 tests, 306 pass. One pre-existing failure:
  `test_signed_anyway_ep001_package_passes` expects a signed-anyway EP001
  metadata package that does not exist in this fork. Not a hackathon blocker;
  do not fabricate that package to make it green.

## Not yet done — owner actions

- No episode exists yet. Start one fresh with `python tools/preflight.py` (stage 00), one stage at a time; owner gates still need human `--approve`.
- `muse-image-1.0`, `sam-3.1`, `muse-voice-transcribe-1.0` endpoints are wired
  and unit-tested with mocked transport, but not yet called live. First live
  image spend happens only after still prompts freeze (stage 04f2).
- Muse Glimmer and Muse Spark Open gate roles are defined in README (free local guards via Modal). They must be run live during the EP001 proof and receipts recorded here before submission; until then this is architecture, not verified usage.
- LTX-2.5 rendering and postproduction are external owner-run tools; they earn
  no Meta credit and are unchanged history for prior episodes.

## Credit plan ($150)

1. Text first: Spark/Wonder for the fresh episode stages 01b–03b, validators free between calls.
2. Images only after prompts freeze: pilot a few clips at 04h before a full batch.
3. SAM on approved stills only; Voice Transcribe on rendered clips only.
Avoid: regenerating locked bible sheets, stills for three channels before a pilot,
and Wonder for cheap checks Spark can do.
