# Render host — LTX-2.5 i2v execution design (owner-approved 2026-10-29)

The pipeline never renders in-process. At 04g it emits a render package
(approved frame-0 stills + hash-bound LTX prompts). This document decides
how those clips get made and returned.

## Path A — rented GPU via SSH (primary)

Local GPU probe first: this machine has no NVIDIA GPU (`nvidia-smi` not
found, 2026-10-29). When no local CUDA GPU is usable, the operator is
asked for the rented host SSH target (`user@host:port`) for that session
only. SSH details are never stored in this repo.

Default vast.ai host profile (owner-stated, confirm at connect):

| Field | Default |
|---|---|
| GPU | NVIDIA RTX PRO 6000, 96 GB VRAM |
| Storage | 80 GB |
| CUDA | 13.x |
| Template | ComfyUI (vast.ai) |
| Workflow | LTX-2.5 two-stage distilled (`LTX25_T2V_I2V_Two_Stage_Distilled.json` in vidgen-dist) |

Connect checklist (logged in the episode recording log at 04h):
1. SSH in; record `nvidia-smi` GPU name, VRAM, CUDA, free disk.
2. Run `tools/pod/ltx25load_distilled.txt` (copy of the owner's pod
   loader; SHA-256 2DF602294005FE0508A62203E7E3243459BA7C485DD8F87E6BF6AC4DB9F25CF2).
   It hash-verifies the five pinned LTX-2.5 BF16 artifacts (~66 GiB).
   Risk: 80 GB storage is tight against ~66 GiB models + staging;
   confirm free space before download, prefer the fp8 loader if short.
3. Upload the 04g stills and prompts; queue the 3 pilot clips first.
4. Download clips + vidgen-dist sidecars (`.mp4` + `.json` + `.txt`)
   into the episode `renders/` folder with exact clip IDs.
5. Owner pilot verdict at 04h before the remaining clips render.

Models live only on the pod. Only the loader script is copied into this
repo for the record (tools/pod/, above) — model weights are never committed.

## Path B — owner manual drop (fallback)

04g prints one drop folder with a sidecar per clip: clip ID, still hash,
prompt hash, expected 20 s / 24 fps / 16:9. The owner renders anywhere
and saves MP4s there under exact clip-ID names. 05-render-ingest
validates hash, duration, fps and aspect against each sidecar and fails
closed on mismatch before 05a transcription QA.

## vidgen-dist execution check (2026-10-29)

`C:\pycode\app-vidgen-dist` was read-only verified from this window:
`python app/rules_guard.py status` runs (exit 0, 0 modified, 2 added -
drift is reported, never silent), and its protected workflows include
the canonical `LTX25_T2V_I2V_Two_Stage_Distilled.json` (481 frames at
20 s / 24 fps). Its README header still says LTX-2.3 - that text is
stale; the rules log and workflow list are authoritative.

vidgen-dist itself is a PyQt GUI (`python main.py`) expecting a ComfyUI
tunnel at localhost:18188 - it is owner-run, not a headless batch API.
This repo therefore treats it as: owner-operated renderer on Path A/B,
with its sidecars as provenance. Anything this pipeline writes stays
inside this repo; vidgen-dist is never modified here (AGENTS.md).
