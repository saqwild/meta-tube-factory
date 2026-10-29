# 04a — visual brief

## Inputs

`story/script.md`, `story/characters.md`, `channel_profiles/<slug>/channel.json` → `render`
and `format`.

## Task

Break the script into a scene list with, per scene: which cast members appear, which
environment, and what new reference assets (if any) this scene requires that don't already
exist as locked references.

For `inside-the-process`, each scene also records the **interior it is set in** (the organ, material or device named by the title, at the scale where the process
happens) and whether it is a **locator** (an outside view used only to show where that interior sits). An inside scene is never an outside view of a digital model
(`bible/VISUAL_STYLE_CONTRACT.md` → "Inside means inside").

This is the last stage before any image or video prompt gets written — it decides *what* needs
a new Muse Image reference sheet versus what an existing locked asset already covers.

### Estimate the clip count, and with it the still count

Under LTX-2.5 i2v the generation unit is the **clip**, and **every clip needs its own frame-0
still**. So this stage's clip estimate is also the episode's image budget:

```
clips ≈ ceil(target_runtime_seconds / render.clip_duration_seconds)
stills = clips          (plus the N variants each generate-and-select loop discards)
```

At the channel's 20-second clip, a 570-second episode is roughly 29 clips and therefore 29
approved stills. State the number here. It is what makes the cost of `04f2` visible before
anyone commits to a scene structure, and it is the difference from the previous engine, where
images were a fixed handful of per-episode references rather than a per-clip artifact.

Also sanity-check the dialogue load against `render.spoken_word_band`: a scene carrying
materially more quoted words than its clip count can hold is a scene that needs splitting, and
this is the cheapest place to notice it.

## Output

`episodes/<slug>/EPxxx/visual/scene-list.md`, including the estimated clip count and the
resulting still count.

## Forbidden

Do not write prompts here. Do not author blocking (that is `04d`). Do not assume an asset is
reusable without checking it actually exists under the channel's locked-reference location.
