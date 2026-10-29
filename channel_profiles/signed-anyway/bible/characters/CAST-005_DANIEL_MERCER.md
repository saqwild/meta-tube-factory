# CAST-005 — Daniel Mercer

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-005 |
| Master identity | Daniel Mercer |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 51–62 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Auditor, attorney, trustee, board chair, elder sibling and institutional witness whose precision may conceal complicity.

**Role boundaries:** Do not cast as an impulsive young founder, physical laborer or youthful romantic lead. Playing age remains inside 51–62.

**Strong pairings:** Noah Vale for technical disagreement; Naomi Reed for institutional peer conflict; Maya Chen for mentor-versus-whistleblower tension; Omar Haddad for competing duties.

## Identity lock

Master identity: an East Asian man in his mid-to-late fifties with light-medium warm skin.

Structural anchors — preserve verbatim and in this order:

1. long rectangular face.
2. silver-streaked black hair combed back.
3. rimless rectangular glasses.
4. narrow dark-brown eyes.
5. subtle cleft at the center of the chin.

Body and posture: average height, slender formal frame, still posture with minimal gestures.

Default wardrobe range: slate suit, ink-navy tie, rimless glasses and a redacted paper memo.

Public mask: Detached professional certainty.

Pressure tell: Removes his glasses and cleans one lens before answering a personal question.

## Voice and performance lock

mature centered baritone, neutral international English, precise measured cadence, quiet breath and a faintly formal register that becomes plainer when the mask breaks.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of an East Asian man in his mid-to-late fifties with light-medium warm skin, defined by these exact structural anchors in order: long rectangular face; silver-streaked black hair combed back; rimless rectangular glasses; narrow dark-brown eyes; subtle cleft at the center of the chin. average height, slender formal frame, still posture with minimal gestures. Detached professional certainty with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing slate suit, ink-navy tie, rimless glasses and a redacted paper memo. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: long rectangular face; silver-streaked black hair combed back; rimless rectangular glasses; narrow dark-brown eyes; subtle cleft at the center of the chin. Show Daniel Mercer as a full figure with average height, slender formal frame, still posture with minimal gestures, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing slate suit, ink-navy tie, rimless glasses and a redacted paper memo. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: long rectangular face; silver-streaked black hair combed back; rimless rectangular glasses; narrow dark-brown eyes; subtle cleft at the center of the chin. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-005 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: long rectangular face; silver-streaked black hair combed back; rimless rectangular glasses; narrow dark-brown eyes; subtle cleft at the center of the chin. Preserve average height, slender formal frame, still posture with minimal gestures; mature centered baritone, neutral international English, precise measured cadence, quiet breath and a faintly formal register that becomes plainer when the mask breaks. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-005/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-005/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-005/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-005/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-005/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

