"""Owner-approved follow-up (2026-10-29): wire the story engine into the story-writing path.

Edits the three story-stage contracts and the story-writer skill. Only inside-the-process text is added; every existing LTX-specific
rule (coverage map, clip_split_check, verify-only follow-up rounds, blind naive-viewer test) is kept. Adapted from sibling-repo's
01-ideation / 03a-writer / 03b-script-review, re-expressed in percentages on this repo's ~32-clip grid. Read-only on sibling-repo.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sub(p: Path, old: str, new: str) -> None:
    s = p.read_text(encoding="utf-8")
    assert s.count(old) == 1, f"{p.name}: anchor count {s.count(old)}: {old[:60]!r}"
    p.write_text(s.replace(old, new), encoding="utf-8", newline="\n")


ST = ROOT / "pipeline" / "stages"

# 01-ideation
sub(ST / "01-ideation.md",
    "## Output\n\n`episodes/<slug>/EPxxx/story/premise.md`",
    """### `inside-the-process` — story definition (`bible/STORY_ENGINE.md`)

From the next LTX episode on, also write `story/story-definition.md`, the Story Definition Sheet (`STORY_ENGINE.md` §10), and give it
to the owner with the premise. It is a draft: every fact in it is a research target until `02a` clears it, and `03a` confirms or
revises it. Choose topics as "you + an everyday action + time". Name the pillar's "you" anchor (§2) and a master metaphor that can be
staged as an inside place the Explorer enters. The sheet's clock must be real: do not promise an hour-by-hour structure for a topic
whose sources do not support one. This sheet is a document, not a machine gate.

## Output

`episodes/<slug>/EPxxx/story/premise.md`""")

# 03a-writer
sub(ST / "03a-writer.md",
    "## Forbidden\n\nDo not perform `03b-script-review` yourself",
    """### `inside-the-process` — story engine (`bible/STORY_ENGINE.md`)

- First confirm or revise `story/story-definition.md` against the cleared `02a` claims. Any fact the sources do not support leaves the sheet.
- Write to the arc in §3, as shares of runtime on this episode's clip grid: hook in the first ~7%; struggle through ~25-40%; climax at
  ~43-50% with the master metaphor paid off inside it; objection at ~53-58%; practical at ~70-85% (explanation, never instruction);
  caveats; a callback plus a clock-tied comment question at the end.
- Narration: Control speaks to "you" throughout. About 20-25% of clips are outside ones showing the recurring "you" figure; the rest are inside.
- Each clip's visible action names a visible change about every 5 s (§6). A declared cut is allowed only as `STORY_ENGINE.md` §7 and
  `LTX_I2V_CONTRACT.md` §4 describe.
- The Explorer's lines are a helmet-radio voice-over, only in rows where the Explorer is visible (`VISUAL_STYLE_CONTRACT.md` voice rule).

## Forbidden

Do not perform `03b-script-review` yourself""")

# 03b-script-review
sub(ST / "03b-script-review.md",
    "EP001 passed an independent review without ever showing what glass is made",
    """**Story-engine checks (`inside-the-process`, from the next LTX episode, `bible/STORY_ENGINE.md`):** also check that
the arc lands at its targets (§3), narration stays second person, the master metaphor is set up early and paid off with the Explorer
inside it, the objection comes before the practical section, the practical section is explanation and not instruction (§11), the
outside share is about 20-25%, the Explorer's lines are helmet-radio voice-over only in rows where the Explorer is visible, and every
metaphor appears in the visualization ledger. Follow-up rounds after a `REVISE` stay verification-only, as above.

EP001 passed an independent review without ever showing what glass is made""")

# the story-writer skill
SK = ROOT / "local_skills" / "explained-from-within-story-writer" / "SKILL.md"
sub(SK, "audio-only Control explains one cause or limit at a time. Neither directs the\nprocess or claims unsupported authority.",
    """audio-only Control explains one cause or limit at a time. Neither directs the
process or claims unsupported authority. Per the channel voice rule
(`VISUAL_STYLE_CONTRACT.md`):
- Explorer words are a voice over the helmet radio, never lip-synced, and the
  face is never revealed.
- Give the Explorer lines only in rows where the Explorer is visible, and place
  them before Control's line in that row.
- In the visible action, the Explorer holds still, watching, while its line
  plays. Name any body gesture for the moment before or after the line.

From the next LTX episode, the story follows `channel_profiles/inside-the-process/bible/STORY_ENGINE.md`:
confirm `story/story-definition.md` first, write Control's narration to "you", place the arc by share
of runtime, stage the master metaphor as an inside place the Explorer enters, and keep practical
sections to explanation. The recurring outside "you" figure (CAST-002) appears only in outside rows.""")
print("story stages + skill updated")
