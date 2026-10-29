# META_MAPPING — Meta model roles for hackathon work

All hackathon calls go through `tools/meta_models.py` to Meta Model API.
Key: `MODEL_API_KEY` env var (or repo-local `.env`). Base: `https://api.meta.ai/v1`.
CLI: `python tools/meta_models.py config|allocation|smoke|call|image|segment|transcribe`.
IDs verified against dev.meta.ai/docs/models on 2026-10-29.

## Allocation (requested names → official Model API IDs)

| Role | Requested | Official model ID | Endpoint | Status |
|---|---|---|---|---|
| reasoning | muse-spark | `muse-spark-1.3` | `POST /v1/responses` | wired |
| creative | muse-wonder | `muse-wonder-1.0` | `POST /v1/responses` | wired |
| image | muse-image | `muse-image-1.0` | `POST /v1/images/generations` | wired |
| segment | sam-3.1 | `sam-3.1` | `POST /v1/responses` | wired |
| transcribe | muse-voice-transcribe | `muse-voice-transcribe-1.0` | `POST /v1/asr/transcribe` (multipart, WAV) | wired |
| local_fast | muse-glimmer | — (open-weight) | self-hosted only | not a Model API ID |
| local_open | muse-spark-open | — (open-weight) | self-hosted only | not a Model API ID |

Changes from the requested short names: every hosted model needs its
version suffix (`-1.3` / `-1.0`); the bare names are not callable IDs.
Suggested change: do not allocate Glimmer/Spark Open to API stages — they
run on your own hardware. Use `muse-spark-1.3` for cheap repeated checks
instead of `muse-wonder-1.0`.

## Per-stage allocation

Defined as `STAGE_ALLOCATION` in `tools/meta_models.py`:
01/01b/02/02a/02b/03b/04d/04f/04f3/06 reasoning (`muse-spark-1.3`);
03a/04a creative (`muse-wonder-1.0`); 04b/04c/04e/04f2 image
(`muse-image-1.0`); 04h segment (`sam-3.1`); 05a transcribe
(`muse-voice-transcribe-1.0`).

## Forward rule for images

New hackathon stills and reference sheets use `muse-image-1.0` only, and
record `still_generator=muse-image-1.0` per artifact. Legacy channel
masters under `channel_profiles/*/locked-references/` stay on disk as
identity history — inputs, never claimed as hackathon output, never
deleted (AGENTS.md: bible/history intact). No new hackathon work may
default to a legacy image generator (`muse-image-1.0` / `muse-image-1.0`
remain only as historical provenance in old artifacts and tests).

History note: prior episodes used non-Meta stills and LTX-2.5 renders.
That history is unchanged; new hackathon artifacts record their real
generator per file.
