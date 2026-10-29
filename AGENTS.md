# Operating rules — vidgen-ltx

## Domain

- Keep every read, write, and generated artifact inside `C:\pycode\vidgen-meta`.
- This copy is a hackathon-adapted fork: owner-authorized 2026-10-29 to adopt Meta models for new hackathon work. History and bibles stay intact; new work records its real generator.
- This repo is **self-contained**. Each channel's deep brand/cast/compliance bible was copied
  in full into `channel_profiles/<slug>/bible/`. Do not add a dependency back on the source
  repos those copies came from.
- `channel_profiles/<slug>/bible/` is a point-in-time copy: treat it as immutable reference,
  **not something a stage edits.** It was last revised outside that rule on 2026-10-29, by the
  owner-directed conversion, to bring every render-dependent figure in line with the current
  stack — clip duration, aspect, prompt format, model licensing. A stage still may not touch it.
- Reading `C:\pycode\app-vidgen-dist` (the vidgen-dist LTX render app; it lived at
  `C:\pycode\vidgen-dist` until 2026-10) and `C:\pycode\askyt_editor` (the
  postproduction tool) is in scope **read-only**, to verify each tool's real ingest contract,
  config schema and settings before a stage builds a handoff package for it. Never write to
  either. `C:\pycode\sceneprocess\` is `askyt_editor`'s own runtime scratch — a stage never
  reads or writes there. Staging clips into it, running the tool, and copying the finished
  video back into the episode folder are **owner actions**, the same way rendering through
  `vidgen-dist` is: the stage produces the handoff, the owner runs the external tool, and an
  in-repo ingest step records the results.
- No other local project is in domain.
- **No git.** State lives in plain JSON (`episodes/<channel>/<EPID>/episode-state.json`) and a
  plain-text append log (`episode-state-log.md`). There is no change-control ledger and no
  commit-hash chain of custody. Because that JSON *is* the whole record, `tools/episode_state.py`
  writes it atomically (temp file + `os.replace`), keeps the last good copy as
  `episode-state.json.bak`, appends the log line before advancing the state, and takes a
  per-episode `episode-state.lock` around any stage-advancing operation. Never hand-edit
  `episode-state.json`; if it is ever reported corrupt, recover from the `.bak`.

## Single active stage

One episode has exactly one `next_stage`. Whoever is driving — human, Claude, Codex, Kimi, or
any other agent — reads that stage's contract under `pipeline/stages/`, does only that stage's
declared work, writes only its declared outputs into the episode folder, then runs
`python tools/preflight.py complete <channel> <episode_id> <stage_id>` and stops. Do not run
two stages in one pass and do not skip ahead because a later stage looks easy.

## Owner gates

A stage marked `owner_gate: true` in the channel's `pipeline_stages` list requires a human to
run `complete ... --approve` before the episode advances. An LLM agent may prepare that stage's
output but may not self-approve past the gate. At `04h` specifically, an agent may prepare the
QA scaffold but **may not supply a verdict for a clip nobody watched.**

## Channel profile is authoritative for identity and numbers

`channel_profiles/<slug>/channel.json` holds render parameters, format/runtime numbers,
metadata-validation constants, and the stage sequence for that channel. Stage contracts
describe *process*; they read numbers from `channel.json`, they don't hardcode them. If a
contract and `channel.json` disagree, `channel.json` wins for that channel.

**Where `channel.json` deliberately contradicts a channel's own bible, it says so in a `_note`
field with the date and the reason.** Do not "fix" such a value back to the bible figure — read
the note first. There are none outstanding: as of 2026-10-29 the bibles were brought in line, so
`channel.json` and `bible/` agree on clip duration, aspect and prompt format.

## Model scope

- **Image generation: Muse Image.** Two structurally different jobs that must never be
  confused:
  - **Reference sheets** (`04b`/`04c`) — persistent identity locks for characters, places and
    props. A handful per episode, reused, promoted across episodes on second use.
  - **Frame-0 stills** (`04f2`) — **one per clip**, the literal first frame that clip is
    conditioned on. Episode-local, never reused, never showing motion.

  Muse Image identity lock across many generations is looser than a dedicated character workflow.
  Treat cast drift as a first-class QA check, and re-anchor a derivative from the same locked
  reference **image** rather than a text description.

  **Generator: Muse Image only** via `tools/meta_models.py image` (Meta Model API, `muse-image-1.0`). No alternate image generator. Whichever Muse model made an episode's stills is recorded per clip as `still_generator` in `_context/ltx-prompt-manifest.json`. `channel.json` `models.image` is `muse-image-1.0` on every channel.

- **Video generation: LTX-2.5, i2v.** Owner-locked PromptRelay-style beat prompts (one `GLOBAL::` anchor plus `BEAT:: <frames> ::` lines totalling 481), native audio. The generation unit is the
  **clip**: one approved frame-0 still conditions exactly one generation. Every clip on every
  channel in this repo is a **fixed 20 seconds** at 24 fps, 16:9 — read the figure from
  `channel.json`, never from a stage contract or a sibling pipeline.

- **The prompt writer for `04f`/`04f3` is `local_skills/ltx-production-writer/SKILL.md`**, and
  for `04f2` it is `local_skills/frame0-still-writer/SKILL.md`. The global `ltx25-prompting`
  skill runs strictly **after** compilation, as a read-only syntax check — it never drafts,
  enhances, paraphrases or rewrites, and where it disagrees with
  `pipeline/LTX_I2V_CONTRACT.md` the contract wins. Every compiled prompt is validated against
  `tools/ltx_prompt_validator.py` / `pipeline/ltx_prompt_validator.md` before acceptance.

- **The one principle: in i2v the image is the contract; the prompt is only the delta.** A
  failure gets fixed at the layer it lives in — the still, the conditioning, the render config,
  or the gate. **Never by adding words to a prompt.**

- **Universal rule — camera-relative facing.** Every shot describes a character's facing
  relative to the **camera**, never relative to another character. No bench, podium or
  head-of-table geometry that puts a speaking character's back to the lens. This applies to
  every channel.

- **Real LTX-2.5 renders so far: three full 29-clip batches** — signed-anyway EP001
  (2026-10-29) and EP002 (2026-10-29, live on YouTube), and clover-and-paws EP001 (2026-10-29).
  signed-anyway EP001 promoted `img_compression 22` and the base-pass cfg figures to Grade
  **[B]** (see `channel.json`'s `cfg_note` / `img_compression_note` and research §6 q4). Every
  other rule in `LTX_I2V_CONTRACT.md` is still graded **[A]** vendor-confirmed, **[B]**
  render-validated on a sibling pipeline, or **[C]** an LTX-2.3-era number kept as a safe
  default and unproven on 2.5 — a few low-motion episodes are not a general proof, and
  inside-the-process has never rendered. Do not upgrade a **[C]** to
  fact without a real render, and do not quietly loosen one without evidence either. The next
  pilot batch at `04h` is the cheapest chance to settle the rest — see
  `pipeline/research/LTX25_PROMPTING_RESEARCH.md` §6.

## Hackathon overlay

For new hackathon work, Meta models are authoritative: reasoning/planning Muse Spark, deep multi-step work Muse Wonder, image generation/edit Muse Image, speech-to-text Muse Voice Transcribe, segmentation/tracking SAM 3.1, local/open-weights Muse Glimmer and Muse Spark Open, coding Muse Code — all through Meta Model API. Do not invent SDK names, model versions, or packages. Do not rewrite `bible/` history or prior episode artifacts; add the Meta layer to new work and record the real generator per artifact.

## Fiction and disclosure

Whatever a channel's `compliance` block in `channel.json` declares (real-world non-depiction
rules, AI-disclosure text, made-for-kids setting) is binding for every episode produced under
that profile. Stage `02b-compliance` runs before a script exists; a `BLOCKED` verdict there
stops the episode with no further stage authorized.

A channel's `hard_safety_floor` is binding on every prompt, image and clip. On an
anthropomorphic channel this includes: **every background figure is stated as an
anthropomorphic animal**, explicitly. A bare "neighbours", "kids" or "crowd" renders as
photoreal humans — the validator catches it (`LTXV-D042`), but the rule is the author's.

## Derived artifacts come from tools, and every ad-hoc script is kept

`_context/ltx-prompt-manifest.json` (04f3) is written by `tools/ltx_prompt_manifest.py` and the
04g render package by `tools/build_render_package.py` — never by hand. Both refuse to run on a
stale review, a PROVISIONAL prompts file, or a prompt/still that changed after it was hashed.

Any one-off script that generates or rewrites a deliverable (a still re-generation batch, a
clip renumbering, a bulk fix) is saved in the episode at `_scripts/<yyyy-mm-dd>-<purpose>.py`
before it runs, and its log beside it — not in the repo root, not in a temp folder. A QA record
that cites a script must cite a file that exists: an unreproducible fix is not an audit trail.

## Universal agent contract

Before doing anything: read this file, the active stage's contract, the episode's
`episode-state.json`, and only that stage's declared inputs. Perform exactly one stage. Never
edit another stage's artifacts, another episode's files, a schema, a channel profile's
`channel.json` render/identity numbers (propose a change to the human instead of editing it in
place), or anything outside this repo. Give a concise confirmation naming what was written,
then stop.
