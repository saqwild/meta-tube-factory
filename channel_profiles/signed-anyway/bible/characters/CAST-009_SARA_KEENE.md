# CAST-009 — Sara Keene

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-009 |
| Master identity | Sara Keene |
| Class | Repertory |
| Master-card version | 1.0.0 |
| Playing age | 40–50 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Spouse, caregiver, union leader, sibling, owner, parent and moral counterweight whose empathy does not imply weakness.

**Role boundaries:** Do not cast as a junior coder, very young heir or emotionally detached technocrat. Playing age remains inside 40–50.

**Strong pairings:** Evelyn Shaw for humane counterargument; Adrian Cole for marriage or labor-versus-management conflict; Elena Marquez for siblings/allied witnesses; Naomi Reed for rival authority; Omar Haddad for marriage or community stakes.

## Identity lock

Master identity: a Middle Eastern woman in her mid-forties with olive skin.

Structural anchors — preserve verbatim and in this order:

1. long oval face.
2. thick dark wavy hair with silver at both temples.
3. dark hazel eyes.
4. strong gently angled eyebrows.
5. pronounced smile lines.

Body and posture: average height, grounded full frame, warm open posture that becomes immovable under pressure.

Default wardrobe range: paper-ivory blouse, ink-navy long jacket and a small aged-brass ring.

Public mask: Generous emotional steadiness.

Pressure tell: Twists the brass ring once, releases it and places both hands openly on the table.

## Voice and performance lock

warm textured contralto, neutral international English with a light Levantine cadence, patient tempo, rounded vowels and a steady rise in intensity without shouting.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a Middle Eastern woman in her mid-forties with olive skin, defined by these exact structural anchors in order: long oval face; thick dark wavy hair with silver at both temples; dark hazel eyes; strong gently angled eyebrows; pronounced smile lines. average height, grounded full frame, warm open posture that becomes immovable under pressure. Generous emotional steadiness with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing paper-ivory blouse, ink-navy long jacket and a small aged-brass ring. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: long oval face; thick dark wavy hair with silver at both temples; dark hazel eyes; strong gently angled eyebrows; pronounced smile lines. Show Sara Keene as a full figure with average height, grounded full frame, warm open posture that becomes immovable under pressure, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing paper-ivory blouse, ink-navy long jacket and a small aged-brass ring. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: long oval face; thick dark wavy hair with silver at both temples; dark hazel eyes; strong gently angled eyebrows; pronounced smile lines. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-009 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: long oval face; thick dark wavy hair with silver at both temples; dark hazel eyes; strong gently angled eyebrows; pronounced smile lines. Preserve average height, grounded full frame, warm open posture that becomes immovable under pressure; warm textured contralto, neutral international English with a light Levantine cadence, patient tempo, rounded vowels and a steady rise in intensity without shouting. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-009/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-009/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-009/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-009/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-009/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

