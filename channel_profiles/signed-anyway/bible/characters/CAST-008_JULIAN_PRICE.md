# CAST-008 — Julian Price

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-008 |
| Master identity | Julian Price |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 27–36 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Founder, trader, husband, son, anxious insider, ambitious witness and persuasive risk-taker whose confidence can fracture.

**Role boundaries:** Do not cast as a senior auditor, elder authority or character older than 36.

**Strong pairings:** Noah Vale for analyst/insider tension; Elena Marquez for spouse or sibling conflict; Maya Chen for startup or inheritance conflict; Sara Keene for son/mother stakes; Omar Haddad for partners or borrower/banker pressure.

## Identity lock

Master identity: a Black man in his early thirties with deep brown skin.

Structural anchors — preserve verbatim and in this order:

1. narrow oval face.
2. short tightly curled hair.
3. wide-set dark-brown eyes.
4. strong tapered jaw.
5. small vertical scar through the left eyebrow.

Body and posture: tall, lean athletic frame, restless energy contained in shoulders and hands.

Default wardrobe range: dark slate open-collar shirt, ink jacket and a slim aged-brass watch.

Public mask: Effortless persuasive confidence.

Pressure tell: Turns the brass watch face inward and hides it under his cuff.

## Voice and performance lock

resonant upper baritone, neutral North American English, fast confident rhythm, clean projection and an audible half-beat delay when deciding whether to lie.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a Black man in his early thirties with deep brown skin, defined by these exact structural anchors in order: narrow oval face; short tightly curled hair; wide-set dark-brown eyes; strong tapered jaw; small vertical scar through the left eyebrow. tall, lean athletic frame, restless energy contained in shoulders and hands. Effortless persuasive confidence with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing dark slate open-collar shirt, ink jacket and a slim aged-brass watch. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: narrow oval face; short tightly curled hair; wide-set dark-brown eyes; strong tapered jaw; small vertical scar through the left eyebrow. Show Julian Price as a full figure with tall, lean athletic frame, restless energy contained in shoulders and hands, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing dark slate open-collar shirt, ink jacket and a slim aged-brass watch. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: narrow oval face; short tightly curled hair; wide-set dark-brown eyes; strong tapered jaw; small vertical scar through the left eyebrow. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-008 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: narrow oval face; short tightly curled hair; wide-set dark-brown eyes; strong tapered jaw; small vertical scar through the left eyebrow. Preserve tall, lean athletic frame, restless energy contained in shoulders and hands; resonant upper baritone, neutral North American English, fast confident rhythm, clean projection and an audible half-beat delay when deciding whether to lie. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-008/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-008/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-008/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-008/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-008/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

