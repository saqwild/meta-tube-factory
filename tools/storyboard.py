#!/usr/bin/env python3
"""Build a single self-contained storyboard page for one episode.

Deliberately simple: one HTML file, a responsive card grid, one card per clip
with its frame-0 still embedded as a data URI, its pose note, its camera move,
its beats and its dialogue. No dependencies, no external assets, no server —
open it and scroll an episode in one pass before any render spend.

A clip with no still yet renders as a labelled placeholder rather than being
omitted, so the gaps are the point of the page rather than invisible.

RUN
---
    python tools/storyboard.py --channel <slug> --episode EPxxx

Output: episodes/<slug>/<EPID>/exports/storyboard.html
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_paths import CHANNEL_PROFILES_DIR, EPISODES_DIR  # noqa: E402
from ltx_prompt_validator import spoken_words  # noqa: E402

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
HEADER = re.compile(r"^##\s*(SC\d{2,3})\s*(?:\|\s*pose:\s*(.*))?$", re.IGNORECASE)
QUOTED = re.compile(r"[\"“]([^\"“”]{1,600}?)[\"”]")
TAG_ONLY_LINE = re.compile(r"^\s*(?:\[\[[A-Za-z0-9_]+\]\]\s*)+$")

# story/script.md — "## CLIP 3 — 0:40–1:00 · …" and "**MAMA ROSA:** "…""
SCRIPT_CLIP = re.compile(r"^#{2,}\s*CLIP\s+(\d{1,3})\b", re.IGNORECASE)
SCRIPT_LINE = re.compile(r"^\*\*([A-Z][A-Z .'-]*?):\*\*\s*[\"“]([^\"“”]+)[\"”]")

CSS = """
:root{color-scheme:dark light}
*{box-sizing:border-box}
body{margin:0;background:#0c0d10;color:#d7d9de;
     font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
header{position:sticky;top:0;z-index:9;background:#111319ee;backdrop-filter:blur(6px);
       border-bottom:1px solid #23262e;padding:12px 18px}
header h1{margin:0;font-size:16px;color:#fff}
header .sub{color:#8a8f99;font-size:12px;margin-top:3px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;padding:18px}
.card{background:#14161c;border:1px solid #23262e;border-radius:10px;overflow:hidden;
      display:flex;flex-direction:column}
.imgwrap{position:relative;aspect-ratio:16/9;background:#000}
.imgwrap img{width:100%;height:100%;object-fit:cover;display:block}
.ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;
    text-align:center;padding:14px;color:#6b7080;font-size:12px;font-style:italic}
.kind{position:absolute;top:6px;right:6px;font-size:10px;padding:2px 7px;border-radius:4px;
      text-transform:uppercase;letter-spacing:.04em}
.kind.still{background:#1f6f43;color:#fff}
.kind.placeholder{background:#2a2d36;color:#8a8f99}
.meta{padding:11px 13px;display:flex;flex-direction:column;gap:7px}
.hd{display:flex;align-items:center;gap:9px}
.num{font-weight:700;color:#fff;font-size:13px}
.cam{color:#8a8f99;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
.flag{margin-left:auto;background:#5a2230;color:#ffd0d8;font-size:10px;padding:2px 8px;
      border-radius:10px}
.words{background:#1e2a3d;color:#9fc4ff;font-size:10px;padding:2px 8px;border-radius:10px;
       letter-spacing:.03em;white-space:nowrap}
.words.out{background:#5a2230;color:#ffd0d8}
.words.none{background:#2a2d36;color:#7f858f}
.src{color:#6b7080;font-size:10px;font-style:italic;padding-left:9px}
.pose{color:#aab0ba;font-size:12px}
.beats{margin:0;padding-left:16px;color:#9aa0aa;font-size:12px}
.dlg{border-left:2px solid #3a4663;padding-left:9px;color:#cfe0ff;font-size:12.5px}
.dlg p{margin:3px 0}
.props{color:#7f858f;font-size:11px}
@media (prefers-color-scheme:light){
  body{background:#f6f7f9;color:#23262e}
  header{background:#ffffffee;border-bottom-color:#e2e5ea}
  header h1{color:#111}
  .card{background:#fff;border-color:#e2e5ea}
  .num{color:#111}.cam{color:#767c86}
  .pose{color:#4a5058}.beats{color:#5a616b}.props{color:#767c86}
  .dlg{color:#26364f;border-left-color:#9fb4d8}
  .words{background:#e4edfb;color:#2a4f88}
  .words.out{background:#fbe3e8;color:#8c2740}
  .words.none{background:#eceef2;color:#767c86}
  .src{color:#8a9099}
}
"""


def parse_still_prompts(path: Path) -> dict[str, str]:
    """{clip_id: pose note} from the `## SC07 | pose: …` headers."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADER.match(line.strip())
        if m:
            out[m.group(1).upper()] = (m.group(2) or "").strip()
    return out


def parse_script_dialogue(path: Path) -> dict[str, list[tuple[str, str]]]:
    """{clip_id: [(speaker, line), …]} from story/script.md.

    The fallback for the FIRST storyboard run, before 04f has written any clip
    prompt. Without it the early page shows camera and beats but no words,
    which is the half of an episode a reader most wants to scan.
    """
    out: dict[str, list[tuple[str, str]]] = {}
    if not path.exists():
        return out
    clip: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = SCRIPT_CLIP.match(line.strip())
        if header:
            clip = f"SC{int(header.group(1)):02d}"
            out.setdefault(clip, [])
            continue
        spoken = SCRIPT_LINE.match(line.strip())
        if spoken and clip:
            out[clip].append((spoken.group(1).strip(), spoken.group(2).strip()))
    if out:
        return {k: v for k, v in out.items() if v}
    # Fall back to the signed-anyway scene/beat format.
    return _parse_scene_beat_dialogue(path)


# signed-anyway: scene headers "## S6 — …  · 4 clips" plus beat lines like
# "**S6.2 — RUTH [35]:** *(stage dir)* "line"" (quote may wrap across source lines),
# and one bare "**EVELYN [34]:** "line"" that follows a non-speaker beat header (S7.1).
_SA_SCENE_HDR = re.compile(r"^#{2,}\s*S(\d+)\b.*?[·|]\s*(\d+)\s*clip", re.IGNORECASE | re.MULTILINE)
_SA_SPOKEN_BEAT = re.compile(
    r"\*\*\s*S(\d+)\.(\d+)\s*—\s*([A-Z][A-Z .'\-]{1,30}?)\s*\[\d+\][^*]*\*\*"
    r"\s*(?:\*\([^)]*\)\*\s*)?[\"“]([^\"“”]+?)[\"”]",
    re.DOTALL,
)
_SA_ANY_BEAT = re.compile(r"\*\*\s*S(\d+)\.(\d+)\s*—", re.MULTILINE)
_SA_BARE = re.compile(
    r"\*\*\s*([A-Z][A-Z .'\-]{1,30}?)\s*\[\d+\][^*]*\*\*\s*[\"“]([^\"“”]+?)[\"”]",
    re.DOTALL,
)


def _sa_offsets(text: str) -> dict[int, int]:
    counts = {int(m.group(1)): int(m.group(2)) for m in _SA_SCENE_HDR.finditer(text)}
    offset, running = {}, 0
    for s in sorted(counts):
        offset[s] = running
        running += counts[s]
    return offset


def _parse_scene_beat_dialogue(path: Path) -> dict[str, list[tuple[str, str]]]:
    text = path.read_text(encoding="utf-8")
    offset = _sa_offsets(text)
    if not offset:
        return {}
    out: dict[str, list[tuple[str, str]]] = {}

    def clip_id(scene: int, beat: int) -> str | None:
        return f"SC{offset[scene] + beat:02d}" if scene in offset else None

    for m in _SA_SPOKEN_BEAT.finditer(text):
        cid = clip_id(int(m.group(1)), int(m.group(2)))
        if cid:
            out.setdefault(cid, []).append(
                (m.group(3).strip(), re.sub(r"\s+", " ", m.group(4)).strip()))

    # S7.1-style: a bare "**NAME [n]:** "…"" sitting under a non-speaker beat header
    for bm in _SA_ANY_BEAT.finditer(text):
        cid = clip_id(int(bm.group(1)), int(bm.group(2)))
        if not cid or cid in out:
            continue
        nxt = _SA_ANY_BEAT.search(text, bm.end())
        segment = text[bm.end(): nxt.start() if nxt else len(text)]
        sm = _SA_BARE.search(segment)
        if sm:
            out.setdefault(cid, []).append(
                (sm.group(1).strip(), re.sub(r"\s+", " ", sm.group(2)).strip()))

    return {k: v for k, v in out.items() if v}


def pose_from_blocking(block: object) -> str:
    """A compact first-pass pose note when 04f2 prompts do not exist yet.

    Frame-zero states are the geometry authority at 04d.  The first storyboard
    is deliberately built before 04f2, so it needs to expose that authority
    rather than showing an empty pose field until a later generation stage.
    """
    if not isinstance(block, dict):
        return ""
    # blocking.json (04d) keys character geometry under `chars`; an embedded
    # frame0-requirements block (04f) uses `frame0_state`. Accept either.
    states = block.get("chars")
    if not isinstance(states, dict) or not states:
        states = block.get("frame0_state")
    if not isinstance(states, dict):
        return ""
    notes: list[str] = []
    for name, state in states.items():
        if not isinstance(state, dict):
            continue
        if state.get("visible") is False:
            continue
        pos = str(state.get("pos", "")).strip()
        pose = str(state.get("pose", "")).strip()
        facing = str(state.get("facing", "")).strip()
        if not (pos or pose or facing):
            continue
        label = str(name).replace("_", " ").title()
        detail = ", ".join(part for part in (pos, pose, facing) if part)
        notes.append(f"{label}: {detail}")
    return "; ".join(notes)


def word_band(channel: str) -> tuple[int, int] | None:
    """`render.spoken_word_band` for the channel, if it declares one."""
    cfg = CHANNEL_PROFILES_DIR / channel / "channel.json"
    if not cfg.exists():
        return None
    try:
        band = json.loads(cfg.read_text(encoding="utf-8")).get("render", {}).get("spoken_word_band")
    except (json.JSONDecodeError, OSError):
        return None
    if isinstance(band, list) and len(band) == 2 and all(isinstance(n, int) for n in band):
        return band[0], band[1]
    return None


def parse_video_prompts(path: Path) -> dict[str, str]:
    """{clip_id: prompt text} from `prompts/7-video-prompts.md`.

    The clip prompts live in one combined file, `## SC07` per block, matching the
    house convention. The `[[TAG]]` line is packet metadata and is dropped.
    """
    out: dict[str, str] = {}
    if not path.exists():
        return out
    clip: str | None = None
    buf: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        header = HEADER.match(line.strip())
        if header:
            if clip:
                out[clip] = "\n".join(buf).strip()
            clip, buf = header.group(1).upper(), []
            continue
        if clip is not None and not TAG_ONLY_LINE.match(line):
            buf.append(line)
    if clip:
        out[clip] = "\n".join(buf).strip()
    return {k: v for k, v in out.items() if v}


def find_still(stills_dir: Path, clip: str) -> Path | None:
    if not stills_dir.exists():
        return None
    for ext in IMAGE_EXTS:
        p = stills_dir / f"{clip}{ext}"
        if p.exists():
            return p
    return None


def data_uri(p: Path) -> str:
    return f"data:{MIME.get(p.suffix.lower(), 'image/png')};base64," + \
        base64.b64encode(p.read_bytes()).decode("ascii")


def build(channel: str, episode: str) -> int:
    ep = EPISODES_DIR / channel / episode
    if not ep.exists():
        print(f"no such episode: {ep}")
        return 1

    poses = parse_still_prompts(ep / "prompts" / "6-image-prompts.md")
    stills_dir = ep / "renders" / "stills"

    prompts = parse_video_prompts(ep / "prompts" / "7-video-prompts.md")

    blocking = {}
    bpath = ep / "_context" / "blocking.json"
    if bpath.exists():
        raw_blocking = json.loads(bpath.read_text(encoding="utf-8")).get("clips", {})
        if isinstance(raw_blocking, dict):
            # Prompt headers and still filenames are canonical SCNN.  Older
            # hand-authored ledgers sometimes use lowercase keys; normalize on
            # read so the derived review page remains useful during migration.
            blocking = {str(key).upper(): value for key, value in raw_blocking.items()}

    script_dialogue = parse_script_dialogue(ep / "story" / "script.md")
    band = word_band(channel)

    clips = sorted(set(poses) | set(prompts) | set(script_dialogue) | {k.upper() for k in blocking})
    if not clips:
        print(f"nothing to draw: no still prompts, clip prompts or blocking under {ep}")
        return 1

    cards, missing, total_words, out_of_band = [], 0, 0, 0
    for clip in clips:
        still = find_still(stills_dir, clip)
        if still:
            img = f'<img src="{data_uri(still)}" alt="{clip}">'
            kind = '<span class="kind still">still</span>'
        else:
            missing += 1
            img = '<div class="ph">no approved still yet</div>'
            kind = '<span class="kind placeholder">pending</span>'

        blk = blocking.get(clip, {})
        camera = blk.get("camera", {}) or {}
        cam = " · ".join(x for x in (camera.get("shot"), camera.get("movement")) if x)
        beats = blk.get("anchors", []) or []
        props = [p.get("name", "") for p in (blk.get("props") or []) if p.get("name")]
        if not props and isinstance(blk.get("props_at_rest"), dict):
            props = [str(name) for name in blk["props_at_rest"]]
        pose = poses.get(clip) or pose_from_blocking(blk)

        # The clip prompt is authoritative once 04f has written it; the script is
        # the fallback so the first run is not wordless.
        prompt_lines = QUOTED.findall(prompts.get(clip, ""))
        if prompt_lines:
            said = [("", x) for x in prompt_lines]
            source = ""
        else:
            said = script_dialogue.get(clip, [])
            source = ' <span class="src">from script</span>' if said else ""

        dialogue = ("<div class=\"dlg\">" + "".join(
            (f"<p><b>{html.escape(who)}</b> “{html.escape(what)}”</p>" if who
             else f"<p>“{html.escape(what)}”</p>")
            for who, what in said) + "</div>") if said else ""

        words = spoken_words(" ".join(f'"{what}"' for _, what in said)) if said else 0
        total_words += words
        if words:
            over = bool(band) and not (band[0] <= words <= band[1])
            out_of_band += 1 if over else 0
            badge = (f'<span class="words{" out" if over else ""}" '
                     f'title="{"outside" if over else "inside"} the '
                     f'{f"[{band[0]}, {band[1]}] " if band else ""}spoken-word band">'
                     f'{words} words</span>')
        else:
            badge = '<span class="words none">no dialogue</span>'

        cards.append(f"""<div class="card" id="{clip}">
<div class="imgwrap">{img}{kind}</div>
<div class="meta">
  <div class="hd"><span class="num">{clip.upper()}</span>{badge}
    {'<span class="flag">no still</span>' if not still else ''}</div>
  <div class="cam">{html.escape(cam)}</div>
  {f'<div class="pose">{html.escape(pose)}</div>' if pose else ''}
  {('<ul class="beats">' + ''.join(f'<li>{html.escape(str(b))}</li>' for b in beats) + '</ul>') if beats else ''}
  {dialogue}{source}
  {f'<div class="props">props: {html.escape(", ".join(props))}</div>' if props else ''}
</div></div>""")

    sub = (f"{len(clips)} clips · {len(clips) - missing} stills approved"
           + (f" · <strong>{missing} pending</strong>" if missing else " · complete")
           + (f" · {total_words} spoken words" if total_words else "")
           + (f" · <strong>{out_of_band} outside the [{band[0]}, {band[1]}] band</strong>"
              if band and out_of_band else
              (f" · all inside the [{band[0]}, {band[1]}] band" if band and total_words else "")))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard — {html.escape(episode)}</title>
<style>{CSS}</style></head><body>
<header><h1>Storyboard — {html.escape(channel)} / {html.escape(episode)}</h1>
<div class="sub">{sub}</div></header>
<div class="grid">
{"".join(cards)}
</div></body></html>"""

    out = ep / "exports" / "storyboard.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out}  ({len(clips)} clips, {missing} without a still)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="storyboard.py")
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    a = ap.parse_args(argv)
    return build(a.channel, a.episode)


if __name__ == "__main__":
    raise SystemExit(main())
