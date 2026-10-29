# CAST-001 (Evelyn Shaw) — promoted to channel-level locked reference

**Promoted:** 2026-10-29, during EP002's `04b-character-refs` stage.

**Trigger:** `pipeline/stages/04b-character-refs.md` — "promote only on
second use across episodes — never on first-episode intent." EP001 was
first use (generated fresh via Muse Image, approved). EP002 is
second use — the exact trigger condition.

**Source:** `episodes/signed-anyway/EP001/visual/references/characters/
EP001-CAST001-{portrait,full-body,sheet}.jpg` — the original approved
generation, copied verbatim (same pixels, not regenerated).

**Master card:** `bible/characters/CAST-001_EVELYN_SHAW.md`, version
1.0.0 (unchanged since EP001).

**Usage going forward:** any future episode using CAST-001 as Evelyn
should copy from *this* folder into its own
`episodes/signed-anyway/EPxxx/visual/references/characters/` folder
(matching `04b`'s per-episode output path requirement), not regenerate
and not copy from an intermediate episode. This folder is now the single
source of truth for her locked identity.

**If her identity ever needs to change** (a wardrobe variant, a version
bump): that's a deliberate `CAST.md` §7 versioning decision — bump the
master-card version, regenerate, and re-promote here. Do not silently
overwrite these files.
