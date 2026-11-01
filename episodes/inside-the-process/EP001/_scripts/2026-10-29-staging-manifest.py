"""Write postprod/staging-manifest.json for the ffmpeg assembly.

For each clip: source render (from the 05 ingest manifest), its
SHA-256, the kept range from the owner's cut list, and the resulting
segment duration in the master. Slides are recorded as inserts.
Run from repo root.
"""
import json
import pathlib

EP = pathlib.Path(__file__).resolve().parents[1]
ingest = json.loads((EP / "renders" / "render-manifest.json").read_text(encoding="utf-8"))
postprod = json.loads((EP / "postprod" / "postprod-manifest.json").read_text(encoding="utf-8"))
timeline = {t["label"]: t for t in postprod["timeline"]}
trim = {"SC02", "SC03", "SC09", "SC10"}

clips = []
for entry in ingest["clips"]:
    clip = entry["clip"]
    clips.append({
        "clip": clip,
        "source": entry["path"],
        "source_sha256": entry["sha256"],
        "kept_range": "0.00-17.04" if clip in trim else "full",
        "staged_video_seconds": timeline[clip]["duration"],
        "staged_audio_seconds": timeline[clip]["duration"],
        "master_start_seconds": timeline[clip]["start"],
    })

doc = {
    "schema_version": 1,
    "episode_id": "EP001",
    "method": "ffmpeg (segments normalized to 1344x768/24fps, audio resampled 48k stereo, concat)",
    "inserts": [
        {"label": "INTRO", "file": "assembly/intro-slide.png", "duration": 3.0},
        {"label": "OUTRO", "file": "assembly/outro-slide.png", "duration": 5.0},
    ],
    "clips": clips,
}
out = EP / "postprod" / "staging-manifest.json"
out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print({"wrote": str(out), "clips": len(clips)})
