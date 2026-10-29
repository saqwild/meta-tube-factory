# vidgen-ltx — one flow, three channels

A single vendor-neutral production pipeline that drives **three YouTube channel profiles**
through the same generation process:

- **image gen:** Muse Image (muse-image-1.0) via Meta Model API - identity reference sheets, and one **frame-0 still per clip**
- **video gen:** LTX-2.5 image-to-video, owner-locked PromptRelay-style beat prompts, native audio
- **render app:** vidgen-dist at [`C:\pycode\app-vidgen-dist`](file:///C:/pycode/app-vidgen-dist)
  (ComfyUI, two-stage distilled graph)
- **orchestration:** any LLM agent (Claude, Codex, Kimi, etc.) or a human — the pipeline
  contracts are plain instructions, not vendor-specific code.

No git, no commits, no change-control ledger.

> **Full Muse mode (owner-directed 2026-10-29):** every model call uses Meta models -
> see [META_MAPPING.md](/C:/pycode/vidgen-meta/META_MAPPING.md) and [SUBMISSION.md](/C:/pycode/vidgen-meta/SUBMISSION.md).
> channel.json models.image is muse-image-1.0 on all channels; every still
> records still_generator=muse-image-1.0. LTX-2.5 remains the external video renderer.

> **LTX-2.5 renders so far: three full 29-clip batches** — signed-anyway EP001 (2026-10-29)
> and EP002 (2026-10-29, live on YouTube), clover-and-paws EP001 (2026-10-29). They confirmed a
> few numbers (`img_compression`, the cfg/artifact tradeoff — now Grade [B]); most rules are
> still unproven on 2.5, and inside-the-process has never rendered. Every rule carries an
> evidence grade — see [Evidence grades](#evidence-grades--read-before-trusting-a-number).

## Flow

```bash
python tools/preflight.py
```

runs preflight checks, asks which channel profile to use, then either resumes the most recent
open episode for that channel or starts a new one, and prints the contract for whatever stage is
next. An operator (human or LLM) reads that stage's file under `pipeline/stages/`, does the
work, then runs:

```bash
python tools/preflight.py complete <channel_slug> <episode_id> <stage_id>
```

which validates the stage matches `next_stage`, checks the stage's declared deliverables and
verdict (`pipeline/stage-gates.json`), records it, and advances the episode — stopping at any
stage flagged `owner_gate` until a human runs `--approve`. A blocking verdict is never
overridden by `--approve`.

## The part worth understanding before touching anything

In i2v the image is the **frame-0 contract**: exactly one still per clip, and the clip can only
continue forward from it. That is not a detail — it shapes the whole middle of the pipeline. The
image count scales with the episode (roughly 29–32 stills for a 10-minute episode at 20-second
clips), and prompt authoring has to resolve a circular dependency:

```
04d   blocking.json — geometry decided ONCE, structured, machine-checkable
       │
04f   draft the motion, dialogue, audio, camera  ──►  frame-0 requirement block
       │                                                    │
04f2   generate N stills FROM that block, gate them  ◄──────┘
       │  ("is the clip's first action performable from this frozen instant?")
       │
04f3   re-anchor the opening clause to the APPROVED PIXELS, validate, emit final prompts
```

The prompt must describe the still's real pixels, but the still must already contain every
object the prompt's action touches — **i2v never invents objects.** Guessing in either
direction produces one of the two classic failures: a prompt that contradicts the render, or a
clip that reaches for a prop that was never drawn.

**In i2v the image is the contract; the prompt is only the delta.** A failure gets fixed at the
layer it lives in — the still, the conditioning, the render config, or the gate. Never by
adding words to a prompt.

## Three channels, one engine, zero code branching

`channel_profiles/<slug>/channel.json` is the only place a channel's identity, render numbers
and stage sequence live. `tools/preflight.py` and every stage contract read that file
generically — another channel is "drop in a new `channel.json`", not a code change.

| | Signed Anyway | Clover & Bruno Stories | Explained From Within |
|---|---|---|---|
| slug | `signed-anyway` | `clover-and-paws` | `inside-the-process` |
| format | dialogue-driven fictional financial/ethics drama, 8–11 min | photoreal anthropomorphic cat-and-dog family stories on Paw Street | source-backed "Micro-Journey" inside a real process, 9–11 min |
| cast | 10-member registry, ≤5 speaking | 7 locked masters, ≤6 speaking; anchors Clover + Bruno | on-screen Explorer + audio-only Control, 1 figure in frame |
| extra stages | `02a-sourcing` (fiction boundary), `02b-compliance` | `02b-compliance` | `01b-coverage-scan` (owner-approved coverage map + YouTube scan), `02a-sourcing` (claim + visualization ledgers), `02b-compliance` |
| clip duration | 20 s, fixed | 20 s, fixed | 20 s, fixed |
| spoken-word band | 32–36 (derived, unmeasured) | 31–34 (derived, unmeasured) | 32–36, split across two voices (unmeasured) |

Clover & Bruno arrived as a **verbatim import** of `C:\pycode\clover_and_paws\channel_profile`;
what changed afterwards and why is in `channel_profiles/clover-and-paws/bible/IMPORT_NOTE.md`.
Explained From Within was ported from the sibling `sibling-repo` repo on 2026-10-29 — its
provenance is in `local_skills/skill-lock.json`.

Every channel renders **16:9 only**. A Short survives as editorial intent and is produced as a
post-production reframe of the same 16:9 footage, never a separate still or clip batch — the
proven LTX-2.5 graph is fixed-aspect.

**Every clip is a fixed 20 seconds on every channel** — an owner decision of 2026-10-29. Each
channel profile and reference bible states that same figure. The thing to watch at pilot QA is
whether performances pad or drift in the final third.

## Evidence grades — read before trusting a number

Every rule in `pipeline/LTX_I2V_CONTRACT.md` carries a grade:

- **[A]** vendor-confirmed — docs.ltx.io and the LTX-2.5 model card, retrieved 2026-10-29
- **[B]** render-validated, on this repo's own renders or a sibling pipeline
- **[C]** `[2.3-RETEST]` — an LTX-2.3-era number kept as the safe default, **unproven on 2.5**

The old ~200-word prompt ceiling was **retired 2026-10-29** — it was LTX-2-era sibling
guidance, and both vendor sources say LTX-2.5 has no word limit. `LTXV-D004` is now only a
450-word runaway tripwire against prompt bloat. `pipeline/research/LTX25_PROMPTING_RESEARCH.md`
§6 lists the remaining open questions in priority order and §7 keeps the render findings of the
removed Cut Plane test profile; `04h`'s pilot batch is the cheapest place to settle the rest.

## Derived artifacts — generated, never hand-written

```bash
python tools/storyboard.py         --channel <slug> --episode EPxxx   # 04e
python tools/image_agent_packet.py --channel <slug> --episode EPxxx   # 04f2
python tools/ltx_prompt_manifest.py --channel <slug> --episode EPxxx --still-gate-pass   # 04f3
python tools/build_render_package.py --channel <slug> --episode EPxxx \
    --pilot SC01,SC08,... --cast "Name,..."                             # 04g
```

- **`exports/storyboard.html`** — one self-contained page, a card per clip with its still,
  dialogue, camera move and beats, for a human to scan an episode before any render spend.
- **`prompts/6-image-agent-packet.md`** — each clip's verbatim still prompt paired with that
  clip's own validation rules, handed as one file to whoever generates the stills.
- **`_context/ltx-prompt-manifest.json`** — binds every final clip prompt to the exact still it
  was re-anchored against, by hash.
- **`exports/ltx-render-package/`** — the vidgen-dist batch package. The builder refuses on a
  stale review, a `PROVISIONAL` prompts file, or a prompt/still that changed after the manifest
  hashed it, then re-reads its own output with the render app's parser to prove every
  `@@ s{n}` pairs with the right prompt and still. Its byte layout reproduces signed-anyway
  EP002's shipped package exactly.

Provenance for the ported tools and skills is in `local_skills/skill-lock.json`.

## Checking an episode

```bash
python tools/preflight.py health <channel_slug> <episode_id>
```

A read-only end-to-end pass: required deliverables for every completed stage, JSON artifacts
against `pipeline/schemas/`, one clip-id set across every manifest, every recorded SHA-256
(including each clip's prompt and still in the 04f3 manifest) against disk, review freshness,
and the final MP4s via `ffprobe`.

## Repo map

```
pipeline/             stage contracts, contracts of record, stage-gates.json, JSON schemas — the source of truth
pipeline/research/    sourced evidence behind the doctrine, with provenance and dates
local_skills/         prompt/story writers, the muse-image generator, skill-lock.json provenance
adapters/             optional per-LLM launch notes — all point back to pipeline/
channel_profiles/     channel identity + render config as data, one folder per channel
custom_stories/       owner-supplied story briefs
tools/                preflight.py (state machine), episode_state.py, episode_health.py,
                      ltx_prompt_validator.py, ltx_prompt_manifest.py, build_render_package.py,
                      render_audio_audit.py, metadata_validator.py, check_reference_assets.py,
                      still_claims.py, image_agent_packet.py, storyboard.py,
                      youtube_benchmark_validator.py, coverage_validator.py, check_download_freshness.py
episodes/             per-channel episode working directories
tests/                state-machine and gate tests, the validator regression suite, tool tests
```

```bash
pip install -r requirements.txt
python -m unittest discover -s tests
```

See [AGENTS.md](AGENTS.md) for operating rules and [pipeline/PIPELINE.md](pipeline/PIPELINE.md)
for the stage table.
