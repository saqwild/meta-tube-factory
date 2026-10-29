"""Regression suite for tools/ltx_prompt_validator.py.

Every test either proves a known-good prompt passes clean, or proves one
specific LTXV rule fires on the exact defect it exists to catch.  Add a case
with any new rule.

    python -m unittest discover -s tests -v
"""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import ltx_prompt_validator as v  # noqa: E402


# A clip prompt that satisfies the owner-locked relay contract. Every negative
# test below is this prompt with exactly one thing broken, so a failure names
# its own cause.
GOOD = (
    "GLOBAL:: Continue from the still. Bruno, the elderly bulldog-mastiff mix in his burnt-orange "
    "cardigan, stands at the garden fence with Pip, the ginger puppy in his red bandana, seated "
    "in the mud beside him. Warm late-afternoon light rests on the fence and overturned watering "
    "can. Photoreal anthropomorphic cozy family look, warm daylight, cream-and-soft-wood palette. "
    "Low motion.\n"
    "BEAT:: 24 :: Bruno's paw slides along the fence rail toward the overturned watering can. "
    "Ambient (slow, subtle): sunlight shifts across the garden bed and the carrot tops sway faintly.\n"
    "BEAT:: 169 :: Bruno's paw tightens on the trowel handle and he grumbles, gruff but wavering, "
    "in a steady gravelly American English elder voice: \"In my day, dogs didn't need rescuing.\" "
    "Pip watches quietly, mouth closed, ears drooping.\n"
    "BEAT:: 168 :: Bruno's ears droop and he mutters: \"Oh, fine. Just for tonight.\" After "
    "speaking, Bruno's mouth closes naturally and he stays rooted at the fence, one paw resting "
    "on the post.\n"
    "BEAT:: 120 :: The camera begins a slow dolly in toward Bruno and Pip. Acoustic environment: "
    "a light warm garden room tone with faint birdsong and the scrape of Bruno's paw on the wooden "
    "rail; clear close dialogue front and center."
)

KWARGS = dict(
    character_first_names=("Bruno", "Pip"),
    visible_character_count=2,
    voice_signatures={"Bruno": "steady gravelly American English elder voice"},
    spoken_word_band=(10, 15),
    anthropomorphic_channel=True,
    style_echo="Photoreal anthropomorphic cozy family look, warm daylight, "
               "cream-and-soft-wood palette",
)


def review(prompt: str, **overrides):
    kwargs = {**KWARGS, **overrides}
    return v.validate_prompt(prompt, **kwargs)


def rule_ids(result) -> set[str]:
    return set(result.as_dict()["facts"]["emitted_rule_ids"])


class HappyPath(unittest.TestCase):
    def test_clean_prompt_passes_with_no_errors(self):
        result = review(GOOD)
        self.assertEqual(result.errors, [], msg="\n".join(result.errors))
        self.assertTrue(result.passed)

    def test_facts_are_reported(self):
        facts = review(GOOD).as_dict()["facts"]
        self.assertTrue(facts["has_dialogue"])
        self.assertEqual(facts["spoken_word_count"], 12)
        self.assertGreater(facts["total_word_count"], 100)


class FormatRules(unittest.TestCase):
    def test_d001_requires_the_locked_relay_structure(self):
        bad = "Bruno reaches for the trowel in a warm garden."
        self.assertIn("LTXV-D001", rule_ids(review(bad)))

    def test_d002_requires_beat_frames_to_sum_to_the_locked_total(self):
        bad = GOOD.replace("BEAT:: 120 ::", "BEAT:: 119 ::")
        self.assertIn("LTXV-D002", rule_ids(review(bad)))

    def test_d002_rejects_unstructured_seconds_inside_a_beat(self):
        bad = GOOD.replace("Bruno's ears droop", "At 4.5 seconds Bruno's ears droop")
        self.assertIn("LTXV-D002", rule_ids(review(bad)))

    def test_d003_rejects_render_config_in_text(self):
        for token in ("shot at 24 fps", "1344x768", "aspect ratio 16:9", "a ~20 second clip"):
            with self.subTest(token=token):
                self.assertIn("LTXV-D003", rule_ids(review(GOOD + " " + token + ".")))

    def test_d004_warns_past_runaway_word_tripwire(self):
        padded = GOOD + " " + ("Bruno shifts his weight on the worn rail. " * 60)
        result = review(padded)
        self.assertGreater(result.facts["total_word_count"], 450)
        self.assertIn("LTXV-D004", rule_ids(result))
        self.assertTrue(any("LTXV-D004" in w for w in result.warnings))

    def test_d004_silent_on_a_dense_three_hander(self):
        dense = GOOD + " " + (
            "Clover, the cream-tabby kitten in a green cardigan, watches Bruno and Pip from "
            "the garden gate, her paw resting steadily on its painted latch. "
            "Clover looks from the bent fence rail to the overturned watering can and says, "
            "brightly: \"We can put it back together before sunset.\" "
            "Bruno raises the trowel only enough to point at the loose soil, then lowers it "
            "again as Pip leans closer without touching the can. "
            "Pip studies the muddy path, ears lifting, and says: \"The little stones show "
            "which way it rolled.\" "
            "Clover keeps both paws visible on the gate latch and listens while the birdsong "
            "continues softly beyond the carrot tops. "
            "Bruno glances toward Clover, his mouth closed between words, and says: \"Then "
            "we follow the stones, slowly and together.\" "
            "Camera settles into a three-shot as Bruno, Pip, and Clover look down at the path. "
        )
        result = review(
            dense,
            character_first_names=("Bruno", "Pip", "Clover"),
            visible_character_count=3,
            spoken_word_band=(10, 40),
        )
        self.assertGreaterEqual(result.facts["total_word_count"], 260)
        self.assertLessEqual(result.facts["total_word_count"], 330)
        self.assertNotIn("LTXV-D004", rule_ids(result))
        self.assertIn("total_word_count", result.facts)
        self.assertIn("spoken_word_count", result.facts)


class PositiveOnlyDiscipline(unittest.TestCase):
    def test_d010_rejects_caption_suppression_clause(self):
        bad = GOOD + " No added captions, subtitles or overlay text."
        self.assertIn("LTXV-D010", rule_ids(review(bad)))

    def test_d010_rejects_no_new_characters(self):
        bad = GOOD + " No new characters enter the frame."
        self.assertIn("LTXV-D010", rule_ids(review(bad)))

    def test_d010_ignores_negation_inside_quoted_dialogue(self):
        # "dogs didn't need rescuing" is spoken, not an instruction to the model.
        self.assertNotIn("LTXV-D010", rule_ids(review(GOOD)))

    def test_d011_rejects_static_scene_token(self):
        bad = GOOD.replace("Low motion.", "Static scene.")
        self.assertIn("LTXV-D011", rule_ids(review(bad)))

    def test_d012_rejects_onscreen_text_request(self):
        bad = GOOD + " A title card reads Paw Street."
        self.assertIn("LTXV-D012", rule_ids(review(bad)))

    def test_d013_rejects_pipeline_jargon(self):
        bad = GOOD + " Per blocking.json the pose is locked."
        self.assertIn("LTXV-D013", rule_ids(review(bad)))


class RequiredClauses(unittest.TestCase):
    def test_d020_requires_ambient_sentence(self):
        bad = GOOD.replace(
            "Ambient (slow, subtle): sunlight shifts across the garden bed and the carrot "
            "tops sway faintly.", "")
        self.assertIn("LTXV-D020", rule_ids(review(bad)))

    def test_d021_requires_acoustic_sentence(self):
        bad = GOOD.replace("Acoustic environment: a", "The sound is a")
        self.assertIn("LTXV-D021", rule_ids(review(bad)))

    def test_d022_rejects_merged_ambient_and_acoustic(self):
        merged = GOOD.replace(
            "Ambient (slow, subtle): sunlight shifts across the garden bed and the carrot "
            "tops sway faintly.",
            "Ambient (slow, subtle): the carrot tops sway while Acoustic environment: warm garden room tone.",
        )
        self.assertIn("LTXV-D022", rule_ids(review(merged)))

    def test_d023_requires_dialogue_mix_note(self):
        bad = GOOD.replace("; clear close dialogue front and center", "")
        self.assertIn("LTXV-D023", rule_ids(review(bad)))

    def test_d024_requires_camera_movement(self):
        bad = GOOD.replace("The camera begins a slow dolly in toward Bruno and Pip. ", "")
        self.assertIn("LTXV-D024", rule_ids(review(bad)))

    def test_d024_accepts_an_arc_around_the_group(self):
        arc = GOOD.replace(
            "The camera begins a slow dolly in toward Bruno and Pip.",
            "The camera makes a slow arc around the group toward camera-left.")
        self.assertNotIn("LTXV-D024", rule_ids(review(arc)))

    def test_d025_rejects_camera_move_sharing_a_sentence_with_dialogue(self):
        bad = GOOD.replace(
            "Bruno's ears droop and he mutters: \"Oh, fine. Just for tonight.\"",
            "The camera pans as Bruno's ears droop and he mutters: \"Oh, fine.\"")
        self.assertIn("LTXV-D025", rule_ids(review(bad)))


class DialogueRules(unittest.TestCase):
    def test_d030_rejects_labelled_dialogue_block(self):
        bad = GOOD + "\nSpoken dialogue, lip-synced:\nBruno: \"Fine.\""
        self.assertIn("LTXV-D030", rule_ids(review(bad)))

    def test_d031_requires_a_visible_action_on_each_line(self):
        bad = GOOD.replace(
            "Bruno's paw tightens on the trowel handle and he grumbles, gruff but "
            "wavering, in a steady gravelly American English elder voice:",
            "Bruno says, resigned, in a steady gravelly American English elder voice:")
        self.assertIn("LTXV-D031", rule_ids(review(bad)))

    def test_d033_rejects_repeated_voice_signature(self):
        bad = GOOD.replace(
            "Bruno's ears droop and he mutters:",
            "Bruno's ears droop and, in a steady gravelly American English "
            "elder voice, he mutters:")
        self.assertIn("LTXV-D033", rule_ids(review(bad)))

    def test_d034_enforces_the_channel_spoken_word_band(self):
        self.assertIn("LTXV-D034", rule_ids(review(GOOD, spoken_word_band=(30, 33))))

    def test_d035_rejects_the_word_narrator(self):
        bad = GOOD + " A Narrator explains the moment."
        self.assertIn("LTXV-D035", rule_ids(review(bad)))

    def test_d036_requires_a_closed_mouth_clause_for_non_speakers(self):
        bad = GOOD.replace("Pip watches quietly, mouth closed, ears drooping.",
                           "Pip watches quietly, ears drooping.")
        self.assertIn("LTXV-D036", rule_ids(review(bad)))

    def test_d036_accepts_a_named_plural_closed_mouth_clause(self):
        good = GOOD.replace(
            "Pip watches quietly, mouth closed, ears drooping.",
            "Pip and Clover watch quietly, their mouths closed, ears drooping.")
        self.assertNotIn("LTXV-D036", rule_ids(review(good)))

    def test_d036_does_not_fire_for_a_solo_character(self):
        self.assertNotIn("LTXV-D036", rule_ids(review(GOOD, visible_character_count=1)))


class ProseRules(unittest.TestCase):
    def test_d040_requires_the_first_sentence_to_name_a_character(self):
        bad = GOOD.replace(
            GOOD.splitlines()[0],
            "GLOBAL:: Continue from the still. The garden fence sits in warm light. Low motion.",
        )
        self.assertIn("LTXV-D040", rule_ids(review(bad)))

    def test_d041_requires_the_final_beat_to_name_a_character(self):
        bad = GOOD.replace(
            "BEAT:: 120 :: The camera begins a slow dolly in toward Bruno and Pip. Acoustic environment: "
            "a light warm garden room tone with faint birdsong and the scrape of Bruno's paw on the wooden "
            "rail; clear close dialogue front and center.",
            "BEAT:: 120 :: The camera begins a slow dolly in. Acoustic environment: a light warm garden "
            "room tone with faint birdsong and a soft rail scrape; clear close dialogue front and center.",
        )
        self.assertIn("LTXV-D041", rule_ids(review(bad)))

    def test_d040_d041_invert_when_nobody_is_visible(self):
        # No one visible at frame 0: naming a character in the picture text invites a stranger (EP001 SC13/15/29).
        self.assertTrue({"LTXV-D040", "LTXV-D041"} <= set(rule_ids(review(GOOD, visible_character_count=0))))
        empty = (GOOD.replace(GOOD.splitlines()[0],
                              "GLOBAL:: Continue from the still. The garden fence sits in warm light, the yard "
                              "empty and unattended. Low motion.")
                 .replace("BEAT:: 120 :: The camera begins a slow dolly in toward Bruno and Pip. Acoustic "
                          "environment: a light warm garden room tone with faint birdsong and the scrape of "
                          "Bruno's paw on the wooden rail; clear close dialogue front and center.",
                          "BEAT:: 120 :: The camera begins a slow dolly in on the empty fence. Acoustic "
                          "environment: a light warm garden room tone with faint birdsong; clear close dialogue "
                          "front and center."))
        ids = rule_ids(review(empty, visible_character_count=0))
        self.assertNotIn("LTXV-D040", ids)
        self.assertNotIn("LTXV-D041", ids)

    def test_d041_tolerates_a_trailing_style_echo(self):
        # GOOD ends on a style sentence naming no character; that must not fire.
        self.assertNotIn("LTXV-D041", rule_ids(review(GOOD)))

    def test_d042_rejects_unqualified_background_species(self):
        bad = GOOD + " Bruno glances at the neighbours passing the gate."
        self.assertIn("LTXV-D042", rule_ids(review(bad)))

    def test_d042_accepts_an_explicitly_anthropomorphic_crowd(self):
        ok = GOOD + (" Bruno glances at two anthropomorphic animal neighbours passing the "
                     "gate.")
        self.assertNotIn("LTXV-D042", rule_ids(review(ok)))

    def test_d043_rejects_literal_reader_traps(self):
        bad = GOOD.replace("Bruno's paw slides along the fence rail",
                           "the glint catches his eye")
        self.assertIn("LTXV-D043", rule_ids(review(bad)))

    def test_d044_warns_on_bare_duration_filler(self):
        bad = GOOD.replace("Pip watches quietly, mouth closed, ears drooping.",
                           "Pip watches quietly, mouth closed. A long beat. He waits.")
        self.assertIn("LTXV-D044", rule_ids(review(bad)))


class MultiShotRules(unittest.TestCase):
    def test_d050_rejects_unmarked_cut_language_in_a_single_take(self):
        bad = GOOD + " A hard cut transitions to the porch."
        self.assertIn("LTXV-D050", rule_ids(review(bad)))

    def test_d051_requires_audio_continuity_on_a_declared_cut(self):
        bad = GOOD + " A hard cut transitions to a close-up of Bruno's paw on the rail."
        result = review(bad, declared_cuts=1)
        self.assertIn("LTXV-D051", rule_ids(result))

    def test_declared_cut_with_audio_continuity_passes(self):
        ok = (GOOD + " A hard cut transitions to a close-up of Bruno's paw on the rail; the "
                     "garden room tone continues across the cut.")
        result = review(ok, declared_cuts=1)
        self.assertNotIn("LTXV-D051", rule_ids(result))


BLOCK = {
    "clip": "SC07",
    "touched_objects": ["the trowel", "the watering can"],
    "characters": ["BRUNO", "PIP"],
    "frame0_state": {
        "BRUNO": {"pos": "left", "facing": "camera-left three-quarter", "gaze": "at Pip",
                  "pose": "standing at the fence", "expression": "guarded",
                  "mouth": "closed", "hands": "empty"},
        "PIP": {"pos": "right", "facing": "camera", "gaze": "up at Bruno",
                "pose": "seated in the mud", "expression": "hopeful",
                "mouth": "closed", "hands": "empty"},
    },
    "props_at_rest": {
        "the trowel": "lying flat in the garden bed",
        "the watering can": "on its side, spout camera-right",
    },
    "first_action_performable": True,
    "continues_from": None,
}

PROSE_WITH_PROPS = GOOD.replace("the overturned watering can",
                                "the overturned watering can and the trowel")


class Frame0Requirements(unittest.TestCase):
    def test_complete_block_passes(self):
        self.assertEqual(
            v.validate_frame0_requirements(PROSE_WITH_PROPS, BLOCK,
                                           blocking_characters=("BRUNO", "PIP")),
            [])

    def test_s001_flags_a_missing_field(self):
        block = {k: val for k, val in BLOCK.items() if k != "props_at_rest"}
        errors = v.validate_frame0_requirements(PROSE_WITH_PROPS, block)
        self.assertTrue(any("LTXV-S001" in e for e in errors))

    def test_s001_requires_an_explicit_mouth_state(self):
        block = {**BLOCK, "frame0_state": {
            **BLOCK["frame0_state"],
            "PIP": {**BLOCK["frame0_state"]["PIP"], "mouth": ""},
        }}
        errors = v.validate_frame0_requirements(PROSE_WITH_PROPS, block)
        self.assertTrue(any("LTXV-S001" in e and "mouth" in e for e in errors))

    def test_s001_requires_the_first_action_to_be_performable(self):
        block = {**BLOCK, "first_action_performable": False}
        errors = v.validate_frame0_requirements(PROSE_WITH_PROPS, block)
        self.assertTrue(any("performable" in e for e in errors))

    def test_s002_flags_a_touched_object_with_no_resting_state(self):
        block = {**BLOCK, "touched_objects": ["the trowel", "the watering can", "the kettle"]}
        errors = v.validate_frame0_requirements(PROSE_WITH_PROPS, block)
        self.assertTrue(any("LTXV-S002" in e and "kettle" in e for e in errors))

    def test_s003_flags_a_cast_mismatch_against_blocking(self):
        errors = v.validate_frame0_requirements(
            PROSE_WITH_PROPS, BLOCK, blocking_characters=("BRUNO",))
        self.assertTrue(any("LTXV-S003" in e for e in errors))


class Continuity(unittest.TestCase):
    def test_s004_flags_a_broken_handoff(self):
        s06 = {"end_state": {"BRUNO": {"pos": "left", "pose": "kneeling", "hands": "empty"}}}
        s07 = {"continues_from": "SC06",
               "frame0_state": {"BRUNO": {"pos": "left", "pose": "standing", "hands": "empty"}}}
        failures = v.validate_continuity([("SC06", s06), ("SC07", s07)])
        self.assertIn("SC07", failures)
        self.assertTrue(any("LTXV-S004" in f for f in failures["SC07"]))

    def test_matching_handoff_passes(self):
        s06 = {"end_state": {"BRUNO": {"pos": "left", "pose": "standing", "hands": "empty"}}}
        s07 = {"continues_from": "SC06",
               "frame0_state": {"BRUNO": {"pos": "left", "pose": "standing", "hands": "empty"}}}
        self.assertEqual(v.validate_continuity([("SC06", s06), ("SC07", s07)]), {})

    def test_s004_allows_an_off_screen_character_to_appear_across_a_cut(self):
        off = {"pos": "left", "pose": "off-screen POV observer; not drawn in frame", "hands": "empty, off-screen"}
        s06 = {"end_state": {"BRUNO": off}}
        s07 = {"continues_from": "SC06",
               "frame0_state": {"BRUNO": {"pos": "right", "pose": "standing", "hands": "empty"}}}
        self.assertEqual(v.validate_continuity([("SC06", s06), ("SC07", s07)]), {})


class OffScreenEntry(unittest.TestCase):
    OFF_BLOCK = {**BLOCK, "frame0_state": {
        **BLOCK["frame0_state"],
        "PIP": {**BLOCK["frame0_state"]["PIP"], "pose": "off-screen POV observer; not drawn in frame"},
    }}

    def test_s003_flags_an_off_screen_character_entering_the_frame(self):
        prose = PROSE_WITH_PROPS + " The camera holds as Pip leans back into frame at the edge."
        errors = v.validate_frame0_requirements(prose, self.OFF_BLOCK)
        self.assertTrue(any("LTXV-S003" in e and "off-screen" in e for e in errors))

    def test_s003_allows_an_on_screen_character_to_step_into_view(self):
        prose = PROSE_WITH_PROPS + " Bruno steps into view of the gate."
        errors = v.validate_frame0_requirements(prose, self.OFF_BLOCK)
        self.assertFalse(any("off-screen at frame 0" in e for e in errors))


class StateTransition(unittest.TestCase):
    def test_s005_flags_an_already_completed_action(self):
        still = "The cottage door is already open, warm light spilling onto the step."
        clip = "Bruno knocks twice and waits, ears forward."
        errors = v.validate_state_transition(still, clip)
        self.assertTrue(any("LTXV-S005" in e for e in errors))

    def test_a_legal_start_state_transition_passes(self):
        still = "The cottage door is closed, paint peeling at the hinge."
        clip = "Bruno pushes the door open and steps through, ears forward."
        self.assertEqual(v.validate_state_transition(still, clip), [])


class StillGroundingFacts(unittest.TestCase):
    FACTS = [{
        "clip": "SC02", "character": "BRUNO", "detail": "glasses",
        "confirmed_state_pattern": r"glasses[^.]{0,40}\bface\b",
        "contradicting_pattern": r"glasses[^.]{0,40}\bchain\b",
        "source": "test fixture",
    }]

    def test_d055_flags_a_reverted_confirmed_override(self):
        prompt = "Bruno adjusts his glasses on a thin bronze chain at his chest and looks up."
        errors = v.validate_still_grounding_facts(prompt, "SC02", self.FACTS)
        self.assertTrue(any("LTXV-D055" in e for e in errors))

    def test_d055_passes_when_the_override_is_intact(self):
        prompt = "Bruno adjusts his glasses worn on his face and looks up."
        self.assertEqual(v.validate_still_grounding_facts(prompt, "SC02", self.FACTS), [])

    def test_d055_no_facts_for_this_clip_is_a_silent_skip(self):
        prompt = "Bruno adjusts his glasses on a thin bronze chain at his chest and looks up."
        self.assertEqual(v.validate_still_grounding_facts(prompt, "SC02", []), [])


class PropStateContinuity(unittest.TestCase):
    PROPS = [{"name": "the adjustable wrench", "detail": "x", "resting_state": "x"}]
    BUGGY = (
        "GLOBAL:: Continue from the still. Fin is left, kneeling on the porch, the oversized "
        "wrench turned face-up across both his paws. Clover is right. Low motion.\n"
        "BEAT:: 24 :: Fin turns the wrench over and sets it down flat on the porch boards. "
        "Ambient (slow, subtle): dust turns in the light.\n"
        "BEAT:: 169 :: Fin is kneeling on the porch, the wrench in his paws. Fin sets the "
        "wrench down and turns to Clover and says, in a steady voice: "
        "\"I have rounded the nut off.\". Clover keeps still, mouth closed.\n"
        "BEAT:: 168 :: Clover looks up and says, in a bright voice: "
        "\"It still has to hang straight.\". Clover stays kneeling, still in frame.\n"
        "BEAT:: 120 :: The camera performs a slow dolly in. Acoustic environment: a warm "
        "porch room tone, birdsong; clear close dialogue front and center."
    )

    def test_d056_flags_an_invisible_regrab_across_beats(self):
        r = v.validate_prompt(self.BUGGY, props=self.PROPS)
        self.assertTrue(any("LTXV-D056" in e for e in r.errors))

    def test_d056_clears_when_the_later_beat_reflects_the_rested_state(self):
        fixed = self.BUGGY.replace(
            "Fin is kneeling on the porch, the wrench in his paws. Fin sets the wrench down "
            "and turns to Clover and says",
            "Fin is kneeling on the porch beside the wrench, now resting flat on the boards. "
            "Fin turns to Clover and says")
        r = v.validate_prompt(fixed, props=self.PROPS)
        self.assertFalse(any("LTXV-D056" in e for e in r.errors))

    def test_d056_clears_with_an_explicit_pickup_verb(self):
        fixed = self.BUGGY.replace(
            "Fin is kneeling on the porch, the wrench in his paws. Fin sets the wrench down "
            "and turns to Clover and says",
            "Fin is kneeling on the porch. Fin picks the wrench back up, sets it down again "
            "and turns to Clover and says")
        r = v.validate_prompt(fixed, props=self.PROPS)
        self.assertFalse(any("LTXV-D056" in e for e in r.errors))

    def test_d056_skips_silently_with_no_props(self):
        r = v.validate_prompt(self.BUGGY, props=())
        self.assertFalse(any("LTXV-D056" in e for e in r.errors))
        self.assertIn("LTXV-D056", r.skipped)


STILL = (
    "## SC07 | pose: Bruno stands at the fence; Pip is seated in the mud.\n"
    "[[BRUNO]] [[PIP]]\n"
    "The complete visible cast contains exactly 2 anthropomorphic characters: Bruno and Pip. "
    "Medium two-shot at the garden fence. The trowel lies flat in the garden bed, blade "
    "half-buried. The watering can rests on its side, spout pointing camera-right. "
    "Bruno is on the LEFT, standing upright, mouth closed at frame zero. "
    "Pip is on the RIGHT, seated in the mud, mouth closed at frame zero."
)


class StillCoversRequirements(unittest.TestCase):
    def test_a_correct_still_passes(self):
        self.assertEqual(v.validate_still_covers_requirements(STILL, BLOCK), [])

    def test_s006_flags_a_still_bound_to_the_wrong_clip(self):
        bad = STILL.replace("## SC07", "## SC08")
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "wrong clip" in e for e in errors))

    def test_s006_flags_a_missing_touched_object(self):
        bad = STILL.replace("The watering can rests on its side, spout pointing camera-right. ", "")
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "watering can" in e for e in errors))

    def test_s006_flags_baked_motion_in_a_still(self):
        bad = STILL.replace("standing upright", "reaching for the trowel")
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "settled" in e for e in errors))

    def test_s006_allows_opening_as_a_noun(self):
        """Locked environment strings name doorways: "an arched opening", "whose opening is dim"."""
        for phrase in ("an arched opening glows beyond the fence.",
                       "a tunnel whose opening is dim grey inside."):
            ok = STILL.replace("Medium two-shot at the garden fence.", "Medium two-shot at the garden fence, " + phrase)
            errors = v.validate_still_covers_requirements(ok, BLOCK)
            self.assertFalse(any("motion verb" in e for e in errors), (phrase, errors))

    def test_s006_still_flags_opening_as_a_verb(self):
        bad = STILL.replace("standing upright", "standing upright as the gate is opening")
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "'opening'" in e for e in errors))

    def test_s006_flags_a_character_absent_from_the_still(self):
        bad = STILL.replace("Pip is on the RIGHT, seated in the mud, mouth closed at frame zero.", "")
        bad = bad.replace("Bruno and Pip", "Bruno")
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "PIP" in e for e in errors))

    def test_s006_ignores_a_name_present_only_in_metadata(self):
        """A [[TAG]] binds identity but stages nothing, and the `| pose:` note is
        packet metadata the image model never sees. Neither may satisfy the prose
        check — Pip appears in both here and in no describing sentence."""
        bad = (
            "## SC07 | pose: Bruno stands at the fence; Pip is seated in the mud.\n"
            "[[BRUNO]] [[PIP]]\n"
            "Medium two-shot at the garden fence. The trowel lies flat in the garden bed. "
            "The watering can rests on its side. "
            "Bruno is on the LEFT, standing upright, mouth closed at frame zero."
        )
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "PIP" in e for e in errors))

    def test_s006_flags_a_still_with_no_clip_header(self):
        bad = "\n".join(STILL.splitlines()[1:])
        errors = v.validate_still_covers_requirements(bad, BLOCK)
        self.assertTrue(any("LTXV-S006" in e and "cannot be bound" in e for e in errors))


class RuleDeclaration(unittest.TestCase):
    def test_every_emitted_rule_is_declared(self):
        with self.assertRaises(ValueError):
            v._rule_message("LTXV-D999", "undeclared")


class CliEpisodeReview(unittest.TestCase):
    """The `python tools/ltx_prompt_validator.py --channel .. --episode ..` path
    that stage 04f3 and the writer skill invoke. Regression: for months this
    module had no __main__, so that documented command was a silent no-op."""

    def _episode(self, tmp, prompt_body, *, band=(10, 15)):
        root = Path(tmp)
        chan = root / "channel_profiles" / "tc"
        chan.mkdir(parents=True)
        (chan / "channel.json").write_text(json.dumps({
            "slug": "tc",
            "render": {
                "prompt_format": "prompt_relay_beats_v1",
                "spoken_word_band": list(band),
                "style_echo": KWARGS["style_echo"],
                "max_prompt_words": 450,
            },
            "hard_safety_floor": ["every background character is an anthropomorphic animal"],
        }), encoding="utf-8")
        ep = root / "episodes" / "tc" / "EP001" / "prompts"
        ep.mkdir(parents=True)
        (ep / "7-video-prompts.md").write_text(
            f"## SC01\n[[BRUNO]] [[PIP]]\n{prompt_body}\n", encoding="utf-8")
        return root

    def test_clean_episode_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, GOOD)
            rc = v.review_episode("tc", "EP001", root=root)
        self.assertEqual(rc, 0)

    def test_a_broken_clip_returns_one(self):
        bad = GOOD.replace("BEAT:: 120 ::", "BEAT:: 121 ::")
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, bad)
            rc = v.review_episode("tc", "EP001", root=root)
        self.assertEqual(rc, 1)

    def test_missing_profile_returns_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = v.review_episode("nope", "EP001", root=Path(tmp))
        self.assertEqual(rc, 2)

    def test_emit_review_writes_a_schema_shaped_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, GOOD)
            v.review_episode("tc", "EP001", root=root, emit_review=True)
            doc = json.loads((root / "episodes" / "tc" / "EP001" / "_context"
                              / "ltx-prompt-review.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["status"], "PASS")
        self.assertEqual(doc["clips"][0]["clip"], "SC01")
        self.assertEqual(len(doc["validator_sha256"]), 64)

    # ── draft vs strict: missing inputs ──────────────────────────────────

    def test_draft_run_with_missing_inputs_passes_but_records_the_gap(self):
        """No blocking.json, no frame0-requirements, no still -> a draft run may
        PASS, but the emitted review must say so and list the rules it skipped."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, GOOD)
            rc = v.review_episode("tc", "EP001", root=root, emit_review=True)
            doc = json.loads((root / "episodes" / "tc" / "EP001" / "_context"
                              / "ltx-prompt-review.json").read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(doc["mode"], "draft")
        clip = doc["clips"][0]
        self.assertTrue(clip["input_gaps"], "input_gaps should list the missing files")
        # the S-rules and the cast-dependent D-rules could not be checked
        for r in ("LTXV-S001", "LTXV-S004", "LTXV-S006", "LTXV-D040", "LTXV-D041"):
            self.assertIn(r, clip["skipped_rule_ids"])
            self.assertNotIn(r, clip["checked_rule_ids"])

    def test_strict_run_fails_when_inputs_are_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, GOOD)
            rc = v.review_episode("tc", "EP001", root=root, emit_review=True, strict=True)
            doc = json.loads((root / "episodes" / "tc" / "EP001" / "_context"
                              / "ltx-prompt-review.json").read_text(encoding="utf-8"))
        self.assertEqual(rc, 1)
        self.assertEqual(doc["mode"], "strict")
        self.assertEqual(doc["status"], "FAIL")
        self.assertEqual(doc["clips"][0]["status"], "FAIL")
        self.assertIn("SC01", doc["strict_input_gaps"])

    def test_checked_and_skipped_partition_every_implemented_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._episode(tmp, GOOD)
            v.review_episode("tc", "EP001", root=root, emit_review=True)
            doc = json.loads((root / "episodes" / "tc" / "EP001" / "_context"
                              / "ltx-prompt-review.json").read_text(encoding="utf-8"))
        clip = doc["clips"][0]
        checked, skipped = set(clip["checked_rule_ids"]), set(clip["skipped_rule_ids"])
        self.assertEqual(checked & skipped, set(), "a rule is either checked or skipped")
        self.assertEqual(checked | skipped, set(v.IMPLEMENTED_RULE_IDS))


class SentenceSplitting(unittest.TestCase):
    """Regression: splitting must not cut inside quoted dialogue.

    Found against real EP001 drafts, 2026-10-29. Dialogue routinely ends on `!`
    or `?`, and a naive split on terminal punctuation produced fragments that
    began mid-quote — which made a character action read as a camera move
    (LTXV-D025) and hid the real final beat (LTXV-D041).
    """

    def test_terminal_punctuation_inside_a_quote_does_not_split(self):
        s = v._sentences('Pip lifts the pump and says: "Bruno! Look what I found!" '
                         'Bruno keeps his arms crossed.')
        self.assertEqual(len(s), 2)
        self.assertTrue(s[0].endswith('"'))
        self.assertTrue(s[1].startswith("Bruno keeps"))

    def test_a_quote_final_stop_still_ends_the_outer_sentence(self):
        """English puts the full stop inside the quotes; it ends both."""
        s = v._sentences('Bruno answers: "Morning\'s debatable." Clover lifts the bicycle.')
        self.assertEqual(len(s), 2)
        self.assertIn("debatable.", s[0])
        self.assertTrue(s[1].startswith("Clover lifts"))

    def test_multiple_sentences_inside_one_quote_stay_together(self):
        s = v._sentences('Pip tilts the head up: "It fits her bike. I checked." '
                         'Bruno leans forward.')
        self.assertEqual(len(s), 2)
        self.assertIn("I checked.", s[0])

    def test_sentences_are_sliced_from_the_original_text_unaltered(self):
        text = 'Clover looks down: "It\'s flat! Completely flat?" Rosa rests a paw on the rail.'
        self.assertEqual(" ".join(v._sentences(text)), text)

    def test_unquoted_prose_splits_exactly_as_before(self):
        s = v._sentences("Bruno leans in. Pip waits! Clover looks up?")
        self.assertEqual(s, ["Bruno leans in.", "Pip waits!", "Clover looks up?"])

    def test_a_character_action_in_a_dialogue_sentence_is_not_a_camera_move(self):
        """The end-to-end symptom the splitter bug produced."""
        prompt = ('Pip lifts the pump and calls out: "Bruno! Listen!" '
                  'Bruno keeps his arms crossed and answers: "Put it down, Pip."')
        camera = [s for s in v._sentences(prompt) if v._is_camera_sentence(s)]
        self.assertEqual(camera, [])


if __name__ == "__main__":
    unittest.main()
