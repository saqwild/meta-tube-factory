"""Build captions from the Muse Voice Transcribe master transcript.

Input: assembly/master-transcript-raw.json (turns with startMs/endMs).
Output: exports/final/EP001_HowBreadRisesInsideTheDough_Full.srt and
a burned-in captioned master beside the clean master. Caption text is
the Muse transcript, sentence-split within each turn with timing
distributed by sentence length; immediate ASR word stutters deduped.
Run from repo root (after 2026-10-29-transcribe-master.py).
"""
import json
import pathlib
import re
import subprocess

EP = pathlib.Path(__file__).resolve().parents[1]
RAW = EP / "assembly" / "master-transcript-raw.json"
FINAL = EP / "exports" / "final"
MASTER = FINAL / "EP001_HowBreadRisesInsideTheDough_Full.mp4"
SRT = FINAL / "EP001_HowBreadRisesInsideTheDough_Full.srt"
CAPTIONED = FINAL / "EP001_HowBreadRisesInsideTheDough_Captioned.mp4"


def dedupe_stutter(text):
    return re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", text, flags=re.IGNORECASE)


def sentences(text):
    parts = re.split(r"(?<=[.?!])\s+", text.strip())
    # Re-split long sentences at commas for readable caption lines.
    out = []
    for part in parts:
        while len(part) > 84 and ", " in part:
            head, tail = part.rsplit(", ", 1)
            if len(head) < 40:
                break
            out.append(head + ",")
            part = tail
        out.append(part)
    return [p for p in out if p]


def ts(ms):
    s, ms = divmod(int(ms), 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(text, width=42):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2])


def main():
    doc = json.loads(RAW.read_text(encoding="utf-8"))
    entries = []
    for turn in doc["turns"]:
        start, end = turn["startMs"], turn["endMs"]
        sents = sentences(dedupe_stutter(turn["transcript"]))
        total_chars = sum(len(s) for s in sents) or 1
        cursor = start
        for sent in sents:
            dur = (end - start) * (len(sent) / total_chars)
            entries.append((cursor, cursor + dur, sent))
            cursor += dur
    lines = []
    for i, (a, b, text) in enumerate(entries, 1):
        lines += [str(i), f"{ts(a)} --> {ts(b)}", wrap(text), ""]
    SRT.write_text("\n".join(lines), encoding="utf-8")

    style = ("FontName=Arial,FontSize=22,PrimaryColour=&H00F5EEE6,"
             "BackColour=&HA8000000,BorderStyle=4,Alignment=2,MarginV=36")
    srt_arg = str(SRT).replace("\\", "/").replace(":", "\\:")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(MASTER),
         "-vf", f"subtitles='{srt_arg}':force_style='{style}'",
         "-c:a", "copy", str(CAPTIONED)],
        check=True,
    )
    print({"srt": str(SRT), "entries": len(entries), "captioned": str(CAPTIONED)})


if __name__ == "__main__":
    main()
