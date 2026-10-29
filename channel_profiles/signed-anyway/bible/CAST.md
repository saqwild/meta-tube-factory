# Signed Anyway — Master Cast Registry

## 1. Purpose

This is the channel-level repertory cast. It defines ten reusable performer identities, what each performs best, where each should not be used, and which pairings create useful dramatic contrast.

The master identity is a production identity. An episode may cast a repertory performer as a CFO, spouse, auditor, heir or witness under a story-specific character name. The face, body, voice and age band remain locked; the occupation, wardrobe, objective and story name may change.

## 2. Cast classes

| Class | Rule |
|---|---|
| **Anchor** | Fixed on-screen identity and function across episodes; never recast into family, romantic or accused roles. |
| **Repertory** | Stable performer identity that may play different episode characters inside the approved role boundaries. |
| **Episode-local** | New performer created for one episode when the master cast does not fit; may later be promoted by owner approval. |

## 3. Master cast

| ID | Master identity | Class | Playing age | Best functions | Strong pairings | Master card |
|---|---|---|---:|---|---|---|
| CAST-001 | Evelyn Shaw | Anchor | 39–46 | Examiner, moral pressure, precise cross-examination | 003, 006, 009 | `characters/CAST-001_EVELYN_SHAW.md` |
| CAST-002 | Noah Vale | Anchor | 32–39 | Evidence specialist, technical translation, reconstruction guide | 005, 007, 008 | `characters/CAST-002_NOAH_VALE.md` |
| CAST-003 | Adrian Cole | Repertory | 44–54 | CFO, founder, father, compromised protector, senior spouse | 001, 004, 006, 009, 010 | `characters/CAST-003_ADRIAN_COLE.md` |
| CAST-004 | Elena Marquez | Repertory | 34–43 | Plant manager, spouse, whistleblower, harmed professional, elder daughter | 003, 007, 008, 009 | `characters/CAST-004_ELENA_MARQUEZ.md` |
| CAST-005 | Daniel Mercer | Repertory | 51–62 | Auditor, attorney, board chair, trustee, institutional witness | 002, 006, 007, 010 | `characters/CAST-005_DANIEL_MERCER.md` |
| CAST-006 | Naomi Reed | Repertory | 46–57 | CEO, senior counsel, matriarch, board power, controlled antagonist | 001, 003, 005, 007, 009 | `characters/CAST-006_NAOMI_REED.md` |
| CAST-007 | Maya Chen | Repertory | 25–34 | Analyst, coder, junior whistleblower, daughter, heir, idealist | 002, 004, 005, 008 | `characters/CAST-007_MAYA_CHEN.md` |
| CAST-008 | Julian Price | Repertory | 27–36 | Founder, trader, husband, son, anxious insider, ambitious witness | 002, 004, 007, 009, 010 | `characters/CAST-008_JULIAN_PRICE.md` |
| CAST-009 | Sara Keene | Repertory | 40–50 | Spouse, caregiver, union leader, sibling, owner, moral counterweight | 001, 003, 004, 006, 008, 010 | `characters/CAST-009_SARA_KEENE.md` |
| CAST-010 | Omar Haddad | Repertory | 37–47 | Banker, operations chief, investigator, brother, community leader | 003, 005, 008, 009 | `characters/CAST-010_OMAR_HADDAD.md` |

## 4. Pairing matrix

`3` = primary pairing, `2` = strong, `1` = usable, `—` = same performer, `X` = avoid without an explicit story reason.

|  | 001 | 002 | 003 | 004 | 005 | 006 | 007 | 008 | 009 | 010 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **001 Evelyn** | — | 2 | 3 | 2 | 2 | 3 | 2 | 2 | 3 | 2 |
| **002 Noah** | 2 | — | 1 | 2 | 3 | 1 | 3 | 3 | 1 | 2 |
| **003 Adrian** | 3 | 1 | — | 3 | 2 | 3 | 1 | 2 | 3 | 3 |
| **004 Elena** | 2 | 2 | 3 | — | 1 | 2 | 3 | 3 | 3 | 2 |
| **005 Daniel** | 2 | 3 | 2 | 1 | — | 3 | 3 | 1 | 2 | 3 |
| **006 Naomi** | 3 | 1 | 3 | 2 | 3 | — | 3 | 1 | 3 | 2 |
| **007 Maya** | 2 | 3 | 1 | 3 | 3 | 3 | — | 3 | 2 | 2 |
| **008 Julian** | 2 | 3 | 2 | 3 | 1 | 1 | 3 | — | 3 | 3 |
| **009 Sara** | 3 | 1 | 3 | 3 | 2 | 3 | 2 | 3 | — | 3 |
| **010 Omar** | 2 | 2 | 3 | 2 | 3 | 2 | 2 | 3 | 3 | — |

## 5. Boundary rules

1. One performer plays only one story character in an episode.
2. CAST-001 and CAST-002 retain their names and canonical channel functions.
3. Repertory performers may change story name, occupation, relationship, objective, wardrobe and temporary condition.
4. Repertory performers may not change face geometry, ethnicity, skin tone, eye color, hairline, body frame, stable voice timbre or playing-age band.
5. Do not cast the same performer as the central decision-maker in consecutive episodes; preferred cooldown is two episodes.
6. Do not reuse the same pair as a different intimate relationship—such as spouses followed by siblings—within five episodes.
7. Avoid using more than two previously seen repertory faces in one episode unless it is an intentional crossover.
8. A performer can move between corporate and domestic roles only when the role fits the approved playing age and performance range.
9. Create a new episode-local performer when the story requires a materially different age, physical identity, cultural context, disability, vocal quality or dramatic energy.
10. A new performer joins the master cast only after owner approval and a complete reference pack.

## 6. Episode selection order

```text
Approved case brief
→ required dramatic functions
→ search master cast by function and playing age
→ check pair cooldown and relationship history
→ select master IDs or declare new episode-local performer
→ pin master version and asset hashes
→ write episode role overlays
→ script dialogue
```

The writer may suggest a new performer. It may not silently create one or alter a master identity.

## 7. Versioning

- Current registry version: `1.0.0`.
- Every master character card has its own version.
- Face/voice changes require a major version.
- Prompt clarification without identity change requires a minor version.
- Typographic or path correction requires a patch version.
- An episode records the card version and SHA-256 of every selected master file and reference asset.
