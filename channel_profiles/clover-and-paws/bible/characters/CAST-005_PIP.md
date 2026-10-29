# CAST-005 — PIP
**Status**: LOCKED FINAL 2026-10-29
**Class**: Family Anchor (Bruno's household)
**Source**: identity adapted from `C:\pycode\codex-grumpy\characters\character_profiles.md` (Grumpy Gruffington). **Restyled from that source's 3D animated cozy-realism into this channel's locked photoreal anchor** (`KEY_CHARACTER_PROMPTS.md` §1) — every prompt below is rewritten, not copied. Note: `claude-shorts` also has a character named "Pip" — that is an unrelated one-off guest kitten from a single episode there, not this character; see project notes.

## 1. Identity — LOCKED

- **Token:** `[[PIP]]`
- **Species / age:** ginger puppy, anthropomorphic, bipedal, child/puppy proportions (~3 heads tall, bigger head-to-body ratio than the adult cast) · 4 years old
- **Role:** Bruno's usual sidekick. Comic relief, messenger, softens Bruno — though not always on Bruno's side.
- **Core personality (locked):** loyal, energetic, chaos-energy, naive, idolizes and lightens Bruno. Backing Bruno before nudging him is his most natural move, not a fixed one — let the story decide where he stands.
- **Wardrobe signature (locked):** a bright red bandana, tied loosely and slightly crooked around his neck — his identity anchor, deliberately contrasting Bruno's muted burnt-orange palette for instant silhouette differentiation even in motion or a wide shot. No other clothing.
- **Voice:** young, bright, high-energy American English puppy voice.

## 2. Design — structural anchors (copy verbatim)

- **Muzzle / face:** child-proportioned, slightly oversized head relative to body, large expressive round eyes, eager/curious energy, happy open-mouth grin
- **Fur:** bright ginger-orange coat with lighter cream patches on chest and hands, photoreal fur texture matching real photography
- **Ears:** one ear standing up, one flopped down — deliberate asymmetry that reads as barely-contained chaos energy
- **Body frame:** small, stout, bipedal, humanoid build, standing upright on two legs like a storybook character — never on all fours

## 3. Reference-pack prompts (Muse Image, photoreal — `CHARACTER_BIBLE.md` §7)

### 3a. Identity portrait prompt
```
Photoreal anthropomorphic cozy family, ultra realistic fur, natural cat and dog anatomy with human-like posture, warm daylight, soft natural skin-fur texture, readable gentle eyes, consistent face geometry, warm cream #FFF6E3 and soft wood #D8B589 lighting, shallow depth of field, not cartoon, not painterly graphic-novel, not dark navy tribunal.

A neutral head-and-shoulders identity portrait of Pip, a small anthropomorphic ginger puppy with a stout bipedal humanoid build, standing upright on two legs like a storybook character, NOT on all fours like a realistic dog. Child-proportioned with a slightly oversized head, bright ginger-orange coat with lighter cream patches on chest and hands rendered in ultra realistic photoreal fur texture, one floppy ear up and one down. Large expressive round eyes, wide with eager curious energy, mouth open in a happy panting grin. Tied loosely and slightly crooked around his neck is a bright red bandana — his signature identity accessory, worn with no other clothing. Camera at chest height, straight-on, symmetrical framing, plain warm cream studio backdrop, no props, no text.
```

### 3b. Full-body wardrobe reference prompt
```
[style anchor as above]

A full-body wardrobe reference of Pip, the same ginger puppy, standing upright on two hind legs in a bouncy, fidgety, can't-stay-still pose, small hands raised chest-high mid-gesture, tail caught mid-wag. MUST stand upright on two legs — never on all fours, never in a realistic quadruped running gait. Same red bandana, coat markings, and ear asymmetry as the portrait reference. Plain warm cream studio backdrop, no props, no text.
```

### 3c. Six-panel sheet prompt (front / three-quarter / profile / composed sitting / action holding object / full figure)
```
[style anchor as above]

Using the attached portrait and full-body references as the exact character design to preserve, generate a six-panel character-model-sheet layout for Pip: 1) front view, 2) three-quarter view, 3) side profile view, 4) composed sitting pose, 5) action pose holding a small object (e.g. a rusty pump or a stick he's proudly found), 6) full figure. All panels preserve the same ginger-orange coat with cream patches, red bandana, asymmetric ears, and child/puppy proportions (roughly three heads tall), all standing upright on two legs — never on all fours. Plain warm cream studio backdrop throughout, consistent soft daylight, no labels or text baked into the image.
```

**Known failure mode (inherited lesson from the source research, still applies to this engine):** weak phrasing like "bipedal-capable" plus an action cue implying four-legged motion (e.g. "about to bound forward") can render Pip as a naturalistic four-legged dog instead of anthropomorphic/bipedal. Always give an explicit upright-stance instruction and a bipedal-only action cue.

## 4. Episode role-overlay

Use the compiler in `KEY_CHARACTER_PROMPTS.md` §6. Pip's structural anchors and red bandana carry verbatim into every episode. He is present in most Bruno appearances (80% rule); when he speaks or reacts, mark him non-verbal/silent where the shot only needs Bruno speaking, per the max-speaking-characters rule.

## 5. Asset manifest

| Asset | Path | Status |
|---|---|---|
| Character sheet | `characters/reference_sheets/pip_sheet.jpg` | **LOCKED — 2026-10-29.** SHA-256 `7e38588aaeb44a0c7eaf7940ab35253ec58a8bb15892f67e03a071531bffb028` |
| Voice reference (3–5s) | `characters/voice/pip_voice.wav` | Not yet generated |

Approval status: **Identity portrait LOCKED (2026-10-29)** after two generation rounds — round 1 matched codex-grumpy's cartoon style despite the photoreal prompt (rejected); round 2 used a strengthened prompt with explicit anti-cartoon language (real fur strand detail, natural eye size, no glossy 3D) and passed at the same quality bar already accepted for Bruno's portrait. Full-body and six-panel not yet generated — same non-blocking gap as Bruno's card, see `CAST-004_BRUNO.md` §5.
