"""Edit SC01 still to single-cloth, one-hand staging.

Refs: CAST-002 sheet (identity lock) + current SC01 still (scene to
preserve). Change only the cloth staging: exactly one linen cloth,
held in one hand at the adult's side, the other hand empty, no folded
cloth on the counter, dough fully uncovered in the glass bowl.
Run from repo root.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import meta_models  # noqa: E402

EP = ROOT / "episodes" / "inside-the-process" / "EP001"
SHEET = EP / "visual" / "references" / "characters" / "EP001-CAST002-sheet.png"
SCENE = EP / "renders" / "stills" / "SC01.png"
OUT_RAW = EP / "qa" / "candidates" / "SC01-cloth-v1.raw"
OUT_PNG = EP / "qa" / "candidates" / "SC01-cloth-v1.png"

PROMPT = (
    "Keep the second attached image as the exact scene to preserve: same warm kitchen, same adult "
    "matching the first attached character reference sheet (short tight curly dark hair, medium-brown "
    "skin, round face, plain navy blue hoodie with no logos, grey trousers), same glass bowl with the "
    "pale risen dough fully uncovered, same ivory-and-orange capsule with cyan ring descending above "
    "the bowl, same counter and daylight. Change only the cloth staging: there is exactly one linen "
    "cloth in the whole image, held in the adult's one hand down at the adult's side, clear of the "
    "bowl. The adult's other hand is empty and rests on the counter edge. The counter surface beside "
    "the bowl is bare wood with no folded cloth on it. The dough stays fully uncovered for the whole "
    "frame. Exactly one person, no contact sheet, no text or labels, mouth closed and relaxed. "
    "Photoreal cinematic scientific visualization, warm polished home realism. Clean natural anatomy, "
    "hands anatomically correct, short clean nails, minimal arm hair. 16:9 composition."
)


def main() -> int:
    result = meta_models.image_edit(PROMPT, [str(SHEET), str(SCENE)])
    data = (result.get("data") or [{}])[0]
    import base64

    raw = base64.b64decode(data["b64_json"]) if data.get("b64_json") else b""
    if not raw:
        print({"saved": None, "keys": list(data.keys())})
        return 1
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_bytes(raw)
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.save(OUT_PNG, "PNG")
    print({"saved": str(OUT_PNG), "raw_bytes": len(raw), "size": img.size})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
