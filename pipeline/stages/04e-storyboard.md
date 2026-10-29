# 04e — storyboard

## Inputs

`visual/shot-plan.md`, `_context/blocking.json`, and whatever exists so far under `prompts/` —
still prompts, approved stills, clip prompts. All optional: the storyboard's job includes
showing what is *missing*.

## Task

Build a single self-contained page — one card per clip, with its frame-0 still, pose note,
camera move, beats and dialogue — so a human can scan the whole episode in one scroll before any
render spend.

```bash
python tools/storyboard.py --channel <slug> --episode EPxxx
```

Deliberately simple: one HTML file, a responsive card grid, stills embedded as data URIs, no
scripts and no external assets. It opens from disk with nothing installed.

A clip with no approved still yet renders as a labelled **pending** placeholder rather than being
omitted. The gaps are the point of the page; a storyboard that quietly skips what does not exist
tells you an episode is ready when it is not.

## When to run it

This stage sits before the prompt stages, so its **first** run is mostly placeholders — a shape
check on coverage, pacing and cast spread. Re-run it after `04f2` to review real pixels, and
again before the `04g` owner gate. It is cheap, derived, and safe to regenerate at any time; it
is never an input to a generation model.

## Output

`episodes/<slug>/EPxxx/exports/storyboard.html`.

## Forbidden

Do not hand-edit the generated HTML — it is derived, and an edit is lost on the next run. Fix the
underlying artifact instead. Do not feed it to a model as a reference image.

## Stop condition

Owner reviews the storyboard. A rejection returns to whichever stage owns the problem: `04d` if
the coverage or blocking is wrong, `04f2` if a still is wrong, `04f`/`04f3` if a prompt is.
