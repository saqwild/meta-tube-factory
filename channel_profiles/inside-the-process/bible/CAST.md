# Cast and recurring prop registry

All entries are design specifications, not locked reference assets.

## CAST-001 - Explorer

Role: one curious adult field observer; recurring physical character.
Wardrobe: orange pressure suit with restrained dark seams, white helmet and
dark visor. Adult human proportions and practical equipment. Calm body
language with brief, readable reactions. No franchise likeness or real-person
likeness. Gender, facial detail and voice are not locked by this text.

For the initial style, the visor conceals facial details. This permits a
recognizable silhouette without depending on repeated facial synthesis.
An approved future face reveal must be designed as a separate reference,
not improvised by a video model.

Performance: seated within the capsule, facing as declared relative to camera.
A small head turn or hand brace can communicate attention. The explorer is
an observer and never physically directs a biological repair.

Voice: adult English, curious and concise, heard only over the helmet radio. There is never lip-synced on-screen speech. While the line plays, the visible Explorer holds still, watching, with the visor unchanged; gestures come before or after the line. The face is never revealed (`VISUAL_STYLE_CONTRACT.md` voice rule). LTX-2.5 generates authorized dialogue natively from exact quoted prompt lines (see `channel.json` → `render.narration_mode` and `cast.explorer_voice_mode`). Record the actual accepted clip provenance; a written voice adjective is not an identity lock. No tested voice descriptor exists yet under this profile (see `channel.json` → `render.voice_lock_note`). Post-production may balance or repair reviewed audio but is not the default dialogue source.

## VOICE-001 - Control

Audio-only guide. Calm adult English, plain language, one useful answer at
a time. No visible body, portrait, mouth animation or extra physical person.
Contrast the Explorer's curiosity with measured explanation; avoid long
lectures and fake emergencies.

Snapshot this entry in the cast only when the approved script uses it.
No Muse Image portrait is required for an audio-only role.

## PROP-001 - Capsule

One compact rounded exploration capsule: matte ivory hull, orange horizontal
safety stripe, clear curved canopy, two small cyan navigation lights and
soft white headlamps. One seat and one Explorer. Preserve cockpit, canopy,
light placement, hull proportions and stripe position.

Obtain an approved prop sheet and a composed Explorer-in-capsule reference.
A character portrait alone does not establish this prop. The capsule has no
biological repair beam or particle emitter; its lamps illuminate the action.

## Identity workflow

At 04b, create the Explorer reference and record provenance. At 04c, create
the capsule sheet and compositions using that approved Explorer image.
Store first-episode assets under the episode's visual/references folders.
Promotion to channel locked references follows the existing second-use rule; the Explorer, capsule and "you" masters are already locked (see the section below).
Re-anchor derivatives from the same approved source, not from an expanding
chain of generated derivatives.

## Story-engine additions (`STORY_ENGINE.md`, adopted 2026-10-29)

- **The Explorer (CAST-001) costume is locked.** It is restated positively in every prompt showing the Explorer, and close-ups are zoom-checked at 05a (`VISUAL_STYLE_CONTRACT.md` → "Explorer costume lock"; `STORY_ENGINE.md` §8).
- **CAST-002 — recurring outside "you" figure** (registered in `channel.json` → `cast.core_cast`):
  - silent; never shares a frame with the Explorer (`max_characters_in_frame: 1`);
  - never shown drinking alcohol or smoking (owner on-screen rule, 2026-10-29);
  - one everyman for every episode and pillar, **locked once**: the master is in `locked-references/characters/` and is never regenerated;
  - always narrated as "you", never named aloud, never speaks;
  - generic unbranded wardrobe, restated in every prompt;
  - appears only in outside rows, and only when already present in frame 0.

  See `STORY_ENGINE.md` §9.

## Production-profile note (LTX)

The Explorer (CAST-001), capsule (PROP-001) and "you" (CAST-002) masters in `locked-references/characters/` were adopted from the sibling profile on 2026-10-29 (owner decision) and are the channel masters on both engines. LTX EP001 already used these same Explorer and capsule images (byte-identical copies), so they are unchanged for this profile; only CAST-002 is new. Later episodes' stills are made at `04f2` under `local_skills/frame0-still-writer/SKILL.md`, conditioned on the masters, never on a text description.
