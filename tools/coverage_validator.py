#!/usr/bin/env python3
"""Check an inside-the-process episode's explanation is complete (pipeline/process_coverage.md).

WHY THIS EXISTS
---------------
inside-the-process EP001 passed every stage and an independent script review while never
showing what glass is made of -- the premise had narrowed the question, the YouTube benchmark
saw the ingredients and steered away, and the writer's beat filter dropped an essential but
unsurprising step. No stage owned "what must a complete explanation contain?". That is now
`story/coverage-map.json`, approved by the owner at 01b, and this tool checks each later stage
against it. It is structural: it cannot judge whether an explanation is *good*, only that every
essential question is planned, researched, sourced and placed in the script, or explicitly
disclosed as out of scope.

RUN
---
    python tools/coverage_validator.py --channel inside-the-process --episode EPxxx \\
        --stage 01b-coverage-scan --emit-review

Stages (cumulative): 01b-coverage-scan, 02-research, 02a-sourcing, 03a-writer, 03b-script-review.
--emit-review writes story/coverage-review.json (the stage's completion gate reads it); at 01b it
also writes story/coverage-scope.lock.json, the owner-approved scope later stages may not narrow.

Exit 0 = PASS. Exit 1 = FAIL. Exit 2 = setup problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import clip_split_check  # noqa: E402
import youtube_benchmark_validator  # noqa: E402
from project_paths import ROOT  # noqa: E402

STAGES = ("01b-coverage-scan", "02-research", "02a-sourcing", "03a-writer", "03b-script-review")

# Must match pipeline/process_coverage.md (a test holds them together).
ARCHETYPES: dict[str, tuple[str, ...]] = {
    "manufactured_product": ("composition", "raw_materials", "preparation", "transformation",
                             "conditions", "quality_control", "product_in_use"),
    "biological_process": ("anatomy", "trigger", "sequence", "agents_and_signals", "regulation",
                           "outcome", "misconception"),
    "natural_phenomenon": ("ingredients", "energy_source", "sequence", "outcome",
                           "scale_and_frequency", "misconception"),
    "system_infrastructure": ("source", "stages", "distribution", "endpoint", "controls"),
    "other": (),
}
MIN_CUSTOM_DIMENSIONS = 4
MIN_PROCESS_CHAIN = 3
MIN_NAIVE_QUESTIONS = 5
BENCHMARK_IDS = ("B01", "B02", "B03")

MAP_REL = "story/coverage-map.json"
LOCK_REL = "story/coverage-scope.lock.json"
REVIEW_REL = "story/coverage-review.json"
ITEM_ID = re.compile(r"^COV\d{2,3}$")
CLAIM_ROW = re.compile(r"^\|\s*(CLM-\d+)\s*\|")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _norm(text: str) -> str:
    """Lower-case, curly quotes and dashes folded, punctuation and whitespace collapsed."""
    text = text.lower().replace("’", "'").replace("‘", "'").replace("—", " ").replace("–", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^\w' ]+", " ", text)).strip()


def _dimensions(cmap: dict) -> tuple[str, ...]:
    if cmap.get("archetype") == "other":
        return tuple(str(d.get("id")) for d in cmap.get("custom_dimensions") or [] if d.get("id"))
    return ARCHETYPES.get(cmap.get("archetype", ""), ())


def claim_statuses(sources_text: str) -> dict[str, str]:
    """{CLM-nn: status} from the claim ledger -- status is the row's last cell."""
    out = {}
    for line in sources_text.splitlines():
        m = CLAIM_ROW.match(line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out[m.group(1)] = cells[-1].upper()
    return out


def script_rows(script_text: str) -> dict[str, str]:
    """{row '#': that row's Claim IDs cell} from the scene/beat table."""
    rows: dict[str, str] = {}
    header: list[str] | None = None
    for line in script_text.splitlines():
        if not line.lstrip().startswith("|"):
            header = None  # a table ended; the next beat table needs its own header row
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if "#" in cells and any(c.lower() == "claim ids" for c in cells):
                header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue  # the |---|---| separator
        if len(cells) >= len(header):
            rows[cells[header.index("#")]] = cells[header.index("claim ids")]
    return rows


def scope_fingerprint(cmap: dict) -> dict:
    return {
        "archetype": cmap.get("archetype"),
        "items": {i["id"]: {"priority": i.get("priority"), "scope": i.get("scope")}
                  for i in cmap.get("items") or [] if isinstance(i, dict) and i.get("id")},
    }


def validate(ep: Path, stage: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    upto = STAGES.index(stage)
    if stage == "03b-script-review":
        upto = STAGES.index("03a-writer")

    map_path = ep / MAP_REL
    if not map_path.exists():
        return {"status": "FAIL", "errors": [f"{MAP_REL} is missing -- it is created at 01b-coverage-scan"],
                "warnings": [], "inputs": {}}
    try:
        cmap = json.loads(map_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "FAIL", "errors": [f"{MAP_REL} is not valid JSON ({exc})"],
                "warnings": [], "inputs": {}}
    inputs = {MAP_REL: _sha(map_path)}

    items = [i for i in cmap.get("items") or [] if isinstance(i, dict)]
    by_id = {i.get("id"): i for i in items}
    must_in = [i for i in items if i.get("priority") == "MUST" and i.get("scope") == "in"]

    # ── 01b: the plan itself ─────────────────────────────────────────────
    archetype = cmap.get("archetype")
    if archetype not in ARCHETYPES:
        errors.append(f"archetype {archetype!r} is not one of {', '.join(ARCHETYPES)}")
    dims = _dimensions(cmap)
    if archetype == "other" and len(dims) < MIN_CUSTOM_DIMENSIONS:
        errors.append(f"archetype 'other' needs at least {MIN_CUSTOM_DIMENSIONS} custom_dimensions")
    if len(cmap.get("process_chain") or []) < MIN_PROCESS_CHAIN:
        errors.append(f"process_chain needs at least {MIN_PROCESS_CHAIN} states, from the true raw/original "
                      f"starting substance to the finished result")
    scope = cmap.get("scope") or {}
    for key in ("starts_at", "ends_at"):
        if not str(scope.get(key, "")).strip():
            errors.append(f"scope.{key} is empty")

    seen_ids = set()
    for i in items:
        iid = i.get("id")
        if not ITEM_ID.match(str(iid)):
            errors.append(f"item id {iid!r} must look like COV01")
        if iid in seen_ids:
            errors.append(f"duplicate item id {iid}")
        seen_ids.add(iid)
        if i.get("priority") not in ("MUST", "OPTIONAL"):
            errors.append(f"{iid}: priority must be MUST or OPTIONAL")
        if i.get("scope") not in ("in", "out"):
            errors.append(f"{iid}: scope must be 'in' or 'out'")
        if dims and i.get("dimension") not in dims:
            errors.append(f"{iid}: dimension {i.get('dimension')!r} is not a {archetype} dimension")
        if not str(i.get("question", "")).strip():
            errors.append(f"{iid}: has no question")
        if i.get("priority") == "MUST" and i.get("scope") == "out":
            for key in ("reason", "disclosure"):
                if not str(i.get(key, "")).strip():
                    errors.append(f"{iid}: an out-of-scope MUST item needs a {key}")

    for dim in dims:
        if not any(i.get("dimension") == dim and i.get("priority") == "MUST" for i in items):
            errors.append(f"required dimension {dim!r} has no MUST item")

    naive = [q for q in cmap.get("naive_viewer_questions") or [] if isinstance(q, dict)]
    if len(naive) < MIN_NAIVE_QUESTIONS:
        errors.append(f"naive_viewer_questions needs at least {MIN_NAIVE_QUESTIONS}; found {len(naive)}")
    for q in naive:
        if q.get("item") not in by_id:
            errors.append(f"naive-viewer question {q.get('question', '?')!r} maps to unknown item {q.get('item')!r}")

    topics = [t for t in cmap.get("benchmark_topics") or [] if isinstance(t, dict)]
    contributed = set()
    for t in topics:
        seen = [s for s in t.get("seen_in") or [] if s in BENCHMARK_IDS]
        contributed.update(seen)
        target = by_id.get(t.get("item"))
        label = t.get("topic", "?")
        if not seen:
            errors.append(f"benchmark topic {label!r} lists no B01-B03 video in seen_in")
        if target is None:
            if str(t.get("not_used_reason", "")).strip() and len(seen) < 2:
                continue
            errors.append(f"benchmark topic {label!r} is not mapped to an item"
                          + (" -- it is covered by 2+ top videos, so viewers expect it answered"
                             if len(seen) >= 2 else " (or give a not_used_reason)"))
        elif len(seen) >= 2 and target.get("priority") != "MUST":
            errors.append(f"benchmark topic {label!r} is covered by {len(seen)} top videos but maps to "
                          f"OPTIONAL item {target.get('id')} -- make it MUST (in scope, or out of scope "
                          f"with a disclosure)")
    missing = [b for b in BENCHMARK_IDS if b not in contributed]
    if missing:
        errors.append(f"benchmark_topics has no topic from {', '.join(missing)} -- scan every benchmark video")

    bench = youtube_benchmark_validator.validate(ep)
    for e in bench.get("errors", []):
        errors.append(f"youtube-benchmark.md: {e.get('rule_id')}: {e.get('message')}")
    if (ep / "story/youtube-benchmark.md").exists():
        inputs["story/youtube-benchmark.md"] = _sha(ep / "story/youtube-benchmark.md")

    # ── scope lock: later stages may add items, never narrow the approved scope ──
    lock_path = ep / LOCK_REL
    if stage != "01b-coverage-scan":
        if not lock_path.exists():
            errors.append(f"{LOCK_REL} is missing -- 01b-coverage-scan must emit it")
        else:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            inputs[LOCK_REL] = _sha(lock_path)
            now = scope_fingerprint(cmap)
            if now["archetype"] != lock.get("archetype"):
                errors.append(f"archetype changed from {lock.get('archetype')!r} since 01b approval -- reopen 01b")
            for iid, was in (lock.get("items") or {}).items():
                cur = now["items"].get(iid)
                if cur is None:
                    errors.append(f"{iid} was removed after 01b approval -- reopen 01b")
                elif was.get("priority") == "MUST" and cur.get("priority") != "MUST":
                    errors.append(f"{iid} was demoted from MUST after 01b approval -- reopen 01b")
                elif was.get("scope") == "in" and cur.get("scope") == "out":
                    errors.append(f"{iid} was moved out of scope after 01b approval -- reopen 01b")

    # ── 02: research covers every in-scope MUST item ─────────────────────
    if upto >= STAGES.index("02-research"):
        notes = ep / "story/research-notes.md"
        if not notes.exists():
            errors.append("story/research-notes.md is missing")
        else:
            inputs["story/research-notes.md"] = _sha(notes)
            text = notes.read_text(encoding="utf-8")
            for i in must_in:
                if not re.search(rf"\b{re.escape(i['id'])}\b", text):
                    errors.append(f"{i['id']} ({i.get('question')}) is not cited in research-notes.md")

    # ── 02a: every in-scope MUST item rests on approved claims ──────────
    if upto >= STAGES.index("02a-sourcing"):
        sources = ep / "story/sources.md"
        if not sources.exists():
            errors.append("story/sources.md is missing")
        else:
            inputs["story/sources.md"] = _sha(sources)
            ledger = claim_statuses(sources.read_text(encoding="utf-8"))
            for i in must_in:
                ids = i.get("claim_ids") or []
                if not ids:
                    errors.append(f"{i['id']} ({i.get('question')}) has no claim_ids")
                for cid in ids:
                    status = ledger.get(cid)
                    if status is None:
                        errors.append(f"{i['id']}: {cid} is not a row of the claim ledger in sources.md")
                    elif not (status.startswith("SUPPORTED") or status.startswith("QUALIFIED")):
                        errors.append(f"{i['id']}: {cid} is {status}, not SUPPORTED/QUALIFIED")

    # ── 03a: every in-scope MUST item is on screen; every gap is disclosed ──
    if upto >= STAGES.index("03a-writer"):
        script = ep / "story/script.md"
        if not script.exists():
            errors.append("story/script.md is missing")
        else:
            inputs["story/script.md"] = _sha(script)
            text = script.read_text(encoding="utf-8")
            rows = script_rows(text)
            if not rows:
                errors.append("script.md has no scene/beat table with '#' and 'Claim IDs' columns")
            for i in must_in:
                refs = [str(r) for r in i.get("script_rows") or []]
                if not refs:
                    errors.append(f"{i['id']} ({i.get('question')}) has no script_rows -- it is not in the script")
                    continue
                unknown = [r for r in refs if r not in rows]
                if unknown:
                    errors.append(f"{i['id']}: script_rows {unknown} are not rows of the beat table")
                cited = [r for r in refs if r in rows and any(c in rows[r] for c in i.get("claim_ids") or [])]
                if not unknown and not cited:
                    errors.append(f"{i['id']}: none of its script_rows cites its claim IDs "
                                  f"{i.get('claim_ids')} -- the row does not explain what the item needs")
            body = _norm(text)
            for i in items:
                if i.get("priority") == "MUST" and i.get("scope") == "out":
                    if _norm(str(i.get("disclosure", ""))) not in body:
                        errors.append(f"{i['id']} is out of scope but its disclosure is not in script.md: "
                                      f"{i.get('disclosure')!r}")
            for i in items:
                if i.get("priority") == "OPTIONAL" and i.get("scope") == "in" and not i.get("script_rows"):
                    warnings.append(f"{i['id']} (OPTIONAL) is not placed in the script")
            # Every row's dialogue must divide into its clips at clean pauses with each clip
            # inside the channel's spoken-word band (tools/clip_split_check.py). Each clip's
            # audio is rendered separately; a mid-phrase boundary is heard as a broken line.
            chan_path = ep.parents[2] / "channel_profiles" / ep.parent.name / "channel.json"
            if chan_path.exists():
                band = json.loads(chan_path.read_text(encoding="utf-8")).get("render", {}).get("spoken_word_band")
                if band:
                    for res in clip_split_check.check_script(text, tuple(band)):
                        if not res["ok"]:
                            errors.append(f"script row {res['row']}: {res['detail']}")

    return {"status": "FAIL" if errors else "PASS", "errors": errors, "warnings": warnings,
            "inputs": inputs, "fingerprint": scope_fingerprint(cmap)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--channel", required=True)
    ap.add_argument("--episode", required=True)
    ap.add_argument("--stage", required=True, choices=STAGES)
    ap.add_argument("--emit-review", action="store_true")
    a = ap.parse_args(argv)
    ep = ROOT / "episodes" / a.channel / a.episode
    if not ep.is_dir():
        print(f"no episode folder: {ep}")
        return 2
    result = validate(ep, a.stage)
    print(f"coverage check ({a.stage}) -- {a.channel} / {a.episode}: {result['status']}")
    for e in result["errors"]:
        print(f"  ERROR  {e}")
    for w in result["warnings"]:
        print(f"  warn   {w}")
    if a.emit_review:
        review = {
            "schema_version": 1,
            "episode_id": a.episode,
            "stage": a.stage,
            "status": result["status"],
            "reviewed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "validator_sha256": _sha(Path(__file__).resolve()),
            "input_sha256": result["inputs"],
            "errors": result["errors"],
            "warnings": result["warnings"],
        }
        (ep / REVIEW_REL).write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {ep / REVIEW_REL}")
        if a.stage == "01b-coverage-scan" and result["status"] == "PASS":
            (ep / LOCK_REL).write_text(json.dumps(result["fingerprint"], indent=2) + "\n", encoding="utf-8")
            print(f"wrote {ep / LOCK_REL} (the scope the owner approves at 01b)")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
