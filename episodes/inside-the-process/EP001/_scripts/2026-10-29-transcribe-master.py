"""Transcribe the assembled master with Muse Voice Transcribe.

Saves the raw API response beside the transcript text so the caption
builder (and any re-check) works from the real Muse output.
Run from repo root.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import meta_models  # noqa: E402

EP = pathlib.Path(__file__).resolve().parents[1]
MASTER = EP / "exports" / "final" / "EP001_HowBreadRisesInsideTheDough_Full.mp4"
WAV = EP / "assembly" / "master-audio.wav"
RAW = EP / "assembly" / "master-transcript-raw.json"
TXT = EP / "assembly" / "master-transcript.txt"

subprocess.run(
    ["ffmpeg", "-y", "-v", "quiet", "-i", str(MASTER), "-vn", "-ac", "1", "-ar", "16000", str(WAV)],
    check=True,
)
result = meta_models.transcribe(str(WAV))
RAW.write_text(json.dumps(result, indent=2), encoding="utf-8")


def find_text(o):
    if isinstance(o, dict):
        for k in ("transcript", "text", "transcription"):
            if o.get(k):
                return str(o[k])
        for v in o.values():
            t = find_text(v)
            if t:
                return t
    return ""


TXT.write_text(find_text(result), encoding="utf-8")
print({"raw": str(RAW), "keys": list(result.keys()) if isinstance(result, dict) else type(result).__name__,
       "text_chars": len(find_text(result))})
