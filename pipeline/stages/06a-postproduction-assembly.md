# 06a — postproduction assembly

## Boundary — read this first

`AGENTS.md`: a stage reads and writes **only inside `C:\pycode\vidgen-ltx`**, except that
`C:\pycode\askyt_editor` (the postproduction tool) is readable **read-only** to verify its real
config schema, and `C:\pycode\sceneprocess\` (askyt_editor's runtime scratch) is **off limits
entirely**.

**Episode-local model (owner decision 2026-10-29 — the standing approach).** Every path
`run_episode.py` touches is inside the episode folder: `scenes_dir` → `postprod/_staged/`
(the stage writes all `scene_NNN_*.mp4` there itself), `working_dir` → `postprod/_work/`
(Muse Voice Transcribe cache + intermediates, disposable), `output_dir` → `exports/final/`. **`sceneprocess/`
is not used at all** — it is the shared scratch that caused the 2026-10-29 stale-transcript
collision, and taking it out of the loop makes that failure structurally impossible: each
episode's Muse Voice Transcribe cache lives under its own `postprod/_work/` and cannot be reached by another
config.

Because every write now lands in-domain, **this stage runs `run_episode.py` itself** (owner
decision 2026-10-29). The one thing it writes outside the episode folder is a copy of
`postprod-config.json` into `askyt_editor/<slug>/` — the tool needs its config beside the
runner. `askyt_editor/` source and `POST_PRODUCTION.md` stay read-only otherwise;
`sceneprocess/` is never read or written. The stage builds the package, runs the assembly,
QAs the finished cut, and writes the completion manifest; the **owner gate** is a human
approving the assembled public-facing video, not the mechanics of producing it.

*(EP001's postprod predates this — `askyt_editor/signed-anyway/EP001_signedanyway_postprod_LTX25.json`
still uses `sceneprocess/` paths; it is grandfathered, not a template for the path layout.)*

## Inputs

`renders/render-manifest.json` (all clips ingested; `05a-render-qa.md` all `PASS`),
`metadata/package.md` (verdict A/B text, chapter labels, title — the source of truth for any
overlay copy), `story/script.md` (any on-screen evidence-graphic text scripted verbatim),
`story/characters.md` (voice-memo / faceless-figure notes), the channel's
`VISUAL_STYLE_CONTRACT.md` (exact hex colors) and `CINEMATOGRAPHY_CONTRACT.md` (transition
doctrine), and — read-only — `askyt_editor/POST_PRODUCTION.md` (real CLI flags, config schema,
overlay catalogue, subtitle-safe-zone rule; read that, not this summary, before authoring the
config).

## A real worked example — and its one hard warning

`askyt_editor/signed-anyway/EP001_signedanyway_postprod_LTX25.json` is a real, finished config
for this exact channel, built against every rule below and carrying its own `_fixed_*` log of
actually-caught bugs. Read it (read-only) for the pattern. Note also the *no-suffix*
`EP001_signedanyway_postprod.json` in the same folder is a **different, earlier episode** (the
`sibling-repo`/LTX-2.5 "2,000 jobs" story) — do not copy its scene numbers, text, or paths.

**Confirmed failure mode (2026-10-29):** a config that reuses another config's `working_dir`
makes askyt_editor's Muse Voice Transcribe cache silently reuse a stale transcript from the *other* episode —
it reads exactly like a wrong-audio render defect. The episode-local model above removes this
failure entirely: `working_dir` = `postprod/_work/` is unique per episode by construction, so
there is nothing to collide with. (EP001's grandfathered config avoided it with a `-ltx25`
path suffix instead.)

## Task — build the package, run the assembly, QA the cut

### 1. `postprod/postprod-config.json` — the askyt_editor config, authored here

Author it against `askyt_editor/POST_PRODUCTION.md`'s real schema. Hard requirements:

- `output_dir` → `C:/pycode/vidgen-ltx/episodes/<slug>/EPxxx/exports/final/`.
- `scenes_dir` → `C:/pycode/vidgen-ltx/episodes/<slug>/EPxxx/postprod/_staged/` and
  `working_dir` → `.../postprod/_work/` — both episode-local (see the Boundary section). The
  stage **creates and populates** `_staged/` (task step 2); `_work/` is created empty and
  filled by `run_episode.py`.
- Every overlay's on-screen text copied **verbatim** from `script.md` / `package.md` — never
  invented copy, even a plausible filler card.
- Every overlay `position_y` ≤ 0.72 (`POST_PRODUCTION.md` subtitle safe zone — Muse Voice Transcribe captions
  occupy the bottom ~15% unconditionally). A clip with **no dialogue** may place a card lower;
  say so per-clip.
- `global.watermark.apply_at_assembly` **= `false`**. `true` is a confirmed double-stamp bug
  (the reference config's own note; `claude-shorts`'s 2026-10-29 EP03 incident on this tool).
- `run_episode.py`'s only transition primitive is `freeze_whoosh` — there is no zero-duration
  hard cut. If `script.md` directs one, record it as an accepted mismatch, don't fake it.
- The teaser `source_map` excludes any clip carrying the reversal or verdict content — the same
  no-spoiler rule `SEO.md` applies to the description and thumbnail. Prefer reusing
  `package.md`'s own pre-vetted Shorts-funnel candidate.
- `no_subtitles: true` on any clip whose audible content must not be captioned (a voice-memo
  insert `script.md` says is "never quoted dialogue").

### 2. `postprod/_staged/` + `postprod/staging-manifest.json` — the staged input, written here

The stage writes every clip into `postprod/_staged/` as `scene_NNN_<timestamp>.mp4`
(askyt_editor's scene discovery is the `scene_(NNN)_` filename prefix). Most come from the
`renders/ltx-inbox/` renders; any that need a `postprod/inserts/` override (below) come from
there. The `renders/` originals are never modified.

**A/V-lock every staged clip** (`-c:v copy -af apad -t <exact video seconds>`). The LTX-2.5
renders ship video ~20.042 s but audio ~20.010 s — a ~32 ms per-clip shortfall. askyt's
assembly times the video `xfade` on video length but the audio `acrossfade` on the real audio
length, so that 32 ms **compounds across the clip list into an audible lip-sync drift** that
becomes obvious around the first batch boundary (clip ~6, `batch_size` default 6). Padding each
clip's audio to exactly its own video duration before staging removes the accumulation.
`staging-manifest.json` records `staged_video_seconds` / `staged_audio_seconds` per clip as the
proof they match.

`staging-manifest.json` records, per clip: `staged_file`, its SHA-256, the `source` it was
copied from, and — for an override — `raw_render_sha256` (the untouched render's hash, for
provenance) plus the `override_reason`.

### 3. `postprod/inserts/` — episode-local generated assets

Anything the stage generates in-domain, then copies into `_staged/`:

- **Voice-memo audio** (`script.md` audio carry-note): generate the line (edge-tts / a VO read),
  apply the muffled-recorder treatment, save the `.wav` here. Record the exact voice brief used
  (`story/characters/*`'s voice lock) in `postprod/inserts/README.md`.
- **Clip overrides** — where `script.md` needs a clip extended, re-timed, or trimmed beyond what
  the config can express (a verdict-card runway; a QA-flagged drift window): produce the
  processed `.mp4` here with the ffmpeg recipe recorded in the README, so it can be rebuilt and
  re-staged after a re-roll. The raw vidgen-ltx render in `renders/` is never touched.

### 4. Run the assembly

- Copy `postprod/postprod-config.json` → `askyt_editor/<slug>/EPxxx_<slug>_postprod.json`
  (the one write into `askyt_editor/`). `_staged/` is already populated.
- **Composite pre-check.** Run every scene that carries an overlay, an override, or a
  `no_subtitles` flag: `python run_episode.py <config> --only-scenes <ids> --skip-assembly`.
  Extract frames from each `postprod/_work/sNN.mp4` and verify **by eye** — the watermark
  double-stamp bug (`apply_at_assembly` / `claude-shorts` 2026-10-29) has only ever been caught
  visually. Confirm: exactly one watermark; every overlay legible and clear of the caption
  strip; a `no_subtitles` clip carries no captions; each override clip is sound; any
  script-mandated by-0:10 evidence number is present in time.
- **Full run.** `python run_episode.py <config>` → Muse Voice Transcribe, overlays, transitions, assembly,
  teaser. Outputs land in `exports/final/`.

### 5. QA the finished cut, then ingest

- **Frame sweep** of `_Full.mp4` for artifacts, overlay collisions, and the burned verdict
  card on its runway.
- **Caption check** — transcribe `_Full.mp4` and confirm the captions match the approved
  dialogue (`05a` already verified clip audio against the script; this catches Muse Voice Transcribe timing
  / drift on the assembled track). A `no_subtitles` span must stay uncaptioned.
- **Runtime** vs `package.md`'s Chapters math (≈10:00); **teaser** carries no reversal/verdict
  content.
- Write `postprod/postprod-manifest.json`: SHA-256 of both outputs + the config + each
  `inserts/` file, the assembled duration, and the QA results (PASS/FAIL per check, findings).
- Write `postprod/handoff.md` — now a short **approval brief** for the owner: what was
  assembled, the QA results, anything the owner must eyeball (the SC05 freeze; a marginal
  overlay), and the one-line command to approve.

## Output

| Path | Written by | When |
|---|---|---|
| `postprod/postprod-config.json` | stage | step 1 |
| `postprod/_staged/scene_NNN_*.mp4` | stage | step 2 |
| `postprod/staging-manifest.json` | stage | step 2 |
| `postprod/inserts/*` (+ `README.md`) | stage | step 3 (if any) |
| `askyt_editor/<slug>/EPxxx_<slug>_postprod.json` | stage (the one out-of-domain write) | step 4 |
| `exports/final/EPxxx_<Title>_Full.mp4`, `..._Short.mp4` | stage's `run_episode.py` run | step 4 |
| `postprod/postprod-manifest.json`, `postprod/handoff.md` | stage | step 5 |

## Forbidden

- Writing into `askyt_editor/` beyond the single `postprod-config.json` copy; reading or
  writing `sceneprocess/` at all.
- A config whose `scenes_dir` / `working_dir` / `output_dir` points outside
  `episodes/<slug>/EPxxx/`.
- Inventing on-screen overlay text.
- `apply_at_assembly: true`; an overlay below `position_y` 0.72 on a dialogue clip.
- A teaser that includes reversal/verdict content.
- Moving or editing a `renders/` clip in place — a clip override is a **new file** under
  `postprod/inserts/`, then copied into `_staged/`.
- Marking the stage complete on the QA alone — the owner gate below is a human, not the QA.
- Treating `EP001_signedanyway_postprod.json` (no suffix) as any episode's config.

## Stop condition

**Owner gate.** The stage has produced `_Full.mp4` + `_Short.mp4` in `exports/final/`,
`postprod/postprod-manifest.json` records their SHA-256 and a **passing** QA, and
`postprod/handoff.md` is the approval brief. Completion then requires a **human to actually
watch the assembled cut** (the same `04h`-equivalent bar) and approve — the agent's QA is
thorough but does not substitute for the watch. A QA `FAIL` returns to whichever stage owns the
fix (`04f3`/`04f2` for a prompt/still problem, this stage for an overlay/timing problem, `04g`
for a re-render).
