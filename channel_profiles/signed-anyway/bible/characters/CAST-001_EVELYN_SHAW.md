# CAST-001 — Evelyn Shaw

## Registry

| Field | Value |
|---|---|
| Cast ID | CAST-001 |
| Master identity | Evelyn Shaw |
| Class | Anchor |
| Master-card version | 1.0.0 |
| Playing age | 39–46 |
| Prompt status | READY |
| Asset status | TO GENERATE / NOT APPROVED |

## Casting range

**Best uses:** Canonical examiner; precise cross-examination; calm moral pressure; episode orientation without announcing a verdict.

**Role boundaries:** Fixed identity and function. She is never recast as a spouse, relative, accused decision-maker or harmed witness.

**Strong pairings:** Adrian Cole for compromised authority; Naomi Reed for equal-power conflict; Sara Keene for moral and emotional contrast.

## Identity lock

Master identity: a Black woman in her early forties with deep brown skin.

Structural anchors — preserve verbatim and in this order:

1. oval face.
2. high cheekbones.
3. short natural coiled bob.
4. deep-set dark-brown eyes.
5. small vertical line between the brows.

Body and posture: medium-tall, lean balanced frame, upright economical posture.

Default wardrobe range: dark ink structured jacket, paper-ivory blouse and an aged-brass pen.

Public mask: Composed neutrality.

Pressure tell: Closes the file and pauses before the decisive question.

## Voice and performance lock

low measured alto, educated neutral English with a light British cadence, exact consonants, controlled breath and deliberate pauses; pressure comes from slowing down rather than increasing volume.

The episode may adjust emotional intensity, occupational register and speaking speed within natural performance. It may not change the stable timbre, accent baseline, apparent age or vocal resonance.

## Master portrait prompt

~~~text
A head-and-shoulders identity portrait of a Black woman in her early forties with deep brown skin, defined by these exact structural anchors in order: oval face; high cheekbones; short natural coiled bob; deep-set dark-brown eyes; small vertical line between the brows. medium-tall, lean balanced frame, upright economical posture. Composed neutrality with a neutral closed-mouth expression and unobstructed gaze toward camera. Wearing dark ink structured jacket, paper-ivory blouse and an aged-brass pen. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft directional Rembrandt lighting from camera left, clean text-free #24333D slate background, centered eye-level composition, portrait-lens perspective, crisp eyes and natural skin texture.
~~~

## Full-body reference prompt

Use the approved master portrait as image 1.

~~~text
Preserve the exact identity from image 1 and these structural anchors in order: oval face; high cheekbones; short natural coiled bob; deep-set dark-brown eyes; small vertical line between the brows. Show Evelyn Shaw as a full figure with medium-tall, lean balanced frame, upright economical posture, standing in a relaxed neutral reference pose with both hands clearly visible and weight evenly balanced. Wearing dark ink structured jacket, paper-ivory blouse and an aged-brass pen. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Soft even studio lighting, clean unmarked #24333D slate background, full body entirely inside frame, eye-level camera and sharp face-to-foot detail.
~~~

## Six-panel character-sheet prompt

Use the approved portrait as image 1 and approved full-body reference as image 2.

~~~text
Create a clean six-panel production character sheet preserving the exact face from image 1 and exact body frame from image 2. Preserve these anchors in order: oval face; high cheekbones; short natural coiled bob; deep-set dark-brown eyes; small vertical line between the brows. Panel 1 front head-and-shoulders neutral; panel 2 left three-quarter attentive; panel 3 right profile neutral; panel 4 composed medium shot; panel 5 morally cornered close-up using the pressure tell; panel 6 full figure in the default wardrobe. Cinematic painterly graphic-novel realism with hand-painted editorial texture, controlled visible brushwork, natural adult proportions, grounded facial anatomy, restrained ink-navy and slate shadows, aged-brass accents, prestige-drama lighting, readable silhouette and consistent face geometry. Identical face, hair identity, skin tone, playing age and wardrobe across all panels, even reference lighting, clean text-free slate panels with equal spacing.
~~~

Add cast ID, version and panel labels in post.

## Reference-sheet identity clause

~~~text
<Subject N> is the episode character performed by CAST-001 version 1.0.0, defined by the approved portrait, full-body reference and six-panel sheet. Preserve exactly, in order: oval face; high cheekbones; short natural coiled bob; deep-set dark-brown eyes; small vertical line between the brows. Preserve medium-tall, lean balanced frame, upright economical posture; low measured alto, educated neutral English with a light British cadence, exact consonants, controlled breath and deliberate pauses; pressure comes from slowing down rather than increasing volume. Apply the separately declared episode name, occupation, wardrobe variation and current condition without changing the master identity.
~~~

## Voice-reference recording text

Record a neutral 12–18 second dry voice sample in a quiet room:

> I reviewed the figures twice. The amount is accurate, but the reason behind it is still incomplete. Show me the decision that changed what happened next.

## Planned asset manifest

| Asset | Required path | Status |
|---|---|---|
| Portrait | characters/assets/CAST-001/portrait.png | TO GENERATE |
| Full body | characters/assets/CAST-001/full_body.png | TO GENERATE |
| Six-panel sheet | characters/assets/CAST-001/character_sheet.png | TO GENERATE |
| Voice reference | characters/assets/CAST-001/voice_reference.wav | OPTIONAL |
| Asset hashes | characters/assets/CAST-001/manifest.json | TO CREATE |

## Approval gate

- [ ] Portrait passes structural-anchor review.
- [ ] Full body matches portrait identity and body frame.
- [ ] Six-panel sheet preserves one face and playing age.
- [ ] 98-pixel face crop remains recognizable.
- [ ] Voice sample matches the written voice lock.
- [ ] Every approved asset has a SHA-256 hash.
- [ ] Owner marks the pack APPROVED before episode selection.

