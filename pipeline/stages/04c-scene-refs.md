# 04c — environment and prop reference plates (Muse Image)

## Scope

Reusable **reference plates** for places and props — the same distinction as `04b`: persistent
guides, not frame-0 stills. A clip's actual first frame is generated at `04f2`.

## Inputs

`visual/scene-list.md`; existing environment/prop reference assets for the channel, if any
recur.

## Task

Generate any environment plate or reusable prop this episode needs and does not already have,
with **Muse Image**.

Environment-only references do not need identity-lock treatment the way cast does, but they
must match the channel's locked visual-style language — palette, lighting, photoreal-versus-
stylised — exactly. **Copy the full style string from the reference bible verbatim per
generation.** Muse Image is stateless between calls and will not remember a prior scene's environment
unless you restate it; "the same locked kitchen as before" produces a different kitchen.

For every prop that recurs, fix **one permanent identifying visual mark** now — "one flat dent
beneath the handle" — and record it. That exact wording is restated verbatim every time the
prop appears, in every still and every clip prompt, for the whole episode. Without it the model
has nothing to be consistent with, and the prop quietly becomes a different object scene to
scene.

Name the **visible place**, never who owns it. A model cannot render ownership; an owner's
proper noun is dead tokens at best and summons an unwanted extra character at worst.

## Output

`episodes/<slug>/EPxxx/visual/references/scenes/EP<id>-ENV0XX-<name>.<ext>` for environment
plates and `EP<id>-PROP0XX-<name>.<ext>` for reusable props — flat, same folder.

Plus the shared `visual/references/manifest.md`, which for this stage must carry, per entry:
the **full locked environment string** to be reused verbatim downstream, and each prop's
**permanent identifying detail**.

Plus `_context/environment-locks.json` — `{tag: locked_string}` for every `ENVnnn`/`PROPnnn`
this episode gated, machine-readable copies of the same locked strings above. This is what
feeds `LTXV-D054`: a clip's prose is checked against it for ground/terrain words that aren't
actually in the plate. Added 2026-10-29 after a clip claimed "grass" against a plate that is
pure wooden decking — inherited unedited from the script, written before this stage locked
the real environment, and nothing checked the two against each other until this file existed.
Write it once, here, from the same locked strings — do not hand-author a second description.

This file is a **should, not a must** in `pipeline/stage-gates.json` (deliberately NOT listed
as a required `04c-scene-refs` output there) — `episode_health.py`'s `check_required_files()`
re-checks every already-completed stage's outputs against the CURRENT `stage-gates.json` on
every health run, for every episode, so adding a hard requirement here would retroactively
flag every episode/stage completed before 2026-10-29 that predates this convention (confirmed:
`signed-anyway` EP001 is still open and would FAIL required-files; EP002 is closed and would
WARN). New episodes should still write it — the validator's `LTXV-D054` check is silently
skipped, not failed, when it's absent, so there's no forcing function beyond this instruction.

## Forbidden

Do not generate characters here (that is `04b`) or frame-0 stills (that is `04f2`). Do not
shorthand a previously "locked" environment — restate it in full each time. Do not use an
ownership label as scenery.
