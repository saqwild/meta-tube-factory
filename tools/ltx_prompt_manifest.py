#!/usr/bin/env python3
"""Build `_context/ltx-prompt-manifest.json` for an episode (stage 04f3).

WHY THIS EXISTS
---------------
The manifest binds every final clip prompt to the exact still it was re-anchored
against, by hash, and 04g builds the render package from it. Until 2026-10-29 it
was written by hand, and nothing re-derived its per-clip hashes. This tool derives
every field from the files on disk, and REFUSES to write when those files are not
in a final, validated state:

  * `_context/ltx-prompt-review.json` must be a strict PASS, produced by the
    current validator, against the current `prompts/7-video-prompts.md`;
  * the prompts file must not still carry the 04f draft's PROVISIONAL marker
    (the 04f3 re-anchor pass is what removes it);
  * every clip must have a `## SCnn` block, a `blocking.json` entry with a camera
    movement, a `frame0-requirements.json` block whose first action is performable,
    and exactly one still in `renders/stills/`.

It never edits a prompt, a still or a context file.

RUN
---
    python tools/ltx_prompt_manifest.py --channel <slug> --episode EPxxx --still-gate-pass
    python tools/ltx_prompt_manifest.py ... --still-generator "muse-image-1.0 (muse-image)"

`--still-gate-pass` is the operator's attestation that `qa/still-gate.md` records a
PASS for every still as it is now on disk. The tool cannot read that verdict (it
is prose), so it will not invent one.

Exit 0 = written. Exit 1 = refused (reasons printed). Exit 2 = setup problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ltx_prompt_validator as validator  # noqa: E402
from project_paths import ROOT  # noqa: E402

PROMPTS_REL = "prompts/7-video-prompts.md"
MANIFEST_REL = "_context/ltx-prompt-manifest.json"
REVIEW_REL = "_context/ltx-prompt-review.json"
STILL_EXTS = (".png", ".jpg", ".jpeg", ".webp")
PROVISIONAL = re.compile(r"\bPROVISIONAL\b")
RENDER_KEYS = ("mode", "model", "generation_unit", "clip_duration_seconds", "fps",
               "aspect_ratio", "megapixels", "spoken_word_band", "style_echo")


class Refused(Exception):
    """The inputs are not in a state a manifest may be built from."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def clip_index(clip: str) -> int:
    return int(clip[2:])


def clip_blocks(prompts_path: Path) -> dict[str, str]:
    """{SCnn: block body} exactly as the validator and the render app read it."""
    return dict(validator._iter_clip_blocks(prompts_path.read_text(encoding="utf-8")))


def ordered(clips) -> list[str]:
    return sorted(clips, key=clip_index)


def find_still(ep: Path, clip: str) -> Path | None:
    hits = [ep / "renders" / "stills" / f"{clip}{ext}" for ext in STILL_EXTS]
    hits = [p for p in hits if p.is_file()]
    return hits[0] if len(hits) == 1 else None


def review_problems(ep: Path, root: Path = ROOT) -> list[str]:
    """Why the episode's prompt review cannot vouch for the current prompts file.
    Shared with build_render_package.py -- both refuse on the same conditions."""
    review_path = ep / REVIEW_REL
    prompts_path = ep / PROMPTS_REL
    if not review_path.exists():
        return [f"{REVIEW_REL} is missing -- run the validator with --strict --emit-review"]
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{REVIEW_REL} is not valid JSON ({exc})"]
    out = []
    if review.get("mode") != "strict":
        out.append(f"{REVIEW_REL} is mode {review.get('mode')!r}; 04f3 requires a strict run")
    if review.get("status") != "PASS":
        out.append(f"{REVIEW_REL} status is {review.get('status')!r}, not PASS")
    current = sha256_file(prompts_path) if prompts_path.exists() else None
    recorded = review.get("source_prompts_sha256")
    if not recorded:
        out.append(f"{REVIEW_REL} predates source_prompts_sha256 (2026-10-29) and cannot prove "
                   f"which prompts it read -- re-run the validator with --strict --emit-review")
    elif current and recorded != current:
        out.append(f"{REVIEW_REL} was produced against a different {PROMPTS_REL} "
                   f"-- re-run the validator with --strict --emit-review")
    validator_now = sha256_file(root / "tools" / "ltx_prompt_validator.py")
    if review.get("validator_sha256") != validator_now:
        out.append(f"{REVIEW_REL} was produced by an older ltx_prompt_validator.py "
                   f"-- re-run it so the verdict reflects the current rules")
    return out


def build_manifest(channel_slug: str, episode_id: str, *, still_gate_pass: bool,
                   still_generator: str | None = None, root: Path = ROOT) -> dict:
    ep = root / "episodes" / channel_slug / episode_id
    channel_path = root / "channel_profiles" / channel_slug / "channel.json"
    prompts_path = ep / PROMPTS_REL
    for p in (channel_path, prompts_path):
        if not p.exists():
            raise FileNotFoundError(p)
    channel = json.loads(channel_path.read_text(encoding="utf-8"))
    render = channel.get("render") or {}

    problems = review_problems(ep, root)
    prompts_text = prompts_path.read_text(encoding="utf-8")
    if PROVISIONAL.search(prompts_text):
        problems.append(f"{PROMPTS_REL} still says PROVISIONAL -- the 04f3 re-anchor pass "
                        f"has not replaced the draft GLOBAL:: lines (or its header was not updated)")
    if not still_gate_pass:
        problems.append("--still-gate-pass not given: confirm qa/still-gate.md records a PASS "
                        "for every still exactly as it is now on disk")
    if not (ep / "qa" / "still-gate.md").exists():
        problems.append("qa/still-gate.md is missing")

    blocks = clip_blocks(prompts_path)
    if not blocks:
        problems.append(f"no '## SCnn' blocks in {PROMPTS_REL}")

    def load(rel: str) -> dict:
        p = ep / rel
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    blocking = {str(k).upper(): v for k, v in (load("_context/blocking.json").get("clips") or {}).items()}
    frame0 = {str(b.get("clip", "")).upper(): b
              for b in (load("_context/frame0-requirements.json").get("clips") or [])}

    clips = []
    for clip in ordered(blocks):
        body = blocks[clip]
        b = blocking.get(clip)
        f = frame0.get(clip)
        still = find_still(ep, clip)
        if b is None:
            problems.append(f"{clip}: no blocking.json entry")
        elif not ((b.get("camera") or {}).get("movement") or "").strip():
            problems.append(f"{clip}: blocking.json has no camera.movement")
        if f is None:
            problems.append(f"{clip}: no frame0-requirements block")
        elif f.get("first_action_performable") is not True:
            problems.append(f"{clip}: frame0 first_action_performable is not true")
        if still is None:
            problems.append(f"{clip}: expected exactly one still at renders/stills/{clip}.<png|jpg|jpeg|webp>")
        if b is None or f is None or still is None:
            continue
        characters = f.get("characters")
        if not characters:
            characters = [k for k, s in (b.get("chars") or {}).items()
                          if not isinstance(s, dict) or s.get("visible", True)]
        entry = {
            "clip": clip,
            "index": clip_index(clip),
            "prompt_path": PROMPTS_REL,
            "prompt_sha256": sha256_bytes(body.encode("utf-8")),
            "still_path": still.relative_to(ep).as_posix(),
            "still_sha256": sha256_file(still),
            "still_gate_verdict": "PASS",
            "characters": list(characters),
            "spoken_word_count": validator.spoken_words(body),
            "declared_cuts": int(b.get("declared_cuts", 0) or 0),
            "camera_movement": b["camera"]["movement"].strip(),
            "frame0_requirements": {
                "touched_objects": list(f.get("touched_objects") or []),
                "first_action_performable": True,
                "continues_from": f.get("continues_from"),
            },
        }
        if still_generator:
            entry["still_generator"] = still_generator
        clips.append(entry)

    extra = sorted(set(blocking) - set(blocks), key=clip_index)
    if extra:
        problems.append(f"blocking.json has clips with no prompt block: {', '.join(extra)}")
    if problems:
        raise Refused("\n".join(problems))

    return {
        "schema_version": 1,
        "episode_id": episode_id,
        "channel_slug": channel_slug,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "render": {k: render[k] for k in RENDER_KEYS if k in render},
        "clips": clips,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    ap.add_argument("--still-gate-pass", action="store_true",
                    help="attest that qa/still-gate.md records PASS for every still on disk")
    ap.add_argument("--still-generator", default=None,
                    help="image model that produced the stills (default: channel.json models.image)")
    a = ap.parse_args(argv)
    channel_path = ROOT / "channel_profiles" / a.channel / "channel.json"
    if not channel_path.exists():
        print(f"no channel profile: {channel_path}")
        return 2
    generator = a.still_generator or (json.loads(channel_path.read_text(encoding="utf-8"))
                                      .get("models", {}).get("image"))
    try:
        manifest = build_manifest(a.channel, a.episode, still_gate_pass=a.still_gate_pass,
                                  still_generator=generator)
    except FileNotFoundError as exc:
        print(f"not found: {exc}")
        return 2
    except Refused as exc:
        print("REFUSED -- ltx-prompt-manifest.json not written:")
        for line in str(exc).splitlines():
            print(f"  - {line}")
        return 1
    out = ROOT / "episodes" / a.channel / a.episode / MANIFEST_REL
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(manifest['clips'])} clips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
