"""Approval digests: a completed stage records a hash of the exact bytes it was
completed against, so a later edit to a deliverable is detectable.

The gap this closes: `complete_stage` recorded {stage, completed_at, approved,
note} but nothing about the files. Editing story/script.md after 03b-script-review
was approved left the approval silently "covering" a file it never saw.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import episode_state as es  # noqa: E402


class ApprovalDigest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_appr_"))
        self._c, self._e = es.CHANNEL_PROFILES_DIR, es.EPISODES_DIR
        shutil.copytree(ROOT / "channel_profiles", self.tmp / "channel_profiles")
        (self.tmp / "episodes").mkdir()
        es.CHANNEL_PROFILES_DIR = self.tmp / "channel_profiles"
        es.EPISODES_DIR = self.tmp / "episodes"
        es.create_episode("signed-anyway")
        self.ep = self.tmp / "episodes" / "signed-anyway" / "EP001"

    def tearDown(self):
        es.CHANNEL_PROFILES_DIR, es.EPISODES_DIR = self._c, self._e
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _satisfy(self, stage_id):
        spec = es._load_stage_gates().get(stage_id, {})
        verdict = spec.get("verdict") or {}
        for pat in spec.get("outputs", []):
            rel = pat.replace("*", "STUB")
            p = self.ep / rel
            if p.exists():
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            if pat == verdict.get("file") and "compliance" in pat:
                p.write_text("## OVERALL VERDICT: **CLEARED**\n", encoding="utf-8")
            elif pat == verdict.get("file"):
                p.write_text("**VERDICT: `PASS`**\n", encoding="utf-8")
            elif rel.endswith(".json"):
                p.write_text('{"status": "PASS", "mode": "strict", "clips": []}', encoding="utf-8")
            else:
                p.write_text(f"stub {stage_id}\n", encoding="utf-8")

    def _advance_to(self, target):
        seq = es.load_state("signed-anyway", "EP001")["stage_sequence"]
        for s in seq[: seq.index(target)]:
            self._satisfy(s)
            es.complete_stage("signed-anyway", "EP001", s,
                              approve=es.stage_owner_gate("signed-anyway", s))

    def test_digest_recorded_on_completion(self):
        self._advance_to("01-ideation")
        self._satisfy("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        entry = es.load_state("signed-anyway", "EP001")["completed_stages"][-1]
        self.assertIn("deliverable_digest", entry)
        d = entry["deliverable_digest"]
        self.assertEqual(len(d["digest_sha256"]), 64)
        self.assertEqual([f["path"] for f in d["files"]], ["story/premise.md"])

    def test_log_line_carries_the_digest_prefix(self):
        self._advance_to("01-ideation")
        self._satisfy("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        log = (self.ep / "episode-state-log.md").read_text(encoding="utf-8")
        self.assertRegex(log, r"completed 01-ideation.*digest [0-9a-f]{8}")

    def test_no_drift_when_untouched(self):
        self._advance_to("03a-writer")
        self._satisfy("03a-writer")
        es.complete_stage("signed-anyway", "EP001", "03a-writer")
        self.assertEqual(es.approval_drift("signed-anyway", "EP001"), [])

    def test_drift_detected_when_a_deliverable_is_edited_after_approval(self):
        self._advance_to("03b-script-review")
        self._satisfy("03b-script-review")
        es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)
        # someone edits the reviewed script afterwards
        (self.ep / "story" / "script.md").write_text("# script REV 3 (edited later)\n", encoding="utf-8")
        drift = es.approval_drift("signed-anyway", "EP001")
        self.assertTrue(any("script.md" in d and "CHANGED" in d for d in drift))
        self.assertTrue(any("03a-writer" in d for d in drift))

    def test_drift_detected_when_a_deliverable_is_deleted(self):
        self._advance_to("03a-writer")
        self._satisfy("03a-writer")
        es.complete_stage("signed-anyway", "EP001", "03a-writer")
        (self.ep / "story" / "characters.md").unlink()
        drift = es.approval_drift("signed-anyway", "EP001")
        self.assertTrue(any("characters.md" in d and "GONE" in d for d in drift))

    def test_drift_is_advisory_only_never_blocks_completion(self):
        self._advance_to("03a-writer")
        self._satisfy("03a-writer")
        es.complete_stage("signed-anyway", "EP001", "03a-writer")
        (self.ep / "story" / "script.md").write_text("edited\n", encoding="utf-8")
        # the next stage still completes -- drift does not gate anything
        self._satisfy("03b-script-review")
        state = es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)
        self.assertEqual(state["next_stage"], "04a-visual-brief")

    def test_deliverable_digest_none_for_unknown_stage(self):
        self.assertIsNone(es.deliverable_digest("signed-anyway", "EP001", "99-not-a-stage"))

    def _put(self, rel, body):
        p = self.ep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")

    def test_shared_later_output_excluded_from_digest(self):
        # visual/references/manifest.md is the declared output of BOTH 04b and 04c.
        # 04b's digest must not include it (04c legitimately edits it afterward).
        self._advance_to("04b-character-refs")
        self._put("visual/references/manifest.md", "# manifest (04b)\n")
        d = es.deliverable_digest("signed-anyway", "EP001", "04b-character-refs")
        self.assertIsNone(d)  # manifest.md was 04b's only output, and it's shared with 04c

    def test_04c_editing_the_shared_manifest_does_not_drift_04b(self):
        self._advance_to("04b-character-refs")
        self._put("visual/references/manifest.md", "# manifest (04b section)\n")
        es.complete_stage("signed-anyway", "EP001", "04b-character-refs")
        self._put("visual/references/manifest.md", "# manifest (04b + 04c)\n")  # 04c's edit
        es.complete_stage("signed-anyway", "EP001", "04c-scene-refs")
        drift = es.approval_drift("signed-anyway", "EP001")
        self.assertFalse(any("04b-character-refs" in d for d in drift), drift)

    def test_reopen_recomplete_only_checks_the_latest_completion(self):
        # complete 01-ideation, then reopen + recomplete after editing the deliverable.
        self._advance_to("01-ideation")
        self._satisfy("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        (self.ep / "story" / "premise.md").write_text("# premise REV 2\n", encoding="utf-8")
        es.reopen_stage("signed-anyway", "EP001", "01-ideation", approve=True)
        self._satisfy("01-ideation")  # no-op, file exists
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        # two 01-ideation entries now exist; only the latest digest is checked
        entries = [c for c in es.load_state("signed-anyway", "EP001")["completed_stages"]
                   if c["stage"] == "01-ideation"]
        self.assertEqual(len(entries), 2)
        self.assertEqual(es.approval_drift("signed-anyway", "EP001"), [])


if __name__ == "__main__":
    unittest.main()
