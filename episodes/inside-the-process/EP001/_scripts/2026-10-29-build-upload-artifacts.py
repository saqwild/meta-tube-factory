"""Build metadata/upload.json + metadata/upload-sheet.md for EP001.

Mirrors the approved metadata/package.md fields (title, description,
ordered keyword set = Tags, chapters, problems) into the machine
upload JSON and the human upload sheet. Run from repo root.
"""
import hashlib
import json
import pathlib
import re

EP = pathlib.Path(__file__).resolve().parents[1]
PKG = EP / "metadata" / "package.md"
OUT_JSON = EP / "metadata" / "upload.json"
OUT_SHEET = EP / "metadata" / "upload-sheet.md"

md = PKG.read_text(encoding="utf-8")
title = re.search(r"^## Title\s*\n\s*\*\*(.+?)\*\*", md, re.M).group(1).strip()
desc_block = re.search(r"^## Description\s*\n\s*```text\n(.*?)```", md, re.M | re.S).group(1).strip("\n")
keywords_section = re.search(r"^## Video-specific keywords.*?\n(.*?)(?=^## )", md, re.M | re.S).group(1)
keywords = re.findall(r"^\d+\.\s+(.+)$", keywords_section, re.M)
problems = re.search(r"^## Problems.*?```text\n(.*?)```", md, re.M | re.S).group(1).strip("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(EP)).replace("\\", "/")


files = {
    "video_captioned": EP / "exports" / "final" / "EP001_HowBreadRisesInsideTheDough_Captioned.mp4",
    "video_clean": EP / "exports" / "final" / "EP001_HowBreadRisesInsideTheDough_Full.mp4",
    "caption_track": EP / "exports" / "final" / "EP001_HowBreadRisesInsideTheDough_Full.srt",
    "thumbnail_primary": EP / "metadata" / "thumbnail-concept1.png",
    "thumbnail_alternate": EP / "metadata" / "thumbnail-alternate.png",
}

doc = {
    "episode_id": "EP001",
    "channel": "Explained From Within (inside-the-process)",
    "title": title,
    "description": desc_block,
    "tags": keywords,
    "hashtags": ["#ExplainedFromWithin", "#HowThingsWork", "#BreadScience"],
    "category": "Education",
    "made_for_kids": False,
    "altered_or_synthetic_content": True,
    "visibility_at_upload": "unlisted (hackathon sample)",
    "problems_field": problems.splitlines(),
    "files": {k: {"path": rel(v), "sha256": sha(v), "bytes": v.stat().st_size} for k, v in files.items()},
}
OUT_JSON.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

sheet = f"""# EP001 upload sheet (copy-ready)

- Upload file: `{rel(files['video_captioned'])}`
- Visibility: unlisted (hackathon sample)
- Title: {title}
- Description: the fenced block in metadata/package.md (also in upload.json)
- Tags: {", ".join(keywords)}
- Hashtags: #ExplainedFromWithin #HowThingsWork #BreadScience
- Category: Education | Made for kids: No
- Altered/synthetic content: Yes - AI-generated visualization (declaration text in the description)
- Captions: upload `{rel(files['caption_track'])}` as the English caption track
- Thumbnail: `{rel(files['thumbnail_primary'])}` (alternate: `{rel(files['thumbnail_alternate'])}`)
- Problems field (Studio): paste the block from package.md
- End screen: final 5-20 s subscribe element only (no related video exists yet at launch)
"""
OUT_SHEET.write_text(sheet, encoding="utf-8")
print({"json": str(OUT_JSON), "sheet": str(OUT_SHEET), "tags": len(keywords), "title": title})
