"""Build EP001 thumbnails from approved stills (metadata/package.md brief).

Concept 1: four-panel causal ladder composite of SC01/SC05/SC12 with
composited typography. Alternate: SC12 crumb close-up with one type
block. No generated imagery - approved stills only, per source policy.
Run from repo root.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

EP = pathlib.Path(__file__).resolve().parents[1]
STILLS = EP / "renders" / "stills"
OUT1 = EP / "metadata" / "thumbnail-concept1.png"
OUT2 = EP / "metadata" / "thumbnail-alternate.png"
PREVIEW = EP / "metadata" / "thumbnail-concept1-120px.png"

W, H = 1280, 720
CREAM = (246, 232, 212)
INK = (43, 26, 8)
DARK = (43, 26, 8)
FOOTER_TEXT = (255, 246, 232)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 10:
        f = font(size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(size)


def crop_to(img, box_w, box_h, focus_x=0.5):
    """Crop img to box aspect, centered on focus_x (0..1), full height first."""
    src_ratio = img.width / img.height
    dst_ratio = box_w / box_h
    if src_ratio > dst_ratio:
        new_w = int(img.height * dst_ratio)
        x0 = int((img.width - new_w) * focus_x)
        img = img.crop((x0, 0, x0 + new_w, img.height))
    else:
        new_h = int(img.width / dst_ratio)
        img = img.crop((0, 0, img.width, new_h))
    return img.resize((box_w, box_h), Image.LANCZOS)


def footer(draw):
    draw.rectangle([0, 680, 1000, 720], fill=DARK)
    draw.text((24, 686), "EXPLAINED FROM WITHIN", font=font(28), fill=FOOTER_TEXT)


def concept1():
    canvas = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(canvas)
    # Panel 1: text promise
    f1 = fit_font(d, "FROM DOUGH", 272, 92)
    f2 = fit_font(d, "TO LOAF", 272, 92)
    d.text((24, 250), "FROM DOUGH", font=f1, fill=INK)
    d.text((24, 250 + f1.size + 14), "TO LOAF", font=f2, fill=INK)
    d.text((24, 470), "INSIDE THE RISE", font=fit_font(d, "INSIDE THE RISE", 272, 40), fill=INK)
    # Panels 2-4: approved stills
    panels = [("SC01.png", 0.62), ("SC05.png", 0.5), ("SC12.png", 0.5)]
    for i, (name, focus) in enumerate(panels):
        still = Image.open(STILLS / name).convert("RGB")
        panel = crop_to(still, 320, H, focus)
        canvas.paste(panel, (320 * (i + 1), 0))
    # Dividers
    for x in (320, 640, 960):
        d.rectangle([x - 2, 0, x + 2, H], fill=DARK)
    footer(d)
    canvas.save(OUT1, "PNG")
    canvas.resize((120, 68), Image.LANCZOS).save(PREVIEW, "PNG")
    return OUT1


def alternate():
    still = Image.open(STILLS / "SC12.png").convert("RGB")
    canvas = crop_to(still, W, H, 0.5)
    d = ImageDraw.Draw(canvas)
    f = fit_font(d, "INSIDE THE DOUGH", 900, 84)
    d.text((40, 36), "INSIDE THE DOUGH", font=f, fill=(255, 246, 232),
           stroke_width=8, stroke_fill=INK)
    footer(d)
    canvas.save(OUT2, "PNG")
    return OUT2


for out in (concept1(), alternate()):
    print({"saved": str(out), "bytes": out.stat().st_size})
print({"preview120": str(PREVIEW)})
