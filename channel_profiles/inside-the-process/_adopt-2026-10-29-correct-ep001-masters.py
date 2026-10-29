"""Correction (2026-10-29, found at EP002 04b): the 2026-10-29 adoption docs said LTX EP001's Explorer/capsule references were
'episode-local, not masters'. They are in fact byte-identical copies of the same ltx images now locked as the channel masters
(sha256 compared for all five EP001 files). Fixes the four places that said otherwise and logs the correction."""
from pathlib import Path
H = Path(__file__).resolve().parent
def sub(p, old, new):
    f = H / p; s = f.read_text(encoding="utf-8"); assert s.count(old) == 1, (p, old[:50], s.count(old)); f.write_text(s.replace(old, new), encoding="utf-8", newline="\n")
sub("locked-references/README.md",
    "**Not masters.** The Explorer/capsule references that inside-the-process LTX EP001 generated for itself are episode-local;\nthey stay in that episode and are not channel masters. The Explorer in later episodes is conditioned on the masters above.\nNo voice asset is locked.",
    "**Same images as LTX EP001.** The five Explorer and capsule files above are byte-identical to the copies inside-the-process LTX EP001 already used\n(`episodes/inside-the-process/EP001/visual/references/characters/`; hashes compared 2026-10-29), so EP001 and every later episode share one\nExplorer and one capsule. Only the CAST-002 \"you\" figure is new to this profile. No voice asset is locked.")
sub("bible/CAST.md", "The Explorer/capsule references that LTX EP001 generated for itself are episode-local and are not masters. ",
    "LTX EP001 already used these same Explorer and capsule images (byte-identical copies), so they are unchanged for this profile; only CAST-002 is new. ")
sub("bible/CHARACTER_BIBLE.md", " LTX EP001's own Explorer/capsule references are episode-local, not masters.",
    " LTX EP001 used the same Explorer and capsule images (byte-identical), so the masters are unchanged for this profile.")
sub("channel.json", "LTX EP001's own Explorer/capsule references are episode-local, not masters. No voice asset is locked.",
    "LTX EP001 used the same Explorer and capsule images (byte-identical copies), so only CAST-002 is new to this profile. No voice asset is locked.")
c = H / "CHANGELOG.md"
c.write_text(c.read_text(encoding="utf-8").rstrip("\n") + """

### 2026-10-29 — correction found at EP002 `04b`

The 2026-10-29 adoption said LTX EP001's Explorer/capsule references were episode-local and not masters. That was wrong: EP001's five Explorer and capsule files are byte-identical to the images now locked as the channel masters (it had copied them from the sibling profile on 2026-10-29). Corrected in `locked-references/README.md`, `bible/CAST.md`, `bible/CHARACTER_BIBLE.md` and `channel.json` (`cast.reference_status`). Only CAST-002 is new to this profile. Script: `_adopt-2026-10-29-correct-ep001-masters.py`.
""", encoding="utf-8", newline="\n")
import json; json.loads((H / "channel.json").read_text(encoding="utf-8"))
print("corrected")
