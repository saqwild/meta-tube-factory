"""Tests for tools/render_audio_audit.py.

The scenario this guards is the one that actually happened on EP001 (signed-anyway):
render-manifest.json's structural checks (hash/duration/resolution/silence) all passed
clean while two clips' actual spoken audio belonged to a different episode entirely. This
module is the check that would have caught it.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import render_audio_audit as raa  # noqa: E402


def prompts_md(blocks: dict[str, str]) -> str:
    """blocks: {clip_id: body_text_after_header}"""
    return "\n\n".join(f"## {clip}\n{body}" for clip, body in blocks.items())


class ExtractExpectedDialogue(unittest.TestCase):
    def test_single_quote_extracted(self):
        text = prompts_md({"SC01": 'BEAT:: 337 :: Evelyn says, "Robert Kline signed a will."'})
        out = raa.extract_expected_dialogue(text)
        self.assertEqual(out["SC01"], "Robert Kline signed a will.")

    def test_multiple_quotes_in_one_clip_are_joined(self):
        text = prompts_md({
            "SC02": 'BEAT:: 24 :: Evelyn says "Part one of the line here." '
                    'BEAT:: 120 :: Jonah replies "Part two of the reply here."'
        })
        out = raa.extract_expected_dialogue(text)
        self.assertIn("Part one of the line here.", out["SC02"])
        self.assertIn("Part two of the reply here.", out["SC02"])

    def test_no_quote_means_expected_silent(self):
        text = prompts_md({"SC03": "GLOBAL:: no dialogue here, just a settled state."})
        out = raa.extract_expected_dialogue(text)
        self.assertEqual(out["SC03"], "")

    def test_short_incidental_quote_ignored(self):
        text = prompts_md({"SC04": 'A card reading "OK" is visible on the desk.'})
        out = raa.extract_expected_dialogue(text)
        self.assertEqual(out["SC04"], "")

    def test_clip_id_uppercased_and_multiple_blocks_parsed(self):
        text = prompts_md({
            "sc05": 'BEAT:: 100 :: says "Hello there, this is clip five talking."',
            "SC06": 'BEAT:: 100 :: says "Hello there, this is clip six talking now."',
        })
        out = raa.extract_expected_dialogue(text)
        self.assertEqual(set(out.keys()), {"SC05", "SC06"})


class Similarity(unittest.TestCase):
    def test_identical_text_scores_one(self):
        self.assertEqual(raa.similarity("Robert Kline signed a will", "Robert Kline signed a will"), 1.0)

    def test_both_empty_scores_one(self):
        self.assertEqual(raa.similarity("", ""), 1.0)

    def test_one_empty_scores_zero(self):
        self.assertEqual(raa.similarity("something was said", ""), 0.0)
        self.assertEqual(raa.similarity("", "something was said"), 0.0)

    def test_wrong_episode_dialogue_scores_low(self):
        expected = "Robert Kline signed a will his estate's own machine drafted"
        got = "2000 jobs made it to the other side of this their severance didn't"
        self.assertLess(raa.similarity(expected, got), 0.3)

    def test_asr_quirks_still_score_above_threshold(self):
        # "Kline" misheard as "Klein", contraction differences -- expected real-world noise.
        expected = "Robert Kline signed a will his estate's own machine drafted"
        got = "robert klein signed a will his estates own machine drafted"
        self.assertGreaterEqual(raa.similarity(expected, got), raa.DEFAULT_SIMILARITY_THRESHOLD)


class StructuralReasons(unittest.TestCase):
    def test_negation_multiset_counts_contractions_and_not_together(self):
        c = raa.negation_markers("I did not authorize it and I cannot and I won't")
        self.assertEqual(c["NOT"], 3)

    def test_standalone_negatives_counted_separately(self):
        c = raa.negation_markers("no matter the tax, never clever")
        self.assertEqual(c["no"], 1)
        self.assertEqual(c["never"], 1)

    def test_polarity_flip_is_a_reason_even_when_wording_is_close(self):
        reasons = raa.structural_reasons(
            "I did not authorize the transfer", "I did authorize the transfer")
        self.assertTrue(any("negation mismatch" in r for r in reasons))

    def test_matching_negation_no_reason(self):
        self.assertEqual(
            raa.structural_reasons("I did not authorize", "I did not authorise"), [])

    def test_missing_digit_figure_is_a_reason(self):
        reasons = raa.structural_reasons(
            "the estate was billed 22,000 dollars", "the estate was billed some money")
        self.assertTrue(any("22000" in r for r in reasons))

    def test_single_digits_are_not_checked(self):
        self.assertEqual(
            raa.structural_reasons("he had 8 minutes", "he had eight minutes"), [])


class AuditClips(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_audio_audit_"))
        for name in ("sc01.mp4", "sc02.mp4", "sc03.mp4"):
            (self.tmp / name).write_bytes(b"not a real video, just needs to exist")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_matching_dialogue_passes(self):
        expected = {"SC01": "Robert Kline signed a will his estate's own machine drafted"}
        clips = [("SC01", self.tmp / "sc01.mp4")]
        fake = lambda p: "Robert Kline signed a will his estate's own machine drafted"
        results = raa.audit_clips(clips, expected, fake)
        self.assertEqual(results[0].status, "PASS")

    def test_wrong_dialogue_fails(self):
        expected = {"SC01": "Robert Kline signed a will his estate's own machine drafted"}
        clips = [("SC01", self.tmp / "sc01.mp4")]
        fake = lambda p: "2000 jobs made it to the other side their severance didn't"
        results = raa.audit_clips(clips, expected, fake)
        self.assertEqual(results[0].status, "FAIL")

    def test_polarity_flip_fails_despite_high_similarity(self):
        # The canonical regression: one word changed, ratio well above threshold,
        # but the meaning is inverted -- must FAIL on the negation mismatch.
        expected = {"SC01": "I did not authorize the transfer of any funds that day"}
        clips = [("SC01", self.tmp / "sc01.mp4")]
        fake = lambda p: "I did authorize the transfer of any funds that day"
        results = raa.audit_clips(clips, expected, fake)
        self.assertGreater(results[0].score, raa.DEFAULT_SIMILARITY_THRESHOLD)
        self.assertEqual(results[0].status, "FAIL")
        self.assertTrue(any("negation" in r for r in results[0].reasons))

    def test_silent_clip_with_no_speech_passes(self):
        expected = {"SC02": ""}
        clips = [("SC02", self.tmp / "sc02.mp4")]
        fake = lambda p: ""
        results = raa.audit_clips(clips, expected, fake)
        self.assertEqual(results[0].status, "SILENT_OK")

    def test_silent_clip_that_actually_spoke_flags(self):
        expected = {"SC02": ""}
        clips = [("SC02", self.tmp / "sc02.mp4")]
        fake = lambda p: "someone is clearly speaking a full sentence in this silent clip"
        results = raa.audit_clips(clips, expected, fake)
        self.assertEqual(results[0].status, "SILENT_BUT_SPOKE")

    def test_missing_file_flagged_without_calling_transcriber(self):
        expected = {"SC99": "some line"}
        clips = [("SC99", self.tmp / "does_not_exist.mp4")]
        calls = []
        fake = lambda p: (calls.append(p), "unused")[1]
        results = raa.audit_clips(clips, expected, fake)
        self.assertEqual(results[0].status, "MISSING")
        self.assertEqual(calls, [])


class ReviewEpisode(unittest.TestCase):
    """End-to-end through review_episode(), with the real Muse transcriber swapped out."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_audio_audit_ep_"))
        self.ep = self.tmp / "demo" / "EP001"
        (self.ep / "renders").mkdir(parents=True)
        (self.ep / "prompts").mkdir(parents=True)
        (self.ep / "renders" / "clip01.mp4").write_bytes(b"stub")

        manifest = {"clips": [{"clip": "SC01", "path": "renders/clip01.mp4"}]}
        (self.ep / "renders" / "render-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8")
        (self.ep / "prompts" / "7-video-prompts.md").write_text(
            prompts_md({"SC01": 'BEAT:: 100 :: Evelyn says "Robert Kline signed a will."'}),
            encoding="utf-8")

        self._real_episodes_dir = raa.EPISODES_DIR
        raa.EPISODES_DIR = self.tmp
        self._real_transcriber_factory = raa._muse_transcriber

    def tearDown(self):
        raa.EPISODES_DIR = self._real_episodes_dir
        raa._muse_transcriber = self._real_transcriber_factory
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_passes_when_transcript_matches(self):
        raa._muse_transcriber = lambda model_name: (lambda p: "Robert Kline signed a will.")
        code = raa.review_episode("demo", "EP001", model_name="muse-voice-transcribe-1.0")
        self.assertEqual(code, 0)

    def test_fails_when_transcript_is_a_different_episode(self):
        raa._muse_transcriber = lambda model_name: (
            lambda p: "2000 jobs made it to the other side of this their severance didn't")
        code = raa.review_episode("demo", "EP001", model_name="muse-voice-transcribe-1.0")
        self.assertEqual(code, 1)

    def test_missing_manifest_is_a_setup_error(self):
        (self.ep / "renders" / "render-manifest.json").unlink()
        code = raa.review_episode("demo", "EP001", model_name="muse-voice-transcribe-1.0")
        self.assertEqual(code, 2)

    def test_emit_review_writes_artifact(self):
        raa._muse_transcriber = lambda model_name: (lambda p: "Robert Kline signed a will.")
        raa.review_episode("demo", "EP001", model_name="muse-voice-transcribe-1.0", emit_review=True)
        out = self.ep / "renders" / "audio-content-audit.json"
        self.assertTrue(out.exists())
        doc = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(doc["status"], "PASS")
        self.assertEqual(len(doc["clips"]), 1)

    def test_output_is_ascii_safe(self):
        src = (ROOT / "tools" / "render_audio_audit.py").read_text(encoding="utf-8")
        for i, line in enumerate(src.splitlines(), 1):
            if "print(" in line:
                self.assertTrue(all(ord(c) < 128 for c in line),
                                f"non-ASCII in printed output at line {i}: {line.strip()}")


if __name__ == "__main__":
    unittest.main()
