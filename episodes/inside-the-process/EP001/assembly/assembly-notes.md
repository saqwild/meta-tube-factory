# EP001 assembly notes (06a) - hackathon slides, trims, placement

Status: spec only, written 2026-10-29 before 06a runs. The locked
script and all SC clips stay byte-identical; slides are separate
post-produced cards inserted in assembly, never baked into a clip.

## Intro slide - 3 seconds

- Placement (hackathon sample): t=0, before SC01. Total runtime effect:
  240 s episode + 3 s intro + 5 s outro = 248 s.
- Placement (retention variant, channel release): after the SC01 hook
  clip, before SC02, so the film's own hook lands inside 5 seconds
  first. Assembly chooses one; default for this submission is the
  sample placement above.
- Duration: 3.0 s, hard cut to SC01 (no fade longer than 6 frames).
- Background: warm cream matching the episode palette (kitchen plates,
  ENV001), no generated imagery, no animation except a 12-frame fade-in.
- Exact text (post-produced type, never in a generated still):
  Line 1 (large): How Bread Rises: Inside the Dough
  Line 2: Made for the Meta Global AI Developer Hackathon
  Line 3 (small): Explained From Within - a meta-tube-factory demo
- Audio: silence or the episode music bed at low level; no speech.
- Why here: states the hackathon claim before anyone can miss it,
  without touching locked dialogue. SC01's own hook follows at 0:03
  inside the retention window.

## Outro slide - 5 seconds

- Placement: immediately after SC12's final crumb frame, before the
  06-distribution end card. Runtime effect included above.
- Duration: 5.0 s, fade from SC12's last frame, hold, fade to black.
- Background: black, or final crumb frame darkened 40% behind text.
- Exact text:
  Line 1: Produced end to end with Meta Muse models
  Line 2: Muse Spark - reasoning and verdicts | Muse Wonder - script
  Line 3: Muse Image - stills | SAM 3.1 - pilot QA
  Line 4: Muse Voice Transcribe - dialogue audit
  Line 5 (small): Video rendered with LTX-2.5 image-to-video.
  Line 6 (small): Full pipeline, prompts and QA:
  Line 7 (small): github.com/saqwild/meta-tube-factory
- Audio: episode music resolve, no speech.

## Trim rule (from 04h owner review)

Trim only trailing dead-silence frames per clip at assembly; keep all
dialogue and the productive tail action (the process-close framing).
Record each clip's chosen trim range here when 06a runs.

| Clip | Source duration | Trim range kept | Note |
|---|---|---|---|
| SC01-SC12 | 20 s each (render) | TBD at 06a viewing | trailing silence only |

## Disclosure cards carried from earlier stages

- VIS-08 time-compression card: "Hours of rising, shown here in seconds."
- COV08 scope disclosure is already spoken in SC01 dialogue (locked).
- Synthetic-media disclosure and sources go to 06 metadata, not slides.

## Prohibitions

- No hackathon or credit line is added to any SC dialogue or still.
- Slides must not alter, crop, or re-time any SC clip's dialogue.
- If a slide is regenerated, it is a new post asset with its own file;
  SC clip hashes in _context/ltx-prompt-manifest.json stay untouched.
