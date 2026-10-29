#!/usr/bin/env python3
"""Verify that freshly downloaded generations are actually new.

WHY THIS EXISTS
---------------
`muse-image CLI --download` can return images the current prompt did not produce. It
appears to take the most recent images in the *project*, so a slow or failed
generation yields stale neighbours from earlier runs -- with plausible
filenames and no error.

Verified 2026-10-29: a run for one character returned four files of which NONE
were that character. Two were another character from an earlier run; one was an
unrelated two-shot.

At 04b a wrong character is obvious the moment you look. At 04f2 it is not: a
stale still lands in the wrong clip's slot, looks plausible, and renders. The
render app also binds stills to prompts by filename digit, so that handoff has
two independent silent-mismatch paths.

This catches the repeats. It cannot catch a fresh image of the wrong subject --
only your eyes can do that, so LOOK at the image before promoting it.

RUN
---
    python tools/check_download_freshness.py <gen-root> <new-folder>

<gen-root>    a directory whose subfolders hold all previous downloads
<new-folder>  the folder just downloaded into (may be inside gen-root)

Exit 0 = every file is new. Exit 1 = at least one is a repeat.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def images(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            yield p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="check_download_freshness.py")
    ap.add_argument("gen_root", type=Path)
    ap.add_argument("new_folder", type=Path)
    a = ap.parse_args(argv)

    if not a.new_folder.is_dir():
        print(f"not a directory: {a.new_folder}")
        return 1

    new_files = list(images(a.new_folder))
    if not new_files:
        print(f"no images in {a.new_folder} -- the generation produced nothing")
        return 1

    new_resolved = {p.resolve() for p in new_files}
    previous: dict[str, Path] = {}
    if a.gen_root.is_dir():
        for p in images(a.gen_root):
            if p.resolve() in new_resolved:
                continue
            previous.setdefault(sha256(p), p)

    stale = 0
    for p in new_files:
        h = sha256(p)
        if h in previous:
            stale += 1
            try:
                where = previous[h].relative_to(a.gen_root)
            except ValueError:
                where = previous[h]
            print(f"  STALE  {p.name}  == {where}")
        else:
            print(f"  fresh  {p.name}")

    print()
    if stale:
        print(f"{stale} of {len(new_files)} file(s) are REPEATS of earlier downloads.")
        print("The generation likely did not complete; re-run it into a clean folder.")
        return 1
    print(f"All {len(new_files)} file(s) are new. Now LOOK at them -- this check "
          "cannot tell a fresh image of the wrong subject.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
