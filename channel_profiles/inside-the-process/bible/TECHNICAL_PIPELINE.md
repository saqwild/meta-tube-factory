# Technical Pipeline

## Production stack

| Stage | System | Role |
|---|---|---|
| Research/writing | Repository stage contracts and source ledgers | Evidence, claims, script and state planning |
| Reference sheets | Muse Image | Explorer, capsule, environment identity locks (04b/04c) |
| Frame-0 stills | Muse Image | One settled-state still per clip (04f2), the literal first frame each clip is conditioned on |
| Video/audio | LTX-2.5 i2v | Fixed 20-second motion with native dialogue, soundscape and music |
| Render app | `vidgen-dist` (read-only from this repo) | Runs the ComfyUI LTX-2.5 workflow this channel's `render.workflow` names |
| QA/edit | ffprobe, frame review, transcript check, `tools/ltx_prompt_validator.py`, `tools/image_agent_packet.py` | Integrity, prompt-contract and material-impact QA |
| Post-production | `askyt_editor` + Remotion | Episode-local A/V-locked staging, captions, approved overlays, master and teaser assembly |

This channel has never rendered on LTX-2.5 — everything below is this repo's
general, cross-channel LTX doctrine applied to this channel's own numbers.
Nothing here is channel-specific render evidence yet.

## Prompt authority chain

For `render.mode: i2v` (every channel in this repo, including this one):

1. `local_skills/ltx-production-writer/SKILL.md` is the sole writer for `04f`
   (draft) and `04f3` (final) clip prompts, using the `GLOBAL::`/`BEAT::`
   beat-packet syntax (`channel.json` → `render.prompt_format`).
2. `local_skills/frame0-still-writer/SKILL.md` is the sole writer for `04f2`
   frame-0 stills, deriving each still from that clip's frame-0 requirement
   block — never authored independently ahead of the clip prompt.
3. `tools/ltx_prompt_validator.py` validates every compiled clip prompt
   against `pipeline/ltx_prompt_validator.md` / `pipeline/LTX_I2V_CONTRACT.md`.
   It never rewrites prose.
4. The global `ltx25-prompting` skill runs strictly **after** compilation, as
   a read-only syntax check — it never drafts.

The project contracts are `pipeline/LTX_I2V_CONTRACT.md` (clip prompts) and
`pipeline/MUSE_FRAME0_CONTRACT.md` (frame-0 stills).

## Geometry authority — `04d`

Unlike a single-image-reference engine, LTX-2.5 i2v needs the clip prompt and
the frame-0 still to agree about pose, gaze, facing and prop state, or they
will silently disagree (a still where a character faces camera and a clip
that describes them looking at someone else). `04d-shot-plan` decides this
geometry once, in `_context/blocking.json` — both prompt stages are
projections of it, and neither re-decides it. Facing is always described
**relative to the camera**, never relative to another character (universal
`AGENTS.md` rule, and load-bearing for this channel's Explorer/Control
shot-reverse-shot pattern).

## Per-clip source package

Each fixed 20-second clip has:

- one approved 16:9 frame-0 still (`04f2`) as the literal opening frame;
- one `_context/blocking.json` entry (pose, gaze, expression, mouth, hands,
  prop resting state, camera movement, end state) that both prompt stages
  read rather than re-decide;
- one dominant observable process action, expressed as `GLOBAL::`/`BEAT::`
  beats;
- exact native dialogue words within the channel's `render.spoken_word_band`
  when dialogue is authorized;
- native source-bound soundscape and an authorized score or explicit `N/A`;
- validator review (`LTXV-*` rule ids) before acceptance.

The frame-0 still must already solve Explorer/capsule identity and scale,
focal process state, environment geometry, contact and composition. The clip
prompt animates and reveals that state; it does not redesign it — the
channel's one governing principle from `AGENTS.md`: **in i2v the image is the
contract; the prompt is only the delta.**

## Native audio policy

Clip prompts may carry native Explorer dialogue, Control's off-screen voice,
diegetic process sound, ambience and score in one generation. Independent
generations can vary in voice timbre — see `channel.json` →
`render.voice_lock_note` for why no byte-identical voice string exists yet
for this channel's two speakers. Treat the native result as shot audio to be
reviewed and edited, not a promised reference-locked voice.

## Live pilot gate — `04h`

Before authorizing a full render batch, `04h-ltx-pilot-qa` requires a human to
watch real rendered pixels for the pilot subset: beat adherence, frame-0
fidelity, dialogue accuracy, speaker binding/lip sync, identity/cast count,
prop interaction, environment/camera stability, audio, and artifact-freedom.
Because this is this channel's first LTX-2.5 render, it is also the cheapest
chance to settle this channel's own open questions — notably the
dual-voice `spoken_word_band` question flagged in `channel.json`, and whether
`calibration_note`'s carried-from-signed-anyway render settings (cfg,
img_compression, workflow) actually hold for this channel's photoreal,
two-speaker content. Promote a settled question from grade **[C]** to **[B]**
with the measured evidence, in `channel.json`, not by impression.

## File integrity

- Ingest real `vidgen-dist` render output plus its sidecar into
  `renders/ltx-inbox/`.
- Hash video, prompt, workflow and references.
- Probe codec, duration, resolution, frame rate and audio stream at ingest.
- Preserve original generated files in history before an editorial replacement.
- Keep credentials out of manifests and logs.

## Remotion post-production

- Stage `06a-postproduction-assembly` runs `askyt_editor/run_episode.py` from
  the episode-local model: `scenes_dir`/`working_dir`/`output_dir` all live
  under `episodes/inside-the-process/EPxxx/postprod/`, never `sceneprocess/`.
- A/V-lock every staged clip before assembly (`-c:v copy -af apad -t <exact
  video seconds>`) — LTX-2.5 renders ship video and audio a few dozen
  milliseconds apart, which otherwise compounds into audible lip-sync drift
  across a batch boundary. See `pipeline/stages/06a-postproduction-assembly.md`
  for the full mechanism.
- Preserve native LTX-2.5 dialogue, soundscape and music. Add no replacement
  narration or score by default.
- Burn captions in the channel palette and one 8%-width, 85%-opacity emblem
  at top-left. Disable YouTube Studio's separate video watermark to prevent
  duplication.
- Produce both the long master and a no-spoiler discovery teaser, then
  require a full human watch before approval.
- First-appearance callouts (short on-screen labels for a scientifically
  important entity) are chosen per episode from the approved claim/visual
  ledger — this channel has no fixed callout list until an episode exists.
