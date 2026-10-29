"""Tests for tools/clip_split_check.py -- can each script row be cut into its clips at clean pauses?

The band used throughout is inside-the-process's real render.spoken_word_band, 32-36.
"""
import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import clip_split_check as csc  # noqa: E402

BAND = (32, 36)


def toks(*spoken):
    """[(speaker, token)] from ("Explorer", "text"), ("Control", "text") pairs."""
    return [(spk, t) for spk, text in spoken for t in text.split()]


def words(n, stem="word"):
    return " ".join(f"{stem}{i}" for i in range(n))


class PauseStrength(unittest.TestCase):
    def test_speaker_change_and_sentence_end_are_strongest(self):
        t = toks(("E", "It ends here."), ("C", "Next speaker"))
        self.assertEqual(csc.pause_strength(t, 2), 3)  # "here." and a speaker change
        t = toks(("C", "One sentence. Another"))
        self.assertEqual(csc.pause_strength(t, 1), 3)

    def test_colon_and_dash_beat_comma_beat_nothing(self):
        t = toks(("C", "hot: enough — to move, like thick liquid"))
        self.assertEqual(csc.pause_strength(t, 0), 2)  # "hot:"
        self.assertEqual(csc.pause_strength(t, 1), 2)  # before the standalone dash
        self.assertEqual(csc.pause_strength(t, 4), 1)  # "move,"
        self.assertEqual(csc.pause_strength(t, 5), 0)  # "like ‖ thick"

    def test_closing_quote_does_not_hide_a_sentence_end(self):
        t = toks(("C", 'it "ends." now'))
        self.assertEqual(csc.pause_strength(t, 1), 3)


class CheckRow(unittest.TestCase):
    def test_one_clip_only_needs_the_band(self):
        self.assertEqual(csc.check_row(toks(("E", words(34))), 1, *BAND), (True, [34]))
        ok, detail = csc.check_row(toks(("E", words(37))), 1, *BAND)
        self.assertFalse(ok)
        self.assertIn("cannot fit", detail)

    def test_total_outside_the_clip_band_fails_before_searching(self):
        ok, detail = csc.check_row(toks(("C", words(80) + ".")), 2, *BAND)
        self.assertFalse(ok)
        self.assertIn("80 words cannot fit 2 clip(s)", detail)

    def test_row_with_no_pause_near_the_boundary_fails(self):
        # EP001 revision 9's defect: in band on average, but the only pause sits where it would
        # leave clip 1 at 20 words.
        row = toks(("C", words(20) + ". " + words(48, "w")))
        ok, detail = csc.check_row(row, 2, *BAND)
        self.assertFalse(ok)
        self.assertIn("restructure", detail)

    def test_sentence_end_inside_the_band_passes(self):
        row = toks(("C", words(34) + ". " + words(34, "w") + "."))
        self.assertEqual(csc.check_row(row, 2, *BAND), (True, [34, 34]))

    def test_speaker_change_is_a_clean_cut(self):
        row = toks(("E", words(33)), ("C", words(35, "w")))
        self.assertEqual(csc.check_row(row, 2, *BAND), (True, [33, 35]))

    def test_comma_only_split_passes_but_is_reported(self):
        row = toks(("C", words(34) + ", " + words(34, "w") + "."))
        ok, detail = csc.check_row(row, 2, *BAND)
        self.assertTrue(ok)
        self.assertIn("comma/dash break", detail)

    def test_prefers_the_sentence_end_over_an_earlier_comma(self):
        # Clip 1 could end at the comma (33) or the full stop (35): the full stop must win.
        row = toks(("C", words(33) + ", two more. " + words(33, "w") + "."))
        found = csc.best_split(row, 2, *BAND)
        self.assertEqual(found[1], [35, 33])
        self.assertEqual(csc.pause_strength(row, found[0][0]), 3)

    def test_counts_use_the_validator_tokenizer(self):
        # "seventy-four" is one word for LTXV-D034, so 33 tokens + a hyphenated one = 34.
        row = toks(("C", words(33) + " seventy-four."))
        self.assertEqual(csc.check_row(row, 1, *BAND), (True, [34]))


class CheckScript(unittest.TestCase):
    TABLE = """\
| # | Time | Duration | Explorer words | Control words | Spoken-word estimate |
|---|---|---|---|---|---|
| 1 | 0:00–0:20 | 20s (1 clip) | "{one}" | — | 34 |
| 2 | 0:20–1:00 | 40s (2 clips) | "{e2}" | "{c2}" | 68 |
"""

    def test_reads_clip_count_and_every_words_column(self):
        text = self.TABLE.format(one=words(34) + ".", e2=words(33) + "?", c2=words(35, "w") + ".")
        res = csc.check_script(text, BAND)
        self.assertEqual([(r["row"], r["ok"]) for r in res], [("1", True), ("2", True)])
        self.assertEqual(res[1]["detail"], [33, 35])

    def test_long_quoted_row_is_not_counted_as_zero(self):
        # The validator's QUOTED pattern caps a quote at 600 characters; a long row must still
        # be counted word by word.
        long_c = " ".join(f"considerablylongerword{i}" for i in range(35)) + "."
        self.assertGreater(len(long_c), 600)
        text = self.TABLE.format(one=words(34) + ".", e2=words(33) + "?", c2=long_c)
        self.assertEqual(csc.check_script(text, BAND)[1]["detail"], [33, 35])

    def test_row_without_clip_count_fails(self):
        text = self.TABLE.replace("20s (1 clip)", "20s").format(
            one=words(34) + ".", e2=words(33) + "?", c2=words(35, "w") + ".")
        res = csc.check_script(text, BAND)
        self.assertFalse(res[0]["ok"])
        self.assertEqual(res[0]["detail"], "no clip count in the Duration cell")


class RealEpisode(unittest.TestCase):
    def test_inside_the_process_ep001_passes(self):
        script = ROOT / "episodes" / "inside-the-process" / "EP001" / "story" / "script.md"
        if not script.exists():
            self.skipTest("EP001 not present")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = csc.main(["--channel", "inside-the-process", "--episode", "EP001"])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
