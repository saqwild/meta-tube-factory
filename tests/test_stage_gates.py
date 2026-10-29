"""Tests for episode_state.stage_gate_check — the check that a stage actually
produced its declared deliverables, and that a BLOCKED / REVISE / non-PASS
verdict stops completion instead of riding through on the owner-approval flag.

The gap this guards: `complete_stage` used to check only sequence order and the
approval flag. An episode could advance from 02b-compliance to 03a-writer with a
`compliance.md` that said BLOCKED, or with no compliance.md at all.
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


class StageGateCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_gates_"))
        self._real_channels = es.CHANNEL_PROFILES_DIR
        self._real_episodes = es.EPISODES_DIR
        shutil.copytree(ROOT / "channel_profiles", self.tmp / "channel_profiles")
        (self.tmp / "episodes").mkdir()
        es.CHANNEL_PROFILES_DIR = self.tmp / "channel_profiles"
        es.EPISODES_DIR = self.tmp / "episodes"
        self.state = es.create_episode("signed-anyway")
        self.ep = self.tmp / "episodes" / "signed-anyway" / "EP001"

    def tearDown(self):
        es.CHANNEL_PROFILES_DIR = self._real_channels
        es.EPISODES_DIR = self._real_episodes
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, rel: str, body: str) -> None:
        p = self.ep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")

    def _advance_to(self, stage_id: str) -> None:
        """Walk (satisfying each gate with a trivial passing stub) up to but not
        including stage_id, so the episode's next_stage is stage_id."""
        gates = es._load_stage_gates()
        seq = self.state["stage_sequence"]
        for s in seq[: seq.index(stage_id)]:
            spec = gates.get(s, {})
            verdict = spec.get("verdict") or {}
            for pat in spec.get("outputs", []):
                rel = pat.replace("*", "STUB")
                if (self.ep / rel).exists():
                    continue  # never clobber state-machine-managed files
                if pat == verdict.get("file"):
                    if "json_status" in verdict:
                        self._write(rel, json.dumps(
                            {"status": "PASS", **(verdict.get("json_fields") or {})}))
                    elif "compliance" in pat:
                        self._write(rel, "## OVERALL VERDICT: **CLEARED**\n")
                    elif "STAGE VERDICT" in verdict.get("pass", ""):
                        self._write(rel, "**STAGE VERDICT: PASS**\n")
                    else:
                        self._write(rel, "**VERDICT: `PASS`**\n")
                elif rel.endswith(".json"):
                    self._write(rel, "{}\n")
                else:
                    self._write(rel, "stub\n")
            approve = es.stage_owner_gate("signed-anyway", s)
            self.state = es.complete_stage("signed-anyway", "EP001", s, approve=approve)

    # ── missing deliverable ──────────────────────────────────────────────

    def test_missing_output_blocks_completion(self):
        self._advance_to("01-ideation")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertIn("story/premise.md", str(ctx.exception))

    def test_empty_output_blocks_completion(self):
        self._advance_to("01-ideation")
        self._write("story/premise.md", "")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertIn("empty", str(ctx.exception))

    def test_present_output_completes(self):
        self._advance_to("01-ideation")
        self._write("story/premise.md", "# Premise\n\nsomething real\n")
        state = es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertEqual(state["next_stage"], "02-research")

    def test_glob_output_needs_at_least_one_match(self):
        # 04f2 requires renders/stills/*.png
        self._advance_to("04f2-frame0-stills")
        for rel in ("prompts/6-image-prompts.md", "prompts/6-image-agent-packet.md",
                    "qa/still-gate.md"):
            self._write(rel, "stub\n")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04f2-frame0-stills")
        self.assertIn("renders/stills/*.png", str(ctx.exception))
        self._write("renders/stills/SC01.png", "\x89PNG stub")
        es.complete_stage("signed-anyway", "EP001", "04f2-frame0-stills")

    # ── blocking verdict ─────────────────────────────────────────────────

    def test_compliance_blocked_verdict_stops_even_with_approve(self):
        self._advance_to("02b-compliance")
        self._write("story/compliance.md",
                    "# EP001 compliance\n\n## OVERALL VERDICT: **BLOCKED**\n\n"
                    "reason: a real person is depicted.\n")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "02b-compliance", approve=True)
        self.assertIn("blocking verdict", str(ctx.exception))
        # still at 02b, not advanced
        self.assertEqual(es.load_state("signed-anyway", "EP001")["next_stage"],
                         "02b-compliance")

    def test_compliance_cleared_verdict_completes_with_approve(self):
        self._advance_to("02b-compliance")
        self._write("story/compliance.md",
                    "# EP001 compliance\n\n## OVERALL VERDICT: **CLEARED**\n")
        state = es.complete_stage("signed-anyway", "EP001", "02b-compliance", approve=True)
        self.assertEqual(state["next_stage"], "03a-writer")

    def test_compliance_no_verdict_line_blocks(self):
        self._advance_to("02b-compliance")
        self._write("story/compliance.md", "# EP001 compliance\n\nsome tables, no verdict line\n")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "02b-compliance", approve=True)
        self.assertIn("passing verdict", str(ctx.exception))

    def test_script_review_revise_verdict_blocks(self):
        self._advance_to("03b-script-review")
        self._write("story/script-review.md",
                    "# review\n\n**VERDICT: `REVISE`** — three changes below.\n")
        with self.assertRaises(es.PipelineError):
            es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)

    def test_script_review_pass_verdict_completes(self):
        self._advance_to("03b-script-review")
        self._write("story/script-review.md", "# review\n\n**VERDICT: `PASS`**\n")
        state = es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)
        self.assertEqual(state["next_stage"], "04a-visual-brief")

    def test_script_review_history_of_revises_then_pass_completes(self):
        """A verdict file that accumulated several REVISE rounds via append
        before a final PASS (this repo's own review convention -- see
        episodes/inside-the-process/EP001/story/script-review.md's real
        Round 3-7 history) must complete on the LAST verdict, not fail just
        because an earlier, already-superseded REVISE string is still present
        earlier in the file."""
        self._advance_to("03b-script-review")
        self._write(
            "story/script-review.md",
            "# review\n\n"
            "## Round 1\n**VERDICT: REVISE** — word count short.\n\n"
            "## Round 2\n**VERDICT: REVISE** — one more stale reference.\n\n"
            "## Round 3\n**VERDICT: PASS**\n",
        )
        state = es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)
        self.assertEqual(state["next_stage"], "04a-visual-brief")

    def test_script_review_revise_after_pass_still_blocks(self):
        """The inverse of the above: if the LAST verdict in the file is a
        REVISE (e.g. a fix was reopened and re-reviewed after an earlier
        PASS), that must still block -- appending history must not let a
        stale earlier PASS paper over a real, more recent REVISE."""
        self._advance_to("03b-script-review")
        self._write(
            "story/script-review.md",
            "# review\n\n"
            "## Round 1\n**VERDICT: PASS**\n\n"
            "## Round 2 (content reopened and changed)\n**VERDICT: REVISE**\n",
        )
        with self.assertRaises(es.PipelineError):
            es.complete_stage("signed-anyway", "EP001", "03b-script-review", approve=True)

    def _04f3_deliverables(self, review: dict, prompts: str = "## SC01\nfinal prose\n") -> None:
        self._advance_to("04f3-ltx-prompt-final")
        self._write("prompts/7-video-prompts.md", prompts)
        self._write("_context/ltx-prompt-manifest.json", "{}\n")
        self._write("_context/ltx-prompt-review.json", json.dumps(review))

    def test_json_review_non_pass_status_blocks(self):
        self._04f3_deliverables({"status": "FAIL", "mode": "strict", "clips": []})
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04f3-ltx-prompt-final")
        self.assertIn("FAIL", str(ctx.exception))

    def test_04f3_draft_review_blocks_even_with_pass_status(self):
        """A draft ltx-prompt-review.json cannot clear 04f3 -- only mode: strict."""
        self._04f3_deliverables({"status": "PASS", "mode": "draft", "clips": []})
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04f3-ltx-prompt-final")
        self.assertIn("mode", str(ctx.exception))

    def test_04f3_strict_pass_review_completes(self):
        self._04f3_deliverables({"status": "PASS", "mode": "strict", "clips": []})
        state = es.complete_stage("signed-anyway", "EP001", "04f3-ltx-prompt-final")
        self.assertEqual(state["next_stage"], "04g-ltx-render-package")

    def test_04f3_requires_the_prompt_manifest(self):
        self._04f3_deliverables({"status": "PASS", "mode": "strict", "clips": []})
        (self.ep / "_context/ltx-prompt-manifest.json").unlink()
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04f3-ltx-prompt-final")
        self.assertIn("ltx-prompt-manifest.json", str(ctx.exception))

    def test_04f3_blocks_while_prompts_still_say_provisional(self):
        """inside-the-process EP001 cleared 04f3 with 04f's untouched draft file,
        header still reading 'Every GLOBAL:: line below is PROVISIONAL'."""
        self._04f3_deliverables(
            {"status": "PASS", "mode": "strict", "clips": []},
            prompts="# draft\n**Every `GLOBAL::` line below is PROVISIONAL**\n\n## SC01\nx\n")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04f3-ltx-prompt-final")
        self.assertIn("PROVISIONAL", str(ctx.exception))

    # ── 04h / 05a / 07 verdicts ──────────────────────────────────────────

    def test_04h_pilot_fail_blocks_even_with_approve(self):
        self._advance_to("04h-ltx-pilot-qa")
        self._write("qa/ltx-pilot-qa.json", json.dumps({"status": "FAIL"}))
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "04h-ltx-pilot-qa", approve=True)
        self.assertIn("FAIL", str(ctx.exception))

    def test_04h_pilot_pass_completes(self):
        self._advance_to("04h-ltx-pilot-qa")
        self._write("qa/ltx-pilot-qa.json", json.dumps({"status": "PASS"}))
        state = es.complete_stage("signed-anyway", "EP001", "04h-ltx-pilot-qa", approve=True)
        self.assertEqual(state["next_stage"], "05-render-ingest")

    def test_05a_needs_a_stage_verdict_line(self):
        self._advance_to("05a-render-qa")
        self._write("qa/render-qa.md", "# render QA\n\n| SC01 | PASS |\n")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "05a-render-qa")
        self.assertIn("passing verdict", str(ctx.exception))

    def test_05a_fail_after_earlier_pass_blocks(self):
        self._advance_to("05a-render-qa")
        self._write("qa/render-qa.md",
                    "## Round 1\n**STAGE VERDICT: PASS**\n\n## Re-render\n**STAGE VERDICT: FAIL**\n")
        with self.assertRaises(es.PipelineError):
            es.complete_stage("signed-anyway", "EP001", "05a-render-qa")

    def test_07_stage_verdict_pass_completes(self):
        self._advance_to("07-final-package-qa")
        self._write("final-qa.md", "# final\n\n**STAGE VERDICT: PASS**\n")
        state = es.complete_stage("signed-anyway", "EP001", "07-final-package-qa")
        self.assertEqual(state["status"], "closed")

    # ── sequence check still fires first ─────────────────────────────────

    def test_out_of_sequence_still_rejected_before_gate_check(self):
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "03a-writer")
        self.assertIn("next stage", str(ctx.exception))

    def test_stage_gates_json_covers_every_declared_stage(self):
        """Every stage in every channel's pipeline_stages must have a gate entry —
        an un-gated stage is a hole in exactly the check this adds."""
        gates = es._load_stage_gates()
        for slug in es.list_channel_slugs():
            for s in es.load_channel(slug)["pipeline_stages"]:
                self.assertIn(s["id"], gates, f"{slug}: {s['id']} has no stage-gates.json entry")


if __name__ == "__main__":
    unittest.main()
