# Character System and Identity Contract

## 1. Architecture

Signed Anyway uses a repertory cast: two canonical anchors and eight reusable performers. The same repertory face may play different compatible episode roles, as actors do in an anthology series.

Sources of truth:

| Source | Authority |
|---|---|
| `CAST.md` | Registry, role fit, pairing matrix and reuse boundaries |
| `characters/CAST-XXX_*.md` | Immutable performer identity, prompt suite, voice and approved assets |
| Episode `story/characters.md` | Selected cast, story-character names and episode overlays |
| Episode `visual/character-assets.json` | Hash-bound local reference snapshot used for generation |
| `KEY_CHARACTER_PROMPTS.md` | image and clip prompt syntax and compilation rules |

## 2. What is globally locked

For every master cast member, preserve verbatim:

- cast ID and master-card version;
- structural facial anchors in the stated order;
- ethnicity, skin tone, eye color and playing-age band;
- body frame, height impression, hairline and default hair identity;
- voice timbre, resonance, cadence and accent baseline;
- identity portrait, full-body reference and approved character sheet;
- Reference-sheet identity clause.

## 3. What an episode may change

- story-character name for repertory performers;
- occupation and institutional rank;
- relationship to other story characters;
- objective, secret, contradiction and moral defense;
- wardrobe inside the character’s approved range;
- temporary fatigue, injury, grooming change or emotional condition;
- scene blocking, expression, posture and performance intensity.

An episode must state each change as an overlay. Silence means the master default applies.

## 4. Anchor exception

- CAST-001 Evelyn Shaw remains Evelyn Shaw and remains the examiner.
- CAST-002 Noah Vale remains Noah Vale and remains the evidence specialist.
- Anchors are not spouses, relatives, accused executives or harmed witnesses.
- An episode may omit either anchor when the story format does not require them.

## 5. Repertory boundaries

Recasting is allowed, but audience recognition must be managed:

- one role per performer per episode;
- two-episode cooldown before the same performer again leads the case;
- five-episode cooldown before the same pair changes intimate relationship type;
- no instant victim-to-villain reversal in consecutive uploads;
- no age transformation beyond the master playing range;
- no ethnicity, disability or accent change as a costume;
- no reuse of a role-specific signature prop as if it belonged to the performer globally.

## 6. Episode-local creation rule

Create a new performer when:

- none of the ten profiles fits the required playing age or cultural context;
- all suitable performers violate cooldown or pairing rules;
- the story needs a visual or vocal quality not represented in the catalog;
- using a familiar face would reveal the twist or weaken credibility;
- the character is likely to recur and needs a new stable identity.

New performers are episode-local by default. Promotion to the master cast requires a complete card, approved assets, version number and owner sign-off.

## 7. Reference-pack standard

Each master performer ultimately requires:

1. neutral head-and-shoulders identity portrait;
2. full-body neutral wardrobe reference;
3. six-panel sheet: front, three-quarter, profile, composed, cornered and full figure;
4. optional seated reference for anchors;
5. optional 3–5 second voice/performance reference;
6. asset manifest with paths, dimensions, hashes and approval status.

Do not generate ten independent faces for a sheet. Approve the portrait first, then generate every other reference from that portrait.

## 8. Episode selection snapshot

The episode `story/characters.md` references the master ID and version. Before clip prompting, the selected master card and approved assets are copied into the episode’s reference package and hash-bound. This preserves reproducibility if the global master evolves later.

The snapshot is verbatim. Episode overlays live beside it and never edit the snapshot.

## 9. Dramatic character requirements

Every episode character, master or local, must receive:

1. visible objective;
2. private fear;
3. point of no return;
4. strongest moral defense;
5. evidence-based contradiction;
6. human or institutional cost;
7. public mask;
8. physical tell under pressure.

These are story properties, not global performer identity properties.

## 10. Generation prohibitions

- No celebrity or public-figure likeness or voice.
- No blending of two master faces into a new identity.
- No silent change to stable anchors.
- No generated paragraphs on evidence documents.
- No identity correction by face replacement when a clean rerender is possible.
- No master asset is approved until it passes front, three-quarter, profile and mobile-size face checks.
