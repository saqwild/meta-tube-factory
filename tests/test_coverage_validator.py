"""Tests for tools/coverage_validator.py and the coverage gates (pipeline/process_coverage.md).

Each test builds a small, valid inside-the-process episode -- a glass-bottle coverage map,
research notes, a claim ledger and a beat table shaped like EP001's real files -- then breaks
one thing.
"""
import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))

import coverage_validator as cv  # noqa: E402
import episode_state as es  # noqa: E402
from test_youtube_benchmark_validator import valid_benchmark  # noqa: E402

DIMS = cv.ARCHETYPES["manufactured_product"]

MAP = {
    "schema_version": 1, "episode_id": "EP002", "topic": "how a glass bottle is made",
    "archetype": "manufactured_product",
    "process_chain": ["sand, soda ash, limestone", "batch", "melt", "gob", "bottle", "bottle in use"],
    "scope": {"starts_at": "raw materials at the plant", "ends_at": "an inspected bottle"},
    "items": [
        {"id": f"COV{n:02d}", "dimension": d, "priority": "MUST", "scope": "in",
         "question": f"question about {d}?", "claim_ids": [f"CLM-{n:02d}"], "script_rows": [str(n)]}
        for n, d in enumerate(DIMS, 1)
    ] + [
        {"id": "COV08", "dimension": "raw_materials", "priority": "MUST", "scope": "out",
         "question": "Where is the sand mined?", "reason": "quarrying is its own process",
         "disclosure": "The sand itself was mined long before it reached this plant."},
    ],
    "benchmark_topics": [
        {"topic": "ingredients", "seen_in": ["B01", "B02"], "item": "COV02"},
        {"topic": "annealing", "seen_in": ["B02", "B03"], "item": "COV06"},
        {"topic": "sustainability pitch", "seen_in": ["B03"], "not_used_reason": "marketing aside"},
    ],
    "naive_viewer_questions": [
        {"question": q, "item": f"COV0{n}"} for n, q in enumerate(
            ["what is it made of", "where from", "how mixed", "how shaped", "how hot"], 1)
    ],
}

RESEARCH = "# research\n\n" + "\n".join(f"- COV{n:02d}: finding" for n in range(1, 8)) + "\n"
SOURCES = ("## Claim ledger\n\n| Claim ID | Exact bounded claim | URL | Supports | Limits | Status |\n"
           "|---|---|---|---|---|---|\n"
           + "".join(f"| CLM-{n:02d} | claim {n} | https://x | y | z | SUPPORTED |\n" for n in range(1, 8)))


def script(rows=range(1, 8), extra_words=""):
    head = ("| # | Time | Story question | Claim IDs | Control words |\n"
            "|---|---|---|---|---|\n")
    body = "".join(f"| {n} | 0:{n:02d} | q{n} | CLM-{n:02d} | words |\n" for n in rows)
    return ("# script\n\n## Scene / beat table\n\n" + head + body +
            "\nControl says: “The sand itself — was mined long before it reached this plant.”\n"
            + extra_words)


class Base(unittest.TestCase):
    def setUp(self):
        self.ep = Path(tempfile.mkdtemp(prefix="vidgen_ltx_cov_"))
        (self.ep / "story").mkdir()
        self.map = copy.deepcopy(MAP)
        self.write_map()
        self.put("story/youtube-benchmark.md", valid_benchmark())
        self.put("story/research-notes.md", RESEARCH)
        self.put("story/sources.md", SOURCES)
        self.put("story/script.md", script())

    def tearDown(self):
        shutil.rmtree(self.ep, ignore_errors=True)

    def put(self, rel, text):
        (self.ep / rel).write_text(text, encoding="utf-8")

    def write_map(self):
        self.put(cv.MAP_REL, json.dumps(self.map, indent=2))

    def lock(self):
        result = cv.validate(self.ep, "01b-coverage-scan")
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.put(cv.LOCK_REL, json.dumps(result["fingerprint"]))

    def errors(self, stage):
        return cv.validate(self.ep, stage)["errors"]

    def item(self, iid):
        return next(i for i in self.map["items"] if i["id"] == iid)


class Plan01b(Base):
    def test_valid_map_passes_every_stage(self):
        self.lock()
        for stage in cv.STAGES[1:]:
            self.assertEqual(self.errors(stage), [], stage)

    def test_a_required_dimension_without_a_must_item_fails(self):
        self.item("COV01")["priority"] = "OPTIONAL"   # composition
        self.write_map()
        self.assertTrue(any("'composition' has no MUST item" in e for e in self.errors("01b-coverage-scan")))

    def test_topic_seen_in_two_benchmarks_cannot_be_optional(self):
        """EP001: every top video covered ingredients; the brief treated it as optional."""
        self.item("COV02")["priority"] = "OPTIONAL"
        self.map["items"].append({"id": "COV09", "dimension": "raw_materials", "priority": "MUST",
                                  "scope": "in", "question": "keep the dimension", "claim_ids": ["CLM-02"],
                                  "script_rows": ["2"]})
        self.write_map()
        self.assertTrue(any("'ingredients' is covered by 2 top videos" in e
                            for e in self.errors("01b-coverage-scan")))

    def test_unmapped_benchmark_topic_fails(self):
        self.map["benchmark_topics"].append({"topic": "inspection", "seen_in": ["B02", "B03"]})
        self.write_map()
        self.assertTrue(any("'inspection' is not mapped" in e for e in self.errors("01b-coverage-scan")))

    def test_every_benchmark_must_contribute_topics(self):
        self.map["benchmark_topics"] = [t for t in self.map["benchmark_topics"] if "B03" not in t["seen_in"]]
        self.write_map()
        self.assertTrue(any("no topic from B03" in e for e in self.errors("01b-coverage-scan")))

    def test_needs_five_naive_viewer_questions(self):
        self.map["naive_viewer_questions"] = self.map["naive_viewer_questions"][:4]
        self.write_map()
        self.assertTrue(any("at least 5" in e for e in self.errors("01b-coverage-scan")))

    def test_out_of_scope_must_needs_a_disclosure(self):
        del self.item("COV08")["disclosure"]
        self.write_map()
        self.assertTrue(any("COV08: an out-of-scope MUST item needs a disclosure" in e
                            for e in self.errors("01b-coverage-scan")))

    def test_short_process_chain_fails(self):
        self.map["process_chain"] = ["molten glass", "bottle"]
        self.write_map()
        self.assertTrue(any("process_chain" in e for e in self.errors("01b-coverage-scan")))

    def test_invalid_benchmark_fails_the_scan(self):
        self.put("story/youtube-benchmark.md", valid_benchmark().replace("## Coverage topic scan", "## Notes"))
        self.assertTrue(any("youtube-benchmark.md" in e for e in self.errors("01b-coverage-scan")))

    def test_other_archetype_needs_custom_dimensions(self):
        self.map["archetype"] = "other"
        self.map["custom_dimensions"] = [{"id": "alpha", "question": "?"}]
        self.write_map()
        self.assertTrue(any("custom_dimensions" in e for e in self.errors("01b-coverage-scan")))


class ScopeLock(Base):
    def test_demoting_a_locked_must_item_fails(self):
        self.lock()
        self.item("COV03")["priority"] = "OPTIONAL"
        self.map["items"].append(dict(self.item("COV03"), id="COV10", priority="MUST"))
        self.write_map()
        self.assertTrue(any("COV03 was demoted" in e for e in self.errors("02-research")))

    def test_scoping_out_a_locked_item_fails(self):
        """The cheap way to make a failing script pass -- blocked without reopening 01b."""
        self.lock()
        self.item("COV01").update(scope="out", reason="no time", disclosure="words")
        self.write_map()
        self.assertTrue(any("COV01 was moved out of scope" in e for e in self.errors("03a-writer")))

    def test_adding_an_item_after_approval_is_fine(self):
        self.lock()
        self.map["items"].append({"id": "COV20", "dimension": "conditions", "priority": "OPTIONAL",
                                  "scope": "in", "question": "extra?"})
        self.write_map()
        self.assertEqual(self.errors("02a-sourcing"), [])

    def test_later_stage_needs_the_lock(self):
        self.assertTrue(any(cv.LOCK_REL in e for e in self.errors("02-research")))


class LaterStages(Base):
    def setUp(self):
        super().setUp()
        self.lock()

    def test_research_must_cite_every_in_scope_must_item(self):
        self.put("story/research-notes.md", RESEARCH.replace("- COV04: finding\n", ""))
        self.assertTrue(any("COV04" in e and "research-notes" in e for e in self.errors("02-research")))

    def test_claim_must_be_supported_or_qualified(self):
        self.put("story/sources.md", SOURCES.replace("claim 5 | https://x | y | z | SUPPORTED",
                                                     "claim 5 | https://x | y | z | UNRESOLVED"))
        self.assertTrue(any("CLM-05 is UNRESOLVED" in e for e in self.errors("02a-sourcing")))

    def test_item_without_claims_fails_at_02a(self):
        self.item("COV06")["claim_ids"] = []
        self.write_map()
        self.lock()
        self.assertTrue(any("COV06" in e and "no claim_ids" in e for e in self.errors("02a-sourcing")))

    def test_the_ep001_failure_raw_materials_never_on_screen(self):
        """The script ships without the raw-materials beat: COV02 names a row that is gone."""
        self.put("story/script.md", script(rows=[1, 3, 4, 5, 6, 7]))
        errs = self.errors("03a-writer")
        self.assertTrue(any("COV02: script_rows ['2'] are not rows" in e for e in errs), errs)

    def test_script_row_must_carry_the_items_claim(self):
        self.put("story/script.md", script().replace("| 4 | 0:04 | q4 | CLM-04 |", "| 4 | 0:04 | q4 | — |"))
        self.assertTrue(any("COV04: none of its script_rows cites" in e for e in self.errors("03a-writer")))

    def test_out_of_scope_disclosure_must_be_in_the_script(self):
        self.put("story/script.md", script().replace("The sand itself", "The glass"))
        self.assertTrue(any("COV08 is out of scope but its disclosure" in e for e in self.errors("03a-writer")))

    def test_03b_rechecks_the_03a_rules(self):
        self.put("story/script.md", script(rows=[1, 3, 4, 5, 6, 7]))
        self.assertTrue(self.errors("03b-script-review"))


class ClipSplitAt03a(Base):
    """03a runs tools/clip_split_check.py against the channel's spoken-word band (EP001 revision 10)."""

    def setUp(self):
        super().setUp()
        self.lock()
        root = Path(tempfile.mkdtemp(prefix="vidgen_ltx_covclip_"))
        self.addCleanup(shutil.rmtree, root, True)
        chan = root / "channel_profiles" / "inside-the-process"
        chan.mkdir(parents=True)
        (chan / "channel.json").write_text(json.dumps({"render": {"spoken_word_band": [32, 36]}}), encoding="utf-8")
        self.ep = Path(shutil.copytree(self.ep, root / "episodes" / "inside-the-process" / "EP002"))

    def with_row_one(self, dialogue):
        # Row 1 becomes a 2-clip row carrying the given dialogue; every other row stays silent.
        text = script().replace("| # | Time | Story question | Claim IDs | Control words |\n|---|---|---|---|---|",
                                "| # | Time | Duration | Story question | Claim IDs | Control words |\n|---|---|---|---|---|---|")
        text = text.replace("| 1 | 0:01 | q1 | CLM-01 | words |", f'| 1 | 0:01 | 40s (2 clips) | q1 | CLM-01 | "{dialogue}" |')
        for n in range(2, 8):
            text = text.replace(f"| {n} | 0:{n:02d} | q{n} | CLM-{n:02d} | words |",
                                f"| {n} | 0:{n:02d} | 20s (1 clip) | q{n} | CLM-{n:02d} | — |")
        self.put("story/script.md", text)

    def test_row_that_cannot_be_cut_at_a_pause_fails_03a(self):
        self.with_row_one(" ".join(f"w{i}" for i in range(20)) + ". " + " ".join(f"v{i}" for i in range(48)) + ".")
        self.assertTrue(any(e.startswith("script row 1:") and "restructure" in e for e in self.errors("03a-writer")))

    def test_row_cut_at_a_sentence_end_passes_03a(self):
        self.with_row_one(" ".join(f"w{i}" for i in range(34)) + ". " + " ".join(f"v{i}" for i in range(34)) + ".")
        self.assertEqual(self.errors("03a-writer"), [])


class EmitReview(Base):
    def test_01b_writes_review_bound_to_its_inputs_and_the_scope_lock(self):
        ep_root = Path(tempfile.mkdtemp(prefix="vidgen_ltx_covroot_"))
        self.addCleanup(shutil.rmtree, ep_root, True)
        target = ep_root / "episodes" / "inside-the-process" / "EP002"
        shutil.copytree(self.ep, target)
        real_root = cv.ROOT
        cv.ROOT = ep_root
        try:
            code = cv.main(["--channel", "inside-the-process", "--episode", "EP002",
                            "--stage", "01b-coverage-scan", "--emit-review"])
        finally:
            cv.ROOT = real_root
        self.assertEqual(code, 0)
        review = json.loads((target / cv.REVIEW_REL).read_text(encoding="utf-8"))
        self.assertEqual((review["status"], review["stage"]), ("PASS", "01b-coverage-scan"))
        self.assertEqual(review["input_sha256"][cv.MAP_REL],
                         hashlib.sha256((target / cv.MAP_REL).read_bytes()).hexdigest())
        self.assertTrue((target / cv.LOCK_REL).exists())


class ContractAgreement(unittest.TestCase):
    def test_every_archetype_dimension_is_documented(self):
        doc = (ROOT / "pipeline" / "process_coverage.md").read_text(encoding="utf-8")
        for archetype, dims in cv.ARCHETYPES.items():
            self.assertIn(f"`{archetype}`", doc)
            for d in dims:
                self.assertRegex(doc, rf"`{re.escape(d)}`", f"{archetype}.{d} missing from process_coverage.md")


class CoverageGates(unittest.TestCase):
    """The when_stage mechanism in stage-gates.json + episode_state.stage_spec."""

    def setUp(self):
        self.gates = es._load_stage_gates()

    def test_coverage_verdict_applies_only_to_episodes_that_ran_01b(self):
        with_01b = es.stage_spec(self.gates, "03a-writer", ["01-ideation", "01b-coverage-scan", "03a-writer"])
        without = es.stage_spec(self.gates, "03a-writer", ["01-ideation", "03a-writer"])
        self.assertTrue(any(v["file"] == cv.REVIEW_REL for v in with_01b["verdicts"]))
        self.assertEqual(without["verdicts"], [])

    def test_03b_keeps_its_own_verdict_and_adds_coverage(self):
        spec = es.stage_spec(self.gates, "03b-script-review", ["01b-coverage-scan", "03b-script-review"])
        self.assertEqual([v["file"] for v in spec["verdicts"]], ["story/script-review.md", cv.REVIEW_REL])

    def test_review_is_stale_once_an_input_changes(self):
        ep = Path(tempfile.mkdtemp(prefix="vidgen_ltx_fresh_"))
        self.addCleanup(shutil.rmtree, ep, True)
        (ep / "story").mkdir()
        (ep / "story/script.md").write_text("v1", encoding="utf-8")
        verdict = {"file": cv.REVIEW_REL, "json_status": "PASS", "fresh_inputs_field": "input_sha256"}
        (ep / cv.REVIEW_REL).write_text(json.dumps({
            "status": "PASS", "input_sha256": {"story/script.md": hashlib.sha256(b"v1").hexdigest()}}),
            encoding="utf-8")
        self.assertEqual(es._verdict_problems(ep, verdict), [])
        (ep / "story/script.md").write_text("v2", encoding="utf-8")
        self.assertTrue(any("changed after" in p for p in es._verdict_problems(ep, verdict)))

    def test_inside_the_process_runs_01b_as_an_owner_gate(self):
        stages = {s["id"]: s for s in es.load_channel("inside-the-process")["pipeline_stages"]}
        self.assertTrue(stages["01b-coverage-scan"].get("owner_gate"))
        seq = list(stages)
        self.assertEqual(seq.index("01b-coverage-scan"), seq.index("01-ideation") + 1)


if __name__ == "__main__":
    unittest.main()
