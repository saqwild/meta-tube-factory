"""Owner doctrine (2026-10-29): "Inside means inside". An episode about the inside of X shows the interior of X, with the
Explorer physically in it; it is not an outside view of a digital/see-through body model with a caption. Owner answers in session:
an outside view of the whole body is allowed *when needed* to show where the organ sits (not as the main view), and the negative
terms are added only where they do not stop that locator shot, so x-ray / transparent-body terms are NOT added channel-wide.
Edits: VISUAL_STYLE_CONTRACT, STORY_ENGINE, QA_CHECKLIST, 04a and 05a stage contracts, render negative list, CHANGELOG."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
B = HERE / "bible"


def sub(p: Path, old: str, new: str) -> None:
    s = p.read_text(encoding="utf-8")
    assert s.count(old) == 1, f"{p.name}: anchor count {s.count(old)}: {old[:60]!r}"
    p.write_text(s.replace(old, new), encoding="utf-8", newline="\n")


RULE = """## Inside means inside (owner rule, 2026-10-29)

An episode about the inside of something shows the **interior** of that thing, with the Explorer physically in it. It never substitutes an
outside view of a digital model for the journey.

- **"Inside your brain"** is the brain's interior at the scale where the process happens: the structures that really make it up (neurons,
  glial cells, vessels, fluid). **"Inside your stomach"** is the stomach: gastric folds, mucus, acid. The same holds for a material, a
  machine or a device: the camera is in its interior, not looking at a model of it.
- **Not allowed as the main view of an inside clip:** a whole-body transparent or X-ray figure, a hologram or wireframe body, glowing organs
  floating in an outline, a labelled anatomy diagram, a medical-infographic look. A caption saying "this is your brain" over such a view does
  not make it the inside.
- **Orientation, and the locator exception (owner: "can be integrated if needed").** Where the viewer needs to know where the organ or part
  sits, the story may show **an outside view of the body or object to locate it**, for example the whole body with the brain's position
  marked. This is a brief locator, used only when the story needs it, never the journey itself, and it is a separate clip from every
  inside clip. By default the outside "you" clip, the narration and a Remotion label do the orienting.
- Each inside clip's frame-0 still shows the named interior, built at 04c as a scene plate of its own. The structures in it come from the
  visualization ledger. The "scale, colour and visibility are simplified" disclosure still applies.
- **Checks.** 04a records the interior each scene is set in and whether it is a locator. The 04f2 vision gate asks the neutral question "is the
  camera inside the named place, or looking at a model of it from outside?" before it sees any claim. 05a repeats it on the rendered clip.
"""

sub(B / "VISUAL_STYLE_CONTRACT.md", "## Explorer identity and voice lock\n", RULE + "\n## Explorer identity and voice lock\n")

sub(B / "STORY_ENGINE.md", "- One smaller metaphor per checkpoint, also staged inside.\n",
    "- One smaller metaphor per checkpoint, also staged inside.\n"
    "- **Inside means inside** (`VISUAL_STYLE_CONTRACT.md`): \"inside\" is the real interior of the named organ, material or device, not an outside view of a "
    "digital model. An outside locator view is allowed only when needed to show where it sits.\n")
sub(B / "STORY_ENGINE.md", "An outside clip carries only the \"you\" figure, never the Explorer in the same frame.",
    "An outside clip carries only the \"you\" figure, never the Explorer in the same frame. A locator view of the body or object (where the organ or part sits) is also an outside clip, used only when needed.")

sub(B / "QA_CHECKLIST.md", "- **05a / 04h:** check for dead stretches",
    "- **04f2 and 05a, \"inside means inside\":** for every inside clip ask, before showing any claim, \"is the camera inside the named place, or looking at a model of it from outside?\" "
    "An outside view of a digital or see-through body model fails unless the scene is a declared locator clip.\n"
    "- **05a / 04h:** check for dead stretches")

sub(ROOT / "pipeline/stages/04a-visual-brief.md",
    "This is the last stage before any image or video prompt gets written",
    "For `inside-the-process`, each scene also records the **interior it is set in** (the organ, material or device named by the title, at the scale where the process\n"
    "happens) and whether it is a **locator** (an outside view used only to show where that interior sits). An inside scene is never an outside view of a digital model\n"
    "(`bible/VISUAL_STYLE_CONTRACT.md` → \"Inside means inside\").\n\n"
    "This is the last stage before any image or video prompt gets written")

sub(ROOT / "pipeline/stages/05a-render-qa.md", "## Output\n",
    "For `inside-the-process`, also judge every inside clip against \"inside means inside\" (`bible/VISUAL_STYLE_CONTRACT.md`): the camera is in the named interior, "
    "not looking at a digital or see-through model of it from outside, unless the clip is a declared locator.\n\n## Output\n")

CJ = HERE / "channel.json"
sub(CJ, '      "visible face behind the visor"\n    ],',
    '      "visible face behind the visor",\n      "hologram",\n      "wireframe body",\n      "medical infographic",\n      "neon outline diagram",\n      "labelled anatomy diagram"\n    ],')
json.loads(CJ.read_text(encoding="utf-8"))

CL = HERE / "CHANGELOG.md"
s = CL.read_text(encoding="utf-8")
CL.write_text(s.rstrip("\n") + """

### 2026-10-29 — "Inside means inside" (owner doctrine)

The owner saw earlier episodes show a digital, see-through body model instead of the interior, and asked that "inside your brain" show the real brain interior (structure, cells) with the Explorer in it. `bible/VISUAL_STYLE_CONTRACT.md` now has the rule; `STORY_ENGINE.md`, `QA_CHECKLIST.md`, stage 04a and stage 05a carry it. An outside locator view of the body (to show where the organ sits) is allowed when needed, as its own clip. Five negative terms added (hologram, wireframe body, medical infographic, neon outline diagram, labelled anatomy diagram); "transparent human body" and "x-ray" were left out on purpose so a locator shot is not suppressed. Script: `_adopt-2026-10-29-inside-means-inside.py`.
""", encoding="utf-8", newline="\n")
print("inside-means-inside applied")
