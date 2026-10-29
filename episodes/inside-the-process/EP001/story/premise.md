# EP001 - Project Brief / Premise (inside-the-process, hackathon demo)

## Title

How Bread Rises: Inside the Dough

## Logline

A miniature Explorer rides inside a ball of dough from flour and water
to a sliced loaf, showing how yeast gas, a gluten net, and oven heat
turn mud into bread.

## Runtime target

Demo sample: 4 minutes (240 s), 16:9 - twelve 20-second clips.
This is a shortened proof episode. The channel long-form format is
9-11 minutes; the demo keeps every production stage identical and only
reduces the clip count. Owner decision 2026-10-29.

## Cast count

One figure in frame (the Explorer); two voices (Explorer helmet-radio +
off-screen Control). No other speaking characters.

## Viewer question

"Why does bread dough rise, and what actually happens inside it in the oven?"

## Full process chain

1. Milled flour, water, yeast, and salt as separate raw ingredients.
2. Mixing: flour hydrates, a shaggy wet mass forms.
3. Kneading: gluten strands link into an elastic network.
4. Bulk fermentation: yeast feeds, releases carbon dioxide gas.
5. Gas bubbles inflate and stretch the gluten network; dough rises.
6. Degassing and shaping: large bubbles redistributed, loaf formed.
7. Proofing: second rise, bubbles expand again in the shaped loaf.
8. Baking, early: oven spring - gas expands, yeast dies, starch swells.
9. Baking, late: crust sets, browning, steam escapes.
10. Cooling: crumb sets, moisture redistributes, loaf firms.
11. Finished result in use: a sliced loaf, soft crumb inside a crisp crust.

## Proposed scope

States 2-11: from mixing bowl to sliced loaf. Out of scope, named here
for 01b: growing and harvesting wheat, and milling grain into flour.
Each is a separate process and gets an on-screen disclosure if 01b
requires it.

## Owner rationale

Bread was chosen over glass, battery, screen, caffeine, concrete, and
sneeze topics because its process is a sequence of slow visible state
changes - exactly what LTX-2.5 image-to-video renders best from one
frame-0 still per clip. Every stage is visually distinct, low-risk for
compliance, and gives SAM 3.1 real segmentation work on bubbles, dough
mass, and crust across states.

## Hackathon execution note

Totally Muse: Muse Spark reasoning, Muse Wonder script, Muse Image
stills (still_generator=muse-image-1.0), SAM 3.1 pilot QA, Muse Voice
Transcribe render QA, via tools/meta_models.py. LTX-2.5 i2v is the
external video renderer. A fresh EP001: no prior episode artifacts are
reused.
