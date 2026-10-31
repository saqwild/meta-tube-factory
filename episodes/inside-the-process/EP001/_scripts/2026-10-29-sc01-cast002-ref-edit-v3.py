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
OUT_RAW = EP / "qa" / "candidates" / "SC01-ref-v3.raw"
OUT_PNG = EP / "qa" / "candidates" / "SC01-ref-v3.png"

PROMPT = (
    "Keep the second attached image as the exact scene to preserve: same warm kitchen, same adult at the left counter holding the linen cloth clear of the glass bowl, same uncovered risen dough, same ivory-and-orange capsule with cyan ring descending above the bowl. "
    "Change only the adult's head direction: turn the head three-quarter toward the camera so the full face is clearly visible with both eyes, while the gaze stays slightly down toward the dough. "
    "The adult must remain the exact person in the first attached character reference sheet: short tight curly dark hair close to the head, medium-brown skin, round face, brown eyes, same nose and lips, plain navy blue hoodie with no logos, grey trousers. "
    "Exactly one person, no contact sheet, no text or labels, mouth closed and relaxed. Photoreal cinematic scientific visualization, warm polished home realism. Clean natural anatomy, hands anatomically correct, short clean nails, minimal arm hair. 16:9 composition."
)


def main() -> int:
    result = meta_models.image_edit(PROMPT, [str(SHEET), str(EP / "qa" / "candidates" / "SC01-ref-v1.png")])
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
