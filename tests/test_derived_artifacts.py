"""Tests for tools/still_claims.py, tools/image_agent_packet.py and tools/storyboard.py.

Includes explicit regression cases for the two upstream defects the port fixes.
"""

import base64
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import still_claims as sc  # noqa: E402
import image_agent_packet as pkt  # noqa: E402
import storyboard as sb  # noqa: E402


# A still prompt in this pipeline's documented shape.  Note "the fountain at
# frame-left" in the environment string: that is the exact text that broke the
# upstream position extractor.
STILL_BODY = (
    "The complete visible cast contains exactly 2 anthropomorphic characters: Bruno and Pip. "
    "Medium two-shot at a cream-brick square with a painted route board and the fountain at "
    "frame-left; warm late-afternoon sunlight, credible brick and paper texture. "
    "Pip's red-wheeled lantern cart, two red wheels and a chipped brass bell fixed to the "
    "handle, is stationary at Pip's side.\n\n"
    "Bruno, an anthropomorphic brown-brindle bulldog in a burnt-orange cardigan, is on the "
    "LEFT, standing upright with one paw resting on the fence post, facing the camera and "
    "gazing at Pip; expression: guarded; mouth closed and relaxed at frame zero. "
    "Pip, an anthropomorphic ginger puppy in his red bandana, is on the RIGHT, seated in the "
    "mud beside the overturned watering can, facing the camera and gazing at Bruno; "
    "expression: hopeful; mouth closed and relaxed at frame zero.\n\n"
    "Soft warm sunlight from screen-right, shallow depth of field, a tender picture-book "
    "warmth, coherent natural four-toed paws."
)
CAST = ["BRUNO", "PIP"]


class PositionExtraction(unittest.TestCase):
    def test_left_slot_is_a_character_not_the_environment(self):
        """Regression: 'the fountain at frame-left' must not claim the LEFT slot.

        The upstream matched slots case-insensitively and reported
        `LEFT = warm late-afternoon sunlight` for every scene in its own
        reference episode.
        """
        slots = dict(sc.positions(STILL_BODY, CAST))
        self.assertIn("LEFT", slots)
        self.assertNotIn("sunlight", slots["LEFT"].lower())
        self.assertIn("BRUNO", slots["LEFT"])
        self.assertIn("standing upright", slots["LEFT"])

    def test_right_slot_binds_to_the_nearest_preceding_name(self):
        slots = dict(sc.positions(STILL_BODY, CAST))
        self.assertIn("PIP", slots["RIGHT"])

    def test_repeated_slot_is_kept_not_dropped(self):
        """Regression: two characters legitimately share CENTER in a group frame."""
        body = ("Ada, a tabby, is at CENTER, standing at the rail. "
                "Bo, a terrier, is at CENTER, perched on the cart rim.")
        found = sc.positions(body, ["ADA", "BO"])
        self.assertEqual(len([s for s, _ in found if s == "CENTER"]), 2)

    def test_a_long_identity_anchor_still_binds_its_slot(self):
        """Regression: identity anchors had to grow to carry fur colour, markings,
        eyes and wardrobe — 'a young anthropomorphic tabby kitten' rendered the
        wrong cat. At the old 220-char lookback the name fell outside the window
        and the slot bound to nobody."""
        body = (
            "Clover, a small anthropomorphic kitten with soft cream and pale-apricot ginger "
            "fur, faint pale ginger tabby markings, a round face, large round dark amber eyes "
            "and a cream muzzle and chest, wearing a green collar with a round gold bell, a "
            "blue-and-white horizontally striped short-sleeve tee with a large green four-leaf "
            "clover embroidered on the chest, and blue denim dungarees with a chest pocket, "
            "brass clasps and rolled cuffs, is on the LEFT, squatting at the front wheel."
        )
        slots = dict(sc.positions(body, ["CLOVER", "BRUNO"]))
        self.assertIn("CLOVER", slots["LEFT"])

    def test_the_nearest_name_still_wins_over_an_earlier_one(self):
        body = ("Pip, a ginger puppy, waits by the cart. "
                "Bruno, an elderly bulldog in a cardigan, is on the RIGHT, seated.")
        slots = dict(sc.positions(body, ["PIP", "BRUNO"]))
        self.assertIn("BRUNO", slots["RIGHT"])

    def test_lowercase_position_words_alone_claim_nothing(self):
        self.assertEqual(sc.positions("the lamp sits at left of the fountain", CAST), [])


class ScanCard(unittest.TestCase):
    def test_card_reports_positions_claims_and_states(self):
        lines = sc.scan_card_lines(STILL_BODY, CAST)
        text = "\n".join(lines)
        self.assertIn("LEFT", text)
        self.assertIn("RIGHT", text)
        self.assertIn("mouth", text)
        self.assertIn("contact", text)

    def test_touched_objects_add_the_frame0_forward_checks(self):
        lines = sc.scan_card_lines(STILL_BODY, CAST, ["the trowel", "the watering can"])
        text = "\n".join(lines)
        self.assertIn("frame-0 fwd", text)
        self.assertIn("the trowel", text)
        self.assertIn("performable", text)

    def test_no_frame0_forward_lines_without_touched_objects(self):
        self.assertNotIn("frame-0 fwd", "\n".join(sc.scan_card_lines(STILL_BODY, CAST)))

    def test_crowd_check_fires_for_three_or_more_cast(self):
        lines = sc.scan_card_lines(STILL_BODY, ["A", "B", "C"])
        self.assertIn("crowd", "\n".join(lines))


class EpisodeFixture(unittest.TestCase):
    """Builds a throwaway episode on disk and runs both tools against it."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_derived_"))
        self.ep = self.tmp / "clover-and-paws" / "EP001"
        (self.ep / "renders" / "stills").mkdir(parents=True)
        (self.ep / "prompts").mkdir(parents=True)
        (self.ep / "_context").mkdir(parents=True)

        (self.ep / "prompts" / "6-image-prompts.md").write_text(
            "## SC01 | pose: Bruno stands at the fence; Pip is seated in the mud.\n"
            "[[BRUNO]] [[PIP]]\n" + STILL_BODY + "\n\n"
            "## SC02 | pose: Bruno lifts the trowel.\n"
            "[[BRUNO]]\n" + STILL_BODY + "\n",
            encoding="utf-8")

        (self.ep / "_context" / "frame0-requirements.json").write_text(json.dumps({
            "schema_version": 1, "episode_id": "EP001", "clips": [
                {"clip": "SC01", "touched_objects": ["the trowel", "the watering can"],
                 "characters": ["BRUNO", "PIP"], "frame0_state": {}, "props_at_rest": {},
                 "first_action_performable": True, "continues_from": None, "end_state": {}},
                {"clip": "SC02", "touched_objects": ["the trowel"],
                 "characters": ["BRUNO"], "frame0_state": {}, "props_at_rest": {},
                 "first_action_performable": True, "continues_from": "SC01", "end_state": {}},
            ]}), encoding="utf-8")

        (self.ep / "prompts" / "7-video-prompts.md").write_text(
            "\n".join([
                "# LTX-2.5 Video Prompts",
                "",
                "## SC01",
                "[[BRUNO]] [[PIP]]",
                'A medium two-shot holds on Bruno at the fence. He grumbles: "Fine. Just for '
                'tonight." The camera begins a slow dolly in toward Bruno.',
                "",
            ]), encoding="utf-8")

        (self.ep / "_context" / "blocking.json").write_text(json.dumps({
            "schema_version": 1, "episode_id": "EP001", "clips": {
                "SC01": {"chars": {}, "props": [{"name": "the trowel", "detail": "a flat dent",
                                                "resting_state": "in the bed"}],
                        "camera": {"shot": "medium two-shot", "movement": "slow dolly in"},
                        "anchors": ["Bruno reaches for the trowel", "Pip's ears droop"],
                        "end_state": {}, "frame0": "rest"}}}), encoding="utf-8")

        # 1x1 PNG so one clip has a still and the other does not.
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
        (self.ep / "renders" / "stills" / "SC01.png").write_bytes(png)

        self._real = pkt.EPISODES_DIR
        pkt.EPISODES_DIR = self.tmp
        sb.EPISODES_DIR = self.tmp

    def tearDown(self):
        pkt.EPISODES_DIR = self._real
        sb.EPISODES_DIR = self._real
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- packet ----------------------------------------------------------
    def test_packet_is_written_with_a_block_per_clip(self):
        self.assertEqual(pkt.build("clover-and-paws", "EP001"), 0)
        text = (self.ep / "prompts" / "6-image-agent-packet.md").read_text(encoding="utf-8")
        self.assertIn("## SC01 | pose:", text)
        self.assertIn("## SC02 | pose:", text)
        self.assertIn("SC01 validation rules:", text)
        self.assertIn("[[BRUNO]] [[PIP]]", text)

    def test_packet_carries_the_verbatim_prompt(self):
        pkt.build("clover-and-paws", "EP001")
        text = (self.ep / "prompts" / "6-image-agent-packet.md").read_text(encoding="utf-8")
        self.assertIn("The complete visible cast contains exactly 2 anthropomorphic characters",
                      text)

    def test_packet_carries_the_frame0_forward_objects(self):
        pkt.build("clover-and-paws", "EP001")
        text = (self.ep / "prompts" / "6-image-agent-packet.md").read_text(encoding="utf-8")
        self.assertIn("frame-0 fwd", text)
        self.assertIn("the watering can", text)

    def test_packet_left_slot_is_not_the_environment(self):
        pkt.build("clover-and-paws", "EP001")
        text = (self.ep / "prompts" / "6-image-agent-packet.md").read_text(encoding="utf-8")
        self.assertNotIn("LEFT  = warm late-afternoon sunlight", text)

    def test_packet_fails_cleanly_without_still_prompts(self):
        (self.ep / "prompts" / "6-image-prompts.md").unlink()
        self.assertEqual(pkt.build("clover-and-paws", "EP001"), 1)

    # ---- storyboard ------------------------------------------------------
    def test_storyboard_is_one_self_contained_file(self):
        self.assertEqual(sb.build("clover-and-paws", "EP001"), 0)
        html = (self.ep / "exports" / "storyboard.html").read_text(encoding="utf-8")
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("data:image/png;base64,", html)
        self.assertNotIn("<script", html)
        self.assertNotIn("src=\"http", html)

    def test_storyboard_marks_a_clip_with_no_still_as_pending(self):
        sb.build("clover-and-paws", "EP001")
        html = (self.ep / "exports" / "storyboard.html").read_text(encoding="utf-8")
        self.assertIn("no approved still yet", html)
        self.assertIn("1 pending", html)

    def test_storyboard_shows_camera_beats_and_dialogue(self):
        sb.build("clover-and-paws", "EP001")
        html = (self.ep / "exports" / "storyboard.html").read_text(encoding="utf-8")
        self.assertIn("slow dolly in", html)
        self.assertIn("Bruno reaches for the trowel", html)
        self.assertIn("Fine. Just for tonight.", html)


class StoryboardDialogueAndWordCount(unittest.TestCase):
    """The first storyboard run happens before 04f writes any clip prompt.

    Without a fallback to the script, that early page shows camera and beats but
    no words — the half of an episode a reader most wants to scan.
    """

    SCRIPT = "\n".join([
        "# EP001 — script",
        "",
        "## CLIP 1 — 0:00–0:20 · a porch · BRUNO, PIP",
        "",
        'Staging prose that happens to mention "a quoted phrase" in a note.',
        "",
        '**BRUNO:** "Fine. Just for tonight."',
        '**PIP:** "Thank you, Bruno!"',
        "",
        "## CLIP 2 — 0:20–0:40 · a porch · BRUNO",
        "",
        '**BRUNO:** "Do not tell anyone I hurried."',
        "",
    ])

    S01 = '"Fine. Just for tonight." "Thank you, Bruno!"'
    S02 = '"Do not tell anyone I hurried."'

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_sb_"))
        self.ep = self.tmp / "clover-and-paws" / "EP001"
        (self.ep / "story").mkdir(parents=True)
        (self.ep / "prompts").mkdir(parents=True)
        (self.ep / "story" / "script.md").write_text(self.SCRIPT, encoding="utf-8")

        # A private profile, so the band under test does not track live config.
        self._eps, self._chan = sb.EPISODES_DIR, sb.CHANNEL_PROFILES_DIR
        sb.EPISODES_DIR = self.tmp
        sb.CHANNEL_PROFILES_DIR = self.tmp / "_profiles"
        (sb.CHANNEL_PROFILES_DIR / "clover-and-paws").mkdir(parents=True)
        (sb.CHANNEL_PROFILES_DIR / "clover-and-paws" / "channel.json").write_text(
            json.dumps({"render": {"spoken_word_band": [4, 6]}}), encoding="utf-8")

    def tearDown(self):
        sb.EPISODES_DIR, sb.CHANNEL_PROFILES_DIR = self._eps, self._chan
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _html(self):
        self.assertEqual(sb.build("clover-and-paws", "EP001"), 0)
        return (self.ep / "exports" / "storyboard.html").read_text(encoding="utf-8")

    def test_script_dialogue_is_shown_with_its_speakers(self):
        html = self._html()
        self.assertIn("Fine. Just for tonight.", html)
        self.assertIn("Do not tell anyone I hurried.", html)
        self.assertIn("BRUNO", html)
        self.assertIn("PIP", html)
        self.assertIn("from script", html)

    def test_storyboard_accepts_three_hash_script_headers_and_derives_pose(self):
        script = self.SCRIPT.replace("## CLIP 1", "### CLIP 1")
        (self.ep / "story" / "script.md").write_text(script, encoding="utf-8")
        (self.ep / "_context").mkdir(exist_ok=True)
        (self.ep / "_context" / "blocking.json").write_text(json.dumps({
            "schema_version": 1, "episode_id": "EP001", "clips": {
                "s01": {
                    "camera": {"shot": "medium", "movement": "slow dolly in"},
                    "anchors": ["a fixed anchor"], "props": [],
                    "frame0_state": {
                        "BRUNO": {"pos": "left", "pose": "standing", "facing": "camera-right"}
                    },
                }
            },
        }), encoding="utf-8")
        html = self._html()
        self.assertIn("Fine. Just for tonight.", html)
        self.assertIn("Bruno: left, standing, camera-right", html)

    def test_prose_quotes_outside_a_speech_line_are_not_dialogue(self):
        """Only a '**NAME:** "…"' line is speech; staging prose is also quoted."""
        self.assertNotIn("a quoted phrase", self._html())

    def test_a_clip_prompt_overrides_the_script(self):
        (self.ep / "prompts" / "7-video-prompts.md").write_text(
            "\n".join([
                "# LTX-2.5 Video Prompts",
                "",
                "## SC01",
                'Bruno mutters: "A line from the prompt, not the script."',
                "",
            ]), encoding="utf-8")
        html = self._html()
        self.assertIn("A line from the prompt, not the script.", html)
        self.assertNotIn("Fine. Just for tonight.", html)

    def test_word_counts_are_per_clip_and_flag_the_band(self):
        html = self._html()
        s01, s02 = sb.spoken_words(self.S01), sb.spoken_words(self.S02)
        self.assertIn(f"{s01} words", html)
        self.assertIn(f"{s02} words", html)
        # the band here is [4, 6]: s01 sits above it, s02 inside it
        self.assertGreater(s01, 6)
        self.assertTrue(4 <= s02 <= 6)
        self.assertIn('class="words out"', html)
        self.assertIn("outside the [4, 6] spoken-word band", html)
        self.assertIn(f"{s01 + s02} spoken words", html)

    def test_a_clip_with_no_dialogue_is_labelled_rather_than_left_blank(self):
        (self.ep / "_context").mkdir(parents=True)
        (self.ep / "_context" / "blocking.json").write_text(json.dumps({
            "schema_version": 1, "episode_id": "EP001", "clips": {
                "SC03": {"chars": {}, "props": [],
                        "camera": {"shot": "wide", "movement": "locked"},
                        "anchors": ["a silent beat"], "end_state": {}, "frame0": "rest"}}}),
            encoding="utf-8")
        self.assertIn("no dialogue", self._html())


if __name__ == "__main__":
    unittest.main()
