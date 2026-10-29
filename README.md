# meta-tube-factory

**A documentary-grade AI film factory for YouTube — end to end on Meta Muse models.**

One flow. Unlimited channels. Add a channel by adding one channel profile;
the factory does the rest. This is not a Shorts factory and not a one-off
clip generator: it runs a full production pipeline — ideation, coverage,
research, compliance, script, visual development, render package, QA, and
distribution metadata — with a validator gating every stage before money is
spent.

> Built for the Meta Global AI Developer Hackathon. See
> [SUBMISSION.md](SUBMISSION.md) for the submission summary and
> [META_MAPPING.md](META_MAPPING.md) for the model allocation.

## The Meta stack

Five Meta models, five organs. Every call goes through one client,
`tools/meta_models.py`, to the Meta Model API (`https://api.meta.ai/v1`,
key: `MODEL_API_KEY`).

### Muse Spark series — the main brain

`muse-spark-1.3`. The best reasoning/planning model from Meta.
Research synthesis, scriptwriting support, compliance, SEO, and coverage
logic — every decision stage (01b, 02, 02a, 02b, 03b, 04d, 04f, 04f3, 06)
runs on Spark.

### Muse Wonder — the creative brain

`muse-wonder-1.0`. Deep multi-step reasoning plus story planning.
Complex branching, moral dilemmas, and plot consistency — the script
(03a) and the visual brief (04a) run on Wonder.

### Muse Image — the eyes

`muse-image-1.0`. Image generation and edit.
Character refs (04b), scene refs (04c), storyboards (04e), frame-0 stills
(04f2), thumbnails, and B-roll.

### Muse Voice Transcribe — the ears

`muse-voice-transcribe-1.0`. Speech to text.
Caption QA, audio audit (`tools/render_audio_audit.py`), and voiceover
transcription at render QA (05a).

### SAM 3.1 — the hands

`sam-3.1`. Finds and separates each item in a photo or video.
Segmentation, character consistency checks, and background isolation at
pilot QA (04h).

Video rendering itself is LTX-2.5 i2v, an external owner-run renderer —
no Muse video generation model exists. Muse Glimmer and Muse Spark Open
are open-weight, self-hosted only, not called from this repo.

## One flow, multiple channels

`channel_profiles/<slug>/channel.json` is the only place a channel's
identity, cast, look, render numbers, compliance, and stage sequence live.
Every tool and stage contract reads that file generically — **a new channel
is a new `channel.json`, never a code change.**

Three starter profiles ship as examples. The submission demos **one**
channel end to end; the other two exist to prove the factory is generic.

| Starter profile | Format | Demo role |
|---|---|---|
| `inside-the-process` — Explained From Within | Source-backed journey inside a real process, 9–11 min | **Demo channel** |
| `signed-anyway` | Dialogue-driven financial/ethics drama, 8–11 min | Example profile |
| `clover-and-paws` — Clover & Bruno Stories | Anthropomorphic family stories | Example profile |

Every channel renders 16:9, fixed 20-second clips at 24 fps (481 frames).
A Short is a post-production reframe of the same footage, never a separate
still or clip batch.

## The pipeline

One episode walks its channel's stage sequence, one stage at a time.
Each stage has a plain-text contract under `pipeline/stages/`; an operator
(human or agent) does only that stage's work, then completes it through
`tools/preflight.py`, which checks deliverables and verdicts before
advancing. Owner-gated stages stop until a human approves.

**Phase 0 — Foundation:** `00-preflight`

**Phase 1 — Ideation / Research:** `01-ideation`, `01b-coverage-scan`,
`02-research`, `02a-sourcing`, `02b-compliance`

**Phase 2 — Writing:** `03a-writer`, `03b-script-review`

**Phase 3 — Visual Development:** `04a-visual-brief`, `04b-character-refs`,
`04c-scene-refs`, `04d-shot-plan`, `04e-storyboard`, `04f-ltx-prompt-draft`,
`04f2-frame0-stills`, `04f3-ltx-prompt-final`, `04g-ltx-render-package`,
`04h-ltx-pilot-qa`

**Phase 4 — Render / QA:** `05-render-ingest`, `05a-render-qa`

**Phase 5 — Distribution:** `06-distribution-metadata`,
`06a-postproduction-assembly`, `07-final-package-qa`

Phase 3 is the differentiator. In image-to-video, **the image is the
contract; the prompt is only the delta**: one approved frame-0 still
conditions exactly one clip, the draft prompt declares what that still
must contain, the still is generated and gated against it, and the final
prompt is re-anchored to the approved pixels. A failure is fixed at the
layer it lives in — still, conditioning, render config, or gate — never
by adding words to a prompt. Every character is described facing the
camera, never with a speaking character's back to the lens.

## What you actually have

**`tools/` — 18 production tools**, including `meta_models.py` (the Meta
Model API client), `preflight.py` (the stage state machine),
`episode_state.py` (atomic, locked episode state), `episode_health.py`,
`coverage_validator.py`, `youtube_benchmark_validator.py`,
`ltx_prompt_validator.py`, `ltx_prompt_manifest.py`,
`build_render_package.py`, `image_agent_packet.py`, `storyboard.py`,
`render_audio_audit.py`, `metadata_validator.py`, `clip_split_check.py`,
`check_reference_assets.py`, `check_download_freshness.py`,
`still_claims.py`, and `project_paths.py`.

**`tests/` — 15 test modules** (307 tests) covering every validator, the
state machine and its owner gates, derived-artifact freshness, and the
Meta model client. One known pre-existing failure expects a signed-anyway
EP001 metadata package that does not exist in this repo.

**Derived artifacts are generated, never hand-written:** the storyboard,
the per-clip image agent packet, the hash-bound prompt manifest, and the
render package. Builders refuse to run on a stale review or a prompt/still
that changed after it was hashed.

## Run it

```bash
pip install -r requirements.txt
python tools/meta_models.py config   # key present? models wired?
python tools/meta_models.py smoke    # one live Muse Spark call
python tools/preflight.py            # resume or start an episode
python -m unittest discover -s tests
```

Set `MODEL_API_KEY` in your environment or a local `.env` (never commit
it; see `.env.example`).

## Repo map

```
channel_profiles/  channel identity + render config as data, one folder per channel
pipeline/          stage contracts, contracts of record, stage gates, JSON schemas
tools/             the 18 production tools above
tests/             validator and state-machine test suites
local_skills/      prompt/story writer skills and provenance (skill-lock.json)
adapters/          optional per-agent launch notes, all pointing back to pipeline/
custom_stories/    owner-supplied story briefs
episodes/          per-channel episode working directories (empty until you start one)
```

See [AGENTS.md](AGENTS.md) for operating rules and
[pipeline/PIPELINE.md](pipeline/PIPELINE.md) for the full stage table.

