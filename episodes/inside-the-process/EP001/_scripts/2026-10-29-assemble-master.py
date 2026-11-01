"""Assemble EP001 master with ffmpeg (owner 06a decision: no askyt cut).

Intro 3 s slide + SC01..SC12 (SC02/SC03/SC09/SC10 trimmed to 17.04 s,
the rest full) + outro 5 s slide. Slides are PIL cards per
assembly/assembly-notes.md. Output: exports/final/..._Full.mp4
Run from repo root.
"""
import json
import pathlib
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

EP = pathlib.Path(__file__).resolve().parents[1]
INBOX = EP / "renders" / "ltx-inbox"
FINAL = EP / "exports" / "final"
WORK = EP / "assembly"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"
W, H = 1344, 768


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, y, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


def intro_slide(path):
    img = Image.new("RGB", (W, H), (246, 232, 212))
    d = ImageDraw.Draw(img)
    centered(d, "How Bread Rises: Inside the Dough", 250, font(FONT_BOLD, 64), (43, 26, 8))
    centered(d, "Made for the Meta Global AI Developer Hackathon", 360, font(FONT_REG, 36), (43, 26, 8))
    centered(d, "Explained From Within - a meta-tube-factory demo", 430, font(FONT_REG, 28), (120, 84, 40))
    img.save(path, "PNG")


def outro_slide(path):
    img = Image.new("RGB", (W, H), (10, 8, 6))
    d = ImageDraw.Draw(img)
    lines = [
        ("Produced end to end with Meta Muse models", 56, True),
        ("Muse Spark - reasoning and verdicts | Muse Wonder - script", 34, False),
        ("Muse Image - stills | Muse Voice Transcribe - dialogue audit", 34, False),
        ("Human gates at every stage - owner watched and approved", 34, False),
        ("Video rendered with LTX-2.5 image-to-video.", 28, False),
        ("Full pipeline, prompts and QA:", 28, False),
        ("github.com/saqwild/meta-tube-factory", 28, False),
    ]
    y = 180
    for text, size, bold in lines:
        centered(d, text, y, font(FONT_BOLD if bold else FONT_REG, size), (255, 246, 232))
        y += size + 34
    img.save(path, "PNG")


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def main():
    FINAL.mkdir(parents=True, exist_ok=True)
    intro_png = WORK / "intro-slide.png"
    outro_png = WORK / "outro-slide.png"
    intro_slide(intro_png)
    outro_slide(outro_png)

    # Approved render per clip from the ingest manifest (source of truth).
    ingest = json.loads((EP / "renders" / "render-manifest.json").read_text(encoding="utf-8"))
    by_clip = {c["clip"]: c["path"] for c in ingest["clips"]}
    trim_to = {"SC02": 17.04, "SC03": 17.04, "SC09": 17.04, "SC10": 17.04}

    segments = []  # (label, [ffmpeg input args], duration)
    segments.append(("INTRO", ["-loop", "1", "-t", "3", "-i", str(intro_png),
                               "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=48000:cl=stereo"], 3.0))
    for i in range(1, 13):
        clip = f"SC{i:02d}"
        src = EP / by_clip[clip]
        dur = trim_to.get(clip)
        args = ["-i", str(src)]
        segments.append((clip, args, dur))
    segments.append(("OUTRO", ["-loop", "1", "-t", "5", "-i", str(outro_png),
                               "-f", "lavfi", "-t", "5", "-i", "anullsrc=r=48000:cl=stereo"], 5.0))

    cmd = ["ffmpeg", "-y"]
    for _, args, _ in segments:
        cmd += args
    filters = []
    total = 0.0
    timeline = []
    for idx, (label, _, dur) in enumerate(segments):
        # Locate this segment's video/audio input indices: slides take 2 inputs, clips 1.
        timeline.append((label, round(total, 2)))
        if label in ("INTRO", "OUTRO"):
            v_in, a_in = idx * 2 - (sum(1 for l, _, _ in segments[:idx] if l not in ("INTRO", "OUTRO"))), None
        # Simpler: rebuild input index map below.
        total += dur if dur else 20.04
    # Build input index map deterministically.
    input_index = []
    n = 0
    for label, _, _ in segments:
        if label in ("INTRO", "OUTRO"):
            input_index.append((n, n + 1))
            n += 2
        else:
            input_index.append((n, None))
            n += 1
    for idx, (label, _, dur) in enumerate(segments):
        v_in, a_in = input_index[idx]
        trim = f",trim=duration={dur}" if dur and label not in ("INTRO", "OUTRO") else ""
        fade = ""
        if label == "INTRO":
            fade = ",fade=t=in:st=0:d=0.5"
        if label == "OUTRO":
            fade = ",fade=t=in:st=0:d=0.5,fade=t=out:st=4.2:d=0.8"
        filters.append(
            f"[{v_in}:v]scale={W}:{H},fps=24,format=yuv420p{trim}{fade},setpts=PTS-STARTPTS[v{idx}]"
        )
        if a_in is not None:
            filters.append(f"[{a_in}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{idx}]")
        else:
            atrim = f"atrim=duration={dur}," if dur else ""
            filters.append(f"[{v_in}:a]{atrim}aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{idx}]")
    concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(len(segments)))
    filters.append(f"{concat_inputs}concat=n={len(segments)}:v=1:a=1[outv][outa]")
    out = FINAL / "EP001_HowBreadRisesInsideTheDough_Full.mp4"
    cmd += ["-filter_complex", ";".join(filters), "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
            str(out)]
    run(cmd)
    print({"master": str(out), "timeline_starts": timeline})


if __name__ == "__main__":
    main()
