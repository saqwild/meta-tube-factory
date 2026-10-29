# CAST-006 — Naomi Reed

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-006 |
| Master identity | Naomi Reed |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 46–57 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** CEO, senior counsel, matriarch, board power, trustee and controlled antagonist who can make authority feel rational.

**Role boundaries:** Do not cast as a junior analyst, fragile dependent or youthful spouse. Playing age remains inside 46–57.

**Strong pairings:** Evelyn Shaw for equal-power examination; Adrian Cole or Daniel Mercer for board conflict; Maya Chen for mother/daughter or executive/analyst tension; Sara Keene for rival moral authority.

## Identity lock

Master identity: a white woman in her early fifties with fair cool-toned skin.

Structural anchors — preserve verbatim and in this order:

1. sculpted square-oval face.
2. blunt chin-length auburn bob.
3. pale grey eyes.
4. fine horizontal lines across the brow.
5. long elegant neck.

Body and posture: medium-tall, lean formal frame, level chin and controlled open posture.

Default wardrobe range: ink-navy tailored suit, paper-ivory shell and one aged-brass cuff bracelet.

Public mask: Unshakeable institutional control.

Pressure tell: Rotates the brass cuff bracelet once and then holds completely still.

## Voice and performance lock

cool low contralto, educated neutral North American English, unhurried phrasing, light vocal fry only at sentence endings and firm breath support that rarely breaks.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a white woman in her early fifties with fair cool-toned skin, defined by these exact structural anchors in order: sculpted square-oval face; blunt chin-length auburn bob; pale grey eyes; fine horizontal lines across the brow; long elegant neck. medium-tall, lean formal frame, level chin and controlled open posture. Unshakeable institutional control with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing ink-navy tailored suit, paper-ivory shell and one aged-brass cuff bracelet. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: sculpted square-oval face; blunt chin-length auburn bob; pale grey eyes; fine horizontal lines across the brow; long elegant neck. Show Naomi Reed as a full figure with medium-tall, lean formal frame, level chin and controlled open posture, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing ink-navy tailored suit, paper-ivory shell and one aged-brass cuff bracelet. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: sculpted square-oval face; blunt chin-length auburn bob; pale grey eyes; fine horizontal lines across the brow; long elegant neck. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-006 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: sculpted square-oval face; blunt chin-length auburn bob; pale grey eyes; fine horizontal lines across the brow; long elegant neck. Preserve medium-tall, lean formal frame, level chin and controlled open posture; cool low contralto, educated neutral North American English, unhurried phrasing, light vocal fry only at sentence endings and firm breath support that rarely breaks. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-006/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-006/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-006/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-006/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-006/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

