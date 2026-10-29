"""Smoke tests for the no-git episode state machine.

Discoverable by `python -m unittest discover -s tests` (the documented command)
and still runnable directly with `python tests/test_preflight_smoke.py`.

Two levels of coverage live here:

* the happy-path *walk* — every channel's full pipeline_stages sequence, start to
  closed, satisfying each stage's declared gate first, so a green run proves the
  gate logic does not false-positive when the deliverables are all present;
* walk-level *failure* cases — a missing artifact, a BLOCKED verdict, and a stale
  owner approval each halt the walk at the offending stage.

Per-rule negative cases for `stage_gate_check` (empty file, glob needs a match,
REVISE, draft-mode ltx review, every stage covered) live in test_stage_gates.py;
this file checks that the same guardrails hold when reached through a real walk.
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

STAGE_GATES = json.loads(
    (ROOT / "pipeline" / "stage-gates.json").read_text(encoding="utf-8")
)

_VERDICT_BODY = {
    "story/compliance.md": "# compliance\n\n## OVERALL VERDICT: **CLEARED**\n",
    "story/script-review.md": "# review\n\n**VERDICT: `PASS`**\n",
    "_context/ltx-prompt-review.json": json.dumps(
        {"status": "PASS", "mode": "strict", "clips": []}
    ),
    "qa/ltx-pilot-qa.json": json.dumps({"status": "PASS"}),
    "qa/render-qa.md": "# render QA\n\n**STAGE VERDICT: PASS**\n",
    "final-qa.md": "# final QA\n\n**STAGE VERDICT: PASS**\n",
}


def _satisfy_gate(ep_dir: Path, stage_id: str) -> None:
    """Write a minimal deliverable for every output the stage declares, and a
    passing verdict where one is required. Never clobbers a file that already
    exists (state-machine-managed files, or one a test wrote deliberately) --
    except a machine review JSON, which each stage re-emits for itself."""
    if stage_id not in STAGE_GATES:
        return
    seq = json.loads((ep_dir / "episode-state.json").read_text(encoding="utf-8"))["stage_sequence"]
    spec = es.stage_spec(STAGE_GATES, stage_id, seq)
    verdicts = {v["file"]: v for v in spec["verdicts"]}
    for pat in spec["outputs"]:
        rel = pat.replace("*", "STUB").replace("?", "x").replace("[", "").replace("]", "")
        target = ep_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        verdict = verdicts.get(pat)
        if target.exists() and not (verdict and verdict.get("fresh_inputs_field")):
            continue
        if verdict and verdict.get("fresh_inputs_field"):
            continue  # written below, after every input it vouches for exists
        if verdict:
            target.write_text(_VERDICT_BODY.get(pat, "stub\n"), encoding="utf-8")
        elif rel.endswith(".json"):
            target.write_text("{}\n", encoding="utf-8")
        else:
            target.write_text(f"stub for {stage_id} :: {pat}\n", encoding="utf-8")
    for pat, verdict in verdicts.items():
        if verdict.get("fresh_inputs_field"):
            recorded = {o: es._sha256(ep_dir / o) for o in spec["outputs"]
                        if o != pat and not any(c in o for c in "*?[") and (ep_dir / o).is_file()}
            (ep_dir / pat).write_text(json.dumps({
                "status": verdict["json_status"], **(verdict.get("json_fields") or {}),
                verdict["fresh_inputs_field"]: recorded}), encoding="utf-8")


class StateMachineSmoke(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_smoke_"))
        self._real_channels = es.CHANNEL_PROFILES_DIR
        self._real_episodes = es.EPISODES_DIR
        shutil.copytree(ROOT / "channel_profiles", self.tmp / "channel_profiles")
        (self.tmp / "episodes").mkdir()
        es.CHANNEL_PROFILES_DIR = self.tmp / "channel_profiles"
        es.EPISODES_DIR = self.tmp / "episodes"

    def tearDown(self):
        es.CHANNEL_PROFILES_DIR = self._real_channels
        es.EPISODES_DIR = self._real_episodes
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _ep_dir(self, slug: str, episode_id: str = "EP001") -> Path:
        return self.tmp / "episodes" / slug / episode_id

    def _advance_to(self, slug: str, stop_stage: str, episode_id: str = "EP001") -> dict:
        """Walk from the current next_stage up to (not including) stop_stage,
        satisfying and completing each stage's gate. Returns the live state."""
        state = es.load_state(slug, episode_id)
        ep_dir = self._ep_dir(slug, episode_id)
        while state["next_stage"] and state["next_stage"] != stop_stage:
            stage = state["next_stage"]
            _satisfy_gate(ep_dir, stage)
            approve = es.stage_owner_gate(slug, stage)
            state = es.complete_stage(slug, episode_id, stage, approve=approve)
        return state

    # ── happy-path walk ─────────────────────────────────────────────────

    def test_preflight_check_discovers_sorted_channels(self):
        slugs = es.preflight_check()
        self.assertTrue(slugs, "preflight_check found no channel profiles")
        self.assertEqual(slugs, sorted(slugs))

    def test_every_channel_walks_from_create_to_closed(self):
        for slug in es.preflight_check():
            with self.subTest(slug=slug):
                state = es.create_episode(slug)
                self.assertEqual(state["episode_id"], "EP001")
                self.assertEqual(state["status"], "open")
                self.assertEqual(state["next_stage"], state["stage_sequence"][0])
                ep_dir = self._ep_dir(slug)

                while state["status"] == "open":
                    stage = state["next_stage"]
                    _satisfy_gate(ep_dir, stage)
                    gate = es.stage_owner_gate(slug, stage)
                    try:
                        state = es.complete_stage(slug, "EP001", stage, approve=False)
                        self.assertFalse(gate, f"{slug}/{stage} should have needed --approve")
                    except es.PipelineError:
                        self.assertTrue(gate, f"{slug}/{stage} raised without being a gate")
                        state = es.complete_stage(slug, "EP001", stage, approve=True)

                self.assertEqual(state["status"], "closed")
                self.assertIsNone(state["next_stage"])
                self.assertEqual(
                    len(state["completed_stages"]), len(state["stage_sequence"])
                )

    def test_second_episode_is_numbered_ep002(self):
        es.create_episode("clover-and-paws")
        state2 = es.create_episode("clover-and-paws")
        self.assertEqual(state2["episode_id"], "EP002")

    def test_out_of_sequence_completion_is_rejected(self):
        es.create_episode("clover-and-paws")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("clover-and-paws", "EP001", "07-final-package-qa")
        self.assertIn("next stage", str(ctx.exception))

    # ── walk-level failure cases ────────────────────────────────────────

    def test_missing_artifact_halts_the_walk(self):
        es.create_episode("signed-anyway")
        state = self._advance_to("signed-anyway", "01-ideation")
        self.assertEqual(state["next_stage"], "01-ideation")
        # do NOT write story/premise.md
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertIn("story/premise.md", str(ctx.exception))
        self.assertEqual(
            es.load_state("signed-anyway", "EP001")["next_stage"], "01-ideation"
        )

    def test_blocked_verdict_halts_the_walk_at_compliance(self):
        es.create_episode("signed-anyway")
        self._advance_to("signed-anyway", "02b-compliance")
        (self._ep_dir("signed-anyway") / "story").mkdir(parents=True, exist_ok=True)
        (self._ep_dir("signed-anyway") / "story" / "compliance.md").write_text(
            "# EP001 compliance\n\n## OVERALL VERDICT: **BLOCKED**\n\n"
            "reason: a real person is depicted.\n",
            encoding="utf-8",
        )
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "02b-compliance", approve=True)
        self.assertIn("blocking verdict", str(ctx.exception))
        self.assertEqual(
            es.load_state("signed-anyway", "EP001")["next_stage"], "02b-compliance"
        )

    def test_stale_owner_approval_does_not_override_a_blocking_verdict(self):
        """The owner-gate --approve flag clears the *gate*, not the deliverable
        check. A compliance.md that flips to BLOCKED after an approval was
        intended still stops the walk."""
        es.create_episode("signed-anyway")
        self._advance_to("signed-anyway", "03b-script-review")
        story = self._ep_dir("signed-anyway") / "story"
        story.mkdir(parents=True, exist_ok=True)
        (story / "script-review.md").write_text(
            "# review\n\n**VERDICT: `REVISE`** -- needs another pass.\n", encoding="utf-8"
        )
        with self.assertRaises(es.PipelineError):
            es.complete_stage(
                "signed-anyway", "EP001", "03b-script-review", approve=True
            )
        self.assertEqual(
            es.load_state("signed-anyway", "EP001")["next_stage"], "03b-script-review"
        )


if __name__ == "__main__":
    unittest.main()
