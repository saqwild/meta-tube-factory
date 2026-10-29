# CAST-001 — CLOVER
**Status**: LOCKED FINAL 2026-10-29
**Class**: Core Anchor
**Source**: identity adapted from `C:\pycode\claude-shorts\characters\character_profiles.md` (Clover Tales), wardrobe locked per this channel's own bible. Style anchor already matched — claude-shorts' base design is already photoreal, no restyle needed.

## 1. Identity — LOCKED

- **Token:** `[[CLOVER]]`
- **Species / age:** cream tabby kitten, anthropomorphic, bipedal · 6 years old
- **Role:** the episode's point-of-view lead. Curious, a little clumsy, big heart — makes relatable mistakes (jealousy, fear of failing, guilt, embarrassment) that drive each episode's story. Triggers Bruno's "no first, yes second" gag as the polite requester.
- **Core personality (locked, verbatim across every episode):** very polite, gentle, curious, kind-hearted. Never rude even when Bruno is arrogant. Learns through small mistakes. Soft-spoken.
- **Wardrobe signature (locked):** soft orange onesie, simple and practical.
- **Voice:** young, bright, curious American English child-cat voice; expressive but not squeaky or cartoonish.

## 2. Design — structural anchors (copy verbatim)

- **Muzzle / face:** small, soft-rounded kitten muzzle, large expressive green eyes
- **Distinguishing mark:** a small four-leaf-clover-shaped patch of darker fur on the chest — her signature, distinct from every other cast member's coloring
- **Fur:** cream tabby pattern, soft realistic photoreal texture
- **Ears / tail:** kitten-proportioned upright ears, tail free (no accessory)
- **Body frame:** small, anthropomorphic, standing upright, paws positioned naturally for human-like gestures

## 3. Reference-pack prompts (Muse Image, photoreal — `CHARACTER_BIBLE.md` §7)

Every prompt below opens with the channel's locked style anchor (`KEY_CHARACTER_PROMPTS.md` §1), copied verbatim:
> Photoreal anthropomorphic cozy family, ultra realistic fur, natural cat and dog anatomy with human-like posture, warm daylight, soft natural skin-fur texture, readable gentle eyes, consistent face geometry, warm cream #FFF6E3 and soft wood #D8B589 lighting, shallow depth of field, not cartoon, not painterly graphic-novel, not dark navy tribunal.

### 3a. Identity portrait prompt
```
Photoreal anthropomorphic cozy family, ultra realistic fur, natural cat and dog anatomy with human-like posture, warm daylight, soft natural skin-fur texture, readable gentle eyes, consistent face geometry, warm cream #FFF6E3 and soft wood #D8B589 lighting, shallow depth of field, not cartoon, not painterly graphic-novel, not dark navy tribunal.

A neutral head-and-shoulders identity portrait of Clover, a young cream tabby kitten standing upright in an anthropomorphic pose, large expressive green eyes, a small four-leaf-clover-shaped patch of darker fur visible at the chest, soft realistic fur texture with natural lighting. Wearing her signature soft orange onesie, simple and practical. Gentle, curious, polite expression. Camera at chest height, straight-on, symmetrical framing, plain warm cream studio backdrop, no props, no text.
```

### 3b. Full-body wardrobe reference prompt
```
[style anchor as above]

A full-body wardrobe reference of Clover, the same young cream tabby kitten, standing upright in a relaxed anthropomorphic pose, wearing her soft orange onesie, small paws positioned naturally for human-like gestures. Same lighting and identity as the portrait reference. Plain warm cream studio backdrop, no props, no text.
```

### 3c. Six-panel sheet prompt (front / three-quarter / profile / composed sitting / action holding object / full figure)
```
[style anchor as above]

Using the attached portrait and full-body references as the exact character design to preserve, generate a six-panel character-model-sheet layout for Clover: 1) front view, 2) three-quarter view, 3) side profile view, 4) composed sitting pose, 5) action pose holding a small everyday object (e.g. a bike handlebar or a shopping bag), 6) full figure. All panels preserve the same cream tabby coloring, clover-shaped chest patch, green eyes, orange onesie, and proportions. Plain warm cream studio backdrop throughout, consistent soft daylight, no labels or text baked into the image.
```

## 4. Episode role-overlay

Use the compiler in `KEY_CHARACTER_PROMPTS.md` §6. Clover's `<Subject N>` line preserves exactly: polite young kitten, soft orange onesie, big gentle eyes, cream and wood lighting. Episode overlays may vary temporary condition (dusty, tired, holding a prop) but never the onesie color, the clover chest patch, or the core-polite personality.

## 5. Asset manifest

| Asset | Path | Status |
|---|---|---|
| Four-panel turnaround (front / three-quarter / profile / back) | `characters/reference_sheets/clover_sheet.png` | **LOCKED — 2026-10-29.** SHA-256 `9e9391be5368d3926491ab34511ceff18150c856f5139f2f084c0419fec5c9ee` |
| Voice reference (3–5s) | `characters/voice/clover_voice.wav` | Not yet generated |

Approval status: **LOCKED (2026-10-29).** Source: `claude-shorts/characters/reference_sheets/clover_sheet.jpg`, already photoreal, visually verified against this card's design (cream tabby, clover-shaped chest patch, green eyes). Adopted as-is by owner decision — no rework requested.

**Known gap, accepted as non-blocking:** this turnaround is the bare/undressed identity (no orange onesie) — `claude-shorts` keeps base sheets undressed by design and layers wardrobe per-episode. This card's locked wardrobe signature (orange onesie) is therefore not yet represented in any image. A future wardrobe-dressing pass (this sheet as identity reference + the onesie) can produce that when needed; not required to close this item.
