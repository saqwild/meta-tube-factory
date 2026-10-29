# 04f3 — LTX-2.5 clip prompt final

## Writer authority

**`local_skills/ltx-production-writer/SKILL.md`**, second pass. The global `ltx25-prompting`
skill runs at the end of this stage as a read-only conformance check — it never drafts,
enhances, paraphrases or rewrites, and if it disagrees with `pipeline/LTX_I2V_CONTRACT.md` the
contract wins.

## Why this stage exists

An opening clause written before a still existed is a guess, and it contradicts the render
often enough to be a named failure class. Now that `04f2` has produced approved pixels, the
prompt gets re-anchored to what the still **actually shows** — not the plan carried forward
unedited.

This is a small stage by word count and a load-bearing one by consequence.

## Inputs

`prompts/7-video-prompts.md` (the draft clip prompts, `## SCnn` per block),
`prompts/6-image-prompts.md`, `_context/frame0-requirements.json`, the **approved stills** at
`renders/stills/` and their `qa/still-gate.md` verdicts, `_context/blocking.json`,
`channel_profiles/<slug>/channel.json` → `render` (spoken-word band, style echo, clip duration,
cast rules, safety floor).

## Task

1. **Re-anchor the `GLOBAL::` line of every clip** against its approved still. Shot scale,
   identity anchors, wardrobe, environment, fixed props, light and the closing style echo must
   describe the real pixels. Where the still gate recorded an observation that differs from the
   draft's assumption, the still wins. The `BEAT::` lines and their frame counts normally stand.
2. **Re-check the beats against the still.** Usually they survive unchanged. If they
   does not, the still is wrong and the clip returns to `04f2` — the prose does not bend around
   a bad frame.
3. **Run the validator in strict mode** over every clip. It reads
   `prompts/7-video-prompts.md`, the `_context/` artifacts and the channel profile, runs
   `validate_prompt` per clip **and** the cross-checks in step 4, and exits non-zero on any
   error:
   ```bash
   python tools/ltx_prompt_validator.py --channel <slug> --episode EPxxx --strict --emit-review
   ```
   **`--strict` is mandatory at 04f3** — it requires every clip to have a `blocking.json`
   entry, a `frame0-requirements` block *and* a still in `6-image-prompts.md`, and FAILs any
   clip that does not (a draft run without `--strict` silently skips the checks those inputs
   feed and can PASS with the cross-checks never run). `--emit-review` writes
   `_context/ltx-prompt-review.json` stamped `mode: "strict"`; the `04f3` completion gate
   (`pipeline/stage-gates.json`) accepts **only** a strict review with `status: PASS`. Zero
   `LTXV-*` errors. Warnings are recorded, not silently cleared. The validator reports only —
   it never auto-fixes, and a failure returns the clip to the writer.
4. **The cross-checks** (run automatically by step 3; in strict mode a missing input FAILs the
   clip rather than skipping the check):
   - `LTXV-S002` — every `touched_objects` entry is visible in the approved still and named in
     the prose. (needs `_context/frame0-requirements.json`)
   - `LTXV-S003` — the clip's cast matches `blocking.json`. (needs both `_context/` files)
   - `LTXV-S004` — each continuing clip opens where its predecessor's `end_state` left it.
   - `LTXV-S005` / `LTXV-S006` — the still is bound to the right clip and does not already show
     the completed end state of an action the clip performs. (needs `prompts/6-image-prompts.md`)
5. **Run the global `ltx25-prompting` conformance read** last, as a read-only check.
6. **Build the manifest with the tool — never by hand:**
   ```bash
   python tools/ltx_prompt_manifest.py --channel <slug> --episode EPxxx --still-gate-pass \
       [--still-generator "<model>"]   # default: channel.json models.image
   ```
   It derives every field from disk and **refuses** unless the review from step 3 is a
   strict PASS from the current validator against the current prompts file, the prompts file
   no longer says `PROVISIONAL`, and every clip has its blocking entry, frame-0 block and
   exactly one still. `--still-gate-pass` is your attestation that `qa/still-gate.md` records a
   PASS for every still **as it is now on disk** — a still regenerated after its gate verdict
   needs a new verdict first. Any later edit to a prompt or still makes the manifest stale; the
   04g packager and `episode_health.py` both catch that.

**Step 1 is not optional, and the gate checks it.** 04f writes its file header saying every
`GLOBAL::` line is `PROVISIONAL`. The re-anchor pass rewrites those lines and replaces that
header; `stage-gates.json` refuses to complete 04f3 while the word `PROVISIONAL` is still in
`prompts/7-video-prompts.md`. Deleting the word without doing the re-anchor defeats the one
check this stage exists for.

## Output

- `episodes/<slug>/EPxxx/prompts/7-video-prompts.md` — **edited in place**: the re-anchored
  final prompts replace the draft prose in the same `## SCnn` blocks. There is no separate
  `prompts-draft/` or per-clip `.txt` file; this one file is what `04g` packages.
- `episodes/<slug>/EPxxx/_context/ltx-prompt-manifest.json` — written by
  `tools/ltx_prompt_manifest.py` (step 6), schema
  `pipeline/schemas/ltx-prompt-manifest.schema.json`: per clip, `prompt_path`
  (`prompts/7-video-prompts.md` for every clip) and the SHA-256 of that clip's block body,
  its still path and SHA-256, the frame-0 requirement block, cast, spoken-word count, declared
  cuts, and the camera movement taken from blocking.
- `episodes/<slug>/EPxxx/_context/ltx-prompt-review.json` — schema
  `pipeline/schemas/ltx-prompt-review.schema.json`: per clip, which rule IDs were checked and
  their PASS/WARN/FAIL status.

## Forbidden

Do not change a still here. Do not edit `blocking.json`. Do not let the validator or the
conformance skill rewrite a prompt — both report only. Do not advance a clip whose review
verdict is FAIL. Do not add words to a prompt to compensate for a problem that lives in the
still — in i2v the image is the contract and the prompt is only the delta.

## Stop condition

Every clip has a final prompt, a matching approved still, and a review entry with zero errors.
`04g` refuses to build a package from a review file containing a FAIL.
