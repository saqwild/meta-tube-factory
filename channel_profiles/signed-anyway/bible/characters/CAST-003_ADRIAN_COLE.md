# CAST-003 — Adrian Cole

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-003 |
| Master identity | Adrian Cole |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 44–54 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** CFO, founder, father, senior spouse, compromised protector, executive who can argue necessity without appearing innocent.

**Role boundaries:** Do not cast as a youthful son, junior analyst, physical enforcer or comic relief. Playing age remains inside 44–54.

**Strong pairings:** Evelyn Shaw for interrogation; Elena Marquez or Sara Keene for domestic/cost conflict; Naomi Reed for board power; Omar Haddad for bank-versus-borrower pressure.

## Identity lock

Master identity: a white man in his late forties with fair neutral skin.

Structural anchors — preserve verbatim and in this order:

1. rectangular face.
2. slightly hooded grey-blue eyes.
3. salt-and-pepper hair concentrated at the temples.
4. straight prominent nose.
5. faint diagonal crease on the left cheek.

Body and posture: tall, solid but not athletic frame, controlled shoulders that tighten under pressure.

Default wardrobe range: charcoal suit, pale shirt and understated aged-brass tie bar.

Public mask: Controlled protector.

Pressure tell: Rubs the edge of a paper or tie bar with his thumb.

## Voice and performance lock

restrained lower baritone, neutral North American English, carefully managed pace, slightly dry texture and a tendency to compress the final word when withholding information.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a white man in his late forties with fair neutral skin, defined by these exact structural anchors in order: rectangular face; slightly hooded grey-blue eyes; salt-and-pepper hair concentrated at the temples; straight prominent nose; faint diagonal crease on the left cheek. tall, solid but not athletic frame, controlled shoulders that tighten under pressure. Controlled protector with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing charcoal suit, pale shirt and understated aged-brass tie bar. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: rectangular face; slightly hooded grey-blue eyes; salt-and-pepper hair concentrated at the temples; straight prominent nose; faint diagonal crease on the left cheek. Show Adrian Cole as a full figure with tall, solid but not athletic frame, controlled shoulders that tighten under pressure, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing charcoal suit, pale shirt and understated aged-brass tie bar. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: rectangular face; slightly hooded grey-blue eyes; salt-and-pepper hair concentrated at the temples; straight prominent nose; faint diagonal crease on the left cheek. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-003 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: rectangular face; slightly hooded grey-blue eyes; salt-and-pepper hair concentrated at the temples; straight prominent nose; faint diagonal crease on the left cheek. Preserve tall, solid but not athletic frame, controlled shoulders that tighten under pressure; restrained lower baritone, neutral North American English, carefully managed pace, slightly dry texture and a tendency to compress the final word when withholding information. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-003/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-003/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-003/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-003/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-003/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

