# 04h — LTX representative pilot QA

This stage exists because `04g`'s pilot selection is a recommendation, not a gate. This is the
gate that enforces **watching real rendered pixels** before the full batch spends GPU budget.

## Inputs

The owner-approved `exports/ltx-render-package/`, plus human-rendered pilot clips. The
vidgen-dist app (`C:\pycode\app-vidgen-dist`) writes rendered clips and their sidecars to its own output folder; the operator places them
under `episodes/<slug>/EPxxx/renders/ltx-inbox/`.

## Task

Render the pilot subset marked in `render-manifest.json` at the package's declared settings —
one settings profile for the whole pilot batch, recorded once at the top level, never per clip.

For each pilot clip, **human-watch** and record a PASS/FAIL verdict against each check below.
The first is the one that matters most and the one most often fudged:

1. **Beat adherence.** Did the named action actually happen, in its beat's place in the clip?
   Aggregate motion, "it looks alive", and file size are **not evidence either way**. Name the
   action; say whether it occurred.
2. **Frame-0 fidelity.** Does the clip actually start from the approved still, or does it drift
   or re-stage in the first half-second?
3. **Dialogue.** Authorised words only — no invented, paraphrased or dropped lines. Audible and
   intelligible. Delivered inside the clip rather than rushed or padded.
4. **Speaker binding and lip sync.** The right character's mouth moves; non-speakers stay
   closed-mouthed.
5. **Identity and cast count.** No drift from the reference sheets; no invented extra character.
6. **Prop count and interaction.** No duplication, no lingering ghost of a prop, contacts land.
7. **Environment and camera.** Stable geometry, only the intended ambient motion, and the camera
   movement `blocking.json` declared.
8. **Audio.** Clean start and tail, the named ambient bed present throughout, no invented
   speech filling silence.
9. **Artifacts.** No burned-in captions or model-rendered text; no anatomy failures.

## Also record the open questions

A pilot batch is the cheapest chance to settle the open questions in
`pipeline/research/LTX25_PROMPTING_RESEARCH.md` §6 — above all on a channel's **first** render
(as of 2026-10-29, inside-the-process has never rendered; signed-anyway and clover-and-paws
have). Where a pilot clip happens to
answer one — prompt length, dialogue occupancy at 20 seconds, mouth-lock necessity,
`img_compression 18`, frame-0 adherence strictness — record the observation and promote it into
`LTX_I2V_CONTRACT.md` with its evidence grade upgraded from **[C]** to **[B]**.

**Only measured findings get promoted.** An impression is not a verdict.

## Output

`episodes/<slug>/EPxxx/qa/ltx-pilot-qa.json` — schema
`pipeline/schemas/ltx-pilot-qa.schema.json`. `qa/` is a top-level folder, a sibling of `story/`,
`visual/`, `prompts/`, `renders/` and `exports/`. Its top-level `status` is `PASS` only when
every check on every pilot clip passed; the completion gate refuses a `FAIL` even with
`--approve`.

## Forbidden

Do not change any prompt, still, render setting, clip, story beat or acceptance criterion here.
This stage watches and records; it does not fix. Do not fill in a verdict for a clip nobody
watched.

## Stop condition

**Owner gate.** A human must actually watch the pilot clips. An agent may prepare the scaffold —
clip selection, the checks structure — but may not supply verdicts it did not watch for.

Any failed check fails the **entire stage** and returns to the stage that owns the fix:
`04f3`/`04f` for a prompt problem, `04f2` for a still problem, `04d` if the geometry itself was
wrong. A correction goes through normal process and the **entire** pilot set is re-rendered from
the renewed package — not just the clip that failed, and never a silent per-clip patch.

PASS on every pilot clip authorises the remaining renders and hands off to `05-render-ingest`.
This gate does not itself render, upload or accept the final master.
