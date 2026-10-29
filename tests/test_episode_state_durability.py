"""Durability tests for tools/episode_state.py — atomic writes, a recoverable
backup, and a per-episode lock.

Without git, episode-state.json + episode-state-log.md are the entire chain of
custody. A torn write or two operators racing complete_stage could lose a
completion or corrupt the state with nothing to fall back to.
"""
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import episode_state as es  # noqa: E402


class Durability(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_dur_"))
        self._c, self._e = es.CHANNEL_PROFILES_DIR, es.EPISODES_DIR
        shutil.copytree(ROOT / "channel_profiles", self.tmp / "channel_profiles")
        (self.tmp / "episodes").mkdir()
        es.CHANNEL_PROFILES_DIR = self.tmp / "channel_profiles"
        es.EPISODES_DIR = self.tmp / "episodes"
        self.state = es.create_episode("signed-anyway")
        self.ep = self.tmp / "episodes" / "signed-anyway" / "EP001"
        # advance past 00-preflight so the tests operate at 01-ideation; this also
        # gives us a first _save_state (and therefore a .bak) to work against.
        es.complete_stage("signed-anyway", "EP001", "00-preflight")

    def tearDown(self):
        es.CHANNEL_PROFILES_DIR, es.EPISODES_DIR = self._c, self._e
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _stub_gate(self, stage_id):
        spec = es._load_stage_gates().get(stage_id, {})
        for pat in spec.get("outputs", []):
            rel = pat.replace("*", "STUB")
            p = self.ep / rel
            if p.exists():
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("stub\n", encoding="utf-8")

    # ── atomic write + backup ────────────────────────────────────────────

    def test_no_temp_file_left_after_a_write(self):
        self._stub_gate("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        leftovers = list(self.ep.glob("episode-state.json.tmp*"))
        self.assertEqual(leftovers, [], leftovers)

    def test_backup_holds_the_previous_state(self):
        self._stub_gate("01-ideation")
        before = json.loads((self.ep / "episode-state.json").read_text(encoding="utf-8"))
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        bak = self.ep / "episode-state.json.bak"
        self.assertTrue(bak.exists())
        self.assertEqual(json.loads(bak.read_text(encoding="utf-8"))["next_stage"],
                         before["next_stage"])
        after = json.loads((self.ep / "episode-state.json").read_text(encoding="utf-8"))
        self.assertNotEqual(after["next_stage"], before["next_stage"])

    def test_corrupt_state_load_points_at_the_backup(self):
        self._stub_gate("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")  # creates a .bak
        (self.ep / "episode-state.json").write_text("{ this is not json", encoding="utf-8")
        with self.assertRaises(es.PipelineError) as ctx:
            es.load_state("signed-anyway", "EP001")
        self.assertIn("corrupt", str(ctx.exception))
        self.assertIn(".bak", str(ctx.exception))

    # ── per-episode lock ────────────────────────────────────────────────

    def test_a_held_lock_blocks_a_concurrent_complete(self):
        lock = self.ep / "episode-state.lock"
        lock.write_text(f"pid 999999 @ {es._now()}", encoding="utf-8")
        self._stub_gate("01-ideation")
        with self.assertRaises(es.PipelineError) as ctx:
            es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertIn("lock", str(ctx.exception).lower())
        # the operation did not advance the state
        self.assertEqual(es.load_state("signed-anyway", "EP001")["next_stage"],
                         "01-ideation")

    def test_a_stale_lock_is_broken_and_the_operation_proceeds(self):
        lock = self.ep / "episode-state.lock"
        lock.write_text("pid 999999 @ old", encoding="utf-8")
        old = time.time() - es._LOCK_STALE_SECONDS - 60
        os.utime(lock, (old, old))
        self._stub_gate("01-ideation")
        state = es.complete_stage("signed-anyway", "EP001", "01-ideation")
        self.assertEqual(state["next_stage"], "02-research")
        self.assertFalse(lock.exists())  # released after the op

    def test_lock_is_released_even_when_the_operation_raises(self):
        # a gate failure raises inside the lock; the lock must still be freed
        with self.assertRaises(es.PipelineError):
            es.complete_stage("signed-anyway", "EP001", "01-ideation")  # no stub -> gate fails
        self.assertFalse((self.ep / "episode-state.lock").exists())
        # and a retry after fixing the gate works
        self._stub_gate("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")

    def test_log_line_is_written_before_the_state_advance(self):
        self._stub_gate("01-ideation")
        es.complete_stage("signed-anyway", "EP001", "01-ideation")
        log = (self.ep / "episode-state-log.md").read_text(encoding="utf-8")
        self.assertIn("completed 01-ideation", log)
        self.assertIn("next: 02-research", log)


if __name__ == "__main__":
    unittest.main()
