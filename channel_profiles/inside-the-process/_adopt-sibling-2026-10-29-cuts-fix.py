"""Correction to _adopt-ltx-2026-10-29.py (owner question, 2026-10-29): LTX-2.5 supports cuts natively, and
pipeline/LTX_I2V_CONTRACT.md §4 already allows a *declared* cut (LTXV-D050/D051). The first pass wrote that cuts were a LTX-only
capability that is "not adopted" and that every hard cut is "unplanned". That overstated the contract. This pass rewrites those
passages so the story engine defers to the contract. Camera movement needed no change (the contract already requires it)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE / "bible"


def sub(p: Path, old: str, new: str) -> None:
    s = p.read_text(encoding="utf-8")
    assert s.count(old) == 1, f"{p.name}: anchor count {s.count(old)}: {old[:60]!r}"
    p.write_text(s.replace(old, new), encoding="utf-8", newline="\n")


SE = B / "STORY_ENGINE.md"
sub(SE, "| One state per clip, state changes across cuts; sourcing,",
    "| `LTX_I2V_CONTRACT.md` §4 rules for cuts and camera; sourcing,")
sub(SE, "It is **not** kept alive by morphing the frame-0 object into another state inside the clip; i2v keeps frame 0's shape, and state changes belong across cuts.",
    "It is **not** kept alive by morphing the frame-0 object into another state inside a take; i2v keeps frame 0's shape, so a change of state belongs across a cut (a clip boundary, or a declared cut under §7).")
start = SE.read_text(encoding="utf-8")
i = start.index("## 7. Cuts (not adopted)")
j = start.index("## 8. Recurring-character protection")
new7 = """## 7. Cuts and camera

LTX-2.5 supports cuts inside one prompt natively, and `pipeline/LTX_I2V_CONTRACT.md` §4 already governs them. **This engine adds no new mechanism and no new syntax**; it only sets where this channel may use what the contract allows.

- **Camera movement:** unchanged. Every clip already carries a motivated camera movement in natural language, never a number (`LTXV-D053`). The "visible change about every 5 s" of §6 is delivered first by camera and flow.
- **Single take stays the default**, as in the contract: one continuous take unless the clip genuinely needs a new framing. A cut is never used to escape a frame-0 contradiction.
- **A declared cut is allowed on process and environment clips**, under the contract: name the transition in prose (a hard cut, a match cut and so on), re-establish scale, identity and light after it, state whether dialogue, music and ambience continue across it, and record `declared_cuts` for the clip so `LTXV-D050`/`D051` can check the count. An undeclared cut still fails.
- **Not on Explorer or "you" clips.** After a cut the video model has no frame-0 anchor, and a close-up of the Explorer is where costume drift and a shoulder patch appeared in the sibling profile's tests (§8). Those clips use camera movement instead. This is a channel rule, not an engine limit.
- **Restate every state-bearing detail after the cut** (positions, contact, gap, colours, materials): the shot after it has only text.
- **Place the cut at a sentence break** if the clip has dialogue, and let the narration land on the shot that shows the result (`LTX_I2V_CONTRACT.md` §4).
- **No LTX render on this channel has used a declared cut yet** (EP001 was 32 single takes). Treat the first use as unproven: pilot it at 04h, start with at most one cut per clip, and record the result before relying on it. A cut also changes the "one state per clip" planning rule: a state change may now sit across a declared cut inside a clip, but clip-boundary changes stay the safer default.

"""
SE.write_text(start[:i] + new7 + start[j:], encoding="utf-8", newline="\n")
sub(SE, "3. **At 05 ingest,** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8). With no planned cuts, every hit is reviewed.",
    "3. **At 05 ingest,** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8) and compare each hit with the clip's declared cuts; any hit that is not a declared cut is reviewed.")

CC = B / "CINEMATOGRAPHY_CONTRACT.md"
sub(CC, "- **A clip is one continuous take.** The sibling profile's planned cut inside a clip is not adopted; a change of state happens across clips. Any hard cut in a rendered clip is unplanned and is reviewed at 05.",
    "- **Camera movement and cuts follow `pipeline/LTX_I2V_CONTRACT.md` §4 unchanged.** Single take is the default; a declared cut is allowed on process and environment clips only (never on Explorer or \"you\" clips), with the transition named, state restated and audio continuity stated. See `STORY_ENGINE.md` §7. Any hard cut in a rendered clip that was not declared is reviewed at 05.")
sub(B / "QA_CHECKLIST.md", "Clips here have no planned cuts, so every hit is listed for review.",
    "Hits that match a clip's declared cut are expected; every other hit is listed for review.")

CL = HERE / "CHANGELOG.md"
sub(CL, "- Planned **cuts inside a clip**: not adopted. A clip here is one continuous take, and state changes happen across clips.\n",
    "- The sibling's **cut-inside-a-clip syntax** (`[Shot N] At MM:SS`): not adopted. LTX-2.5 does support cuts, and `LTX_I2V_CONTRACT.md` §4 already governs declared cuts (the first pass of this file wrongly called cuts a LTX-only capability; corrected by `_adopt-ltx-2026-10-29-cuts-fix.py`). `STORY_ENGINE.md` §7 defers to the contract.\n")
print("cuts fix applied")
