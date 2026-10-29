#!/usr/bin/env python3
"""Verify a channel's locked reference sheets against what its cast cards claim.

WHY THIS EXISTS
---------------
Reference sheets get re-generated and replaced. When they do, the master cards
under `bible/characters/` silently keep pointing at the old filenames and the
old SHA-256 hashes, and nothing notices — until stage 04b conditions a
derivative on a path that no longer resolves, or worse, resolves to different
pixels than the card was approved against. That is the cast-drift failure this
whole reference-sheet system exists to prevent, arriving through the back door.

This is a deterministic check, not a judgement call: a path either resolves or
it does not, and a hash either matches or it does not.

Two lock conventions exist and both are checked:

  * `bible/characters/reference_sheets/` + a SHA-256 in each `CAST-*.md` card row
    (clover-and-paws).
  * `channel_profiles/<slug>/locked-references/characters/CAST-*/` holding
    `portrait` / `full-body` / `sheet` images + a `PROMOTION.md`, with the integrity
    check coming from the episodes that copied them: a `04b` `visual/references/
    manifest.md` row records the copy's SHA-256, and `PROMOTION.md` forbids silently
    overwriting the source -- so the locked file must still hash to what the episode
    recorded (signed-anyway).

RUN
---
    python tools/check_reference_assets.py --channel <slug>
    python tools/check_reference_assets.py            # every channel

Exit 0 = clean. Exit 1 = at least one missing file, hash mismatch, or orphan.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_paths import CHANNEL_PROFILES_DIR, EPISODES_DIR  # noqa: E402

# A row in a cast card's asset table: a backticked repo-relative path, then an
# optional SHA-256 declaration somewhere after it on the same line.
ASSET_ROW = re.compile(
    r"`(characters/reference_sheets/[^`]+)`(?P<rest>[^\n|]*(?:\|[^\n]*)?)")
SHA_TOKEN = re.compile(r"SHA-256\s*`([0-9a-f]{64})`", re.IGNORECASE)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# locked-references/ convention (channel-level identity locks, e.g. signed-anyway).
CAST_DIR = re.compile(r"^CAST-\d{2,3}$")
CAST_ID_IN_LINE = re.compile(r"CAST-\d{2,3}")
BARE_SHA = re.compile(r"\b([0-9a-f]{64})\b")
LOCKED_REF_IN_LINE = re.compile(r"locked-references/characters/(CAST-\d{2,3})/([A-Za-z0-9._-]+)")
LOCKED_ROLE_STEMS = ("portrait", "full-body", "full_body", "sheet")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_channel(slug: str) -> tuple[list[str], list[str]]:
    """Return (problems, notes) for one channel."""
    problems: list[str] = []
    notes: list[str] = []
    bible = CHANNEL_PROFILES_DIR / slug / "bible"
    cards_dir = bible / "characters"
    sheets_dir = cards_dir / "reference_sheets"

    claimed: set[Path] = set()
    if not cards_dir.exists():
        notes.append(f"{slug}: no bible/characters/ - skipping the reference-sheet convention")
        cards_dir = None  # type: ignore[assignment]

    for card in sorted(cards_dir.glob("CAST-*.md")) if cards_dir else []:
        text = card.read_text(encoding="utf-8")
        for line in text.splitlines():
            # Provenance prose cites other repos' paths; only table rows are claims.
            if not line.lstrip().startswith("|"):
                continue
            for match in ASSET_ROW.finditer(line):
                rel = match.group(1)
                target = bible / rel
                claimed.add(target.resolve())
                if not target.exists():
                    problems.append(
                        f"{slug}/{card.name}: references {rel} -- FILE DOES NOT EXIST")
                    continue
                declared = SHA_TOKEN.search(line)
                if not declared:
                    notes.append(f"{slug}/{card.name}: {target.name} has no declared SHA-256")
                    continue
                actual = sha256(target)
                if actual != declared.group(1).lower():
                    problems.append(
                        f"{slug}/{card.name}: {target.name} HASH MISMATCH\n"
                        f"    card says {declared.group(1)}\n"
                        f"    file  is  {actual}")

    if sheets_dir.exists():
        on_disk = {p.resolve() for p in sheets_dir.iterdir()
                   if p.is_file() and p.suffix.lower() in IMAGE_EXTS}
        for orphan in sorted(on_disk - claimed):
            problems.append(
                f"{slug}: {orphan.name} is on disk but no cast card claims it - "
                "either wire it into a card or remove it")
    elif claimed:
        problems.append(f"{slug}: cast cards claim reference sheets but the folder is missing")

    # Second convention: channel-level locked-references/.
    locked_problems, locked_notes, locked_verified = check_locked_references(slug)
    problems.extend(locked_problems)
    notes.extend(locked_notes)

    if not claimed and not locked_verified and not locked_problems:
        # Neither convention has anything to verify yet -- a legitimate pre-04b state.
        notes.append(f"{slug}: no locked reference images yet - 04b generates and promotes them")
    elif not problems:
        total = len(claimed) + locked_verified
        notes.append(f"{slug}: {total} reference image(s) verified, all paths and hashes match")
    return problems, notes


def check_locked_references(slug: str) -> tuple[list[str], list[str], int]:
    """Check `channel_profiles/<slug>/locked-references/` if it exists.

    Returns (problems, notes, verified_count). The integrity check on each locked
    file is the SHA-256 an episode's `04b` manifest recorded when it copied that
    file verbatim -- PROMOTION.md forbids silently overwriting the source, so the
    locked file must still hash to what the episode recorded.
    """
    problems: list[str] = []
    notes: list[str] = []
    root = CHANNEL_PROFILES_DIR / slug / "locked-references"
    chars = root / "characters"
    if not chars.is_dir():
        return problems, notes, 0

    on_disk_dirs = {d.name for d in chars.iterdir() if d.is_dir() and CAST_DIR.match(d.name)}

    # 1. Each CAST dir is structurally complete.
    for cast in sorted(on_disk_dirs):
        d = chars / cast
        have = {p.name.lower() for p in d.iterdir() if p.is_file()}
        for stem in ("portrait", "sheet"):
            if not any(n.startswith(stem + ".") and n.rsplit(".", 1)[-1] in
                       {e[1:] for e in IMAGE_EXTS} for n in have):
                problems.append(f"{slug}: locked-references/{cast}/ has no {stem} image")
        if not any(n.startswith(("full-body.", "full_body.")) for n in have):
            problems.append(f"{slug}: locked-references/{cast}/ has no full-body image")
        if "promotion.md" not in have:
            problems.append(f"{slug}: locked-references/{cast}/ has no PROMOTION.md")

    # 2. README Contents table lists exactly the CAST dirs on disk.
    readme = root / "README.md"
    if not readme.exists():
        problems.append(f"{slug}: locked-references/ has no README.md")
    else:
        documented = {
            m.group(0)
            for line in readme.read_text(encoding="utf-8").splitlines()
            if line.lstrip().startswith("|")
            for m in [CAST_ID_IN_LINE.search(line)] if m
        }
        for cast in sorted(documented - on_disk_dirs):
            problems.append(f"{slug}: locked-references/README.md documents {cast} but the folder is absent")
        for cast in sorted(on_disk_dirs - documented):
            problems.append(f"{slug}: locked-references/{cast}/ exists but README.md's table does not list it")

    # 3. Cross-check against the episodes that copied these files.
    verified = 0
    ep_root = EPISODES_DIR / slug
    manifests = sorted(ep_root.glob("*/visual/references/**/manifest.md")) if ep_root.is_dir() else []
    seen: set[tuple[str, str]] = set()
    for manifest in manifests:
        for line in manifest.read_text(encoding="utf-8").splitlines():
            ref = LOCKED_REF_IN_LINE.search(line)
            sha = BARE_SHA.search(line)
            if not ref or not sha:
                continue
            cast, fname = ref.group(1), ref.group(2)
            key = (cast, fname)
            locked_file = chars / cast / fname
            if not locked_file.exists():
                # tolerate an extension difference (sheet.jpg recorded, sheet.jpeg on disk)
                stem = fname.rsplit(".", 1)[0]
                cands = list((chars / cast).glob(stem + ".*")) if (chars / cast).is_dir() else []
                locked_file = cands[0] if len(cands) == 1 else locked_file
            if not locked_file.exists():
                problems.append(
                    f"{slug}: {manifest.relative_to(EPISODES_DIR)} copied "
                    f"locked-references/{cast}/{fname} -- that file is now MISSING")
                continue
            actual = sha256(locked_file)
            if actual != sha.group(1).lower():
                problems.append(
                    f"{slug}: locked-references/{cast}/{locked_file.name} HASH MISMATCH\n"
                    f"    {manifest.relative_to(EPISODES_DIR)} recorded {sha.group(1)}\n"
                    f"    file is now              {actual}\n"
                    f"    PROMOTION.md forbids silently overwriting a locked reference")
            elif key not in seen:
                verified += 1
                seen.add(key)

    if on_disk_dirs and verified == 0 and not problems:
        notes.append(
            f"{slug}: {len(on_disk_dirs)} locked-reference dir(s) present but no episode "
            f"manifest records a hash to check them against yet")
    return problems, notes, verified


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="check_reference_assets.py")
    ap.add_argument("--channel", help="slug; omit to check every channel")
    a = ap.parse_args(argv)

    slugs = [a.channel] if a.channel else sorted(
        p.name for p in CHANNEL_PROFILES_DIR.iterdir()
        if p.is_dir() and (p / "channel.json").exists())

    all_problems: list[str] = []
    for slug in slugs:
        problems, notes = check_channel(slug)
        for n in notes:
            print(f"  {n}")
        all_problems.extend(problems)

    if all_problems:
        print("\nPROBLEMS:")
        for p in all_problems:
            print(f"  FAIL {p}")
        print(f"\n{len(all_problems)} problem(s). Locked references and their claims disagree.")
        return 1
    print("\nOK - every locked reference exists and matches its declared hash.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
