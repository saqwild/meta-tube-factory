# Signed Anyway — Brand Asset Prompts

This is the implementation prompt library for channel branding and episode thumbnails. `VISUAL_STYLE_CONTRACT.md` is the visual source of truth; this file applies that contract without replacing approved raster assets.

## 1. Asset registry

| Asset | Current file | Status | Use |
|---|---|---|---|
| Primary avatar | `assets/signed_anyway_avatar_800.png` | Approved | YouTube channel avatar and master logo raster |
| Small avatar | `assets/signed_anyway_avatar_98.png` | Approved | Small-size legibility check |
| Signature stroke | `assets/signed_anyway_continuous_signature.webp` | Approved | Watermark, end card and subtle series mark |
| Banner candidate A | `assets/b1.webp` | **Recommended** | Two-line banner; stronger mobile legibility |
| Banner candidate B | `assets/b2.webp` | Alternate | One-line banner; quieter but smaller text |

Both current banner candidates are 2048×1152. This meets YouTube’s minimum channel-art canvas. Export the selected production master at 2560×1440 when possible.

## 2. Brand locks

| Token | Specification |
|---|---|
| Channel name | **Signed Anyway** |
| Primary tagline | **They knew the cost. They signed anyway.** |
| Banner copy | **Money. Power. Betrayal. You decide.** |
| Series mark | **The Moral Ledger** |
| Visual style | Cinematic painterly graphic-novel realism |
| Ink navy | `#07131C` |
| Slate | `#24333D` |
| Aged brass | `#C79A45` |
| Paper ivory | `#E8E0D1` |
| Oxblood | `#7B2D26`, maximum 3% of frame |
| Display type | Source Serif 4 |
| Data type | IBM Plex Mono |

All generation prompts must describe desired content positively. FLUX prompts do not use a negative-prompt field.

## 3. Channel banner

### Production specification

- Master: 2560×1440, 16:9.
- Critical text/logo safe area: centered 1546×423.
- Keep the outer canvas quiet because television, desktop and mobile crop it differently.
- Use one centered message, one brass rule, and no episode imagery.
- Preferred line break: `Money. Power. Betrayal.` / `You decide.`

### Recommended two-pass workflow

1. Generate the background and centered ink panel without text.
2. Add exact copy in an editor using an elegant high-contrast serif.
3. Export PNG master and WebP working copy.
4. Test mobile crop and television crop before upload.

### Banner background prompt — FLUX

```text
A minimalist cinematic YouTube channel banner for a prestige financial ethics drama. A smooth horizontal gradient moves from #07131C ink navy on the left to #24333D slate on the right, with subtle painted paper texture and gentle edge falloff. A centered wide rectangular panel in near-black ink has softly rounded corners and fits entirely inside the channel safe area. Beneath the future headline position is one thin horizontal rule in #C79A45 aged brass. The composition is symmetrical, restrained, sophisticated and spacious, with clean unmarked surfaces and no figures. 2560×1440, exact 16:9 composition, critical design elements confined to the centered 1546×423 safe area.
```

### Exact typography overlay

```text
Money. Power. Betrayal.
You decide.
```

Typography specification:

- Paper ivory `#E8E0D1`.
- Elegant editorial serif with high stroke contrast.
- First line approximately 1.35× the width of the second.
- Center aligned, generous tracking, normal sentence case.
- Brass underline centered beneath the second line.
- No drop shadow; use only a subtle one-pixel dark edge if needed for compression.

### One-pass FLUX Flex prompt

Use only when a typography-capable model is available:

```text
A centered YouTube channel banner displaying the exact two-line text "Money. Power. Betrayal." above "You decide." in elegant high-contrast editorial serif typography, paper-ivory #E8E0D1 lettering inside a near-black ink rectangular panel with softly rounded corners. A thin #C79A45 aged-brass rule is centered below the text. The surrounding 2560×1440 canvas is a restrained gradient from #07131C ink navy to #24333D slate with subtle painted paper texture. All text and the brass rule remain inside the centered 1546×423 safe area, perfectly spelled, balanced and highly legible.
```

## 4. Logo and avatar

### Meaning

The mark is one continuous aged-brass signature stroke. It suggests an abstract letter **A**, an upward decision path, and the final sweep of a signature without becoming literal handwriting.

### Reproduction rule

Use `signed_anyway_avatar_800.png` as the identity reference whenever the mark is regenerated. Do not ask a model to invent a new logo for each asset.

### Avatar prompt — reference edit

```text
Preserve the exact continuous signature-stroke symbol from reference image 1: one elegant tapered line forming a tall abstract A-like rise, a narrow descending inner curve, and a long low horizontal finishing sweep. Center the symbol with generous breathing room on a square #07131C ink-navy background with subtle painted paper texture. Render the stroke in flat #C79A45 aged brass with smooth edges and consistent identity. Minimal premium editorial branding, perfectly legible at 98×98 pixels, square 1:1 master at 800×800.
```

### Avatar export set

- `signed_anyway_avatar_800.png`: 800×800 PNG master.
- `signed_anyway_avatar_98.png`: 98×98 PNG validation/export.
- The full mark must remain recognizable at 48×48.
- Preserve at least 8% clear space on all sides.

## 5. Signature watermark and end-card mark

### Watermark prompt — reference edit

```text
Preserve the exact continuous aged-brass signature stroke from reference image 1 on a transparent canvas. The mark consists of one smooth tapered path with a tall rising arc, narrow descending curve and long low finishing sweep. Maintain #C79A45 aged brass, clean antialiased edges and generous transparent margins. Horizontal 16:9-friendly layout for a subtle lower-right video watermark and end-card accent.
```

Recommended use:

- Lower-right corner at 3–5% of frame width.
- 45–65% opacity over video.
- Full opacity on end cards.
- Do not animate it like handwriting in every episode; reserve the full signature animation for the opening or final verdict handoff.

## 6. Master thumbnail system

### Production specification

- Master: 3840×2160, 16:9; compress the upload below 2 MB when practical.
- Heavily darkened, episode-specific set plate grounded in Ink navy.
- One expressive fictional face on the right at 40–50% of the frame unless an object-led variant is being tested.
- One decisive evidence object and one secondary consequence cue.
- Keep critical content inside the central 80%; reserve the lower-right 25% width × 18% height for YouTube interface overlays.
- Leave the left third clean for zero to three overlay words; leave a safely inset bottom-left position for one story number.
- Test at 10% scale before approval.
- Title explains the event; thumbnail adds the emotional or evidentiary contradiction.

### Base-image prompt template — FLUX

Replace every `[[...]]` field before generation.

```text
A high-impact YouTube thumbnail for a cinematic financial moral-dilemma story. A heavily darkened [[EPISODE SET PLATE]] establishes the case. [[PRIMARY CHARACTER]] occupies the right 40–50% in a tight three-quarter close-up, showing [[SPECIFIC AUTHENTIC EMOTION]] and looking toward [[HERO EVIDENCE OBJECT]] in the left half. A simplified [[CONSEQUENCE CUE]] supports the evidence without competing with the face. Cinematic painterly graphic-novel realism with authored brush texture, expressive natural anatomy, practical motivated light and prestige-drama contrast. #07131C ink navy and #24333D slate dominate; #C79A45 aged brass identifies the evidence; one small #7B2D26 oxblood cue occupies no more than 3% of the frame. Clean left-third negative space for a maximum three-word post overlay and a safely inset bottom-left position for one post-added story number. The lower-right 25% width by 18% height remains visually quiet for platform overlays. No generated wording, numbers or logos. Immediate one-second readability, 3840×2160, 16:9.
```

### Reference roles

When recurring or episode characters exist:

- Image 1: exact character face/identity.
- Image 2: exact wardrobe.
- Image 3: hero evidence object or composition board.
- Image 4: painterly visual-style reference.

State each role explicitly in the prompt. Generate title text separately unless FLUX Flex is being used.

### Text overlay specification

- Short quotation/display line: Source Serif 4 in Paper ivory `#E8E0D1` with a restrained Ink edge, left third, no more than three words.
- Quotation marks are allowed only when the wording is spoken or shown exactly in the episode.
- Story number: IBM Plex Mono in Aged brass `#C79A45`, bottom-left, at least 10% inward from the left and bottom edges.
- The number must be accurate in-story and appear on screen by 0:10.
- Oxblood never colors the main number or an entire word block.
- Text must add information absent from the title.

## 7. Pilot thumbnail — SA-001

**Title:** He Saved 2,000 Jobs by Lying to the Bank  
**Title communicates:** the lie, the bank and the jobs saved.  
**Thumbnail must add:** workers ultimately paid the cost.

### Primary prompt

```text
Use image 1 as the exact identity reference for Marcus Vance and image 2 as his charcoal-suit wardrobe reference. A heavily darkened factory-finance set plate grounds the composition. Marcus occupies the right 45% in a tight three-quarter close-up, exhausted and morally cornered rather than villainous, holding a blank white covenant certificate with one aged-brass signature line. In the left third, a dark factory locker stands open beside an unmarked severance card; a stopped factory clock is softly visible behind it. Cinematic painterly graphic-novel realism, ink-navy and slate shadows, aged-brass evidence accents and one tiny oxblood consequence mark occupying less than 3% of frame. Leave clean left-third space for the post-added exact line and a safely inset bottom-left space for the post-added brass number 2,000. Keep the lower-right platform-overlay zone quiet. No generated wording, numbers or logos. One-second mobile readability, 3840×2160.
```

**Overlay:** `WHO PAID?`

### A/B variants

| Variant | Change one variable only | Hypothesis |
|---|---|---|
| A | Replace `WHO PAID?` with no text | Tests whether the $0 severance object is sufficient. |
| B | Keep everything; change Marcus from looking at the certificate to looking toward the empty locker | Tests stronger human consequence. |
| C | Keep everything; replace the open locker with a row of deactivated worker badges | Tests scale versus personal loss. |

## 8. Week-two thumbnail — SA-002

**Title:** My Husband Hid $180,000 in Debt—Then the Bank Called Me  
**Thumbnail must add:** her identity was used, not merely the shared money.

### Primary prompt

```text
Use image 1 as the exact identity reference for the wife and image 2 as the exact identity reference for the husband. A heavily darkened domestic-finance set plate grounds the composition. The wife fills the right 45% in a tight painterly close-up, phone held slightly away from her ear, expression shifting from confusion to controlled betrayal as she looks at a blank loan document in the lower-left foreground with one aged-brass signature line. The husband is a small, softly focused silhouette behind frosted glass, recognizable by wardrobe but not visually dominant. Cinematic painterly graphic-novel realism, ink navy, slate, paper ivory, aged brass and one tiny oxblood contradiction cue occupying less than 3% of frame. Leave clean left-third space for the post-added exact line and a safely inset bottom-left space for the post-added brass number 180,000. Keep the lower-right platform-overlay zone quiet. No generated wording, numbers or logos. 3840×2160.
```

**Overlay:** `MY NAME?`

### A/B variants

- A: remove the husband silhouette; test cleaner evidence-first framing.
- B: keep composition and change the wife’s gaze from document to camera; test direct viewer confrontation.
- C: keep composition and replace the paper with seven stacked loan envelopes; test countable scale.

## 9. Week-three thumbnail — SA-003

**Title:** An AI Fired 10,000 Workers. Who Is Responsible?  
**Thumbnail must add:** a human-approved objective drove the automated decision.

### Primary prompt

```text
A heavily darkened near-future finance set plate in cinematic painterly graphic-novel realism. One deactivated employee badge sits large in the left foreground with a tiny oxblood status cue occupying less than 3% of frame. On the right 45%, a finance executive in profile presses an aged-brass approval control on a restrained translucent interface and looks toward the human badge, conveying dawning responsibility. Ink navy and slate dominate; aged brass marks human approval. Leave clean left-third space for the post-added exact line and a safely inset bottom-left space for the post-added brass number 10,000. Keep the lower-right platform-overlay zone quiet. No generated wording, numbers or logos. Immediate mobile readability, 3840×2160.
```

**Overlay:** `WHO FIRED THEM?`

### A/B variants

- A: remove the overlay; test whether badge plus approval gesture carries the question.
- B: keep everything and replace the executive profile with a visible human hand only; test anonymity/system focus.
- C: keep everything and replace the single badge with a receding row of three badges; test scale.

## 10. Week-four thumbnail — SA-004

**Title:** Three Children, One Will—and a Signature Their Mother Never Made  
**Thumbnail must add:** the disputed signature conflicts with another form of intent.

### Primary prompt

```text
A heavily darkened inheritance-hearing set plate in cinematic painterly graphic-novel realism. One principal sibling occupies the right 45% in a restrained mid-expression close-up, looking toward a torn Paper-ivory will in the left foreground split through an aged-brass signature line. Two other siblings remain small, softly separated silhouettes in the background and do not compete with the principal face. A compact unmarked voice-note device provides the contradiction cue, with one tiny oxblood indicator occupying less than 3% of frame. Leave clean left-third space for the post-added exact line and a safely inset bottom-left space for the post-added brass number 3. Keep the lower-right platform-overlay zone quiet. No generated wording, numbers or logos. 3840×2160.
```

**Overlay:** `NOT HER SIGNATURE`

### A/B variants

- A: change only the overlay to `HER REAL WISH?`.
- B: keep everything and make the will the only focal subject, removing visible faces for object-led search traffic.
- C: keep everything and replace the waveform with a small sealed voice-note device; test tangible versus abstract evidence.

## 11. Thumbnail QA gate

- [ ] Title and thumbnail contribute different information.
- [ ] One focal point is obvious in under one second.
- [ ] Character identity matches the approved reference.
- [ ] Emotion is specific and credible, not generic surprise.
- [ ] Overlay contains zero to three words.
- [ ] Overlay remains readable at 10% scale.
- [ ] Oxblood occupies no more than 3% of the frame and appears on one consequence cue only.
- [ ] Story number uses IBM Plex Mono in Aged brass, is safely inset bottom-left and appears in the episode by 0:10.
- [ ] Lower-right platform-overlay reserve is clear.
- [ ] Real logos, bank names, public figures and generated document paragraphs are absent.
- [ ] Thumbnail depicts an event actually present in the episode.
- [ ] Master is 3840×2160 16:9; critical content stays in the central 80%; upload is compressed below 2 MB when practical.

## 12. Naming convention

```text
assets/channel/signed_anyway_avatar_master.png
assets/channel/signed_anyway_banner_a.webp
assets/channel/signed_anyway_banner_b.webp
assets/thumbnails/SA-001/SA-001_thumb_A.png
assets/thumbnails/SA-001/SA-001_thumb_B.png
assets/thumbnails/SA-001/SA-001_thumb_C.png
```

Do not rename the current approved files until every consuming profile, workflow and upload reference has been migrated.

## 13. Testing protocol

- Prepare three variants before publishing each long-form episode.
- Use YouTube Studio Test & Compare when available.
- Judge the winner by watch-time share, not click-through rate alone.
- Review click-through rate by traffic source and average view duration for misleading curiosity.
- Finance/business and entertainment reference ranges are starting context only; establish Signed Anyway’s own baseline after the first four comparable uploads.
