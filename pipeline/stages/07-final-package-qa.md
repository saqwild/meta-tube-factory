# 07 — final package QA

## Inputs

Every artifact produced for this episode, including `postprod/postprod-manifest.json` and
`exports/final/EPxxx_<Title>_Full.mp4` / `..._Short.mp4` from `06a-postproduction-assembly`.

## Task

Final human sign-off that the episode package is complete and internally
consistent: script, references, render manifest, render QA, metadata, and the
assembled final video/teaser all agree with each other and with the channel
profile's constraints. Specifically re-verify — do not just trust that `06`
produced them correctly:

- A 10–15 phrase video-specific keyword set exists, contains the approved
  primary phrase, matches the Tags field, and is mirrored in the upload sheet
  and upload JSON.
- The thumbnail brief contains the full primary and alternate prompts, exact
  text/font/color/layout/output specifications, and every referenced asset
  exists at its stable project path.
- The delivered thumbnail matches the brief and remains legible at mobile
  size (10% scale).

This closes the episode.

## Output

`episodes/<slug>/EPxxx/final-qa.md` — sign-off note and timestamp, ending with one line,
exactly `**STAGE VERDICT: PASS**` or `**STAGE VERDICT: FAIL**`. The completion gate reads the
last such line; a FAIL cannot close the episode.

## Stop condition

Terminal. No `next_stage` after this one; `episode-state.json` is marked
`closed`.
