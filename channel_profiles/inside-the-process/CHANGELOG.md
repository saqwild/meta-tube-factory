# inside-the-process (LTX profile) — change log

## 2026-10-29 — channel-setup changes adopted from sibling-repo

**Owner instruction:** check `sibling-repo/channel_profiles/inside-the-process` and adopt the changes that relate to the channel. No change in video generation: it stays LTX-2.5 i2v, 20 s clips, same render settings. Done by `_adopt-ltx-2026-10-29.py` (this folder; every edit asserts its anchor). The pre-edit profile was backed up to the session scratchpad. Vidgen-ltx was read, never written.

**Owner decisions in the session:** copy the ltx locked masters; add the insignia negative terms; profile only (no skill or stage-contract edits).

### Adopted

| Area | Change |
|---|---|
| Story | New `bible/STORY_ENGINE.md`: second-person narration, clock as plot, arc (climax ≈45%, objection ≈55%, practical 70-85%, callback), master metaphor the Explorer enters, "no dead 5 s", Story Definition Sheet, "you" anchor per pillar. Rewritten for 20 s clips and a ~32-clip grid. Applies from the next LTX episode; EP001 unaffected |
| Cast | CAST-002, the recurring outside "you" figure (registered in `cast.core_cast`; silent, never in frame with the Explorer, no alcohol or smoking on screen) |
| Locked masters | `locked-references/characters/`: Explorer CAST-001 (4 images), capsule PROP-001, CAST-002 (4 images). Copied byte-for-byte; hashes in that README match the sibling's files |
| Voice and look | Helmet-radio Explorer voice rule and the Explorer costume lock written into `VISUAL_STYLE_CONTRACT.md`, `CAST.md`, `CHARACTER_BIBLE.md`, `SCRIPT_BRIEF.md`, `SCRIPT_CRAFT.md` |
| Compliance | No real-world insignia on any character; no on-screen alcohol or smoking; practical sections are explanation, never instruction; Body-topic safety boundary. In `COMPLIANCE_GATE.md` and `hard_safety_floor` |
| Negative terms | 9 terms added to `render.negative_prompt_additions`: shoulder patch, arm badge, chest emblem, insignia, flag, mission patch, ribbed helmet band, helmet stripes, visible face behind the visor |
| Evidence wording | "research shows" / "in a clinical trial" / "people who… tend to" / "in mice, researchers found" table in `SCIENCE_AND_SOURCING.md` |
| Coverage map | Coverage-map lines in `EPISODE_SPEC.md`, `SCRIPT_BRIEF.md`, `SCRIPT_CRAFT.md` (the 01b stage and the 02/03 contracts already used it) |
| SEO and thumbnails | Four-panel causal-ladder primary thumbnail (phrase ≤ 6 words, context ≤ 3, brand footer ≤ 3, total ≤ 12) in `SEO.md`, `BRAND_ASSET_PROMPTS.md`, `channel.json` (`youtube.thumbnail_system`, `metadata_validation`); timeline title variants (SEO rule 11) |
| QA | Story-engine checks in `QA_CHECKLIST.md`: hard-cut scan at 05, Explorer/"you" zoom-check at 05a, dead-stretch check, arc check at 03b |
| Channel facts | Live playlists (Inside Your Body, Inside Manufacturing, Inside Materials; Inside Technology pending) and the sibling's scheduled videos in `playlists` and `CHANNEL_SETUP.md`; `visual_identity` palette and typefaces; `postproduction` watermark policy; launch status |

### Not adopted (LTX-2.5 specific, or outside the owner's scope)

- I2V, 15 s shots, `<d>` dialogue tags, the 960x544 → 1344x768 upscale profile, `LTX_PROMPT_FRAMEWORK.md`, `TECHNICAL_PIPELINE.md`, `PRODUCTION.md`, the i2v contract gate and the ltx `negative_prompt_base.txt`.
- The sibling's **cut-inside-a-clip syntax** (`[Shot N] At MM:SS`): not adopted. LTX-2.5 does support cuts, and `LTX_I2V_CONTRACT.md` §4 already governs declared cuts (the first pass of this file wrongly called cuts a LTX-only capability; corrected by `_adopt-ltx-2026-10-29-cuts-fix.py`). `STORY_ENGINE.md` §7 defers to the contract.
- `youtube_studio` block in the sibling's `channel.json`: its content is already in this file under `channel`, `youtube` and `brand_assets`; a second copy would drift.
- Per-episode facts: the sibling's EP001 worked SEO derivation, first-appearance callouts, pilots and proposals.

### Added the same day (owner approved "go ahead" after asking who writes the story)

Script `_adopt-ltx-2026-10-29-story-stages.py`: the story engine is now wired into the story-writing path.
- `pipeline/stages/01-ideation.md`: also write `story/story-definition.md` (a document, not a machine gate); topics as "you + everyday action + time".
- `pipeline/stages/03a-writer.md`: confirm the sheet, write to the arc by share of runtime, second-person narration, 20-25% outside clips, helmet-radio voice rule.
- `pipeline/stages/03b-script-review.md`: story-engine checks added to the review; follow-up rounds stay verification-only.
- `local_skills/explained-from-within-story-writer/SKILL.md`: the Explorer helmet-radio voice rule (it was missing there) and a pointer to `STORY_ENGINE.md`; provenance recorded in `local_skills/skill-lock.json`.
- Kept as they were (ahead of the sibling): the 01 viewer-question/process-chain rule, the coverage map, `clip_split_check`, the blind naive-viewer test, verify-only follow-up rounds.

### Still open

- No reusable hard-cut scan tool exists here. The sibling's `tools/cut_scan.py` is a reference; EP001's cut scan was run by hand.
- `tools/metadata_validator.py` warns `META-W001` for the new thumbnail keys; that check stays manual, as for the existing thumbnail keys.
- Nothing machine-checks that `story/story-definition.md` exists; it is a document convention.

### 2026-10-29 — "Inside means inside" (owner doctrine)

The owner saw earlier episodes show a digital, see-through body model instead of the interior, and asked that "inside your brain" show the real brain interior (structure, cells) with the Explorer in it. `bible/VISUAL_STYLE_CONTRACT.md` now has the rule; `STORY_ENGINE.md`, `QA_CHECKLIST.md`, stage 04a and stage 05a carry it. An outside locator view of the body (to show where the organ sits) is allowed when needed, as its own clip. Five negative terms added (hologram, wireframe body, medical infographic, neon outline diagram, labelled anatomy diagram); "transparent human body" and "x-ray" were left out on purpose so a locator shot is not suppressed. Script: `_adopt-2026-10-29-inside-means-inside.py`.

### 2026-10-29 — correction found at EP002 `04b`

The 2026-10-29 adoption said LTX EP001's Explorer/capsule references were episode-local and not masters. That was wrong: EP001's five Explorer and capsule files are byte-identical to the images now locked as the channel masters (it had copied them from the sibling profile on 2026-10-29). Corrected in `locked-references/README.md`, `bible/CAST.md`, `bible/CHARACTER_BIBLE.md` and `channel.json` (`cast.reference_status`). Only CAST-002 is new to this profile. Script: `_adopt-2026-10-29-correct-ep001-masters.py`.
