# inside-the-process — channel-level locked reference images

**Adopted from the sibling repo `sibling-repo` on 2026-10-29 (owner decision).** The files in `characters/` are the
channel masters for the Explorer, the capsule and the recurring "you" figure. They are still images and engine-agnostic;
they were copied byte-for-byte and the SHA-256 values below match the source files. Do not regenerate them.

| File | Role | SHA-256 |
|---|---|---|
| `EP001-CAST001-sheet.png` | Explorer master sheet (never a conditioning input) | `61a11b4eb79e73c88ba606f72fdef0d24b5ffe93363e1cc96561ad3decbf7728` |
| `EP001-CAST001-full-body.png` | Explorer, full body | `b7f47933ea090195c85b87d19a0fd674c217d949ef434d27c896e2d37dd02a02` |
| `EP001-CAST001-portrait.png` | Explorer, portrait | `0024b9fe9ba8551c47bf3ce00d3ce740967599ef262b27642962f35835080446` |
| `EP001-CAST001-seated-in-capsule.png` | Explorer seated in the capsule | `5b4dc965b1d6ae5c6c84c8cb4765664cf8b3fdcd306ece01d2106fb415394ca5` |
| `EP001-PROP001-capsule-sheet.png` | Capsule master sheet | `41770ae9d00b5222bbccd07971bfa09005ca7792516fd7db3e6a26d67742d612` |
| `EP004-CAST002-sheet.png` | "You" figure master sheet (never a conditioning input) | `e313375153c3815bf20bf1005d67fd2923f5c5333ea7c9a5d7cd0b688949485e` |
| `EP004-CAST002-full-body.png` | "You" figure, full body | `476dc92e799c2c4945b4c1c30f22ce9b0d352a8b13cf20bb6b945287285822c8` |
| `EP004-CAST002-portrait.png` | "You" figure, portrait | `1890a0ae89f76c134cd41b8ed4a40710f2176a212f8bad3b346b58cfe8e1e202` |
| `EP004-CAST002-seated-desk.png` | "You" figure, seated at a desk | `7ea66109ae0cd1efc5d69eb3216389e6109eca2217cf98d1308920ae58191579` |

The `EP001-`/`EP004-` prefixes are the **sibling profile's** episode numbers (where each master was made and locked: Explorer and
capsule by the owner on 2026-10-29; CAST-002 owner-selected from three candidates at that profile's EP004 04b on 2026-10-29,
generated with muse-image-1.0 via muse-image as an owner-directed exception to Muse Image). Keep the names unchanged so the
hashes and the sibling's manifests stay traceable. This profile's own episode numbering is separate.

**Use.** Condition frame-0 stills on the bare `full-body`, `portrait`, `seated-in-capsule` or `seated-desk` file, never on a
whole `sheet` (a still-image model fed a composed sheet inherits the whole page). Episodes snapshot the files they use
byte-for-byte into `visual/references/characters/` and record their SHA-256 hashes in `visual/references/manifest.md`.

**Same images as LTX EP001.** The five Explorer and capsule files above are byte-identical to the copies inside-the-process LTX EP001 already used
(`episodes/inside-the-process/EP001/visual/references/characters/`; hashes compared 2026-10-29), so EP001 and every later episode share one
Explorer and one capsule. Only the CAST-002 "you" figure is new to this profile. No voice asset is locked.

The authoritative designs are `../bible/CAST.md`, `../bible/CHARACTER_BIBLE.md` and `../bible/VISUAL_STYLE_CONTRACT.md`.
