# signed-anyway — channel-level locked reference images

Character sheets that are the **single source of truth** for a cast member's identity, reused
across every episode. A `04b-character-refs` run copies from here into its own
`episodes/<EPID>/visual/references/characters/` — it never regenerates a locked identity and
never copies from an intermediate episode.

Promotion rule (`pipeline/stages/04b-character-refs.md`): a character is promoted here only on
its **second use across episodes**, never on first-episode intent.

## Contents

| Cast | Story identity | Files | Provenance |
|---|---|---|---|
| `CAST-001/` | Evelyn Shaw (anchor examiner) | portrait · full-body · sheet | Copied verbatim from `C:\pycode\sibling-repo\channel_profiles\signed-anyway\locked-references\characters\CAST-001\` — the promoted canonical Evelyn (originally generated + approved for that repo's signed-anyway EP001, painterly-realism, Muse Image, then promoted on EP002 = second use). Same channel, same `CAST-001_EVELYN_SHAW.md` v1.0.0, same painterly look. Model-agnostic image; reused here for `vidgen-ltx` EP001. |
| `CAST-010/` | Omar Haddad (repertory) | portrait · full-body · sheet | Copied verbatim from `C:\pycode\sibling-repo\episodes\signed-anyway\EP002\visual\references\characters\EP002-CAST010-*` — approved painterly generation from `CAST-010_OMAR_HADDAD.md` prompts verbatim (Muse Image; all 5 structural anchors verified in that repo's manifest). Master-default wardrobe (slate suit, no tie, paper-ivory shirt) — the same wardrobe `vidgen-ltx` EP001 uses for **Jonah Park**. `vidgen-ltx` EP001 is this identity's second use → promoted here. |

## Not locked (generate per episode until second use)

CAST-002, 003, 004, 005, 006, 007, 008, 009 — no channel-level lock in `vidgen-ltx` yet. For
`vidgen-ltx` EP001, **CAST-006 (Ruth Merrill) and CAST-007 (Lena Kline)** are generated fresh at
`04b` (see `episodes/signed-anyway/EP001/visual/references/character-image-prompts.md`); they
promote here if a later `vidgen-ltx` episode reuses them.
