"""Stage 05 render ingest for EP001.

Probes every clip in renders/ltx-inbox with ffprobe, hashes it, reads
its vidgen-dist sidecar settings, cross-checks both against the 04g
package manifest, and writes renders/render-manifest.json.
Run from repo root.
"""
import hashlib
import json
import pathlib
import re
import subprocess

EP = pathlib.Path(__file__).resolve().parents[1]
INBOX = EP / "renders" / "ltx-inbox"
PKG = EP / "exports" / "ltx-render-package" / "render-manifest.json"
OUT = EP / "renders" / "render-manifest.json"

pkg = json.loads(PKG.read_text(encoding="utf-8"))
pkg_clips = {c["clip"]: c for c in pkg["clips"]}
pkg_settings = pkg["settings"]


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    d = json.loads(out)
    video = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    audio = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    return {
        "duration_seconds": round(float(d["format"]["duration"]), 2),
        "width": video.get("width"),
        "height": video.get("height"),
        "video_codec": video.get("codec_name"),
        "audio_present": audio is not None,
        "audio_codec": (audio or {}).get("codec_name"),
    }


entries = []
problems = []
for mp4 in sorted(INBOX.glob("s*.mp4")):
    m = re.match(r"s(\d+)_", mp4.name)
    clip = f"SC{int(m.group(1)):02d}"
    side_path = mp4.with_suffix(".json")
    if not side_path.exists():
        problems.append(f"{clip}: missing sidecar {side_path.name}")
        continue
    side = json.loads(side_path.read_text(encoding="utf-8"))
    sl = side.get("settings_ltx", {})
    entry = {
        "clip": clip,
        "path": f"renders/ltx-inbox/{mp4.name}",
        "sha256": hashlib.sha256(mp4.read_bytes()).hexdigest(),
        **probe(mp4),
        "sidecar": f"renders/ltx-inbox/{side_path.name}",
        "sidecar_settings": {
            "workflow": pathlib.Path(side.get("workflow", {}).get("path", "")).name,
            "megapixels": sl.get("megapixels"),
            "duration_seconds": sl.get("duration"),
            "cfg": sl.get("cfg"),
            "cfg_refine": sl.get("cfg_refine"),
            "cfg_audio": sl.get("cfg_audio"),
            "img_compression": sl.get("img_compression"),
            "diffusion_model": sl.get("diffusion_model"),
        },
        "source_image_uploaded_as": side.get("source_image", {}).get("uploaded_as"),
        "package_prompt_sha256": pkg_clips[clip]["prompt_sha256"],
        "package_still_sha256": pkg_clips[clip]["still_sha256"],
        "is_pilot": pkg_clips[clip]["is_pilot"],
    }
    # Cross-checks
    if abs(entry["duration_seconds"] - pkg_settings["duration_seconds"]) > 0.6:
        problems.append(f"{clip}: duration {entry['duration_seconds']} != {pkg_settings['duration_seconds']}")
    if not entry["audio_present"]:
        problems.append(f"{clip}: no audio stream")
    if entry["source_image_uploaded_as"] != f"{clip}.png":
        problems.append(f"{clip}: source image {entry['source_image_uploaded_as']} != {clip}.png")
    for key, pkg_key in [("megapixels", "megapixels"), ("duration_seconds", "duration_seconds"),
                         ("cfg", "cfg"), ("cfg_refine", "cfg_refine"),
                         ("cfg_audio", "cfg_audio"), ("img_compression", "img_compression")]:
        if entry["sidecar_settings"][key] != pkg_settings[pkg_key]:
            problems.append(f"{clip}: sidecar {key}={entry['sidecar_settings'][key]} != package {pkg_settings[pkg_key]}")
    entries.append(entry)

expected = {f"SC{i:02d}" for i in range(1, 13)}
seen = {e["clip"] for e in entries}
if seen != expected:
    problems.append(f"clip set mismatch: missing {sorted(expected - seen)}, extra {sorted(seen - expected)}")

doc = {
    "schema_version": 1,
    "episode_id": "EP001",
    "channel_slug": "inside-the-process",
    "package_manifest_sha256": hashlib.sha256(PKG.read_bytes()).hexdigest(),
    "clips": entries,
    "problems": problems,
    "status": "PASS" if not problems else "FAIL",
}
OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
for e in entries:
    print(f"{e['clip']}  {e['duration_seconds']:>5}s  {e['width']}x{e['height']}  audio={e['audio_present']}  sha={e['sha256'][:12]}")
print(f"status={doc['status']} problems={problems}")
