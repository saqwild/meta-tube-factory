# Technical Pipeline — i2v First

## Decision

Use **LTX-2.5 image-to-video** as the technical core because this channel depends on recurring-character identity, native dialogue/audio and reusable performance references. LTX Video 2.5 remains the publication-safe fallback and the utility model for exact first-frame shots.

Use **FLUX only for static reference creation**. FLUX text-to-image originates the first approved character portrait and environment anchor; FLUX image-to-image derives each character's full-body and six-panel references and any controlled environment/prop variants. It is not an episode-video model in this pipeline. Record the exact checkpoint, generation settings, seed where available, and commercial-use licence evidence before accepting an asset.

This is a **technical lock, not yet a legal publication lock**. See `COMPLIANCE_GATE.md`.

## Why i2v first

| Requirement | i2v advantage |
|---|---|
| Recurring examiner and evidence specialist | Reuses identity and wardrobe references across many shots |
| Dialogue performance | Native audiovisual generation within the same shot prompt |
| Reusable sets/props | Subject references reduce the need to regenerate a unique still for every clip |
| Production scale | One approved reference pack can support many compositions |
| Complex shot anchor | A `<Picture N>` can still be used when an exact concrete frame is necessary |

I2V remains useful, but making 40 independent Frame-0 images creates a second continuity system and a second failure surface. Use it selectively, not as the default.

## Model routing

| Asset or shot need | Primary route | Fallback |
|---|---|---|
| First character identity portrait | Muse Image text-to-image | None; re-run with a tightened identity prompt |
| Portrait-derived full-body and six-panel pack | Muse Image, conditioned on the approved portrait as a reference asset | Rerun or simplify; no second image model |
| Environment and reusable-prop reference plate | Muse Image | Rerun or simplify; no second image model |
| Shot need | Primary route | Fallback |
|---|---|---|
| Recurring dialogue close-up/two-shot | LTX-2.5 i2v from the approved frame-0 still | Re-roll the still, then re-render |
| Exact evidence composition | Compose it in the frame-0 still; the clip only moves forward from it | Re-roll the still |
| Silent transition/inserts | LTX-2.5 i2v, the same graph as every other clip | Re-roll the still |
| High-motion reconstruction | Keep the motion plausible and split it across clips; chaotic physics still artifacts | Simplify the action |
| Publication | Cleared: LTX-2.5 is an open-weights release rendered locally, with no per-output display gate |

## Clip prompt contract

There is no sectioned prompt format. Every clip prompt is a single continuous
chronological paragraph of native prose, with no subject labels and **no timing
syntax of any kind** - ordering comes only from chronological connectives
("Initially...", "A moment later...", "As she finishes speaking...").

Each prompt opens on shot scale and a named character, continues forward from
the approved frame-0 still, carries an `Ambient (slow, subtle):` visual-motion
sentence and a separate `Acoustic environment:` sound sentence, folds every
dialogue line into the speaker's visible action, states one motivated camera
movement, and ends on a productive tail rather than a frozen pose.

The binding authority is `pipeline/LTX_I2V_CONTRACT.md`, and every compiled
prompt is checked by `tools/ltx_prompt_validator.py` before it can be packaged.

## Production settings

| Stage | Starting setting | Purpose |
|---|---|---|
| Prompt/continuity proof | 0.98 MP, 20 sec, 24 fps | Fast rejection of identity, blocking, dialogue and audio failures |
| Final dialogue clip | 0.98 MP, 20 sec, 24 fps | Approved performance render |
| Master | 16:9 timeline, 24 fps | Long-form assembly |
| GPU planning rate | US$1.10/hour | Vast.ai budget assumption; verify at rental time |

Render-time benchmarks for this stack have not been measured yet. Record them from the first pilot batch rather than carrying a figure across from a different model.

MP values are runtime-manifest settings, never prompt prose. Create a new batch
manifest with `tools/render_profile_override.py` to switch all scenes between
`test_0.4mp` and `production_0.98mp`; preserve the approved source manifest,
prompt hashes, references, workflow and seeds. A persistent selector inside the
downstream render application is a separate app change outside this repository.

## Cost model

For `N` final-generation attempts averaging `m` minutes:

`GPU cost = N × m ÷ 60 × hourly rate`

Substitute this episode's own clip count and the render time measured from the first pilot batch; no render-time figure for this stack has been measured yet. Storage, reference and frame-0 still generation, failed rentals, upscaling and post work are all additional. Do not confuse clip count with final runtime: 30 × 20 seconds equals ten minutes only if every second survives the edit, which is unrealistic once trims, reactions and rerenders are considered.

Plan an initial 8–11 minute episode, targeting 9:30, around **30–36 approved 20-second clips** — and therefore the same number of approved frame-0 stills. Many clips will be trimmed shorter in the final edit.

## Workflow

1. Lock script and shot timing.
2. Build/approve FLUX static reference packs: portrait first, then portrait-derived full-body/sheet and required environment/prop stills; archive checkpoint, settings, seeds and licence evidence.
3. Compile shot manifest with labels, speaker IDs, eyelines, starting/ending states and audio needs.
4. Run 0.4 MP proofs for all dialogue and difficult motion.
5. Reject identity, lip, timing, hand, prop, eyeline and audio failures.
6. Render only approved shots at 0.98 MP.
7. Add readable evidence graphics, sound repair, room tone, captions and grade in post.
8. Archive prompts, seeds/settings, references, selected renders and rejection reasons.

## Failure policy

- Never repair a wrong identity with aggressive face replacement when a rerender is viable.
- Never accelerate dialogue to fit a clip; split the line.
- Never trust generated document text.
- If three rerenders fail for the same blocking/action, simplify the shot or move the information to an insert.
- Never geo-restrict an ordinary YouTube upload to work around a model-licensing question; resolve the licence or change the model.
