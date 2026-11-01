# meta-tube-factory

**▶ Watch the sample film: <a href="https://youtu.be/UapzJhl72m0" target="_blank" rel="noopener">How Bread Rises: Inside the Dough (EP001, unlisted)</a>** — produced end to end by this factory: script, stills, QA, captions and metadata all generated through the pipeline below and approved at human gates.

<a href="https://youtu.be/UapzJhl72m0" target="_blank" rel="noopener"><img src="https://img.youtube.com/vi/UapzJhl72m0/hqdefault.jpg" alt="How Bread Rises: Inside the Dough - EP001 sample film"></a>

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
pilot QA (04h). On an independent run this is the standard validation
path for frame-0 stills and pilot clips: SAM checks the cast and props
the still claims, before any render money is spent.

*Sample note:* for this EP001 hackathon sample the owner chose to
validate pilot stills and clips by direct watched review instead
(owner gates at 04f2/04h, plus the Muse Voice Transcribe audit at
05a). That was a sample-submission exception, not the factory's
default; the SAM seat in the pipeline is unchanged.

Video is LTX-2.5 i2v. Frame-0s are Muse Image validated by SAM 3.1
on independent runs (owner-review exception for the sample, above).
Glimmer and Spark Open are open weights: each operator runs them
wherever they choose (below); paid Muse Spark/Wonder calls run only
after the free gates pass.

### Free gate before the paid gate

The open-weight models never duplicate the API models. They guard them.
Being open weights, **where they run is the operator's choice**:
downloaded onto a local GPU, served with SGLang, run inside a ComfyUI
host, or on a serverless GPU provider. For this hackathon submission
we used Modal, because the event offered participants credit for
exactly that; nothing in the pipeline depends on Modal, and an
operator with their own GPU pays nothing and needs no account.

- **Muse Glimmer (open weights, $0 API cost)** — ultra-fast preflight gate:
  `tools/preflight.py`, `tools/check_download_freshness.py`,
  `tools/project_paths.py`. Does the file exist? Is the hash stale? Is the
  owner gate approved? If Glimmer says no, paid Spark is never called.
- **Muse Spark Open (open weights, $0 API cost)** — local compliance gate:
  `tools/metadata_validator.py`, `tools/episode_state.py`, and durability
  checks. Privacy-sensitive checks stay offline, and the 307-test suite
  runs without spending API credit.

API models are the paid brain, spent only on work that passed both free
gates. Local open weights are the free guards. That split is spend control,
not duplication.

## Human in the loop — the safety system

Automation drafts. Humans decide. The factory never publishes, never
spends render budget, and never locks identity or scope without a person.

- **Owner gates.** Stages flagged `owner_gate` in a channel profile stop
  hard until a human runs `preflight.py complete ... --approve`. An agent
  may prepare the work; it may never self-approve past a gate. At pilot QA
  (04h), no agent may record a verdict for a clip nobody has watched.
- **Compliance before script.** Stage `02b-compliance` runs before a word
  of script exists. A BLOCKED verdict stops the episode outright.
- **Scope lock.** At `01b` the owner approves what a complete explanation
  must answer. Later stages may add to it, never silently shrink it.
- **Verdicts, not vibes.** Every stage completes only when its validator
  returns a passing verdict bound to the exact file hashes it read. Any
  later edit makes that verdict stale and blocks completion.
- **Spend control.** Validators are local and free; paid Muse calls happen
  only after the free checks pass, so credit is spent on approved work.

This human-gated design is the point: the factory is a production house
with an accountable owner, not an unattended content pump.

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

You do not drive the `.py` tools stage by stage. You run **Muse
Code** inside this repo and talk to it in plain language; the agent
reads the operating rules, does one pipeline stage at a time, and
stops at every owner gate for your approval. The commands below are
all the setup there is.

### 1. Install Muse Code

Windows (PowerShell):

```powershell
irm https://dev.meta.ai/install.ps1 | iex
```

macOS / Linux:

```bash
curl -fsSL https://dev.meta.ai/install.sh | bash
```

### 2. Get the repo and open it

```bash
git clone https://github.com/saqwild/meta-tube-factory.git
cd meta-tube-factory
pip install -r requirements.txt
```

Set `MODEL_API_KEY` in your environment or in a local `.env` file
(never commit it; see `.env.example`). Then start Muse Code in
this folder.

### 3. Start with a natural prompt

Examples of how an episode actually starts and continues:

> Review the repo, check if anything is pending, then start a new
> episode for inside-the-process.

> The new episode is "How Bread Rises: Inside the Dough". Run the
> next stage, then stop and show me what you produced.

> Approve 04g.

The agent resumes from `episode-state.json`, works the single active
stage, and waits at owner gates (script review, render package,
pilot QA, metadata, assembled cut) until you approve in plain words,
exactly as EP001 above was produced. Rendering itself happens in the
external LTX app from the package the pipeline hands you; the agent
tells you when, and what to bring back.

### Adding a new channel

A channel is data, not code — one folder under `channel_profiles/`.

1. Copy the sample channel folder to your new channel's slug:
   `channel_profiles/inside-the-process` →
   `channel_profiles/<your-slug>`.
2. Ask the model to adapt it, for example:

> Review the sample channel files I copied into
> `channel_profiles/<your-slug>` and update each file for my niche:
> [describe your niche, audience, and format]. Keep the same schema
> and stage sequence; change identity, cast, compliance, and format
> numbers only where my niche requires, and draft the channel bible
> to match instead of keeping the sample channel's.

3. Start an episode on the new channel with the same natural prompt
   as above, naming your channel.

### Changing the video engine

The video generation process is **locked to LTX-2.5 image-to-video
through a ComfyUI host** (this repo drives it through the vidgen-dist
batch app: approved frame-0 still in, PromptRelay-style beat prompt
in, 20-second native-audio clip out). That lock is deliberate — the
prompt validator, the frame-0 contract, and every QA gate in Phase
3–4 are tuned to what LTX-2.5 i2v actually does.

Different operators will want different engines, and the factory is
built so that choice is a prompt, not a fork. If you want MiniMax,
a fal-hosted model, an ElevenLabs audio flow, or any other provider,
ask the model in plain language, for example:

> Replace the video generation process (LTX-2.5 via ComfyUI) with
> MiniMax on fal. Keep the script, stills, QA, and metadata stages
> unchanged; adapt only the render-package stage, re-tune the prompt
> contract and validator for the new engine, and tell me what
> changes before you edit.

Expect the agent to change the render-package builder, the prompt
format for that channel, and the ingest checks — and to flag anything
the new engine cannot do (native dialogue, 20-second fixed clips,
frame-0 conditioning) before spending anything. The rest of the
factory — ideation, coverage, compliance, script, stills, human
gates, captions, metadata — carries over untouched. A swap can also
be scoped to one channel profile, leaving the others on LTX-2.5.

### Under the hood (optional checks)

```bash
python tools/meta_models.py config   # key present? models wired?
python tools/meta_models.py smoke    # one live Muse Spark call
python tools/preflight.py resume inside-the-process EP001
python -m unittest discover -s tests
```

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

