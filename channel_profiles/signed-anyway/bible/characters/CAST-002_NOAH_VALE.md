# CAST-002 — Noah Vale

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-002 |
| Master identity | Noah Vale |
| Class | Anchor |
| Master-card version | 1.0.0 |
| Playing age | 32–39 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Canonical evidence specialist; financial mechanism explanation; timeline reconstruction; technical-to-human translation.

**Role boundaries:** Fixed identity and function. He is never recast as a romantic lead, accused executive or family member.

**Strong pairings:** Daniel Mercer for expert disagreement; Maya Chen for technical discovery; Julian Price for analyst-versus-insider tension.

## Identity lock

Master identity: a South Asian man in his mid-thirties with medium-brown skin.

Structural anchors — preserve verbatim and in this order:

1. long oval face.
2. thick straight eyebrows.
3. wavy black hair swept back.
4. close-trimmed beard.
5. warm dark-brown eyes.

Body and posture: average-tall, slim functional frame, slightly forward analytical posture.

Default wardrobe range: slate shirt with rolled sleeves, dark trousers and a simple brass-edged evidence tablet.

Public mask: Analytical calm.

Pressure tell: Stops manipulating the evidence interface and looks directly at the affected witness.

## Voice and performance lock

clear mid-register baritone, neutral international English, steady tempo, lightly softened endings and restrained warmth when evidence reaches a human consequence.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a South Asian man in his mid-thirties with medium-brown skin, defined by these exact structural anchors in order: long oval face; thick straight eyebrows; wavy black hair swept back; close-trimmed beard; warm dark-brown eyes. average-tall, slim functional frame, slightly forward analytical posture. Analytical calm with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing slate shirt with rolled sleeves, dark trousers and a simple brass-edged evidence tablet. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: long oval face; thick straight eyebrows; wavy black hair swept back; close-trimmed beard; warm dark-brown eyes. Show Noah Vale as a full figure with average-tall, slim functional frame, slightly forward analytical posture, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing slate shirt with rolled sleeves, dark trousers and a simple brass-edged evidence tablet. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: long oval face; thick straight eyebrows; wavy black hair swept back; close-trimmed beard; warm dark-brown eyes. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-002 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: long oval face; thick straight eyebrows; wavy black hair swept back; close-trimmed beard; warm dark-brown eyes. Preserve average-tall, slim functional frame, slightly forward analytical posture; clear mid-register baritone, neutral international English, steady tempo, lightly softened endings and restrained warmth when evidence reaches a human consequence. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-002/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-002/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-002/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-002/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-002/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

