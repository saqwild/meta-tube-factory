"""Shared still-prompt claim extraction — SINGLE SOURCE OF TRUTH.

Turns the staging claims a frame-0 still prompt already makes (who is where,
what is touching what, what state an object is in) into a checklist a reviewer —
human or agent — can verify against actual pixels.

Used by `image_agent_packet.py` (pre-render, handed to whoever generates the
stills) so the pre-generation self-check and any post-render gate stay identical
rather than silently diverging.

Two defects in the upstream implementation this was ported from are fixed here;
both are covered by tests:

1. **Position slots were matched case-insensitively.** An environment string
   containing "the fountain at frame-left" therefore claimed the LEFT slot, and
   every scene in the upstream reference episode reported
   `LEFT = warm late-afternoon sunlight` instead of a character. Slots are now
   matched case-sensitively against the documented caps convention and must be
   introduced by "on the" / "at" / "is".
2. **Only the first match per slot was kept.** Two characters legitimately share
   CENTER in a group frame; the second was silently dropped from the checklist.
   All slot claims are now retained.
"""

from __future__ import annotations

import re

# End-state patterns worth visual verification.
STATE_PATTERNS = [
    ("door/window", r"\b(?:door(?:way)?|gate|window|lid)\b[^.]{0,50}\b(?:standing\s+)?(?:open|ajar|closed|shut)\b"
                    r"|\b(?:open|closed)\s+(?:front\s+)?(?:door(?:way)?|gate|window|lid)\b"),
    ("light", r"\b(?:lamp|lantern|candle|hearth|fire|wick)\b[^.]{0,40}\b(?:lit|glowing|burning|unlit|dark|cold)\b"
              r"|\b(?:lit|unlit|glowing|burning)\s+(?:\w+\s+){0,2}(?:lamp|lantern|candle|hearth|fire)\b"),
    ("pose", r"\b(?:seated|sitting|standing|kneeling|crouched|lying|bent(?:\s+over)?|leaning|perched)\b"),
    ("held/placed", r"\b(?:held(?:\s+out)?|holding|gripping|clutching|resting|set\s+down|placed|parked|stationary"
                    r"|on\s+the\s+(?:table|counter|ledge|floor|ground))\b"),
    ("intact/broken", r"\b(?:cracked|broken|shattered|torn|intact|whole|empty|full|overturned)\b"),
    ("cast count", r"\bexactly\s+\w+\s+(?:distinct\s+)?(?:anthropomorphic\s+)?(?:figures?|people|characters)\b"),
]

CLAIM_PATTERNS = [
    ("contact", r"\b(?:both|one|each|either|left|right)\s+(?:fore)?paws?\b[^.]{0,60}"
                r"|\b(?:under|beneath|on top of|against)\s+(?:her|his|their)\s+(?:left |right )?(?:fore)?paw\b"
                r"|\b(?:paws?|hands?)\s+(?:pressing|resting|gripping|holding|touching|pinning|clutching|hovering)\b[^.]{0,50}"),
    ("facing", r"\bears?\s+(?:swivell?ed|turned|pricked|flattened|angled|pointing|tipped)\b[^.]{0,50}"
               r"|\b(?:glancing|looking|gazing|peering|turned|facing|craning)\s+"
               r"(?:back |round |around |over )?(?:toward|towards|at|to|over)\b[^.]{0,60}"
               r"|\bover\s+(?:her|his|their)\s+shoulder\b"
               r"|\b(?:eyes|gaze|head)\s+(?:on|toward|towards|fixed on|turned)\b[^.]{0,40}"),
    ("mouth", r"\bmouth\s+(?:closed|open)[^.]{0,40}"),
    ("containment", r"\b(?:down\s+)?into\s+(?:it|the\s+\w+)\b"
                    r"|\b(?:half\s+)?(?:inside|tucked|crammed|stuffed|buried|hidden)\b[^.]{0,50}"
                    r"|\bdisappearing\b[^.]{0,50}"
                    r"|\b(?:spilling|hanging|draped)\s+(?:out|over|off)\b[^.]{0,40}"),
    ("placement", r"\b(?:against|beside|behind|in front of|next to|atop|on)\s+the\s+(?:\w+\s+){0,2}\w+\b"
                  r"|\b(?:one|two|three|a few|several)\s+steps?\s+(?:down|up|back|away|forward)\b"
                  r"|\b(?:centre|center|left|right)\s+of\s+(?:the\s+)?frame\b"),
]

# Any surface that DEPICTS figures. In an anthropomorphic world these must show
# the channel's own species — a photo or screen showing the wrong kind of figure
# breaks the world.
DEPICTION_PATTERN = (r"\b(?:family\s+)?(?:photo(?:graph)?s?|portraits?|pictures?|paintings?|posters?|"
                     r"framed\s+\w+|artwork|drawings?|magazines?|book\s+covers?|screens?|television|tv)\b")
CROWD_HINT = r"\b(?:crowd|gathered|group|several|neighbou?rs|onlookers|villagers|families)\b"

# Case-SENSITIVE on the slot: the caps convention is the whole point, and
# lowercase "frame-left" inside an environment string is not a position claim.
# The description is captured through a LOOKAHEAD so the match stays zero-width
# past the slot — a greedy capture swallowed the next character's slot claim and
# finditer then skipped it entirely.
POSITION = re.compile(
    r"(?:[Oo]n the|[Aa]t|[Ii]s at)\s+(LEFT|RIGHT|CENTER|CENTRE)\b[,:]?\s*(?=(.{0,110}))")


def positions(body: str, cast: list[str]) -> list[tuple[str, str]]:
    """[(slot, who/what)] from the 'on the LEFT / at CENTER' convention.

    Reviewing a still means first knowing WHO SHOULD BE WHERE — swapped sides is
    a real defect that reads as "fine" unless you were told the intended
    arrangement up front.
    """
    out: list[tuple[str, str]] = []
    for m in POSITION.finditer(body):
        slot = m.group(1).upper().replace("CENTRE", "CENTER")
        desc = re.sub(r"\s+", " ", m.group(2)).strip(" .,;—-")
        if not desc:
            continue
        # Identify WHO from the clause preceding the slot: our convention is
        # "<Name>, <description>, is on the LEFT, <pose>". Take the name NEAREST
        # the slot by position — iterating the cast list and keeping the last
        # hit picks by cast order, which binds the wrong character whenever an
        # earlier sentence mentions someone else (e.g. "Pip's cart" before
        # "Bruno ... is on the LEFT").
        # 220 chars was too tight once identity anchors had to carry fur colour,
        # markings, eyes and wardrobe — the name fell outside the window and the
        # slot bound to nobody. Widening is safe because the NEAREST preceding
        # name still wins, which is the whole point of the scan below.
        before = body[max(0, m.start() - 420):m.start()]
        best_at, who = -1, ""
        for tag in cast:
            hits = list(re.finditer(rf"\b{re.escape(tag.split('_')[0])}\b", before, re.I))
            if hits and hits[-1].start() > best_at:
                best_at, who = hits[-1].start(), tag
        short = desc.split(",")[0][:62]
        out.append((slot, short + (f"  [{who}]" if who else "")))
    return out


def terse(frag: str, width: int = 62) -> str:
    f = re.sub(r"\s+", " ", frag).strip(" .,;—-")
    f = re.sub(r"^(?:the|a|an|her|his|their)\s+", "", f, flags=re.I)
    return (f[: width - 1] + "…") if len(f) > width else f


def scan_card_lines(body: str, cast: list[str], touched: list[str] | None = None) -> list[str]:
    """The checklist body for ONE clip: positions, numbered claims and states,
    diegetic/crowd checks, and the frame-0-forward objects this clip's action
    will touch."""
    clean = re.sub(r'"[^"]*"', " ", body)
    lines: list[str] = []
    for slot, who in positions(body, cast):
        lines.append(f"     {slot:<6}= {who}")

    claims: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, pat in CLAIM_PATTERNS:
        for m in re.finditer(pat, clean, re.I):
            frag = re.sub(r"\s+", " ", m.group(0)).strip().rstrip(",;")
            if len(frag) > 3 and frag.lower() not in seen:
                seen.add(frag.lower())
                claims.append((label, frag))

    states: list[tuple[str, str]] = []
    for label, pat in STATE_PATTERNS:
        for m in re.finditer(pat, clean, re.I):
            frag = re.sub(r"\s+", " ", m.group(0)).strip()
            if frag.lower() not in seen:
                seen.add(frag.lower())
                states.append((label, frag))

    k = 0
    for label, frag in claims:
        if re.fullmatch(r"(?:on the\s+)?(?:left|right|cent(?:er|re))(?:\s+frame)?", frag, re.I):
            continue
        if len(frag.split()) < 3:
            continue
        k += 1
        lines.append(f"     n{k} {label:<11}: {terse(frag)}")

    bare = sorted({f.lower() for _l, f in states if len(f.split()) < 3})
    for label, frag in [(l, f) for l, f in states if len(f.split()) >= 3]:
        k += 1
        lines.append(f"     n{k} {label:<11}: {terse(frag)}")
    if bare:
        k += 1
        lines.append(f"     n{k} {'states':<11}: {', '.join(bare)}")

    if re.search(DEPICTION_PATTERN, clean, re.I):
        depicted = sorted({re.sub(r"\s+", " ", m.group(0)).strip().lower()
                           for m in re.finditer(DEPICTION_PATTERN, clean, re.I)})
        k += 1
        lines.append(f"     n{k} {'diegetic':<11}: {', '.join(depicted)} "
                     f"→ must match this world's species, never human")

    if len(cast) > 2 or re.search(CROWD_HINT, clean, re.I):
        k += 1
        lines.append(f"     n{k} {'crowd':<11}: figures visually DISTINCT? no cloned faces/outfits")

    # The frame-0-forward check. The upstream this was ported from could not
    # produce this line: its image stage ran before any video prompt existed, so
    # nothing knew what the clip would reach for. Here 04f runs first, so every
    # object the action touches is known and MUST be visible in this still.
    if touched:
        k += 1
        lines.append(f"     n{k} {'frame-0 fwd':<11}: these must be VISIBLE and at rest — "
                     f"{', '.join(touched)}")
        k += 1
        lines.append(f"     n{k} {'performable':<11}: is the clip's first action performable "
                     f"from this frozen instant?")

    return lines
