# CAST-010 — Omar Haddad

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-010 |
| Master identity | Omar Haddad |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 37–47 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Banker, operations chief, investigator, brother, community leader and disciplined intermediary caught between policy and people.

**Role boundaries:** Do not cast as a teenage son, elderly patriarch or flamboyant speculative trader. Playing age remains inside 37–47.

**Strong pairings:** Adrian Cole for bank/borrower or brother conflict; Daniel Mercer for competing institutional duties; Julian Price for partners or creditor/debtor tension; Sara Keene for family or community stakes.

## Identity lock

Master identity: an Arab man in his early forties with olive-brown skin.

Structural anchors — preserve verbatim and in this order:

1. broad oval face.
2. short dense black curls.
3. close boxed beard with grey at the chin.
4. amber-brown eyes.
5. broad straight nose.

Body and posture: medium-tall, broad practical frame, steady grounded stance with economical hand movement.

Default wardrobe range: slate suit without a tie, paper-ivory shirt and a plain aged-brass pen clip.

Public mask: Measured reasonableness.

Pressure tell: Aligns the brass pen exactly parallel to the table edge before delivering an unfavorable decision.

## Voice and performance lock

steady middle baritone, neutral international English with a light Gulf-Arab cadence, deliberate tempo, calm resonance and a firmer onset when institutional duty overrides sympathy.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of an Arab man in his early forties with olive-brown skin, defined by these exact structural anchors in order: broad oval face; short dense black curls; close boxed beard with grey at the chin; amber-brown eyes; broad straight nose. medium-tall, broad practical frame, steady grounded stance with economical hand movement. Measured reasonableness with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing slate suit without a tie, paper-ivory shirt and a plain aged-brass pen clip. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: broad oval face; short dense black curls; close boxed beard with grey at the chin; amber-brown eyes; broad straight nose. Show Omar Haddad as a full figure with medium-tall, broad practical frame, steady grounded stance with economical hand movement, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing slate suit without a tie, paper-ivory shirt and a plain aged-brass pen clip. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: broad oval face; short dense black curls; close boxed beard with grey at the chin; amber-brown eyes; broad straight nose. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-010 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: broad oval face; short dense black curls; close boxed beard with grey at the chin; amber-brown eyes; broad straight nose. Preserve medium-tall, broad practical frame, steady grounded stance with economical hand movement; steady middle baritone, neutral international English with a light Gulf-Arab cadence, deliberate tempo, calm resonance and a firmer onset when institutional duty overrides sympathy. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-010/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-010/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-010/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-010/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-010/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

