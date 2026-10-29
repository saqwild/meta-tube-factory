# Clover & Bruno Stories — Brand Asset Prompts
**Status**: LOCKED FINAL 2026-10-29
**Channel**: Clover & Bruno Stories @cloverandbruno
**Replaces**: previous financial drama prototype brand assets — ABANDONED

This is implementation prompt library for channel branding and episode thumbnails. VISUAL_STYLE_CONTRACT.md is visual source of truth; this file applies that contract for cat n dog photoreal.

## 1. Asset registry

| Asset | Current file | Status | Use |
|---|---|---|---|
| Primary avatar | assets/clover_bruno_avatar_800.png | **FINAL — generated 2026-10-29.** SHA-256 `9cc68917c3a2b1e3cc95b12a85dc0ad00c51ab0ee9d4875b6cb662b3ef0b1f3f` | YouTube channel avatar — Clover + Bruno faces together |
| Small avatar | assets/clover_bruno_avatar_98.png | **FINAL — generated 2026-10-29.** SHA-256 `5d2bf565a8af1a6c051147184f5666ec60ba29bff2a3d2f7a26538e917038f06` | Small-size legibility check — verified legible at 98x98 |
| Banner | assets/clover_bruno_banner_2560.png | **FINAL — generated 2026-10-29.** SHA-256 `9ecf9d50e5ba71e60ae01d3025baddb8bd9b3d2b5232807fd6a1bedeeb548ba3` | YouTube banner 2560x1440 |
| Signature mark | assets/paw_street_mark.png | **FINAL — generated 2026-10-29.** SHA-256 `3dbb02fe06ba4fd185f608e8ae80efb471554909220b7b1556d660db5befc93a` | Watermark — round Clover + Bruno character badge |

Export banner master at 2560x1440, avatar at 800x800.

## 2. Brand locks

| Token | Specification |
|---|---|
| Channel name | Clover & Bruno Stories |
| Handle | @cloverandbruno |
| Primary tagline | Every day starts with Clover. Every legend starts grumpy. |
| Banner copy | Polite kitten meets grumpy 70-year-old dog. |
| Series mark | Paw Street Stories |
| Visual style | Photoreal anthropomorphic cozy family — not painterly graphic-novel, not dark navy |
| Warm Cream | #FFF6E3 |
| Soft Wood | #D8B589 |
| Finn Orange | #FF9F6B |
| Bruno Cardigan | #C97B4A |
| Gentle Green | #A8C8A0 |
| Display type | Rounded sans / warm serif, friendly |

All generation prompts must describe desired content positively. No negative-prompt field for Muse Image. Photoreal cat and dog, not cartoon.

## 3. Channel banner

### SELECTED — 2026-10-29

**"Paw Street market" variant chosen as the final banner art.** Owner-iterated beyond the v1/v2 prompts documented below into a livelier market-street composition — cream cottage porches give way to a lit shopfront street with "PAW STREET" and "PAWS & TREATS" signage, string lights, warm dusk light. Cast shown: Papa Fin, Clover, and Bruno (with Pip visible at the edge). Verified against YouTube Studio's actual safe-zone crop preview: Fin, Clover, and Bruno all sit correctly inside the "viewable on all devices" band — the safe-zone failure that sank the earlier porch-scene attempts (`v1`/`v2` below) is fixed here. The exact generation prompt was not captured verbatim (iterated live, outside this file); if it needs to be reproduced or varied later, redescribe this scene using the same "characters framed low/centered, not full-body-on-ground" discipline that fixed the safe-zone problem, per the lesson logged under v1/v2.

**Text-in-safe-zone is not actually a requirement (owner correction, 2026-10-29):** YouTube renders the channel name as its own UI text on the channel page regardless of what's baked into the banner image — the title/tagline text in the art is decorative, not load-bearing. It only needs to read well in the desktop/TV crop, where it currently does; it does not need to survive the mobile "viewable on all devices" crop. See `channel.json`'s `brand_assets.banner_text_note`. The earlier "text above the safe zone" note below no longer blocks anything.

**Source art:** `assets/paw_street_golden_hour_1.webp`, SHA-256 `8684eea306d7727ae73d4907d835ddd5279d4a660c38b23f6cacf0a462dc75cd` (2048x1152, kept for provenance).

**FINAL — delivered 2026-10-29:** `assets/clover_bruno_banner_2560.png`, upscaled from the source (2048x1152 → 2560x1440, same 16:9 ratio, Lanczos resample), SHA-256 `9ecf9d50e5ba71e60ae01d3025baddb8bd9b3d2b5232807fd6a1bedeeb548ba3`. This is the delivered banner — see the asset registry above for the same hash.

**Scope note:** this banner is a YouTube channel-display asset only — set once in Studio, never read by any episode-production stage (`00-preflight` through `07-final-package-qa`). It has no bearing on episode work, unlike the CAST-001..007 character reference packs.

### Production spec
- Master: 2560x1440, 16:9.
- Critical safe area: centered 1546x423 — keep the **main characters'** faces inside this band; text is decorative and does not need to be, since YouTube renders the channel name as its own UI text regardless (`channel.json` `banner_text_note`).
- Keep outer canvas quiet, warm home/street blurred because TV/desktop/mobile crop differently.
- Two or more characters + one centered message is fine — no episode-specific clutter.

### Banner background prompt — Muse Image (recommended: full-cast Paw Street scene)

A two-character split-portrait sells a "vs" thumbnail, not the channel. The banner is brand key art — it should sell the *world* (a whole cozy street, a whole cast living on it), not just the two leads. Two scene-based alternatives, both built around the full cast:

**A — "Paw Street" wide establishing scene, v1 (superseded — see v2):**
```
A wide warm establishing shot of Paw Street, a cozy small-town street at golden-hour daylight, for a photoreal anthropomorphic cat and dog family stories YouTube channel banner. On the left, in front of a cream-colored cottage with a soft wood porch, Mama Rosa in her apron hangs laundry while Papa Fin fixes a bicycle, and young kitten Clover in her orange onesie waves cheerfully from the porch steps. On the right, across the quiet street, Bruno — a 70-year-old retired dog in a burnt-orange knit cardigan and round tortoiseshell reading glasses on a bronze chain — sits in a wooden rocking chair on his own porch, arms crossed with a grumpy scowl, while ginger puppy Pip in his red bandana bounds excitedly at his feet. Further back in the softly blurred midground, small and unobtrusive so the scene stays uncluttered: Mimi, a grey tabby cat in a golden-yellow cardigan with cat-eye glasses pushed up on her head, glances out from a window a few doors down; Tico, a raccoon in a mismatched bowtie with his canvas messenger bag, pushes a small lemonade-stand cart along the far side of the street. Warm cream and soft wood tones throughout, soft bokeh street trees and lampposts in the background, no other people. Photoreal anthropomorphic animals, cozy storybook lighting, shallow depth of field toward the outer edges and background figures, sharp focus reserved for Clover's household and Bruno's porch in the center band. 2560x1440, keep the five foreground characters composed inside a centered 1546x423 safe strip, Mimi and Tico kept small, soft-focused, and peripheral only — do not let them compete with the main cast, no text.
```
**v1 failure (2026-10-29):** first render turned Rosa and Fin into dogs (a golden retriever and a sheepdog-type) instead of cats, dropped Mimi and Tico entirely, put Bruno's glasses on his nose instead of hanging from the chain, and rendered Bruno content/smiling instead of grumpy. Root cause: the prompt named each character but didn't hard-lock species per-character or explicitly forbid the wrong states, so the model defaulted "parent figures" to dogs and simplified away the background pair. v2 below fixes this with explicit species locks, an explicit-forbidden-state per detail, and a trailing MUST block — same discipline as `codex-grumpy`'s "MUST be bipedal, not on all fours" pattern, which was added there for an identical reason.

**A — "Paw Street" wide establishing scene, v2 (use this one):**
```
A wide warm establishing shot of Paw Street, a cozy small-town street at golden-hour daylight, for a photoreal anthropomorphic cat and dog family stories YouTube channel banner.

LEFT SIDE — Clover's household, all CATS, none of them dogs: In front of a cream-colored cottage with a soft wood porch stand Mama Rosa, an adult cat with a honey-tabby coat, feline face, cat ears and a cat tail, wearing her apron, and Papa Fin, an adult cat with a charcoal-grey coat, feline face, cat ears and a cat tail, wearing his blue shirt. Both are cats — not dogs, not a golden retriever, not a sheepdog. Below them on the porch steps, young kitten Clover, a cream tabby cat in her orange onesie, waves cheerfully.

RIGHT SIDE — Bruno's household, dogs: Across the quiet street, on his own porch, Bruno, a 70-year-old retired Bulldog/Mastiff-mix dog, sits in a wooden rocking chair, wearing a burnt-orange knit cardigan. His round tortoiseshell reading glasses hang from a thin bronze chain resting against his chest — the glasses are NOT worn on his nose or face. His expression is grumpy and unimpressed: furrowed brow, arms crossed, a scowling frown — he is not smiling, not relaxed, not peacefully reading a book. Ginger puppy Pip, with a bright ginger-orange coat and distinct lighter cream patches on his chest and hands, wears his red bandana and bounds excitedly at Bruno's feet.

BACKGROUND DETAIL — small, soft-focused, must not compete with the foreground five: a few doors down from Rosa and Fin's cottage, Mimi, a grey tabby cat in a golden-yellow cardigan with cat-eye glasses pushed up on her head, glances out from a window. Further along the far side of the street near Bruno's porch, Tico, a raccoon with a black facial mask and ringed tail, wearing a mismatched bowtie and carrying his canvas messenger bag, pushes a small lemonade-stand cart.

Warm cream and soft wood tones throughout, soft bokeh street trees and lampposts in the background, no other people, no animals beyond the seven named above.

Rendered in ultra-realistic photographic detail — real fur texture, real material weight in the clothing, natural daylight and shadow. This must read like a photograph of anthropomorphic animals, not a digital illustration, not a painted storybook style, not a glossy 3D render.

Overlay text, exact two lines, warm cream lettering with a soft dark outline, centered: "Clover & Bruno Stories" / "Polite kitten meets grumpy 70-year-old dog."

2560x1440. Keep Rosa, Fin, Clover, Bruno, Pip, and the text composed inside a centered 1546x423 safe strip. Mimi and Tico stay small, soft-focused, and peripheral only.

MUST: Rosa and Fin are cats with feline faces and cat ears — not dogs, not a golden retriever, not a sheepdog. MUST: Bruno's glasses hang from the chain at his chest, never worn on his nose. MUST: Bruno's expression is grumpy and scowling, never smiling or content. MUST: exactly seven animal characters total — Rosa, Fin, Clover, Bruno, Pip, Mimi, Tico — no extras, no humans.
```

**B — "Gathered together" full-cast group portrait:**
```
A warm group photoreal portrait of the full Clover & Bruno Stories cast standing together on a sunlit porch, for a YouTube channel banner. Center-left: young kitten Clover in her orange onesie, polite and smiling, flanked by Mama Rosa in her apron and Papa Fin in his blue shirt, both warm and relaxed. Center-right, a step apart: Bruno, a 70-year-old retired dog in a burnt-orange knit cardigan and round tortoiseshell reading glasses on a bronze chain, arms crossed with a grumpy scowl but soft eyes, with ginger puppy Pip in his red bandana leaning happily against his leg. Warm cream #FFF6E3 walls and soft wood #D8B589 porch boards, gentle golden daylight, shallow depth of field, no other people. Photoreal anthropomorphic animals, cozy family lighting. 2560x1440, keep the full group composed within a centered 1546x423 safe strip, quiet blurred street scene at the outer edges, no text.
```

**C — simple two-character split (fallback only, not recommended as primary):**
```
A cozy warm YouTube channel banner for a photoreal cat and dog family stories channel. Left side: a polite young kitten (Clover) in soft orange onesie, big gentle eyes, standing in a warm cream kitchen doorway with soft wood furniture. Right side: a 70-year-old retired grumpy old dog (Bruno) with graying fur, wearing a burnt-orange knit cardigan and round tortoiseshell reading glasses on a thin bronze chain resting at his chest, arms crossed with slight arrogant attitude but soft eyes, on a porch. Center gap leaves space for text. Background is a quiet sunny Paw Street with soft bokeh, warm daylight, no people. Photoreal anthropomorphic animals, cozy family lighting, shallow depth of field. 2560x1440, critical design in centered 1546x423 safe area, no text in image generation.
```

### Exact typography overlay
```
Clover & Bruno Stories
Polite kitten meets grumpy 70-year-old dog.
```

Typography:
- Warm cream #FFF6E3 with soft dark outline for legibility.
- Rounded sans, friendly, high legibility on mobile.
- First line larger/bold, second line smaller regular.
- Center aligned.

### One-pass prompt (if model can do text)

```
A centered YouTube channel banner for Paw Street, a cozy small-town street at golden-hour daylight, displaying exact two-line text "Clover & Bruno Stories" above "Polite kitten meets grumpy 70-year-old dog." in warm friendly rounded sans typography, cream lettering with soft outline, positioned in the open sky/street gap between the two households. Left: Mama Rosa and Papa Fin's cream cottage porch, with young kitten Clover in her orange onesie waving from the steps. Right: Bruno's porch, Bruno in a burnt-orange knit cardigan and round tortoiseshell reading glasses on a bronze chain sitting in a rocking chair, ginger puppy Pip in his red bandana at his feet. Photoreal anthropomorphic animals, cozy storybook lighting, warm cream and soft wood tones. All text inside centered 1546x423 safe area, perfectly spelled, highly legible. 2560x1440.
```

## 4. Logo and avatar

### FINAL — delivered 2026-10-29

**"Kitten and bulldog duo" close-up chosen as the final avatar art.** Owner-generated, source `assets/kitten_bulldog_duo.webp` (1600x1600, exact square — no crop needed, SHA-256 `beab3dbb9b2429c2486a1d0ce6d84add5be935296d4ffa4c6d8edbc307666adc`, kept for provenance), downscaled to the two delivery sizes:
- `assets/clover_bruno_avatar_800.png` — SHA-256 `9cc68917c3a2b1e3cc95b12a85dc0ad00c51ab0ee9d4875b6cb662b3ef0b1f3f`
- `assets/clover_bruno_avatar_98.png` — SHA-256 `5d2bf565a8af1a6c051147184f5666ec60ba29bff2a3d2f7a26538e917038f06`, visually confirmed both faces still read clearly at that size

This is the best photoreal result of any brand-asset generation so far — no painterly/3D style drift, and Bruno's grumpy arms-crossed expression is correct where several banner attempts weren't. Same recurring wardrobe drift as the banner (Clover in blue-striped overalls with a clover pin, not the locked orange onesie) — not treated as a blocker for this brand asset, per the same precedent set for the banner.

**Alternate considered and declined (2026-10-29):** a circular watercolor emblem logo ("Clover & Bruno" lettering, gold vine border, cream parchment background) was proposed as a replacement avatar. Declined — it's a painted illustration style, not photoreal, which would have put the avatar in a different visual language than the already-finalized photoreal banner and watermark. The kitten-and-bulldog close-up above remains the official avatar. Not saved into the project; this note is the record in case it comes up again.

**Not reusable as a video thumbnail as-is:** this source is 1:1 square; thumbnails need 3840x2160 (16:9). Build thumbnail art separately from §6's Duo templates rather than stretching or letterboxing this file.

### Meaning
Avatar is two faces together: Clover polite + Bruno grumpy. Instantly signals cat n dog channel.

### Avatar prompt — Muse Image

```
Square 1:1 YouTube avatar 800x800. Left half: close-up photoreal polite young kitten Clover with big gentle eyes, soft orange onesie, warm cream background. Right half: close-up photoreal 70-year-old retired dog Bruno with graying fur, slight grumpy arrogant expression but soft eyes, burnt-orange knit cardigan, round tortoiseshell reading glasses on a bronze chain. Both looking slightly toward camera, expressive, cozy lighting, photoreal anthropomorphic, not cartoon. Split down middle but cohesive. No text. Highly legible at 98x98. Warm cream #FFF6E3 background.
```

### Avatar export set
- clover_bruno_avatar_800.png: 800x800 PNG master
- clover_bruno_avatar_98.png: 98x98 PNG validation
- Must remain recognizable at 48x48 — both faces visible
- At least 8% clear space on all sides

## 5. Watermark

### FINAL — delivered 2026-10-29, design superseded

**Design changed (owner decision, 2026-10-29):** the original "paw print + street sign icon" concept below is superseded by a **round Clover + Bruno character badge** — a circular close-up of both faces together, transparent outside the circle, same character art as the avatar rather than an abstract icon. This matches YouTube's own standard convention more closely than a custom icon mark would (most channels' video watermark is just their round avatar). Delivered: `assets/paw_street_mark.png`, 98x98, RGBA with transparent corners, SHA-256 `3dbb02fe06ba4fd185f608e8ae80efb471554909220b7b1556d660db5befc93a`.

Superseded original spec (kept for record, not the current design):
```
Preserve exact paw street mark: small simple paw print with tiny street sign shape, warm wood #D8B589 color, on transparent canvas. Minimal, cozy, not financial brass. For lower-right video watermark.
```

Use at 3-5% frame width, 45-65% opacity over video — this placement/opacity guidance still applies to the new badge design.

## 6. Master thumbnail system — LOCKED for cat n dog

### Production spec
- Master: 3840x2160, 16:9; compress below 2MB.
- Bright warm set plate: kitchen or porch daylight, cozy.
- Duo episodes: Clover left 40%, Bruno right 40%, both expressive. Single family: one face big 50%.
- One small story-critical object center: shopping bag, lawnmower part, coin.
- 2-4 words overlay in cream with dark outline, exact line from episode.
- Keep lower-right reserve clear.

### Thumbnail prompt template — Duo Clover-led

```
Use image 1 as exact identity reference for Clover (polite kitten, orange onesie) and image 2 as exact identity reference for Bruno (70y old retired dog, gray fur, burnt-orange cardigan, glasses-on-a-chain, grumpy but soft). Bright warm cozy kitchen set plate, daylight, photoreal anthropomorphic. Left side: Clover close-up polite gentle eyes looking at Bruno, holding [OBJECT]. Right side: Bruno close-up grumpy arrogant scoff expression, arms crossed, looking away slightly. Small [OBJECT] large in center foreground. Warm cream #FFF6E3 and soft wood #D8B589 tones. Leave clean top space for post-added 2-4 word text and keep lower-right overlay zone quiet. No generated wording, numbers, or logos. 3840x2160.
```

Overlay: `BRUNO SAYS NO` (example)

### Thumbnail prompt template — Duo Bruno-led

```
Same references Clover + Bruno. Bruno porch setting, warm daylight. Bruno in foreground grumpy with attitude, Clover in background polite holding [TASK] item. Same specs.
```

Overlay: `CLOVER ASKS POLITELY`

### Thumbnail prompt template — Clover Family Only

```
Use references Clover + Mama Rosa + Papa Fin. Cozy kitchen. Clover center big 50% polite, Rosa + Fin small background warm. [OBJECT] center.
```

Overlay: `MAMA HELPS`

### Thumbnail prompt template — Bruno & Co Only

```
Use references Bruno + Pip. Porch/garage. Bruno grumpy, Pip loyal bright. [OBJECT] center.
```

Overlay: `BRUNO HELPS ANYWAY`

## 7. Week-one thumbnail — CB-001 Duo example

Title: Polite Clover Asks Grumpy Bruno to Fix Her Bike - He Says No At First

Prompt:

```
Use image 1 as exact identity for Clover polite kitten orange onesie, image 2 as exact identity for Bruno 70y retired dog gray fur burnt-orange cardigan glasses-on-a-chain grumpy. Bright warm cozy Paw Street porch, daylight photoreal. Left 40%: Clover holding small bike with flat tire, polite gentle eyes. Right 40%: Bruno arms crossed grumpy scoff, looking away. Small bike tire in center foreground large. Warm cream and soft wood tones. Leave top space for post-added text and bottom-left for small number if needed. No generated text. 3840x2160.
```

Overlay: `BRUNO SAYS NO`

A/B variants:
- A: Replace overlay with `PLEASE BRUNO?` — tests polite request
- B: Change Bruno gaze to camera — tests direct confrontation
- C: Remove Pip, keep only Clover+Bruno — tests cleaner Duo

## 8. Thumbnail QA gate — LOCKED

- [ ] Title and thumbnail contribute different info but both show cat n dog.
- [ ] One or two focal faces obvious in under 1 second — Clover polite + Bruno grumpy contrast.
- [ ] Character identity matches approved reference (Clover always orange onesie, Bruno always 70y gray + burnt-orange cardigan and glasses-on-a-chain).
- [ ] Emotion specific: Clover polite gentle, Bruno grumpy arrogant first, not generic shock.
- [ ] Overlay 2-4 words, readable at 10% scale (mobile).
- [ ] Warm bright plate, not dark navy.
- [ ] Lower-right overlay reserve clear.
- [ ] No arrows, red circles, shocked human faces, fake logos.
- [ ] Thumbnail depicts event actually in episode (Bruno says no first).
- [ ] Master 3840x2160, critical in central 80%, upload <2MB.
- [ ] For Duo episodes, both cat and dog visible.

## 9. Naming convention

```
assets/clover_bruno_avatar_800.png
assets/clover_bruno_banner_2560.png
assets/thumbnails/CB-001/CB-001_thumb_A.png
assets/thumbnails/CB-001/CB-001_thumb_B.png
```

Channel-level assets (avatar, banner, watermark) sit directly in `channel_profile/assets/`, matching §1's asset registry and `channel.json`'s `brand_assets` block — not in an `assets/channel/` subfolder. Per-episode thumbnails keep their own `assets/thumbnails/<episode-id>/` subfolder.

Do not reuse old prototype file names.

## 10. Testing protocol

- Prepare 3 variants per episode (especially Duo).
- Use YouTube Studio Test & Compare.
- Judge winner by watch-time share, not CTR alone.
- Track which face combo wins: Clover solo vs Bruno solo vs Duo both.
- Establish Clover & Bruno baseline after first 4 uploads.
