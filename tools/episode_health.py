#!/usr/bin/env python3
"""One read-only end-to-end health check for an episode.

WHY THIS EXISTS
---------------
Each stage has its own checker (`ltx_prompt_validator`, `render_audio_audit`,
`metadata_validator`, `check_reference_assets`, the `stage-gates.json` gate). None
of them answers "is this whole episode still internally consistent?" -- a question
that comes up every time an episode is revisited: did a recorded hash drift, does
every manifest agree on the clip list, did a review go stale when its source was
re-generated, is the final MP4 actually 16:9 with audio.

This tool only does mechanical cross-consistency. Anything that needs a model
(beat adherence, cast drift, "does it look right") stays in its own stage.

RUN
---
    python tools/episode_health.py --channel signed-anyway --episode EP001
    python tools/episode_health.py --channel signed-anyway --episode EP001 --json

Exit 0 = no FAIL (WARN is allowed). Exit 1 = at least one FAIL. Exit 2 = setup
problem (unknown channel/episode).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import episode_state as es  # noqa: E402
import ltx_prompt_validator as validator  # noqa: E402
from project_paths import EPISODES_DIR, ROOT  # noqa: E402

SCHEMA_DIR = ROOT / "pipeline" / "schemas"
SC_RE = re.compile(r"SC\d{2,3}", re.IGNORECASE)
SC_HEADING = re.compile(r"(?m)^##\s*(SC\d{2,3})\b", re.IGNORECASE)
BACKTICK_PATH = re.compile(r"`([^`]+\.(?:png|jpe?g|webp|txt|md|json))`")
BARE_SHA = re.compile(r"\b([0-9a-f]{64})\b")


@dataclass
class Finding:
    level: str  # OK, WARN, FAIL
    category: str
    message: str


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# category: required files (every completed stage's declared deliverables)
# ─────────────────────────────────────────────────────────────────────────────

def check_required_files(ep: Path, state: dict) -> list[Finding]:
    out: list[Finding] = []
    gates = es._load_stage_gates()
    completed = [c["stage"] for c in state.get("completed_stages", [])]
    # A gap in an OPEN episode blocks progress -> FAIL. A gap in a CLOSED episode
    # is history (it shipped; the stage may predate the current gate) -> WARN.
    lvl = "WARN" if state.get("status") == "closed" else "FAIL"
    for stage in dict.fromkeys(completed):  # de-dup, keep order
        for pat in es.stage_spec(gates, stage, state.get("stage_sequence"))["outputs"]:
            if any(c in pat for c in "*?["):
                if not list(ep.glob(pat)):
                    out.append(Finding(lvl, "required-files", f"{stage}: no file matches {pat!r}"))
            else:
                p = ep / pat
                if not p.exists():
                    out.append(Finding(lvl, "required-files", f"{stage}: missing {pat}"))
                elif p.is_file() and p.stat().st_size == 0:
                    out.append(Finding(lvl, "required-files", f"{stage}: {pat} is empty"))
    if not out:
        out.append(Finding("OK", "required-files",
                           f"all deliverables present for {len(set(completed))} completed stage(s)"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# category: schemas
# ─────────────────────────────────────────────────────────────────────────────

_SCHEMA_MAP = {
    "episode-state.json": "episode-state.schema.json",
    "_context/blocking.json": "blocking.schema.json",
    "_context/frame0-requirements.json": "frame0-requirements.schema.json",
    "_context/ltx-prompt-manifest.json": "ltx-prompt-manifest.schema.json",
    "_context/ltx-prompt-review.json": "ltx-prompt-review.schema.json",
    "exports/ltx-render-package/render-manifest.json": "ltx-render-package.schema.json",
    "qa/ltx-pilot-qa.json": "ltx-pilot-qa.schema.json",
    "story/coverage-map.json": "coverage-map.schema.json",
}


def check_schemas(ep: Path, state: dict) -> list[Finding]:
    try:
        import jsonschema
    except ImportError:
        return [Finding("WARN", "schemas", "jsonschema not installed -- skipped")]
    out: list[Finding] = []
    checked = 0
    for rel, schema_name in _SCHEMA_MAP.items():
        target = ep / rel
        schema_path = SCHEMA_DIR / schema_name
        if not target.exists() or not schema_path.exists():
            continue
        checked += 1
        try:
            jsonschema.validate(_load_json(target), _load_json(schema_path))
        except json.JSONDecodeError as exc:
            out.append(Finding("FAIL", "schemas", f"{rel}: not valid JSON ({exc})"))
        except jsonschema.ValidationError as exc:
            loc = "/".join(str(p) for p in exc.absolute_path) or "(root)"
            out.append(Finding("FAIL", "schemas", f"{rel}: schema violation at {loc}: {exc.message}"))
    if not any(f.level == "FAIL" for f in out):
        out.append(Finding("OK", "schemas", f"{checked} JSON artifact(s) validate against their schema"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# category: clip coverage
# ─────────────────────────────────────────────────────────────────────────────

def _clip_ids_from_md(path: Path) -> set[str]:
    return {m.group(1).upper() for m in SC_HEADING.finditer(path.read_text(encoding="utf-8"))}


def _manifest_clip_ids(path: Path):
    d = _load_json(path)
    clips = d.get("clips")
    if isinstance(clips, dict):
        return list(clips.keys())
    return [c.get("clip") for c in (clips or [])]


def check_clip_coverage(ep: Path, state: dict) -> list[Finding]:
    sources: dict[str, set[str]] = {}
    out: list[Finding] = []

    def add(name: str, path: Path, loader) -> None:
        if not path.exists():
            return
        try:
            ids = loader(path)
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            out.append(Finding("FAIL", "clip-coverage", f"{name}: unreadable ({exc})"))
            return
        s = {str(x).upper() for x in ids if x and SC_RE.fullmatch(str(x))}
        if s:
            sources[name] = s

    add("blocking.json", ep / "_context/blocking.json", _manifest_clip_ids)
    add("frame0-requirements.json", ep / "_context/frame0-requirements.json", _manifest_clip_ids)
    add("ltx-prompt-manifest.json", ep / "_context/ltx-prompt-manifest.json", _manifest_clip_ids)
    add("7-video-prompts.md", ep / "prompts/7-video-prompts.md", _clip_ids_from_md)
    add("renders/stills/", ep / "renders/stills",
        lambda d: [f.stem for f in d.glob("*.png")])
    add("04g render-manifest", ep / "exports/ltx-render-package/render-manifest.json",
        _manifest_clip_ids)
    add("05 render-manifest", ep / "renders/render-manifest.json", _manifest_clip_ids)

    if len(sources) < 2:
        if not out:
            out.append(Finding("OK", "clip-coverage", "not enough clip sources to cross-check yet"))
        return out

    union = set().union(*sources.values())
    for name, ids in sorted(sources.items()):
        missing = union - ids
        if missing:
            out.append(Finding("FAIL", "clip-coverage",
                               f"{name} is missing {', '.join(sorted(missing))} "
                               f"(present in other sources)"))
    if not any(f.level == "FAIL" for f in out):
        out.append(Finding("OK", "clip-coverage",
                           f"{len(union)} clip(s) consistent across {len(sources)} sources"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# category: hashes
# ─────────────────────────────────────────────────────────────────────────────

_TEXT_SUFFIXES = {".txt", ".md", ".json"}


def _hash_matches(file: Path, recorded: str) -> bool:
    raw = file.read_bytes()
    if hashlib.sha256(raw).hexdigest() == recorded:
        return True
    # text deliverables are frequently hashed LF-normalized but checked out CRLF
    # on Windows (and vice versa) -- not content drift.
    if file.suffix.lower() in _TEXT_SUFFIXES:
        return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() == recorded
    return False


def _check_hash(out: list[Finding], label: str, file: Path, recorded: str) -> None:
    recorded = recorded.lower()
    if not file.exists():
        out.append(Finding("WARN", "hashes",
                           f"{label}: {file.name} is recorded but no longer on disk "
                           f"(renamed or moved?)"))
        return
    if not _hash_matches(file, recorded):
        out.append(Finding("FAIL", "hashes",
                           f"{label}: {file.name} recorded {recorded[:12]}..., "
                           f"now {_sha256(file)[:12]}..."))


def check_hashes(ep: Path, state: dict) -> list[Finding]:
    out: list[Finding] = []
    checked = 0

    pkg = ep / "exports/ltx-render-package"
    m = pkg / "render-manifest.json"
    if m.exists():
        d = _load_json(m)
        for key, fname in (("master_prompt_sha256", "master-prompt.txt"),
                           ("negative_prompt_sha256", "negative-prompt.txt")):
            if d.get(key):
                checked += 1
                _check_hash(out, f"04g {key}", pkg / fname, d[key])
        for c in d.get("clips", []):
            if c.get("still_sha256") and c.get("still_file"):
                checked += 1
                _check_hash(out, f"04g still {c['clip']}", pkg / "stills" / c["still_file"],
                            c["still_sha256"])

    m = ep / "_context/ltx-prompt-manifest.json"
    prompts = ep / "prompts/7-video-prompts.md"
    if m.exists():
        blocks = (dict(validator._iter_clip_blocks(prompts.read_text(encoding="utf-8")))
                  if prompts.exists() else {})
        manifest_prompt_hashes = {}
        for c in _load_json(m).get("clips", []):
            clip = c.get("clip", "?")
            if c.get("prompt_sha256"):
                manifest_prompt_hashes[clip] = c["prompt_sha256"].lower()
                checked += 1
                body = blocks.get(clip)
                if body is None:
                    out.append(Finding("FAIL", "hashes",
                                       f"04f3 manifest {clip}: no ## {clip} block in 7-video-prompts.md"))
                # a pre-tool (hand-built) manifest may have hashed the body with a
                # trailing newline -- same content, not drift.
                elif c["prompt_sha256"].lower() not in {
                        hashlib.sha256(body.encode("utf-8")).hexdigest(),
                        hashlib.sha256((body + "\n").encode("utf-8")).hexdigest()}:
                    out.append(Finding("FAIL", "hashes",
                                       f"04f3 manifest {clip}: prompt block changed since the "
                                       f"manifest was built -- rebuild it (tools/ltx_prompt_manifest.py)"))
            if c.get("still_sha256") and c.get("still_path"):
                checked += 1
                _check_hash(out, f"04f3 manifest still {clip}", ep / c["still_path"], c["still_sha256"])
        pkg_manifest = ep / "exports/ltx-render-package/render-manifest.json"
        if pkg_manifest.exists():
            for c in _load_json(pkg_manifest).get("clips", []):
                want = manifest_prompt_hashes.get(c.get("clip"))
                if want and c.get("prompt_sha256", "").lower() != want:
                    out.append(Finding("FAIL", "hashes",
                                       f"04g package {c.get('clip')}: prompt hash disagrees with the "
                                       f"04f3 manifest -- the package predates the current prompts"))

    m = ep / "renders/render-manifest.json"
    if m.exists():
        for c in _load_json(m).get("clips", []):
            if c.get("sha256") and c.get("path"):
                checked += 1
                _check_hash(out, f"05 render {c.get('clip', '?')}", ep / c["path"], c["sha256"])

    m = ep / "postprod/postprod-manifest.json"
    if m.exists():
        d = _load_json(m)
        if d.get("config_sha256"):
            checked += 1
            _check_hash(out, "postprod config", ep / "postprod/postprod-config.json", d["config_sha256"])
        for name, o in (d.get("outputs") or {}).items():
            if o.get("sha256") and o.get("path"):
                checked += 1
                _check_hash(out, f"postprod {name}", ep / o["path"], o["sha256"])

    m = ep / "visual/references/manifest.md"
    if m.exists():
        base = m.parent
        # a re-issued reference appends a new row and keeps the old one as the audit trail,
        # so only the LAST recorded hash for a path is the current one.
        latest: dict[str, str] = {}
        for line in m.read_text(encoding="utf-8").splitlines():
            if not line.lstrip().startswith("|"):
                continue
            path_m, sha_m = BACKTICK_PATH.search(line), BARE_SHA.search(line)
            if path_m and sha_m:
                latest[path_m.group(1)] = sha_m.group(1)
        for rel, sha in latest.items():
            checked += 1
            _check_hash(out, "visual/references/manifest.md", base / rel, sha)

    if not any(f.level == "FAIL" for f in out):
        out.append(Finding("OK", "hashes", f"{checked} recorded hash(es) still match on disk"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# category: review freshness
# ─────────────────────────────────────────────────────────────────────────────

def check_review_freshness(ep: Path, state: dict) -> list[Finding]:
    out: list[Finding] = []

    audit = ep / "renders/audio-content-audit.json"
    if audit.exists():
        d = _load_json(audit)
        for key, src in (("source_manifest_sha256", ep / "renders/render-manifest.json"),
                         ("source_prompts_sha256", ep / "prompts/7-video-prompts.md")):
            if d.get(key) and src.exists() and _sha256(src) != d[key].lower():
                out.append(Finding("WARN", "review-freshness",
                                   f"audio-content-audit.json ran against an older {src.name} "
                                   f"-- re-run render_audio_audit.py"))

    review = ep / "_context/ltx-prompt-review.json"
    if review.exists():
        d = _load_json(review)
        prompts = ep / "prompts/7-video-prompts.md"
        manifest = ep / "_context/ltx-prompt-manifest.json"
        if d.get("source_prompts_sha256"):
            if prompts.exists() and _sha256(prompts) != d["source_prompts_sha256"].lower():
                out.append(Finding("WARN", "review-freshness",
                                   "ltx-prompt-review.json ran against an older 7-video-prompts.md "
                                   "-- the recorded PASS predates the current file"))
        elif d.get("source_manifest_sha256"):
            # Legacy reviews hashed the manifest if it existed, else the prompts
            # file (always the prompts file at 04f3) -- either match is fresh.
            legacy = d["source_manifest_sha256"].lower()
            now = {_sha256(p) for p in (prompts, manifest) if p.exists()}
            if now and legacy not in now:
                out.append(Finding("WARN", "review-freshness",
                                   "ltx-prompt-review.json (legacy) matches neither the current "
                                   "7-video-prompts.md nor ltx-prompt-manifest.json"))
        # A shipped episode's review necessarily predates later rule changes --
        # only an open episode still has to re-validate against current rules.
        validator = ROOT / "tools/ltx_prompt_validator.py"
        if (state.get("status") != "closed" and d.get("validator_sha256")
                and _sha256(validator) != d["validator_sha256"].lower()):
            out.append(Finding("WARN", "review-freshness",
                               "ltx-prompt-review.json was produced by an older "
                               "ltx_prompt_validator.py -- the recorded PASS predates the current rules"))

    # Only the latest completion entry per stage — a reopened+re-completed stage
    # keeps earlier entries as history and those necessarily predate the files.
    latest_entries: dict[str, dict] = {}
    for entry in state.get("completed_stages", []):
        latest_entries[entry.get("stage", "?")] = entry
    for stage, entry in latest_entries.items():
        digest = entry.get("deliverable_digest")
        if not digest:
            continue
        when = entry.get("completed_at", "?")
        for f in digest.get("files", []):
            fp = ep / f["path"]
            if not fp.is_file():
                out.append(Finding("WARN", "review-freshness",
                                   f"{stage} approved {when} but {f['path']} is now gone"))
            elif _sha256(fp) != f["sha256"]:
                out.append(Finding("WARN", "review-freshness",
                                   f"{stage} approved {when} against an older {f['path']} "
                                   f"-- it has changed since"))

    if not out:
        out.append(Finding("OK", "review-freshness", "every recorded review still matches its source"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# category: final media
# ─────────────────────────────────────────────────────────────────────────────

def _ffprobe(path: Path) -> dict | None:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", str(path)],
            capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout) if r.returncode == 0 else None
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def check_final_media(ep: Path, state: dict) -> list[Finding]:
    finals = sorted((ep / "exports/final").glob("*.mp4")) if (ep / "exports/final").is_dir() else []
    if not finals:
        return [Finding("OK", "final-media", "no final MP4 yet")]

    out: list[Finding] = []
    recorded_durations = []
    pm = ep / "postprod/postprod-manifest.json"
    if pm.exists():
        for o in (_load_json(pm).get("outputs") or {}).values():
            if o.get("duration_seconds"):
                recorded_durations.append(float(o["duration_seconds"]))

    # the render geometry the clips were actually produced at (channel.json says
    # "16:9" but LTX renders 1344x768 = 7:4); accept that exact size or a ratio
    # within 0.05 of 16:9.
    want_res = None
    rm = ep / "renders/render-manifest.json"
    if rm.exists():
        for c in _load_json(rm).get("clips", []):
            if c.get("resolution"):
                want_res = c["resolution"]
                break

    probed_any = False
    for mp4 in finals:
        info = _ffprobe(mp4)
        if info is None:
            out.append(Finding("WARN", "final-media", f"{mp4.name}: ffprobe unavailable or failed"))
            continue
        probed_any = True
        streams = info.get("streams", [])
        vids = [s for s in streams if s.get("codec_type") == "video"]
        has_audio = any(s.get("codec_type") == "audio" for s in streams)
        dur = float(info.get("format", {}).get("duration", 0) or 0)

        if not has_audio:
            out.append(Finding("FAIL", "final-media", f"{mp4.name}: no audio stream"))
        if vids:
            w, h = vids[0].get("width", 0), vids[0].get("height", 0)
            res = f"{w}x{h}"
            ratio_ok = bool(h) and abs((w / h) - (16 / 9)) <= 0.05
            if not (res == want_res or ratio_ok):
                out.append(Finding("FAIL", "final-media",
                                   f"{mp4.name}: {res} is neither the render geometry "
                                   f"({want_res}) nor ~16:9"))
        else:
            out.append(Finding("FAIL", "final-media", f"{mp4.name}: no video stream"))
        if dur <= 0:
            out.append(Finding("FAIL", "final-media", f"{mp4.name}: zero/unknown duration"))
        elif recorded_durations and not any(abs(dur - rd) < 1.5 for rd in recorded_durations):
            out.append(Finding("WARN", "final-media",
                               f"{mp4.name}: {dur:.1f}s matches no duration recorded in "
                               f"postprod-manifest.json ({', '.join(f'{d:.1f}' for d in recorded_durations)})"))

    if probed_any and not any(f.level == "FAIL" for f in out):
        out.append(Finding("OK", "final-media",
                           f"{len(finals)} final MP4(s): 16:9, audio present, duration sane"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# aggregate
# ─────────────────────────────────────────────────────────────────────────────

_CATEGORIES = (
    check_required_files,
    check_schemas,
    check_clip_coverage,
    check_hashes,
    check_review_freshness,
    check_final_media,
)


def run_health(channel_slug: str, episode_id: str, *, root: Path | None = None) -> list[Finding]:
    base = (root / "episodes") if root else EPISODES_DIR
    ep = base / channel_slug / episode_id
    state = _load_json(ep / "episode-state.json")
    findings: list[Finding] = []
    for fn in _CATEGORIES:
        cat = fn.__name__.replace("check_", "").replace("_", "-")
        try:
            findings.extend(fn(ep, state))
        except Exception as exc:  # noqa: BLE001 -- a broken checker must not hide the others
            findings.append(Finding("FAIL", cat, f"health check crashed: {exc!r}"))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="episode_health.py",
        description="Read-only end-to-end consistency check for one episode. Never writes.")
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)

    ep = EPISODES_DIR / a.channel / a.episode
    if not (ep / "episode-state.json").exists():
        print(f"not found: {ep / 'episode-state.json'}")
        return 2

    findings = run_health(a.channel, a.episode)
    fails = [f for f in findings if f.level == "FAIL"]
    warns = [f for f in findings if f.level == "WARN"]

    if a.json:
        print(json.dumps({
            "channel": a.channel, "episode": a.episode,
            "status": "FAIL" if fails else ("WARN" if warns else "OK"),
            "findings": [asdict(f) for f in findings],
        }, indent=2))
        return 1 if fails else 0

    print(f"episode health -- {a.channel} / {a.episode}\n")
    for cat in dict.fromkeys(f.category for f in findings):
        print(f"  [{cat}]")
        for f in [x for x in findings if x.category == cat]:
            print(f"    {f.level:<4} {f.message}")
        print()
    print(f"OVERALL: {'FAIL' if fails else ('WARN' if warns else 'OK')}  "
          f"({len(fails)} fail, {len(warns)} warn, "
          f"{sum(1 for f in findings if f.level == 'OK')} ok)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
