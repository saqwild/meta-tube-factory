"""Tests for tools/episode_health.py -- the read-only end-to-end consistency check.

Category functions are pure `(ep_dir, state) -> list[Finding]`, so most of these
build a minimal episode tree in a tempdir and call one category directly.
"""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import episode_health as h  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"pixels"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def levels(findings, category=None):
    return {f.level for f in findings if category is None or f.category == category}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_health_"))
        self.ep = self.tmp / "episodes" / "demo" / "EP001"
        self.ep.mkdir(parents=True)
        self.state = {
            "episode_id": "EP001", "channel_slug": "demo", "status": "open",
            "stage_sequence": [], "next_stage": None, "completed_stages": [],
            "created_at": "x", "updated_at": "x",
        }
        (self.ep / "episode-state.json").write_text(json.dumps(self.state), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel, text):
        p = self.ep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def write_bytes(self, rel, b):
        p = self.ep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
        return p


class RequiredFiles(Base):
    def test_missing_declared_output_is_a_fail(self):
        self.state["completed_stages"] = [{"stage": "01-ideation"}]
        findings = h.check_required_files(self.ep, self.state)
        self.assertIn("FAIL", levels(findings))
        self.assertTrue(any("story/premise.md" in f.message for f in findings))

    def test_present_outputs_pass(self):
        self.state["completed_stages"] = [{"stage": "01-ideation"}]
        self.write("story/premise.md", "real premise\n")
        findings = h.check_required_files(self.ep, self.state)
        self.assertEqual(levels(findings), {"OK"})

    def test_missing_output_on_a_closed_episode_is_only_a_warn(self):
        self.state["status"] = "closed"
        self.state["completed_stages"] = [{"stage": "01-ideation"}]
        findings = h.check_required_files(self.ep, self.state)
        self.assertIn("WARN", levels(findings))
        self.assertNotIn("FAIL", levels(findings))


class Hashes(Base):
    def test_content_drift_is_a_fail(self):
        self.write_bytes("renders/clip01.mp4", b"rendered")
        manifest = {"clips": [{"clip": "SC01", "path": "renders/clip01.mp4", "sha256": _sha(b"OTHER")}]}
        self.write("renders/render-manifest.json", json.dumps(manifest))
        findings = h.check_hashes(self.ep, self.state)
        self.assertTrue(any(f.level == "FAIL" and "SC01" in f.message for f in findings))

    def test_renamed_file_is_a_warn_not_a_fail(self):
        pm = {"outputs": {"full_episode": {"path": "exports/final/Old_Name.mp4", "sha256": _sha(b"x")}}}
        self.write("postprod/postprod-manifest.json", json.dumps(pm))
        findings = h.check_hashes(self.ep, self.state)
        self.assertIn("WARN", levels(findings, "hashes"))
        self.assertNotIn("FAIL", levels(findings, "hashes"))

    def test_crlf_normalised_text_hash_still_matches(self):
        # deliverable hashed LF-normalised, checked out CRLF -- not drift
        self.write_bytes("exports/ltx-render-package/master-prompt.txt", b"line one\r\nline two\r\n")
        m = {"master_prompt_sha256": _sha(b"line one\nline two\n"), "clips": []}
        self.write("exports/ltx-render-package/render-manifest.json", json.dumps(m))
        findings = h.check_hashes(self.ep, self.state)
        self.assertNotIn("FAIL", levels(findings, "hashes"))


    def _prompt_manifest(self, body_hash):
        self.write("prompts/7-video-prompts.md", "## SC01\n[[TAG]]\nGLOBAL:: x\n")
        self.write_bytes("renders/stills/SC01.png", PNG)
        self.write("_context/ltx-prompt-manifest.json", json.dumps({"clips": [{
            "clip": "SC01", "prompt_sha256": body_hash,
            "still_path": "renders/stills/SC01.png", "still_sha256": _sha(PNG)}]}))

    def test_prompt_manifest_matching_blocks_is_clean(self):
        self._prompt_manifest(_sha(b"GLOBAL:: x"))
        self.assertNotIn("FAIL", levels(h.check_hashes(self.ep, self.state), "hashes"))

    def test_prompt_edited_after_manifest_is_a_fail(self):
        self._prompt_manifest(_sha(b"GLOBAL:: an older prompt"))
        findings = h.check_hashes(self.ep, self.state)
        self.assertTrue(any(f.level == "FAIL" and "SC01" in f.message and "prompt block" in f.message
                            for f in findings))


class ClipCoverage(Base):
    def _prompts(self, ids):
        self.write("prompts/7-video-prompts.md",
                   "\n\n".join(f"## {i}\nGLOBAL:: x" for i in ids))

    def test_consistent_sets_pass(self):
        self._prompts(["SC01", "SC02"])
        self.write("_context/blocking.json",
                   json.dumps({"clips": {"SC01": {}, "SC02": {}}}))
        findings = h.check_clip_coverage(self.ep, self.state)
        self.assertEqual(levels(findings), {"OK"})

    def test_a_gap_is_a_fail(self):
        self._prompts(["SC01", "SC02", "SC03"])
        self.write("_context/blocking.json", json.dumps({"clips": {"SC01": {}, "SC02": {}}}))
        findings = h.check_clip_coverage(self.ep, self.state)
        self.assertTrue(any(f.level == "FAIL" and "SC03" in f.message for f in findings))


class ReviewFreshness(Base):
    def test_stale_audio_audit_is_a_warn(self):
        self.write("renders/render-manifest.json", '{"clips": []}')
        self.write("prompts/7-video-prompts.md", "## SC01\nx")
        audit = {
            "source_manifest_sha256": _sha(b"an older manifest"),
            "source_prompts_sha256": _sha((self.ep / "prompts/7-video-prompts.md").read_bytes()),
        }
        self.write("renders/audio-content-audit.json", json.dumps(audit))
        findings = h.check_review_freshness(self.ep, self.state)
        self.assertIn("WARN", levels(findings))
        self.assertTrue(any("older" in f.message for f in findings))

    def test_matching_source_hash_is_clean(self):
        mtext = '{"clips": []}'
        self.write("renders/render-manifest.json", mtext)
        self.write("prompts/7-video-prompts.md", "## SC01\nx")
        audit = {
            "source_manifest_sha256": _sha(mtext.encode()),
            "source_prompts_sha256": _sha((self.ep / "prompts/7-video-prompts.md").read_bytes()),
        }
        self.write("renders/audio-content-audit.json", json.dumps(audit))
        self.assertEqual(levels(h.check_review_freshness(self.ep, self.state)), {"OK"})


    def test_legacy_review_that_hashed_the_prompts_file_is_not_stale(self):
        """Legacy reviews stored the PROMPTS hash under source_manifest_sha256
        whenever no manifest existed yet -- which was always, at 04f3. That used
        to raise a false 'recorded PASS predates the current file' warning."""
        self.write("prompts/7-video-prompts.md", "## SC01\nx")
        self.write("_context/ltx-prompt-manifest.json", '{"clips": []}')
        review = {"source_manifest_sha256": _sha((self.ep / "prompts/7-video-prompts.md").read_bytes())}
        self.write("_context/ltx-prompt-review.json", json.dumps(review))
        self.assertEqual(levels(h.check_review_freshness(self.ep, self.state)), {"OK"})

    def test_review_of_an_older_prompts_file_is_a_warn(self):
        self.write("prompts/7-video-prompts.md", "## SC01\nx")
        self.write("_context/ltx-prompt-review.json",
                   json.dumps({"source_prompts_sha256": _sha(b"older prompts")}))
        findings = h.check_review_freshness(self.ep, self.state)
        self.assertTrue(any(f.level == "WARN" and "older 7-video-prompts.md" in f.message
                            for f in findings))


class FinalMedia(Base):
    def test_no_final_is_ok(self):
        self.assertEqual(levels(h.check_final_media(self.ep, self.state)), {"OK"})


class Integration(Base):
    def test_run_health_aggregates_all_categories_without_crashing(self):
        self.state["completed_stages"] = [{"stage": "01-ideation"}]
        self.write("story/premise.md", "premise\n")
        findings = h.run_health("demo", "EP001", root=self.tmp)
        cats = {f.category for f in findings}
        self.assertEqual(cats, {"required-files", "schemas", "clip-coverage",
                                "hashes", "review-freshness", "final-media"})

    def test_a_broken_checker_does_not_hide_the_others(self):
        (self.ep / "_context").mkdir()
        (self.ep / "_context" / "blocking.json").write_text("{ not json", encoding="utf-8")
        findings = h.run_health("demo", "EP001", root=self.tmp)
        # still get findings from every category
        self.assertEqual(len({f.category for f in findings}), 6)


class AsciiSafe(unittest.TestCase):
    def test_output_is_ascii_safe(self):
        src = (ROOT / "tools" / "episode_health.py").read_text(encoding="utf-8")
        for i, line in enumerate(src.splitlines(), 1):
            if "print(" in line:
                self.assertTrue(all(ord(c) < 128 for c in line),
                                f"non-ASCII in printed output at line {i}")


if __name__ == "__main__":
    unittest.main()
