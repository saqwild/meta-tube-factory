"""Validate the mandatory pre-writer YouTube topic-market brief.

The validator is intentionally structural. It checks current-query provenance,
three opening-caption-backed market records, and a concise original market
brief. It never downloads videos, changes content, or judges competitor facts.

Ported from sibling-repo 2026-10-29. In this repo it runs at
01b-coverage-scan for inside-the-process only (moved from 03a-writer on
2026-10-29, see pipeline/youtube_benchmark.md), and again inside
tools/coverage_validator.py at every later stage.

The `## Coverage topic scan` section (added 2026-10-29) records how each
benchmark's full topic list was retrieved; the topics themselves live in
story/coverage-map.json -> benchmark_topics, where coverage_validator.py
checks that every one is mapped to an item.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = (
    "## Research snapshot",
    "## Ranking and selection",
    "## Top-three market scan",
    "## Coverage topic scan",
    "## Topic-market brief",
    "## Originality and evidence boundaries",
)

BENCHMARK_FIELDS = (
    "Source video URL",
    "Current view snapshot",
    "Duration",
    "Opening-caption sample status",
    "Opening evidence",
    "Opening behavior",
    "Format signal",
)

MARKET_BRIEF_FIELDS = (
    "Audience promise to meet",
    "Current format signal",
    "Explained From Within differentiation",
)


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    next_heading = text.find("\n## ", start + len(heading))
    return text[start:] if next_heading < 0 else text[start:next_heading]


def _benchmark_block(text: str, benchmark_id: str) -> str:
    header = re.search(rf"(?m)^### {benchmark_id}(?:\s|—|-)", text)
    if not header:
        return ""
    following = re.search(r"(?m)^### B0[1-3](?:\s|—|-)", text[header.end() :])
    end = len(text) if not following else header.end() + following.start()
    return text[header.start() : end]


def _has_field(text: str, label: str) -> bool:
    return bool(re.search(rf"(?mi)^-\s+{re.escape(label)}:\s*\S+", text))


def validate(episode_dir: Path) -> dict[str, Any]:
    path = episode_dir / "story" / "youtube-benchmark.md"
    errors: list[dict[str, str]] = []
    if not path.is_file():
        return {
            "status": "FAIL",
            "artifact": str(path),
            "errors": [{"rule_id": "YTB001", "message": "Missing story/youtube-benchmark.md."}],
        }

    text = path.read_text(encoding="utf-8")
    for heading in REQUIRED_SECTIONS:
        if heading not in text:
            errors.append({"rule_id": "YTB002", "message": f"Missing required section: {heading}"})

    research = _section(text, "## Research snapshot")
    query_count = len(re.findall(r"(?mi)^-\s+Query:\s*\S+", research))
    if not 4 <= query_count <= 6:
        errors.append(
            {
                "rule_id": "YTB003",
                "message": f"Research snapshot must record 4–6 query variants; found {query_count}.",
            }
        )

    selection = _section(text, "## Ranking and selection")
    for required in ("view", "direct", "caption", "exclu"):
        if required not in selection.lower():
            errors.append(
                {
                    "rule_id": "YTB004",
                    "message": "Ranking/selection must describe views, relevance, opening-caption eligibility and exclusions.",
                }
            )
            break

    benchmark_area = _section(text, "## Top-three market scan")
    for benchmark_id in ("B01", "B02", "B03"):
        block = _benchmark_block(benchmark_area, benchmark_id)
        if not block:
            errors.append({"rule_id": "YTB005", "message": f"Missing market-scan record for {benchmark_id}."})
            continue
        for field in BENCHMARK_FIELDS:
            if not _has_field(block, field):
                errors.append(
                    {"rule_id": "YTB006", "message": f"{benchmark_id} missing field: {field}."}
                )
        if not re.search(r"https://(?:www\.)?youtube\.com/", block):
            errors.append({"rule_id": "YTB007", "message": f"{benchmark_id} lacks a public YouTube URL."})
        sample = re.search(r"(?mi)^-\s+Opening-caption sample status:\s*(.+)$", block)
        if not sample or re.search(r"unavailable|missing|failed|none", sample.group(1), re.I):
            errors.append(
                {
                    "rule_id": "YTB008",
                    "message": f"{benchmark_id} must have a retrieved, usable opening-caption sample; unavailable captions belong in exclusions.",
                }
            )

    coverage = _section(text, "## Coverage topic scan")
    for benchmark_id in ("B01", "B02", "B03"):
        if coverage and not re.search(rf"(?mi)^-\s+{benchmark_id}\s+topic source:\s*\S+", coverage):
            errors.append(
                {
                    "rule_id": "YTB011",
                    "message": f"Coverage topic scan missing '- {benchmark_id} topic source:' "
                    "(chapters and/or full captions read, and retrieval date).",
                }
            )

    market_brief = _section(text, "## Topic-market brief")
    for field in MARKET_BRIEF_FIELDS:
        if not _has_field(market_brief, field):
            errors.append({"rule_id": "YTB009", "message": f"Topic-market brief missing field: {field}."})

    originality = _section(text, "## Originality and evidence boundaries").lower()
    if "must not copy" not in originality or "source ledger" not in originality:
        errors.append(
            {
                "rule_id": "YTB010",
                "message": "Originality/evidence section must prohibit copying and preserve the source-ledger boundary.",
            }
        )

    return {
        "status": "PASS" if not errors else "FAIL",
        "artifact": str(path),
        "query_count": query_count,
        "benchmark_count": len(re.findall(r"(?m)^### B0[1-3](?:\s|—|-)", benchmark_area)),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_dir", type=Path, help="Episode directory containing story/youtube-benchmark.md")
    args = parser.parse_args()
    report = validate(args.episode_dir)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
