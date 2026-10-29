# Pipeline — stage catalog

This is the **union** of every stage contract that exists in this repo. Which stages a given
episode actually walks — and in what order — is declared by that channel's
`channel_profiles/<slug>/channel.json` → `pipeline_stages` array, read by `tools/preflight.py`.
A stage contract never hardcodes which channel uses it.

| Stage | Contract | Declared result | Used by |
|---|---|---|---|
| 00 | [preflight](stages/00-preflight.md) | episode created/resumed, first stage handoff | all |
| 01 | [ideation](stages/01-ideation.md) | locked premise + owner decisions | all |
| 01b | [coverage scan](stages/01b-coverage-scan.md) | owner-approved coverage map of what a complete explanation must answer + YouTube market/coverage scan ([process_coverage.md](process_coverage.md)) | inside-the-process |
| 02 | [research](stages/02-research.md) | supporting evidence / reference notes | all |
| 02a | [sourcing](stages/02a-sourcing.md) | fiction boundary (Branch A) or claim + visualization ledgers (Branch B) | signed-anyway, inside-the-process |
| 02b | [compliance](stages/02b-compliance.md) | fiction/non-depiction/disclosure gate | all |
| 03a | [writer](stages/03a-writer.md) | cast snapshot + full script/story package | all |
| 03b | [script review](stages/03b-script-review.md) | independent craft verdict (never the 03a author) | all |
| 04a | [visual brief](stages/04a-visual-brief.md) | scene list + visual requirements | all |
| 04b | [character refs](stages/04b-character-refs.md) | Muse Image identity **reference sheets** | all |
| 04c | [scene refs](stages/04c-scene-refs.md) | environment/prop **reference plates** + locked env strings | all |
| 04d | [shot plan](stages/04d-shot-plan.md) | clip breakdown + `_context/blocking.json`, the geometry authority | all |
| 04e | [storyboard](stages/04e-storyboard.md) | self-contained `exports/storyboard.html`, one card per clip | all |
| 04f | [LTX prompt draft](stages/04f-ltx-prompt-draft.md) | clip prompt draft + **frame-0 requirement block** per clip | all |
| 04f2 | [frame-0 stills](stages/04f2-frame0-stills.md) | **one still per clip**, generated from that block, gated, + the agent packet | all |
| 04f3 | [LTX prompt final](stages/04f3-ltx-prompt-final.md) | prompts re-anchored to the approved pixels + validator review + tool-built prompt manifest | all |
| 04g | [render package](stages/04g-ltx-render-package.md) | tool-built, self-verified vidgen-dist ingest package (`master-prompt.txt` + `stills/`) | all |
| 04h | [pilot QA](stages/04h-ltx-pilot-qa.md) | human-watched pilot verdict before the full render | all |
| 05 | [render ingest](stages/05-render-ingest.md) | hashed local master manifest | all |
| 05a | [render QA](stages/05a-render-qa.md) | human beat-adherence QA of that exact master | all |
| 06 | [metadata](stages/06-distribution-metadata.md) | title/description/tags/thumbnail package | all |
| 06a | [postproduction assembly](stages/06a-postproduction-assembly.md) | episode-local askyt_editor handoff package, then in-repo ingest of the hash-verified final MP4/teaser | all |
| 07 | [final QA](stages/07-final-package-qa.md) | closed local production package | all |

"All" = signed-anyway, clover-and-paws and inside-the-process — the three channels this repo
hosts.

Read the individual stage contract for its inputs, declared output, forbidden actions and stop
condition. Read `AGENTS.md` for the rules that apply across every stage.

## The 04f → 04f2 → 04f3 loop

The one part of this pipeline that is not a straight line, and the reason it isn't:

**i2v has a circular dependency.** The clip prompt must describe the still's real pixels, but
the still must already contain every object the clip's action touches — i2v never invents
objects. Guessing in either direction produces one of two named failures: a prompt that
contradicts the render, or a clip that reaches for a prop that was never drawn.

```
04d   blocking.json — geometry decided ONCE, structured
       │
04f   draft the motion, dialogue, audio, camera  ──►  frame-0 requirement block
       │                                                    │
04f2   generate N stills FROM that block, gate them  ◄──────┘
       │  ("is the clip's first action performable from this frozen instant?")
       │
04f3   re-anchor the opening clause to the APPROVED PIXELS, validate
```

A failure gets fixed at the layer it lives in. A still that can't support the action is
re-rolled at `04f2` — it is never patched by rewording the clip. **In i2v the image is the
contract; the prompt is only the delta.**

## Derived artifacts

Four deliverables are **generated, never hand-written**. All are plain stdlib scripts and never
an input to a generation model.

```bash
python tools/storyboard.py         --channel <slug> --episode EPxxx   # 04e
python tools/image_agent_packet.py --channel <slug> --episode EPxxx   # 04f2
python tools/ltx_prompt_manifest.py --channel <slug> --episode EPxxx --still-gate-pass   # 04f3
python tools/build_render_package.py --channel <slug> --episode EPxxx \
    --pilot SC01,... --cast "Name,..."                                  # 04g
```

The last two **refuse** rather than write when their inputs are not final: a review that is not
a strict PASS from the current validator against the current prompts file, a prompts file that
still says `PROVISIONAL`, or a prompt/still that changed after it was hashed. The packager also
re-reads its own output with the render app's parser and fails on any mispairing.

`prompts/6-image-agent-packet.md` front-loads the still checklist to *before* generation, so the
first time anyone sees what an image must show is not after a render has been spent.
`exports/storyboard.html` lets a human scan an episode in one scroll, with clips that have no
approved still shown as labelled placeholders rather than quietly omitted.

## Authorities

| Concern | File |
|---|---|
| Clip prompt rules | [`LTX_I2V_CONTRACT.md`](LTX_I2V_CONTRACT.md) |
| Frame-0 still rules | [`MUSE_FRAME0_CONTRACT.md`](MUSE_FRAME0_CONTRACT.md) |
| Validator rule catalog | [`ltx_prompt_validator.md`](ltx_prompt_validator.md) |
| Evidence and provenance | [`research/LTX25_PROMPTING_RESEARCH.md`](research/LTX25_PROMPTING_RESEARCH.md) |
| Clip prompt writer | `local_skills/ltx-production-writer/SKILL.md` |
| Still prompt writer | `local_skills/frame0-still-writer/SKILL.md` |
| Vendor syntax conformance | the global `ltx25-prompting` skill — **read-only, runs last, never drafts** |

## Stage completion gates

`tools/preflight.py complete` no longer just checks sequence order and the `--approve` flag. Per
`pipeline/stage-gates.json` (read by `episode_state.stage_gate_check`), a stage cannot be marked
complete unless:

- every path in that stage's `outputs` exists and is non-empty (a `*`/`?`/`[` makes it a glob
  needing ≥1 match), and
- where a `verdict` is declared, the verdict artifact carries a passing result and does **not**
  carry a blocking one.

A **`BLOCKED`** compliance verdict, a **`REVISE`** script review, a review or pilot-QA JSON
whose `status` isn't `PASS`, or a render-QA / final-QA whose last `**STAGE VERDICT:**` line is
`FAIL` hard-stops completion — `--approve` does not override it. A `forbid` entry blocks a stage
while a marker is still present (04f3 cannot complete while `7-video-prompts.md` says
`PROVISIONAL`). The way forward
is to fix the deliverable, or `reopen` an earlier stage. Every stage in every channel's
`pipeline_stages` has an entry (a test enforces that); a stage with no entry would be a hole in
exactly this check.

On completion each gated stage also records a **`deliverable_digest`** — the SHA-256 of every
file its `outputs` resolve to — onto its `completed_stages` entry. `episode_state.approval_drift`
(surfaced by `reopen` and by the health check below) then reports when a deliverable was edited
after the stage that approved it. This is advisory, never blocking.

## Episode health check

`python tools/episode_health.py --channel <slug> --episode EPxxx` (also
`preflight.py health <slug> <ep>`) is a **read-only** end-to-end consistency pass over one
episode: required deliverables for every completed stage, JSON artifacts against
`pipeline/schemas/`, one clip-id set across every manifest, recorded SHA-256s vs disk, reviews
vs the sources they name, and the final MP4s (16:9, audio, sane duration) via `ffprobe`. It runs
no model. Exit 1 on any `FAIL`; a closed episode's missing deliverables are `WARN`, not `FAIL`.

## Owner gates (v1)

Kept intentionally sparser than a full change-control ledger, since this repo has no git-based
audit trail to lean on. A stage is an owner gate only where getting it wrong is expensive or
irreversible:

- `01b-coverage-scan` (inside-the-process) — the owner approves what the episode must explain
  before any research is spent; later stages may add to that scope but not narrow it.
- `02b-compliance` — a `BLOCKED` verdict must stop a human, not an agent.
- `03b-script-review` — script locked before any visual spend.
- `04g-ltx-render-package` — last checkpoint before GPU render spend.
- `04h-ltx-pilot-qa` — a human must actually watch the pilot clips; an agent may not fill in
  verdicts it did not watch for.
- `06-distribution-metadata` — last checkpoint before the packaging (title/description/tags/
  thumbnail) is public-facing.
- `06a-postproduction-assembly` — a human must actually watch the assembled, watermarked,
  subtitled result start to finish before the final MP4 itself is public-facing; same
  must-actually-watch bar as `04h`, now applied to the finished cut.

Every other stage auto-advances when `complete` is called. A channel may add more gates by
listing them in its own `channel.json`; it never needs a code change to do so.

Note that `04f2` is deliberately **not** an owner gate even though it has a hard gate of its
own. Its gate is per-still and runs dozens of times per episode; making it an owner gate would
mean an approval call per still. The batch-level human checkpoint is `04g`, and the
watched-pixels checkpoint is `04h`.
