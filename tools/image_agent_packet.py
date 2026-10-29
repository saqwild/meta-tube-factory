#!/usr/bin/env python3
"""Build the frame-0 GENERATION PACKET handed to the image-generation agent.

WHY THIS EXISTS
---------------
A still gate that runs AFTER a still exists is useful, but it means the first
time anyone sees "here is exactly what this image must show" is after a render
has already been spent. This builds the same checklist — reusing the extraction
in `still_claims.py`, so the two can never silently diverge — and pairs it with
each clip's VERBATIM still prompt, at 04f2 time, before any image exists.

Handed as ONE file to whoever generates the stills: generate, self-check the
RESULT against the embedded conditions, correct (inpaint one detail, or re-roll)
and re-check, finalise. Then the next clip. The post-render still gate remains a
separate, later check — this front-loads the same discipline.

Unlike the upstream this was ported from, the packet also carries each clip's
`touched_objects` and the performable-first-action question, because in this
pipeline the clip prompt (04f) is authored BEFORE the still.

RUN
---
    python tools/image_agent_packet.py --channel <slug> --episode EPxxx

Output: episodes/<slug>/<EPID>/prompts/6-image-agent-packet.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_paths import CHANNEL_PROFILES_DIR, EPISODES_DIR  # noqa: E402
from still_claims import scan_card_lines  # noqa: E402

HEADER = re.compile(r"^##\s*(SC\d{2,3})\s*(\|.*)?$", re.IGNORECASE)
TAG_LINE = re.compile(r"^\s*(?:\[\[[A-Za-z0-9_]+\]\]\s*)+$")
TAG = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")


def parse_blocks(md: str) -> dict[str, dict[str, str]]:
    """{clip_id: {header, tags, body}} from the `## SC07 | pose: …` convention."""
    blocks: dict[str, dict[str, str]] = {}
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if current is None:
            return
        lines = [ln for ln in buf]
        tags = ""
        while lines and not lines[0].strip():
            lines.pop(0)
        if lines and TAG_LINE.match(lines[0]):
            tags = lines.pop(0).strip()
        blocks[current]["tags"] = tags
        blocks[current]["body"] = "\n".join(lines).strip()

    for line in md.splitlines():
        m = HEADER.match(line.strip())
        if m:
            flush()
            current = m.group(1).upper()
            blocks[current] = {"header": line.strip(), "tags": "", "body": ""}
            buf = []
        elif current is not None:
            buf.append(line)
    flush()
    return blocks


def build(channel: str, episode: str) -> int:
    ep = EPISODES_DIR / channel / episode
    src = ep / "prompts" / "6-image-prompts.md"
    if not src.exists():
        print(f"not found: {src}\nRun 04f2's still-prompt authoring first.")
        return 1

    blocks = parse_blocks(src.read_text(encoding="utf-8"))
    if not blocks:
        print(f"no '## SC<NN>' blocks found in {src}")
        return 1

    touched_by_clip: dict[str, list[str]] = {}
    req = ep / "_context" / "frame0-requirements.json"
    if req.exists():
        data = json.loads(req.read_text(encoding="utf-8"))
        for clip in data.get("clips", []):
            touched_by_clip[str(clip.get("clip", "")).upper()] = [
                str(o) for o in clip.get("touched_objects", [])
            ]
    else:
        print(f"WARNING: {req} missing — the packet will omit the frame-0-forward "
              f"checks, which are the whole point of running 04f before 04f2.")

    # Only used to tell a character tag from an environment/prop tag; the packet
    # itself carries tags, never local paths, which the image agent cannot follow.
    refmap: dict[str, dict] = {}
    rmp = ep / "_context" / "reference-map.json"
    if rmp.exists():
        rm = json.loads(rmp.read_text(encoding="utf-8"))
        refmap = rm.get("references", {})
    else:
        print(f"NOTE: {rmp} missing — every tag will be treated as a character.")

    style = ""
    profile = CHANNEL_PROFILES_DIR / channel / "channel.json"
    if profile.exists():
        style = json.loads(profile.read_text(encoding="utf-8")).get("render", {}).get("style_echo", "")

    out_lines = [
        f"# Frame-0 Agent Packet — {channel} / {episode}",
        "",
        "For whoever generates the stills. Per clip: the exact prompt to submit, then that",
        "clip's own validation rules — the staging claims the prompt already makes, turned",
        "into checks.",
        "",
        "Workflow: (1) generate a candidate from the prompt as written, (2) check the RESULT",
        "first for the hard blockers below, then use the validation-rules lines as a useful",
        "continuity checklist, (3) correct or re-roll only a hard blocker, and (4) finalise",
        "the first clear, story-usable candidate. Retain other candidates; the post-render",
        "still gate remains a separate check.",
        "",
        "## Rules for this packet",
        "",
        "### Acceptance threshold",
        "",
        "- **Hard blockers:** a required character, setting landmark, or prop touched in the",
        "  following clip is missing, materially wrong, duplicated, or impossible to act from;",
        "  the image starts in the middle of an action; or an unwanted performer, unsafe beat,",
        "  or obvious continuity contradiction changes the story.",
        "- **Tolerate without a re-roll:** a slightly open-looking or partly occluded mouth when",
        "  nobody is visibly speaking; empty paws partly hidden in a pocket or behind the body",
        "  when no prop is held; small eyeline or expression variation; or a tiny surface mark",
        "  that is not readable at the shot's framing. Record it only when useful.",
        "- Do not spend another generation merely to perfect one of those tolerated details.",
        "",
        "- Every character reference is declared by the `[[TAG]]` line directly below its clip",
        "  header. Those tagged reference assets already exist — use the listed tags as the",
        "  reference bindings and do not invent a replacement identity.",
        "- `## SC<NN> | pose: …` is packet metadata, **not** text to submit to the image model.",
        "  The prompt begins after it: the `[[TAG]]` line, then the prose.",
        "- The two `frame-0 fwd` / `performable` lines are the ones that protect the render.",
        "  Every listed object must be VISIBLE and at its resting state, because the clip's",
        "  action touches it and image-to-video never invents objects. If the first action is",
        "  not performable from the frozen instant, **re-roll the still — do not reword the",
        "  clip.**",
        "- Save the approved keep as `SC<NN>.png` in `renders/stills/` — exactly that name. The",
        "  render app binds a still to its clip by the scene number PREFIXING the filename stem;",
        "  any other name is skipped and a second file for the same number is ambiguous.",
        "",
    ]
    if style:
        out_lines += [f"[STYLE] = {style}", ""]
    out_lines += ["---", ""]

    total_checks = 0
    for clip in sorted(blocks):
        blk = blocks[clip]
        # The tag line carries EVERY reference the clip uses, so the packet is
        # self-contained for whoever generates. Only the character tags are the
        # cast, though — an environment or prop tag has no LEFT/RIGHT slot, and
        # treating one as a character fills the scan card with nonsense.
        tags_on_line = TAG.findall(blk["tags"])
        cast = [t for t in tags_on_line
                if refmap.get(t, {}).get("kind", "character") == "character"] if refmap \
            else tags_on_line
        out_lines.append(blk["header"])
        if blk["tags"]:
            out_lines.append(blk["tags"])
        out_lines.append(blk["body"])
        out_lines.append("")
        out_lines.append(f"{clip} validation rules:")
        if blk["tags"]:
            out_lines.append(blk["tags"])
        card = scan_card_lines(blk["body"], cast, touched_by_clip.get(clip))
        out_lines.extend(card)
        total_checks += sum(1 for ln in card if re.match(r"\s*n\d+ ", ln))
        out_lines += ["", "---", ""]

    out = ep / "prompts" / "6-image-agent-packet.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {out}")
    print(f"      ({len(blocks)} clips, {total_checks} validation-rule lines)")
    missing = [c for c in blocks if c not in touched_by_clip]
    if touched_by_clip and missing:
        print(f"      WARNING: no frame-0 requirement block for: {', '.join(sorted(missing))}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="image_agent_packet.py")
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    a = ap.parse_args(argv)
    return build(a.channel, a.episode)


if __name__ == "__main__":
    raise SystemExit(main())
