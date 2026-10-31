# EP001 pilot QA (04h, in progress)

Pilot clips: SC01, SC02, SC05, SC08, SC12. No verdict is final until
the owner has watched each clip; frame grabs below support, never
replace, that viewing.

## SC01 - s01_20261031222018.mp4 - FAIL (owner + frame check)

- Spec check: 20.04 s, 1344x768, 24 fps, native audio present. PASS.
- Finding (owner, confirmed on frames f1/f3/f5 in qa/frames-s01/):
  the clip starts with the dough uncovered (matching the still), then
  drapes the cloth over the bowl - the reverse of the scripted lift.
  Mid and end frames show the dough dome visible through/above the
  cloth: the bread is neither fully covered nor uncovered.
- Root cause layer: prompt delta, not the still. Beat 1 said "The cloth
  lifts slowly" without stating direction or end state; the model chose
  covering. Fix at 04f3 for SC01 only: state the adult lifts the cloth
  clear of the bowl, holds it aside, dough fully uncovered at end.
- Action: re-render SC01 only after the prompt fix. Do not re-roll the
  still; SC01 still is correct (uncovered dough, cloth in hand).

## Remaining pilots

SC02, SC05, SC08, SC12: awaiting owner viewing and verdicts.

## SC02, SC03, SC04 - owner viewed 2026-10-29

- Verdict: PASS (owner watched; clips look fine).
- Post note for 06a assembly: trim dead-silence tails on rendered clips during postproduction. This is an assembly trim, not a re-render: keep each clip's dialogue and productive tail action, cut only trailing silent frames, and record per-clip trim ranges in the assembly notes at 06a.

- SC05 (s05 render): owner viewed 2026-10-29 - PASS. Dead-silence tail trim at 06a if present, as with SC02-SC04.

- SC06 (s06 render): owner viewed 2026-10-29 - PASS. Dead-silence tail trim at 06a if present.

## Owner overall review (2026-10-29) - process-focus revision

- Overall: dialogue feels short with dead tails (trim at 06a); too many clips end on the Explorer. Show the tech/process, not the presenter.
- SC01 REVISE: capsule now descends into the risen dough (transition into the interior); cloth beat already fixed. Note: dough doubling is proofing warmth, not oven heat - oven spring stays SC08.
- SC02 PASS, SC03 PASS (owner).
- SC04 REVISE still: yeast/bubble macro, Explorer small at edge.
- SC05 REVISE still: stretched net fills frame.
- SC06 REVISE (agent review): Explorer hands were gripping strands - violates never-touch rule; regenerated hands empty at sides, process wide.
- SC07 REVISE still: slow proofing bubbles wide, Explorer small.
- SC08 REVISE still: expanding bubbles/dome fill frame.
- SC09 PASS (owner); more dialogue requested - spoken band is capped 38-42 words/clip by channel format, so no added lines without a format change; perceived shortness is the dead tail, fixed by 06a trims.
- SC10 REVISE still: crumb surroundings fill frame.
- SC11 REVISE still: set cooling crumb per spoken content.
- SC12 REVISE still: bread zoom, person cropped at edge.
- All revised clips: final prompt beats now end on the process, not the Explorer. Stills regenerated, strict validator PASS, manifest/package rebuilt. Awaiting owner re-render of SC01, SC04-SC08, SC10-SC12.
