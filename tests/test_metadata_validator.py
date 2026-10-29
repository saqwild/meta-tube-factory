"""Tests for tools/metadata_validator.py.

The scenario this guards is the one that actually happened for EP001: the
06-distribution-metadata package was checked against channel.json's
metadata_validation constants with a one-off script that was then thrown
away, leaving no repeatable check for the next episode.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import metadata_validator as mv  # noqa: E402


def package_md(title: str = "A Short Enough Title", description: str = "Fine. #Tag") -> str:
    return (
        "# EP001 -- distribution metadata package (06)\n\n"
        "## Title\n\n"
        f"**{title}**\n\n"
        "63 characters.\n\n"
        "## Description\n\n"
        "```text\n"
        f"{description}\n"
        "```\n\n"
        "**Placeholder note:** none.\n\n"
        "## Tags\n\n"
        "```text\n"
        "one, two\n"
        "```\n"
    )


CHANNEL = {
    "metadata_validation": {
        "required_disclosure_terms": ["fictional disclosure", "synthetic performers"],
        "banned_description_terms": ["true story"],
        "banned_title_patterns": ["shocking"],
        "title_max_chars": 70,
    },
    "youtube": {
        "required_hashtags": ["#RequiredTag"],
        "title_max_characters": 70,
    },
}


class ParsePackage(unittest.TestCase):
    def test_parses_title_and_description(self):
        fields = mv.parse_package(package_md(title="Hello World", description="Body text here."))
        self.assertEqual(fields.title, "Hello World")
        self.assertEqual(fields.description, "Body text here.")

    def test_missing_title_section_is_none(self):
        text = "## Description\n\n```text\nBody\n```\n"
        fields = mv.parse_package(text)
        self.assertIsNone(fields.title)

    def test_missing_description_fence_is_none(self):
        text = "## Title\n\n**Hi**\n\n## Description\n\nno fence here\n"
        fields = mv.parse_package(text)
        self.assertIsNone(fields.description)


class ValidatePackage(unittest.TestCase):
    def test_clean_package_passes(self):
        fields = mv.PackageFields(
            title="A Fine Title",
            description=(
                "Body copy. Fictional disclosure: synthetic performers used throughout. "
                "#RequiredTag"
            ),
        )
        review = mv.validate_package(fields, CHANNEL)
        self.assertEqual(review.errors, [])

    def test_title_over_limit_fails(self):
        fields = mv.PackageFields(title="x" * 80, description="Fictional disclosure: synthetic performers. #RequiredTag")
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D001" in e for e in review.errors))

    def test_banned_title_pattern_fails(self):
        fields = mv.PackageFields(title="This Is Shocking News",
                                   description="Fictional disclosure: synthetic performers. #RequiredTag")
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D002" in e for e in review.errors))

    def test_missing_disclosure_term_fails(self):
        fields = mv.PackageFields(title="Fine Title", description="No disclosure here. #RequiredTag")
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D003" in e for e in review.errors))

    def test_banned_description_term_fails(self):
        fields = mv.PackageFields(
            title="Fine Title",
            description="This is a true story. Fictional disclosure: synthetic performers. #RequiredTag",
        )
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D004" in e for e in review.errors))

    def test_missing_required_hashtag_fails(self):
        fields = mv.PackageFields(
            title="Fine Title",
            description="Fictional disclosure: synthetic performers used.",
        )
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D005" in e for e in review.errors))

    def test_unparseable_title_fails(self):
        fields = mv.PackageFields(title=None, description="Fictional disclosure: synthetic performers. #RequiredTag")
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D006" in e for e in review.errors))

    def test_unparseable_description_fails(self):
        fields = mv.PackageFields(title="Fine Title", description=None)
        review = mv.validate_package(fields, CHANNEL)
        self.assertTrue(any("META-D007" in e for e in review.errors))

    def test_required_description_line_missing_fails(self):
        channel = {
            "metadata_validation": {},
            "youtube": {"description_line_required": "AI-generated original stories."},
        }
        fields = mv.PackageFields(title="Fine Title", description="Nothing matching here.")
        review = mv.validate_package(fields, channel)
        self.assertTrue(any("META-D008" in e for e in review.errors))

    def test_required_description_line_present_passes(self):
        channel = {
            "metadata_validation": {},
            "youtube": {"description_line_required": "AI-generated original stories."},
        }
        fields = mv.PackageFields(
            title="Fine Title",
            description="Intro.\n\nAI-generated   original\nstories.\n\nOutro.",
        )
        review = mv.validate_package(fields, channel)
        self.assertEqual([e for e in review.errors if "META-D008" in e], [])

    def test_unknown_metadata_validation_key_warns(self):
        channel = {
            "metadata_validation": {"thumbnail_overlay_words_min": 2},
            "youtube": {},
        }
        fields = mv.PackageFields(title="Fine Title", description="Body.")
        review = mv.validate_package(fields, channel)
        self.assertTrue(any("META-W001" in w and "thumbnail_overlay_words_min" in w
                            for w in review.warnings))

    def test_title_max_chars_mismatch_warns(self):
        channel = {
            "metadata_validation": {"title_max_chars": 70},
            "youtube": {"title_max_characters": 90},
        }
        fields = mv.PackageFields(title="Fine Title", description="Body.")
        review = mv.validate_package(fields, channel)
        self.assertTrue(any("META-W002" in w for w in review.warnings))

    def test_undeclared_rule_id_raises(self):
        with self.assertRaises(ValueError):
            mv._rule_message("NOT-A-REAL-RULE", "boom")

    def test_output_is_ascii_safe(self):
        """The Windows console is cp1252; a non-ASCII marker crashed a real run
        for another tool in this repo -- keep the same guarantee here."""
        src = (ROOT / "tools" / "metadata_validator.py").read_text(encoding="utf-8")
        for i, line in enumerate(src.splitlines(), 1):
            if "print(" in line:
                self.assertTrue(all(ord(c) < 128 for c in line),
                                f"non-ASCII in printed output at line {i}: {line.strip()}")


class RealRepo(unittest.TestCase):
    def test_signed_anyway_ep001_package_passes(self):
        exit_code = mv.review_metadata("signed-anyway", "EP001")
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
