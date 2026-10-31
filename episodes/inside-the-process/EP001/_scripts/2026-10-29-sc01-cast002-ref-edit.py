"""Regenerate SC01 frame-0 still with CAST-002 sheet attached as reference.

Uses Muse Image /images/edits (tools.meta_models.image_edit) so identity is
conditioned on the actual locked sheet, not only on text. Candidate is saved
outside renders/stills until it passes visual identity validation.
Run from repo root: python episodes/inside-the-process/EP001/_scripts/2026-10-29-sc01-cast002-ref-edit.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import meta_models  # noqa: E402

EP = ROOT / "episodes" / "inside-the-process" / "EP001"
SHEET = EP / "visual" / "references" / "characters" / "EP001-CAST002-sheet.png"
OUT_RAW = EP / "qa" / "candidates" / "SC01-ref-v1.raw"
OUT_PNG = EP / "qa" / "candidates" / "SC01-ref-v1.png"

PROMPT = (
    "Use the attached character reference sheet as the exact identity lock for the one person in this scene. "
    "The person must be that same adult: short tight curly dark hair close to the head (not long, not voluminous), "
    "medium-brown skin, round face, brown eyes, same nose and lips, wearing a plain navy blue hoodie with no logos "
    "and grey trousers. Do not invent a different person, do not make the hair longer, do not change the face. "
    "Show exactly one person, not a contact sheet, no reference-sheet layout, no text or labels. "
    "Scene: medium wide shot in a warm home kitchen with wooden counter and soft daylight. The adult stands at the "
    "counter on the left, body facing camera three-quarter, face fully visible and unobstructed, mouth closed and "
    "relaxed, gaze directed toward a glass mixing bowl on the counter. One hand holds a linen cloth beside the bowl, "
    "the cloth held clear of the bowl and not covering the dough. Inside the glass bowl is a pale risen dough ball, "
    "doubled in size, fully uncovered. Above the bowl a small ivory-and-orange capsule with a cyan light ring is "
    "descending toward the dough. Photoreal cinematic scientific visualization, warm polished home realism, "
    "ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct, "
    "short clean nails, minimal arm hair. 16:9 composition."
)


def main() -> int:
    result = meta_models.image_edit(PROMPT, [str(SHEET)])
    data = (result.get("data") or [{}])[0]
    import base64

    raw = base64.b64decode(data["b64_json"]) if data.get("b64_json") else b""
    if not raw and data.get("url"):
        import urllib.request

        raw = urllib.request.urlopen(data["url"], timeout=120).read()
    if not raw:
        print({"saved": None, "response_keys": list(result.keys()), "data_keys": list(data.keys())})
        return 1
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_bytes(raw)
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.save(OUT_PNG, "PNG")
    print({"saved": str(OUT_PNG), "raw_bytes": len(raw), "size": img.size, "raw_format": Image.open(io.BytesIO(raw)).format})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
