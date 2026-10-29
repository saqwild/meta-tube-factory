from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from youtube_benchmark_validator import validate


def valid_benchmark() -> str:
    market_records: list[str] = []
    for benchmark_id in ("B01", "B02", "B03"):
        market_records.append(
            f"""### {benchmark_id} — Example

- Source video URL: https://www.youtube.com/watch?v={benchmark_id}
- Current view snapshot: 100,000 at 2026-10-29T00:00:00Z
- Duration: 05:00
- Opening-caption sample status: Retrieved English captions through 01:00
- Opening evidence: paraphrase at 00:00
- Opening behavior: outcome appears first
- Format signal: concise question then a stepwise explanation
"""
        )
    return """# Benchmark

## Research snapshot

- Query: first topic query
- Query: second topic query
- Query: third topic query
- Query: fourth topic query

## Ranking and selection

Candidates were ranked by visible view count, direct relevance, and opening-caption eligibility. Higher-view exclusions record missing captions.

## Top-three market scan

""" + "\n".join(market_records) + """
## Coverage topic scan

- B01 topic source: uploader chapters + full English captions, read 2026-10-29
- B02 topic source: full English auto-captions, read 2026-10-29
- B03 topic source: uploader chapters only (no captions past 01:00), read 2026-10-29

Topics are recorded in story/coverage-map.json -> benchmark_topics.

## Topic-market brief

- Audience promise to meet: explain the familiar transformation clearly
- Current format signal: concise question followed by process stages
- Explained From Within differentiation: a conceptual inside-view causal journey

## Originality and evidence boundaries

The writer must not copy wording, titles, visuals, or sequence from benchmarks. The approved source ledger remains the only factual authority.
"""


class YouTubeBenchmarkValidatorTests(unittest.TestCase):
    def write_artifact(self, text: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        story = Path(temp.name) / "story"
        story.mkdir()
        (story / "youtube-benchmark.md").write_text(text, encoding="utf-8")
        return Path(temp.name)

    def test_valid_benchmark_passes(self) -> None:
        report = validate(self.write_artifact(valid_benchmark()))
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["query_count"], 4)
        self.assertEqual(report["benchmark_count"], 3)

    def test_missing_market_scan_field_fails(self) -> None:
        text = valid_benchmark().replace("- Format signal: concise question then a stepwise explanation\n", "", 1)
        report = validate(self.write_artifact(text))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(error["rule_id"] == "YTB006" for error in report["errors"]))

    def test_unavailable_transcript_fails(self) -> None:
        text = valid_benchmark().replace(
            "- Opening-caption sample status: Retrieved English captions through 01:00",
            "- Opening-caption sample status: unavailable",
            1,
        )
        report = validate(self.write_artifact(text))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(error["rule_id"] == "YTB008" for error in report["errors"]))

    def test_missing_coverage_topic_scan_fails(self) -> None:
        """inside-the-process EP001's benchmark read only each video's first 60-90 s, so the
        topics the videos covered (ingredients, inspection) never reached the plan."""
        start = valid_benchmark().index("## Coverage topic scan")
        end = valid_benchmark().index("## Topic-market brief")
        report = validate(self.write_artifact(valid_benchmark()[:start] + valid_benchmark()[end:]))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Coverage topic scan" in e["message"] for e in report["errors"]))

    def test_coverage_scan_needs_every_benchmark_source(self) -> None:
        text = valid_benchmark().replace("- B02 topic source: full English auto-captions, read 2026-10-29\n", "")
        report = validate(self.write_artifact(text))
        self.assertTrue(any(error["rule_id"] == "YTB011" for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
