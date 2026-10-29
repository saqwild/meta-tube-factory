# Production workflow

## Stack

Muse Image creates static references at `04b`/`04c` and frame-0 stills at
`04f2`. LTX-2.5 creates clip-level motion through this repo's standard i2v
pipeline. Each approved frame-0 still is the exact opening frame and the clip
prompt directs its motion, causal state change, camera, dialogue, soundscape
and music. The active contracts are `pipeline/LTX_I2V_CONTRACT.md` (clip
prompts) and `pipeline/MUSE_FRAME0_CONTRACT.md` (stills) — this channel has no
per-channel prompt-framework doc; the shared `local_skills/ltx-production-writer`
and `local_skills/frame0-still-writer` skills are the writers for every
channel in this repo, including this one.

Source render settings live in `../channel.json`. Preserve this repo's
mode-specific project-local production writers, matching official syntax
guide, blocking spec and validator. The generic global `ltx25-prompting`
skill is a read-only format authority, not the production writer. Concept
prompts from a conversation are not production-ready LTX prompts.

## Before references

Approve the story, sources and visualization conventions. At `04a` identify
required identity sheets, environment geometry, focal process entities and
composition/process-state references. Start with the state BEFORE the action.

## At 04b/04c

Create and review the Explorer identity, capsule prop, location and process
references per `KEY_CHARACTER_PROMPTS.md`'s templates (Explorer master sheet,
Capsule master sheet, composed Explorer-in-capsule plate). A composed scene
may incorporate an already approved Explorer reference at 04c, but may not
invent or redesign the character.

Record exact paths, model/tool, source references, prompt and approval status
in `visual/references/manifest.md`. Process entities and initial-state plates
are static reference assets. Never mark an image as approved, generated or
locked if only its prompt exists.

If the named Muse Image integration is unavailable, prepare prompts and
asset specifications for the owner, and stop that stage short of completion
until the actual reviewed image files exist. Do not silently substitute a
different image model.

## At 04d — geometry, once

`04d-shot-plan` decides pose, gaze, expression, mouth, hands, prop resting
state, camera movement and end-state for every clip in `_context/blocking.json`
— see `TECHNICAL_PIPELINE.md`'s "Geometry authority" section. Neither the
clip-prompt stage nor the still stage may re-decide it; a disagreement is
flagged back here, not patched downstream.

## At 04f/04f2/04f3

Each clip uses one approved frame-0 still as its exact opening frame. `04f`
drafts the `GLOBAL::`/`BEAT::` clip prompt and its frame-0 requirement block;
`04f2` derives the still from that requirement block (never the reverse);
`04f3` finalizes the clip prompt against the approved still. No extra
character, environment, prop, style or audio reference is sent to the
renderer beyond what that single still already composes.

Only one continuous-shot environment geometry anchor. Separate micro and
macro locations into different clips. Use approved Explorer and Control
dialogue in the native prompt within the channel's spoken-word band; LTX-2.5
also generates the source-bound soundscape and authorized score. Do not
insert off-screen radio dialogue as a visible physical speaker merely to
satisfy a validator.

Read resolution and render-setting values from the channel profile.
Workflow/quality selection remains one global render-session setting per
pilot batch, not per-clip prompt prose (`TECHNICAL_PIPELINE.md`'s "Live pilot
gate" section).

## At 04h and after

Choose a representative opening, hard contact/transformation clip and
continuity handoff. Human-watch them under `04h-ltx-pilot-qa`'s checklist
before rendering the remainder. Frame inspection alone cannot certify audio,
lip-sync, exact playback timing, or the dual-voice pattern this channel adds
beyond the sibling channels' evidence.

Ingest only real `vidgen-dist` files under `renders/ltx-inbox/` and record
hashes/probe data. Editing uses the approved sequence, voice plan, labels and
source notes.
