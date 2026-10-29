# 04g — LTX render package (app-vidgen-dist)

## Build it with the tool

```bash
python tools/build_render_package.py --channel <slug> --episode EPxxx \
    --pilot SC01,SC08,SC11,SC13,SC18 --cast "Evelyn,Adrian,Elena"   [--force]
```

Every step below is mechanical, so `tools/build_render_package.py` does all of it and this file
is its specification. It **refuses** unless the `04f3` review is a strict PASS from the current
validator against the current prompts file, the prompts no longer say `PROVISIONAL`, and every
per-clip prompt and still hash in `_context/ltx-prompt-manifest.json` still matches the files
on disk. After writing, it re-reads the package with the render app's own section parser and
still-filename rule (mirrored from `app/batch.py`) and fails if any `@@ s{n}` would pair with
the wrong prompt or still. Its byte layout reproduces signed-anyway EP002's shipped package
exactly. Two inputs stay human: the **pilot selection** (below) and the **cast snapshot names**
for the negative prompt. Do not hand-build or hand-edit a package.

## Target, verified

This stage emits a package the **`app-vidgen-dist`** app (`C:\pycode\app-vidgen-dist`; formerly
`C:\pycode\vidgen-dist`) ingests directly through its Batch tab. The format below was read from
that app's own source (`app/batch.py`, `app/config.py`, `workflows/`) on 2026-10-29, and the
still-pairing rule re-read on 2026-10-29 — **not** from its README, which still documents the
retired LTX-2.3 prompt-relay app and is stale. Re-verify against the source, not the docs, before
changing anything here.

```
workflow          workflows/LTX25_T2V_I2V_Two_Stage_Distilled.json
megapixels        0.98      -> 1344x768, 16:9
fps               24
duration          20        SECONDS; the graph derives 1 + floor(fps*duration/8)*8 internally
cfg / cfg_refine  1.0 / 1.0 LTXVDualCFGGuider.video_cfg, per pass
cfg_audio         1.0
img_compression   18        LTXVPreprocess — the anti-invented-character lever
steps             inert on this graph (distilled model, fixed ManualSigmas schedules)
```

**Do not hand-enter a frame count.** The graph computes it from seconds, and that is what keeps
`num_frames % 8 == 1` satisfied.

`cfg` and `img_compression` above are `vidgen-dist`'s shipped app defaults, not a fixed
requirement — pull the actual values from the channel's own `channel.json → render`, which is
render-validated per channel and takes precedence over this table (e.g. `signed-anyway` runs
`cfg 1.2` / `img_compression 22` since EP001, not the 1.0/18 default; see that channel's
`render.cfg_note` / `render.img_compression_note`).

## Inputs

Final `prompts/7-video-prompts.md`, `_context/ltx-prompt-manifest.json`, a **PASS**
`_context/ltx-prompt-review.json`, and the approved stills at `renders/stills/`.

## Task

Build `episodes/<slug>/EPxxx/exports/ltx-render-package/` containing:

### 1. `master-prompt.txt`

The batch-import file. One `@@ s{n}` marker per clip, in clip order, each followed by that
clip's final prompt verbatim:

```
@@ s1
<SC01's final prompt, the `## SC01` block body from prompts/7-video-prompts.md, verbatim>

@@ s2
<SC02's final prompt>
```

Mechanics that are not stylistic preferences:
- The clip prompts come from `prompts/7-video-prompts.md`, one `## SCnn` block each — the
  `## SCnn` header line and any `[[TAG]]` line are dropped; only the prose is copied in.
- `@@ s{n}` must sit **alone on its line**. `@@ i{n}` markers also act as section boundaries
  and are skipped by the parser.
- A leading line consisting only of `[[TAG]]` tokens is stripped before the text reaches LTX,
  so tags may be carried for human readability but never for the model.
- `{n}` is the clip's integer index (`SC01` → `1`) and must match the still's filename number.

### 2. `stills/`

The approved stills, copied — never moved — from `renders/stills/`, keeping their `SC01.png`,
`SC02.png`, … names. The app matches each still to its prompt by the **scene number that
prefixes the filename stem** (`SC07.png` and `SC07_v2.png` → `@@ s7`; an unrecognised name such
as `take3_SC07.png` is skipped, and two files with the same number make that scene ambiguous).
A mispaired batch renders successfully and looks plausible, so the tool verifies every pairing
mechanically; the owner still eyeballs the pairing in `exports/storyboard.html` at the gate.

### 3. `render-settings.json`

The exact settings above, recorded so a render is reproducible and a drift is visible. Duration
is **20 seconds for every clip on both channels**, an owner decision of 2026-10-29. Both channel
profiles and both bibles state the same figure; if you find one that does not, it is a bug.

### 4. `render-manifest.json`

Schema `pipeline/schemas/ltx-render-package.schema.json`. Per clip: index, prompt SHA-256,
still path and SHA-256, spoken-word count, declared cuts, and the settings block. Plus a
package-level count and the source `ltx-prompt-manifest.json` hash, so a package can be proven
to match the prompts it was built from.

### 5. `negative-prompt.txt`

The single negative prompt for the batch, assembled — not invented — from three parts:

1. `pipeline/negative-prompt-base.txt` — model-level artifact terms, verbatim.
2. `channel.json` → `render.negative_prompt_additions` — that channel's style and safety terms.
3. **One `second <Name>` term per cast member appearing this episode**, from the episode's cast
   snapshot. Identity duplication is the failure this catches, and it can only be written once
   the cast is known.

**This is the only place suppression lives.** LTX-2.5 has a real negative channel; the same
terms in a positive prompt cause the exact artifact they name, and `LTXV-D010` rejects them
upstream. If you find yourself wanting to add "no captions" to a clip prompt, it belongs here.

## Pilot subset

Mark, in `render-manifest.json`, the clips selected for `04h`'s pilot batch. Selection covers at
minimum: the opening clip, a dense or multi-speaker dialogue clip, a multi-character staging
clip, a difficult prop interaction, and an environment/camera continuity pair. At least five
clips, more where one cannot cover a category.

## Forbidden

Do not change any approved prompt or still here — packaging copies, it does not author. Do not
render, upload or publish. Do not write a per-clip duration, aspect or resolution field; those
are render-session settings. Do not build a package from a review file containing a FAIL. Do
not move stills out of `renders/stills/` — `04f2` owns them.

## Stop condition

**Owner gate.** Last checkpoint before GPU spend. The package is complete when every clip has a
`@@ s{n}` block, a correctly numbered still, a manifest entry with matching hashes, and the
prompt-to-still pairing has been verified by eye rather than assumed from the filenames.
