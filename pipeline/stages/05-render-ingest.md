# 05 — render ingest

Reachable only after `04h-ltx-pilot-qa` PASSes. A channel without a pilot-QA stage in its
`pipeline_stages` would skip straight from `04g`, but every channel currently defined here has
one.

## Inputs

Manually produced render outputs — **this pipeline never invokes a renderer**. The owner renders
through `vidgen-dist` and places the results under
`episodes/<slug>/EPxxx/renders/ltx-inbox/` (**`renders/` is a top-level folder**, a sibling of
`visual/`, `prompts/`, `qa/` and `exports/`).

`vidgen-dist` writes two sidecars beside every clip — a readable `.txt` report and a
machine-readable `.json` carrying the exact settings, seeds and model filenames used. **Ingest
both.** They are the only record of what a given clip was actually rendered at, and the app's
"load settings from a render" feature reads the `.json` to reproduce a run exactly. A clip
whose sidecar is missing cannot be reproduced and should be re-rendered rather than accepted.

Prior attempts move to a `history/` subfolder rather than being overwritten.

## Task

Probe each rendered file locally — duration, resolution, codec, whether an audio track is
present and non-silent — compute its SHA-256, and record it alongside the settings its sidecar
declares. This is the local, git-free equivalent of a hash-bound manifest: the manifest file
itself is the record.

Cross-check each clip against the package it came from: the clip index maps to the right
`@@ s{n}` prompt and the right still, and the rendered duration matches the declared 20 seconds.
A silently mispaired batch renders successfully and looks plausible — this is the stage that
catches it.

## Output

`episodes/<slug>/EPxxx/renders/render-manifest.json` — one entry per clip: path, sha256,
duration, resolution, audio present, the settings from its sidecar, and the prompt/still hashes
it should correspond to.

## Forbidden

Do not re-encode or edit a render here. Do not accept a file that is not already on disk under
`renders/ltx-inbox/`. Do not accept a clip whose sidecar is missing or whose declared settings
differ from the package's `render-settings.json` without recording the discrepancy explicitly.
