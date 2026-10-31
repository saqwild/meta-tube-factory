"""Promote the CAST-002-anchored SC01 candidate to renders/stills/SC01.png.

Source candidate was generated with the CAST-002 sheet attached via
tools.meta_models.image_edit (see 2026-10-29-sc01-cast002-ref-edit-v3.py).
Resized to the episode still size 2016x1152, saved as true PNG.
Run from repo root.
"""
import pathlib

from PIL import Image

EP = pathlib.Path(__file__).resolve().parents[1]
SRC = EP / "qa" / "candidates" / "SC01-ref-v3.png"
DST = EP / "renders" / "stills" / "SC01.png"

img = Image.open(SRC).convert("RGB")
img = img.resize((2016, 1152), Image.LANCZOS)
img.save(DST, "PNG")
print({"promoted": str(DST), "size": img.size, "format": "PNG"})
