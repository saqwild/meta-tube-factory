# 04f — LTX-2.5 clip prompt draft

## Writer authority

**`local_skills/ltx-production-writer/SKILL.md` is the sole writer for this stage.** The global
`ltx25-prompting` skill runs strictly *after* compilation at `04f3`, as a read-only syntax and
conformance check against the official LTX-2.5 format — it never drafts, enhances, paraphrases
or rewrites. If a conformance check fails, the clip returns to the production writer, not to
the syntax skill.

Read, in this order, before writing anything: this file;
`local_skills/ltx-production-writer/SKILL.md`; `pipeline/LTX_I2V_CONTRACT.md`;
`pipeline/ltx_prompt_validator.md`; the approved shot plan, `_context/blocking.json`, the
storyboard, and `visual/references/manifest.md`.

## Why this stage runs before the stills

i2v has a circular dependency. The prompt must match the still's real pixels, but the still
must already contain every object the prompt's action touches — **i2v never invents objects.**
Guessing in either direction produces one of the two classic failures: a prompt that
contradicts the render, or a clip that reaches for a prop that was never drawn.

The pipeline resolves it by splitting authoring across three stages:

```
04f   draft the beats: motion, performance, dialogue, audio, camera  -> + frame-0 requirement block
04f2  generate the still FROM that block, gate it                    -> approved pixels
04f3  re-anchor the GLOBAL:: line from those pixels, validate        -> final prompts
```

This stage owns the first box. It writes every beat of the clip **except** a final `GLOBAL::`
anchor, which cannot honestly be written until a still exists.

## Inputs

`visual/shot-plan.md`, `_context/blocking.json`, the approved storyboard,
`visual/references/manifest.md`, `channel_profiles/<slug>/channel.json` → `render` and
`format`.

## Task

One owner-locked PromptRelay-style beat prompt per clip — one `GLOBAL::` continuation anchor
plus `BEAT:: <frames> ::` lines totalling 481, no loose timing markers, no negation in the
positive. Content order, required clauses, dialogue handling and the forbidden list all live
in `LTX_I2V_CONTRACT.md`; the writer skill
carries the template and a worked example.

Geometry is **projected from `blocking.json`, never re-decided here.** The establishing pose
comes from `chars.<TOK>.pos/facing/gaze/pose`; the action sequence walks `anchors` in order;
the settle tail matches `end_state`; the camera movement is `camera.movement`. If an entry
looks wrong once you are looking at the actual staging, flag it back to `04d` rather than
silently overriding it.

Mark the `GLOBAL::` line **provisional**. It will be re-anchored at `04f3` against real pixels;
the `BEAT::` lines and frame counts are written to stand. Say so in the file header with the
literal word `PROVISIONAL` (e.g. "Every `GLOBAL::` line below is PROVISIONAL"): the `04f3`
completion gate refuses to pass while that word is still in the file, so the re-anchor pass
cannot be skipped by accident.

### Emit the frame-0 requirement block

Per clip, alongside the prose — this is the handoff that makes `04f2`'s still derivable rather
than guessed, and it is validated by `LTXV-S001`/`S002`/`S003`:

```
clip, touched_objects, characters, frame0_state (pos/facing/gaze/pose/expression/mouth/hands
per character), props_at_rest, first_action_performable, continues_from, end_state
```

Two fields carry real weight:

- **`touched_objects`** — every object a character contacts, lifts, leans on, reaches for, or
  treats as a focal object. Walk the prose and list them. An omission here is how a clip ends
  up reaching for a prop that does not exist in its own first frame.
- **`first_action_performable`** — asserting `true` means you actually checked that the clip's
  opening action can begin from that frozen instant. It is not a formality.

## Output

- `episodes/<slug>/EPxxx/prompts/7-video-prompts.md` — the single clip-prompt file, one
  `## SCnn` block per clip (a leading `[[TAG]]` line is metadata, dropped before the model
  sees it). This one file is the canonical prompt source for `04f3`, the storyboard, the
  validator and `04g` — there are no per-clip `.txt` files. **`prompts/` is a top-level
  folder, a sibling of `visual/` and `story/`**, never nested under `visual/`.
- `episodes/<slug>/EPxxx/_context/frame0-requirements.json` — the requirement blocks, schema
  `pipeline/schemas/frame0-requirements.schema.json`.
- Optionally `prompts/NOTES.md` for rationale that belongs in neither.

## Forbidden

Do not generate any image here. Do not finalise the `GLOBAL::` anchor. Do not invent an object,
prop or character that the blocking spec, the references and the prior clip all fail to
establish. Do not run the validator's final pass — that is `04f3`, after the pixels exist.

## Stop condition

Every clip has a draft prompt and a complete frame-0 requirement block whose
`first_action_performable` has actually been checked, not assumed.
