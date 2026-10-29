#!/usr/bin/env python3
"""Check that every script row's dialogue can be split into its clips at clean pauses.

WHY THIS EXISTS
---------------
Each 20-second clip is rendered separately, with its own audio. A spoken line that runs
across a clip boundary is heard as two separate deliveries, so a boundary must fall where a
speaker would naturally pause. inside-the-process EP001's script passed review with every
ROW inside the channel's per-clip word band on average, yet in 7 of its 15 rows every split
that kept each clip in band cut a phrase in half ("a pair ‖ of blades", "find a weak ‖ point
later"). Nothing checked it until 04f, three stages and one independent review later.

WHAT IT CHECKS
--------------
For each beat-table row of story/script.md: the row's clip count (from the Duration cell,
"40s (2 clips)"), its spoken lines (every column whose header ends in " words", in table
order), and the channel's render.spoken_word_band. It searches every way to place the row's
clip boundaries at CLEAN pauses only -- a speaker change, a sentence end (. ? !), a colon or
semicolon, a dash, or a comma -- and passes the row if at least one placement keeps every clip
inside the band. Words are counted with tools/ltx_prompt_validator.py's own tokenizer, the
same count LTXV-D034 enforces at 04f3.

RUN
---
    python tools/clip_split_check.py --channel inside-the-process --episode EP001

Exit 0 = every row splits cleanly. Exit 1 = at least one row does not (each is listed with
the reason). Exit 2 = setup problem. Also used by tools/coverage_validator.py at 03a.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ltx_prompt_validator as validator  # noqa: E402
from project_paths import ROOT  # noqa: E402

CLIPS = re.compile(r"\((\d+)\s+clips?\)")
MAX_COMBOS = 200_000


def table_rows(script_text: str):
    """Yield {header: cell} for each row of the beat table(s) that have '#' and 'Duration'."""
    header = None
    for line in script_text.splitlines():
        if not line.lstrip().startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if "#" in cells and "Duration" in cells:
                header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if len(cells) >= len(header):
            yield dict(zip(header, cells))


def dialogue_tokens(row: dict, speaker_columns: list[str]) -> list[tuple[str, str]]:
    toks = []
    for col in speaker_columns:
        cell = row.get(col, "").strip()
        if cell in ("", "—", "-"):
            continue
        if cell.startswith('"') and cell.endswith('"'):
            cell = cell[1:-1]
        toks += [(col, t) for t in cell.split()]
    return toks


def pause_strength(toks: list[tuple[str, str]], i: int) -> int:
    """How strong a pause follows token i: 3 speaker change / sentence end, 2 colon, semicolon
    or dash, 1 comma, 0 none (mid-phrase)."""
    spk, t = toks[i]
    nspk, nt = toks[i + 1]
    t = t.rstrip('"”')
    if nspk != spk or re.search(r"[.?!]$", t):
        return 3
    if re.search(r"[:;—]$", t) or nt == "—" or t == "—":
        return 2
    if t.endswith(","):
        return 1
    return 0


def clean_breaks(toks: list[tuple[str, str]]) -> list[int]:
    """Indices i where a clip may end after token i."""
    return [i for i in range(len(toks) - 1) if pause_strength(toks, i)]


def best_split(toks, n_clips: int, lo: int, hi: int):
    """The in-band clean split with the strongest weakest boundary (ties: strongest total).
    Returns (boundary token indices, per-clip word counts), or None if no clean split exists."""
    if n_clips == 1:
        total = count([t for _, t in toks])
        return ([], [total]) if lo <= total <= hi else None
    best, best_key = None, None
    for k, combo in enumerate(itertools.combinations(clean_breaks(toks), n_clips - 1)):
        if k > MAX_COMBOS:
            break
        bounds = [-1, *combo, len(toks) - 1]
        counts = [count([t for _, t in toks[bounds[j] + 1: bounds[j + 1] + 1]]) for j in range(n_clips)]
        if all(lo <= c <= hi for c in counts):
            strengths = [pause_strength(toks, b) for b in combo]
            key = (min(strengths), sum(strengths))
            if best_key is None or key > best_key:
                best, best_key = (list(combo), counts), key
    return best


def count(words: list[str]) -> int:
    # The validator's own word tokenizer (what LTXV-D034 counts inside each quoted line).
    # Not spoken_words('"…"'): its QUOTED pattern caps a quote at 600 characters, so a whole
    # long row would silently count as 0.
    return len(validator.WORD.findall(" ".join(words)))


def check_row(toks, n_clips: int, lo: int, hi: int):
    """Return (ok, detail). detail is the first clean split found, or the reason it failed."""
    total = count([t for _, t in toks])
    if n_clips <= 0:
        return False, "no clip count in the Duration cell"
    if not (lo * n_clips <= total <= hi * n_clips):
        return False, f"{total} words cannot fit {n_clips} clip(s) at {lo}-{hi} each"
    found = best_split(toks, n_clips, lo, hi)
    if found:
        combo, counts = found
        weak = [" ".join(t for _, t in toks[max(0, b - 2): b + 1]) for b in combo
                if pause_strength(toks, b) < 3]
        return True, counts if not weak else f"{counts} (comma/dash break after: {'; '.join(weak)})"
    return False, (f"{total} words over {n_clips} clips: no placement of clip boundaries at clean pauses "
                   f"(speaker change, sentence end, colon/semicolon, dash, comma) keeps every clip inside "
                   f"{lo}-{hi}; restructure the row's sentences so a pause falls near each boundary")


def check_script(script_text: str, band: tuple[int, int]) -> list[dict]:
    results = []
    for row in table_rows(script_text):
        m = CLIPS.search(row.get("Duration", ""))
        n = int(m.group(1)) if m else 0
        cols = [h for h in row if h.lower().endswith(" words")]
        toks = dialogue_tokens(row, cols)
        if not toks:
            results.append({"row": row.get("#"), "ok": True, "detail": "no dialogue"})
            continue
        ok, detail = check_row(toks, n, *band)
        results.append({"row": row.get("#"), "ok": ok, "detail": detail})
    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    a = ap.parse_args(argv)
    chan = ROOT / "channel_profiles" / a.channel / "channel.json"
    script = ROOT / "episodes" / a.channel / a.episode / "story" / "script.md"
    if not chan.exists() or not script.exists():
        print(f"not found: {chan if not chan.exists() else script}")
        return 2
    band = json.loads(chan.read_text(encoding="utf-8")).get("render", {}).get("spoken_word_band")
    if not band:
        print("channel declares no render.spoken_word_band -- nothing to check")
        return 0
    results = check_script(script.read_text(encoding="utf-8"), tuple(band))
    bad = [r for r in results if not r["ok"]]
    for r in results:
        print(f"  row {r['row']:>3}  {'OK ' if r['ok'] else 'FAIL'}  {r['detail']}")
    print(f"clip split check -- {a.channel} / {a.episode}: {'PASS' if not bad else 'FAIL'} "
          f"({len(results) - len(bad)}/{len(results)} rows split cleanly)")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
