# Visual Style Contract

> **CONFIRMED as the on-screen look (owner, 2026-10-29, with a style reference image).** The
> "painterly graphic-novel realism / **not photoreal**" north star below is the channel scope
> for stills **and** video — every character sheet, frame-0 still and rendered clip. An earlier
> 2026-10-29 note that reinterpreted this toward photoreal was **wrong and is withdrawn.**
> `channel.json → render.look_and_feel` and `KEY_CHARACTER_PROMPTS.md` §1 carry the exact style
> anchor to inline into every image prompt. Open pilot-QA question (`04h`): whether LTX-2.5
> holds this painterly look across a 20-second i2v clip — it is untested, but it is the look.

## North star

**Cinematic painterly graphic-novel realism:** the emotional credibility of a prestige drama, the authored texture of painted editorial illustration, the graphic clarity of an evidence exhibit, and a restrained near-future edge. The visual system must hide model weaknesses through deliberate framing, not through noisy effects.

This is an illustrated realism lock: **not photoreal**, not cel-shaded cartoon, not comic caricature, not flat vector, and not glossy 3D/toy rendering.

## Palette

| Color | Hex | Use |
|---|---|---|
| Ink navy | `#07131C` | Shadows, evidence room, backgrounds |
| Slate | `#24333D` | Walls, desks, wardrobe support |
| Aged brass | `#C79A45` | Signature motif, key evidence, practical lights |
| Paper | `#E8E0D1` | Documents, titles, skin-tone contrast |
| Oxblood | `#7B2D26` | One consequence or contradiction cue; maximum 3% of frame |

Legacy red `#A93832` is retired. Do not introduce alternate Ink, Slate, Brass, Paper or red hex values in prompts or post templates.

## Typography

| Role | Typeface | Rule |
|---|---|---|
| Display, short quotations, verdict prompt | Source Serif 4 | Paper by default; sentence or restrained uppercase case |
| Amounts, timestamps, evidence data | IBM Plex Mono | Aged brass by default; tabular figures where available |

Generated type is never final delivery type. Add all readable wording and evidence data in post.

## World sets

1. **Evidence Room:** dark acoustic walls, long table, brass practical, projection surface; recurring visual home.
2. **Domestic Finance:** real apartment or house textures, ordinary bills, phone light, restrained mess; never luxury stock imagery unless story-required.
3. **Corporate Pressure:** boardroom, plant corridor, finance office, empty trading floor; practical fluorescents and specific props.
4. **Reconstruction Space:** stylized but plausible event timeline; distinct from testimony through cooler exposure and more kinetic camera.
5. **Future Verdicts:** same brand palette with one plausible technology change, not generic neon cyberpunk.

## Image rules

- 16:9 master; compose safe for 9:16 short crops.
- Human faces and hands receive priority over background detail.
- Use shallow-to-moderate depth of field; critical evidence remains readable through post graphics.
- At least one practical light source must motivate every scene.
- Generated visible text is prohibited beyond a short number or single word; insert documents and interface text in post.
- No real corporate logos, recognizable products, flags used as accusation shorthand, or visual copying of a living artist.

## Thumbnail contract

- Use a heavily darkened, episode-specific set plate grounded in Ink navy.
- Place one mid-expression fictional face on the right at 40–50% of frame unless a decisive story object wins a documented A/B concept test.
- Place zero to three words on the left third in Paper-colored Source Serif 4. Quotation marks require an exact line spoken or shown in the episode.
- Place one accurate story number bottom-left in Aged-brass IBM Plex Mono; the same number must appear in the episode by 0:10.
- Use one thin fixed brass hairline. A small fictional company/sector silhouette is allowed; real logos are not.
- Oxblood may occupy no more than 3% of the frame. Large red balances, panels and glows fail QC.
- Generate a 3840×2160 16:9 master; compress the upload below 2 MB when practical. Keep critical content inside the central 80% and verify at 10% scale.
- Reserve the lower-right 25% width × 18% height for YouTube's duration/interface overlay. Keep the bottom-left number at least 10% inward from both edges.
- Ban arrows, circles, red rings, shocked-face-plus-explosion layouts, more than three words, episode numbers, fake news lower-thirds and unreadable generated documents.

## Shot-color grammar

- Testimony: neutral ink/slate, stable camera.
- Evidence: paper/brass with surgical warning-red accent.
- Reconstruction: cooler slate, slightly faster motion.
- Reversal: warmth drops, contrast increases subtly.
- Verdict prompt: return to balanced ink/brass; no color-coding one side as morally correct.

## Quality rejection triggers

Reject and rerender any shot with identity drift, unstable wardrobe, deformed hands on a story-critical prop, impossible eyelines, background motion that steals focus, unintended lip movement, or synthetic text presented as evidence.

Every clip manifest must inherit this contract and state the practical light, palette, wardrobe, hero prop, camera, eyeline and 9:16-safe composition. Inspect beginning, middle and end frames rather than only the first frame. Log a coded rejection reason. After three failures on the same action or composition, simplify the shot or move the information to a controlled insert.
