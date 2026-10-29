#!/usr/bin/env python3
"""Build the 04g render package that app-vidgen-dist's Batch tab ingests.

WHY THIS EXISTS
---------------
04g is the last checkpoint before GPU spend, and until 2026-10-29 its package was
assembled by hand -- prompt bodies, `@@ s{n}` markers, still copies, hashes, the
negative prompt. Three hand-built packages in this repo used three different byte
conventions, and the 04g contract itself warns that "a mispaired batch renders
successfully and looks plausible". Every step here is mechanical, so it is a tool:

  1. REFUSE unless the inputs are final: a strict PASS review from the current
     validator against the current prompts file, no PROVISIONAL marker, and an
     ltx-prompt-manifest.json whose per-clip prompt and still hashes still match
     the files on disk.
  2. WRITE `exports/ltx-render-package/`: master-prompt.txt, stills/,
     negative-prompt.txt, render-settings.json, render-manifest.json.
  3. VERIFY by re-reading the package the way the render app does (its own
     section parser and its own still-filename rule, mirrored below) and
     checking every clip pairs with exactly its own still and its own prompt.

The byte layout reproduces signed-anyway EP002's shipped package exactly
(master-prompt.txt and negative-prompt.txt CRLF; `@@ s{n}` blocks separated by a
blank line; prompt_sha256 = SHA-256 of the UTF-8 block body).

RUN
---
    python tools/build_render_package.py --channel <slug> --episode EPxxx \\
        --pilot SC01,SC08,SC11,SC13,SC18 --cast "Evelyn,Adrian,Elena"
    ... --force        rebuild over an existing package

`--pilot` is a human selection (04g "Pilot subset"): at least five clips including
the opening clip. `--cast` lists the episode's cast snapshot first names; each
becomes one `second <Name>` negative term.

Exit 0 = built and verified. Exit 1 = refused or verification failed. Exit 2 = setup.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ltx_prompt_manifest as lpm  # noqa: E402
from project_paths import ROOT  # noqa: E402

PACKAGE_REL = "exports/ltx-render-package"
SETTINGS_KEYS = ("workflow", "megapixels", "fps", "duration_seconds", "cfg",
                 "cfg_refine", "cfg_audio", "img_compression")
MIN_PILOTS = 5

# Mirrored from C:\pycode\app-vidgen-dist\app\batch.py (read 2026-10-29):
# parse_scene_sections() and _scene_number(). Kept as a copy -- this repo takes
# no code dependency on the render app. Re-read that file if the app changes.
_APP_SECTION = re.compile(r"^@@\s*([is])(\d+)\s*$", re.MULTILINE | re.IGNORECASE)
_APP_TAG_LINE = re.compile(r"(?:\[\[[A-Za-z0-9_\-]+\]\]\s*)+")
_APP_SCENE_NUMBER = re.compile(r"^(?:(?:image|scene|img|sc|s|i)[-_ ]*)?(\d+)(?=$|[_. -])", re.IGNORECASE)


class Refused(Exception):
    pass


def _app_clean_block(body: str) -> str:
    lines = body.strip().splitlines()
    start = 0
    for index, line in enumerate(lines):
        if line.strip():
            if _APP_TAG_LINE.fullmatch(line.strip()):
                start = index + 1
            break
    return "\n".join(lines[start:]).strip()


def app_scene_prompts(text: str) -> dict[int, str]:
    """{n: prompt} for every `@@ s{n}` section, as the render app parses it."""
    matches = list(_APP_SECTION.finditer(text))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        if m.group(1).lower() == "s":
            out[int(m.group(2))] = _app_clean_block(text[m.end():end])
    return out


def app_scene_number(filename: str) -> int | None:
    m = _APP_SCENE_NUMBER.match(Path(filename).stem)
    return int(m.group(1)) if m else None


def render_master(order: list[str], blocks: dict[str, str]) -> bytes:
    text = "\n\n".join(f"@@ s{lpm.clip_index(c)}\n{blocks[c]}" for c in order) + "\n"
    return text.replace("\n", "\r\n").encode("utf-8")


def render_negative(base_text: str, additions: list[str], cast: list[str]) -> bytes:
    terms = [base_text.strip()] + [a.strip() for a in additions if a.strip()]
    terms += [f"second {name}" for name in cast]
    return (", ".join(terms) + "\n").replace("\n", "\r\n").encode("utf-8")


def settings_from(render: dict) -> dict:
    src = dict(render)
    src["duration_seconds"] = render.get("clip_duration_seconds")
    missing = [k for k in SETTINGS_KEYS if src.get(k) is None]
    if missing:
        raise Refused(f"channel.json render is missing {', '.join(missing)}")
    return {k: src[k] for k in SETTINGS_KEYS}


def _parse_list(raw: str) -> list[str]:
    return [x.strip() for x in (raw or "").split(",") if x.strip()]


def build_package(channel_slug: str, episode_id: str, *, pilots: list[str], cast: list[str],
                  force: bool = False, root: Path = ROOT) -> dict:
    ep = root / "episodes" / channel_slug / episode_id
    channel = json.loads((root / "channel_profiles" / channel_slug / "channel.json")
                         .read_text(encoding="utf-8"))
    render = channel.get("render") or {}
    prompts_path = ep / lpm.PROMPTS_REL
    manifest_path = ep / lpm.MANIFEST_REL
    pkg = ep / PACKAGE_REL

    problems = lpm.review_problems(ep, root)
    if lpm.PROVISIONAL.search(prompts_path.read_text(encoding="utf-8")):
        problems.append(f"{lpm.PROMPTS_REL} still says PROVISIONAL -- 04f3 re-anchor not done")
    if not manifest_path.exists():
        raise Refused("\n".join(problems + [f"{lpm.MANIFEST_REL} is missing -- run "
                                            f"tools/ltx_prompt_manifest.py at 04f3"]))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    blocks = lpm.clip_blocks(prompts_path)
    entries = {c["clip"]: c for c in manifest.get("clips", [])}
    if set(entries) != set(blocks):
        problems.append(f"manifest clips {sorted(set(entries) ^ set(blocks))} do not match "
                        f"the ## SCnn blocks in {lpm.PROMPTS_REL}")
    for clip in lpm.ordered(set(entries) & set(blocks)):
        e = entries[clip]
        if lpm.sha256_bytes(blocks[clip].encode("utf-8")) != e.get("prompt_sha256"):
            problems.append(f"{clip}: prompt block changed since the manifest was built")
        still = ep / e.get("still_path", "")
        if not still.is_file():
            problems.append(f"{clip}: still {e.get('still_path')} is missing")
        elif lpm.sha256_file(still) != e.get("still_sha256"):
            problems.append(f"{clip}: still changed since the manifest was built")
        if e.get("still_gate_verdict") != "PASS":
            problems.append(f"{clip}: manifest still_gate_verdict is not PASS")
        if app_scene_number(Path(e.get("still_path", "")).name) != lpm.clip_index(clip):
            problems.append(f"{clip}: still filename would bind to scene "
                            f"{app_scene_number(Path(e.get('still_path', '')).name)} in the render app")

    order = lpm.ordered(entries)
    bad_pilots = [p for p in pilots if p not in entries]
    if bad_pilots:
        problems.append(f"--pilot names unknown clips: {', '.join(bad_pilots)}")
    if len(set(pilots)) < MIN_PILOTS:
        problems.append(f"--pilot needs at least {MIN_PILOTS} clips (04g Pilot subset); got {len(set(pilots))}")
    if order and order[0] not in pilots:
        problems.append(f"--pilot must include the opening clip {order[0]}")
    if not cast:
        problems.append("--cast is required: the episode's cast snapshot first names, "
                        "one 'second <Name>' negative term each")
    try:
        settings = settings_from(render)
    except Refused as exc:
        problems.append(str(exc))
    if pkg.exists() and any(pkg.iterdir()) and not force:
        problems.append(f"{PACKAGE_REL} already exists -- pass --force to rebuild it")
    if problems:
        raise Refused("\n".join(problems))

    base = (root / "pipeline" / "negative-prompt-base.txt").read_text(encoding="utf-8")
    master = render_master(order, blocks)
    negative = render_negative(base, list(render.get("negative_prompt_additions") or []), cast)

    stills_dir = pkg / "stills"
    stills_dir.mkdir(parents=True, exist_ok=True)
    wanted = {Path(entries[c]["still_path"]).name for c in order}
    for stale in stills_dir.iterdir():  # our own previous output only
        if stale.is_file() and stale.name not in wanted:
            stale.unlink()
    for clip in order:
        src = ep / entries[clip]["still_path"]
        shutil.copy2(src, stills_dir / src.name)
    (pkg / "master-prompt.txt").write_bytes(master)
    (pkg / "negative-prompt.txt").write_bytes(negative)
    (pkg / "render-settings.json").write_text(json.dumps({
        "_note": f"Built by tools/build_render_package.py from channel_profiles/{channel_slug}/"
                 f"channel.json -> render. app-vidgen-dist derives the frame count from "
                 f"duration_seconds; never hand-enter a frame count.",
        **settings}, indent=2) + "\n", encoding="utf-8")

    doc = {
        "schema_version": 1,
        "episode_id": episode_id,
        "channel_slug": channel_slug,
        "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_manifest_sha256": lpm.sha256_file(manifest_path),
        "master_prompt_sha256": lpm.sha256_bytes(master),
        "negative_prompt_sha256": lpm.sha256_bytes(negative),
        "settings": settings,
        "clips": [{
            "index": lpm.clip_index(c),
            "clip": c,
            "marker": f"@@ s{lpm.clip_index(c)}",
            "prompt_sha256": entries[c]["prompt_sha256"],
            "still_file": Path(entries[c]["still_path"]).name,
            "still_sha256": entries[c]["still_sha256"],
            "spoken_word_count": entries[c].get("spoken_word_count", 0),
            "declared_cuts": entries[c].get("declared_cuts", 0),
            "is_pilot": c in pilots,
        } for c in order],
    }
    (pkg / "render-manifest.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    errors = verify_package(pkg, doc, blocks)
    if errors:
        raise Refused("package written but FAILED verification:\n" + "\n".join(errors))
    return doc


def verify_package(pkg: Path, doc: dict, blocks: dict[str, str]) -> list[str]:
    """Re-read the package as the render app would and prove every pairing."""
    errors = []
    prompts = app_scene_prompts((pkg / "master-prompt.txt").read_text(encoding="utf-8"))
    by_scene: dict[int, list[str]] = {}
    for f in (pkg / "stills").iterdir():
        if f.is_file():
            by_scene.setdefault(app_scene_number(f.name), []).append(f.name)
    for c in doc["clips"]:
        n, clip = c["index"], c["clip"]
        if prompts.get(n) != blocks[clip]:
            errors.append(f"{clip}: @@ s{n} does not parse back to the clip's own prompt")
        files = by_scene.get(n, [])
        if files != [c["still_file"]]:
            errors.append(f"{clip}: render app would pair @@ s{n} with {files or 'no still'}")
        elif lpm.sha256_file(pkg / "stills" / c["still_file"]) != c["still_sha256"]:
            errors.append(f"{clip}: copied still does not match its recorded hash")
    extra = sorted(set(prompts) - {c["index"] for c in doc["clips"]})
    if extra:
        errors.append(f"master-prompt.txt has unexpected scenes: {extra}")
    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    ap.add_argument("--pilot", required=True, help="comma-separated clip ids, e.g. SC01,SC08,...")
    ap.add_argument("--cast", required=True, help="comma-separated cast first names")
    ap.add_argument("--force", action="store_true", help="rebuild over an existing package")
    a = ap.parse_args(argv)
    if not (ROOT / "channel_profiles" / a.channel / "channel.json").exists():
        print(f"no channel profile: {a.channel}")
        return 2
    if not (ROOT / "episodes" / a.channel / a.episode / lpm.PROMPTS_REL).exists():
        print(f"no {lpm.PROMPTS_REL} for {a.channel}/{a.episode}")
        return 2
    try:
        doc = build_package(a.channel, a.episode, pilots=[p.upper() for p in _parse_list(a.pilot)],
                            cast=_parse_list(a.cast), force=a.force)
    except Refused as exc:
        print("REFUSED -- render package not built:")
        for line in str(exc).splitlines():
            print(f"  - {line}")
        return 1
    print(f"built {PACKAGE_REL} for {a.channel}/{a.episode} -- {len(doc['clips'])} clips, verified")
    print("  clip   marker  still        pilot")
    for c in doc["clips"]:
        print(f"  {c['clip']:<6} {c['marker']:<7} {c['still_file']:<12} {'yes' if c['is_pilot'] else ''}")
    print("Owner gate: eyeball the pairing in exports/storyboard.html before approving 04g.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
