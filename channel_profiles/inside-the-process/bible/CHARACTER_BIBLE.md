# Character and Recurring Prop Bible

`CAST.md` is the registry. This file defines identity control and reuse rules.

## CAST-001 — Explorer

Adult field observer with practical proportions, orange pressure suit, restrained dark seams, white helmet and dark visor. The silhouette—not a face—is the channel identity. The Explorer is curious, calm and observant. They never command cells, operate a factory step, repair a device or claim expertise beyond what Control explains.

### Invariants

- One adult body; no child proportions.
- White helmet, dark visor, orange suit and practical gloves/boots.
- No exposed face unless a separately approved future redesign replaces the visor contract.
- No weapon, magic tool, repair beam or branded equipment.
- No real-person or franchise likeness.

### Performance range

Allowed: observe, point without touching, brace during movement, turn toward a process, react with contained surprise and speak concise questions. Speech is always a voice heard over the helmet radio. While the line plays, the Explorer holds still, watching, with the visor unchanged. Gestures (lean, helmet turn, pointing, open-palm question) come in the speech-free moments before or after the line. There is never lip-synced speech, and the face is never shown (`VISUAL_STYLE_CONTRACT.md` voice rule). Avoid exaggerated comedy, panic, triumph, dancing and direct manipulation of the process.

## VOICE-001 — Control

Audio-only adult English guide. Calm, plain and precise. Control supplies causal explanation and corrects overstatement. No visible portrait or body is created. Voice identity/model and rights must be recorded when a reusable audio reference is locked.

## PROP-001 — Capsule

Compact rounded ivory exploration capsule, one orange horizontal stripe, clear curved canopy, two small cyan navigation lights, soft white headlamps and one seat. The capsule is transport and observation equipment only.

### Invariants

- Stable hull silhouette and canopy proportion.
- Orange stripe remains horizontal and continuous.
- Two cyan lights retain their position.
- One Explorer; no extra passengers.
- No biological beam, manipulator arms or unexplained size change.

## Reference hierarchy

1. Approved channel master sheet and hash, once promoted.
2. Episode snapshot copied from that master.
3. Approved composed first-frame plate.
4. Generated video derived from the plate.

Do not re-anchor from a late generated frame when the master exists. The channel masters in `../locked-references/characters/` are the image locks (adopted from the sibling profile 2026-10-29, owner decision); the text specification alone is not an image lock. LTX EP001 used the same Explorer and capsule images (byte-identical), so the masters are unchanged for this profile.

## Versioning

Master cards use semantic versions. A color correction or cleaned edge is a patch; wardrobe or geometry change is a minor version; face reveal or capsule redesign is a major version. Record the selected version and asset hashes in every episode manifest.
