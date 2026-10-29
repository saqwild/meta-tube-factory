# Explained From Within — channel bible (LTX production profile)

Public brand: **Explained From Within**. Target handle: `@explainedfromwithin` (claimed in YouTube Studio on 2026-10-29). Internal repository slug remains `inside-the-process` for pipeline compatibility.

## Authority and status

- `../channel.json` is authoritative for runtime, renderer, stage order and machine-consumed validation.
- `channel.json` in this folder is the public brand/setup mirror and points back to the runtime authority.
- The name was owner-approved and the handle @explainedfromwithin was claimed in YouTube Studio on 2026-10-29.
- Profile, banner and watermark assets are generated and technically validated; owner visual acceptance status is not recorded here.
- **This is a second, independent production path for the same channel.** The channel is already live under the sibling repo `sibling-repo`'s LTX-2.5 profile (that repo's EP001 shipped there). This LTX profile has produced no episode of its own — no premise, topic or production history carries over. Its own EP001 starts fresh from `01-ideation`.
- **Channel masters locked (adopted 2026-10-29):** the Explorer, capsule and recurring "you" figure masters are in `../locked-references/characters/` (copied from the sibling profile; hashes in that folder's README).
- **Story engine adopted 2026-10-29:** `STORY_ENGINE.md` controls story structure from the next LTX episode on. Only its storytelling logic is taken; the render path (LTX-2.5 i2v, 20 s clips) is unchanged.

## File map

| Area | Files |
|---|---|
| Niche and competition | `NICHE_DECISION.md`, `COMPETITOR.md`, `CHANNEL_STRATEGY.md` |
| Public identity | `BRAND_AND_PERSONA.md`, `CHANNEL_SETUP.md`, `BRAND_ASSET_PROMPTS.md`, `channel.json` |
| Characters and world | `CAST.md`, `CHARACTER_BIBLE.md`, `KEY_CHARACTER_PROMPTS.md` |
| Visual production | `VISUAL_STYLE_CONTRACT.md`, `CINEMATOGRAPHY_CONTRACT.md`, `AMBIENT_LIFE_CONTRACT.md` |
| Evidence and compliance | `SCIENCE_AND_SOURCING.md`, `COMPLIANCE_GATE.md` |
| Story | **`STORY_ENGINE.md` (controls story structure from the next LTX episode)**, `EPISODE_SPEC.md`, `PILOT_AND_EPISODE_FORMATS.md`, `SCRIPT_BRIEF.md`, `SCRIPT_CRAFT.md` |
| Technical production | `PRODUCTION.md`, `TECHNICAL_PIPELINE.md`, `QA_CHECKLIST.md`, `PILOT_LESSONS.md` |
| Growth and launch | `SEO.md`, `MONETIZATION_PLAN.md`, `LAUNCH_PLAN.md`, `30_DAY_LAUNCH_PLAN.md` |

The prompt-writing authority (equivalent to the LTX profile's `LTX_PROMPT_FRAMEWORK.md`) is **not** a bible doc in this repo — it is the shared, cross-channel `local_skills/ltx-production-writer/SKILL.md` (04f/04f3) and `local_skills/frame0-still-writer/SKILL.md` (04f2), same as every other channel here.

## Stage reading map

| Stage | Required profile inputs |
|---|---|
| 00–01 | `STORY_ENGINE.md` (§2 anchors, §10 Story Definition Sheet), `NICHE_DECISION.md`, `CHANNEL_STRATEGY.md`, `BRAND_AND_PERSONA.md`, `EPISODE_SPEC.md` |
| 02–02b | `SCIENCE_AND_SOURCING.md`, `COMPLIANCE_GATE.md`, `STORY_ENGINE.md` §5 and §11, `COMPETITOR.md` when topic positioning matters |
| 03a–03b | `STORY_ENGINE.md` (§3-5, §10), `SCRIPT_BRIEF.md`, `SCRIPT_CRAFT.md`, `CAST.md`, `CHARACTER_BIBLE.md`, `EPISODE_SPEC.md`, plus `local_skills/explained-from-within-story-writer/SKILL.md` and `pipeline/youtube_benchmark.md` |
| 04a–04c | `VISUAL_STYLE_CONTRACT.md`, `CINEMATOGRAPHY_CONTRACT.md`, `AMBIENT_LIFE_CONTRACT.md`, `KEY_CHARACTER_PROMPTS.md`, `STORY_ENGINE.md` §9 ("you" figure) |
| 04d–04h | `STORY_ENGINE.md` (§6, §8), `PRODUCTION.md`, `TECHNICAL_PIPELINE.md`, `QA_CHECKLIST.md`, `pipeline/LTX_I2V_CONTRACT.md`, `pipeline/MUSE_FRAME0_CONTRACT.md` |
| 05–05a | `STORY_ENGINE.md` §8, `QA_CHECKLIST.md`, `TECHNICAL_PIPELINE.md`, `PILOT_LESSONS.md` |
| 06 | `SEO.md`, episode keyword research, `CHANNEL_SETUP.md`, `SCIENCE_AND_SOURCING.md` |
| 07 | `QA_CHECKLIST.md`, `CHANNEL_SETUP.md`, `COMPLIANCE_GATE.md` |

## Current launch gates

1. Record owner visual acceptance of the generated brand assets (shared with the LTX profile — do not regenerate them here).
2. Choose and research this profile's own first topic at `01-ideation` / `02-research`.
3. Create the remaining pillar playlists when their first episodes are ready (channel-level YouTube Studio action, shared across both production profiles).
