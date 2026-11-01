"""Build the 1080p HD upload master from the clean master + SRT.

Source renders are 1344x768; YouTube serves its lower tier at that
size. Upscaling to 1920x1080 (same 16:9) with a high-quality encode
puts the upload in YouTube's 1080p HD tier. Captions are applied
after scaling so the text stays crisp. Run from repo root.
"""
import pathlib
import subprocess

EP = pathlib.Path(__file__).resolve().parents[1]
FINAL = EP / "exports" / "final"
MASTER = FINAL / "EP001_HowBreadRisesInsideTheDough_Full.mp4"
SRT = FINAL / "EP001_HowBreadRisesInsideTheDough_Full.srt"
OUT = FINAL / "EP001_HowBreadRisesInsideTheDough_Captioned_HD.mp4"

style = ("FontName=Arial,FontSize=16,PrimaryColour=&H00F5EEE6,"
         "BackColour=&HA8000000,BorderStyle=4,Alignment=2,MarginV=20")
srt_arg = str(SRT).replace("\\", "/").replace(":", "\\:")
subprocess.run(
    ["ffmpeg", "-y", "-v", "error", "-i", str(MASTER),
     "-vf", f"scale=1920:1080:flags=lanczos,subtitles='{srt_arg}':force_style='{style}'",
     "-c:v", "libx264", "-crf", "16", "-preset", "medium",
     "-c:a", "copy", str(OUT)],
    check=True,
)
print({"saved": str(OUT), "bytes": OUT.stat().st_size})
