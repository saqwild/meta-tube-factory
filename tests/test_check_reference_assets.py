"""Tests for tools/check_reference_assets.py.

The scenario this guards is the one that actually happened: reference sheets
were regenerated and replaced, filenames and extensions changed, and every cast
card kept pointing at paths and hashes that no longer existed.
"""

import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_reference_assets as chk  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"fake-pixels-for-testing"
PNG_SHA = hashlib.sha256(PNG).hexdigest()


def card(path_rel: str, sha: str | None) -> str:
    status = f"**LOCKED.** SHA-256 `{sha}`" if sha else "Not yet generated"
    return ("# CAST-001 - TEST\n\n"
            "| Asset | Path | Status |\n"
            "|---|---|---|\n"
            f"| Character sheet | `{path_rel}` | {status} |\n\n"
            "Approval status: source `some-other-repo/characters/reference_sheets/old_name.jpg`.\n")


class ReferenceAssetCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_refs_"))
        self.bible = self.tmp / "demo" / "bible"
        self.cards = self.bible / "characters"
        self.sheets = self.cards / "reference_sheets"
        self.sheets.mkdir(parents=True)
        (self.tmp / "demo" / "channel.json").write_text("{}", encoding="utf-8")
        (self.sheets / "hero_sheet.png").write_bytes(PNG)
        self._real = chk.CHANNEL_PROFILES_DIR
        self._real_eps = chk.EPISODES_DIR
        chk.CHANNEL_PROFILES_DIR = self.tmp
        chk.EPISODES_DIR = self.tmp / "_episodes"

    def tearDown(self):
        chk.CHANNEL_PROFILES_DIR = self._real
        chk.EPISODES_DIR = self._real_eps
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_card(self, rel, sha):
        (self.cards / "CAST-001_HERO.md").write_text(card(rel, sha), encoding="utf-8")

    def test_matching_path_and_hash_passes(self):
        self.write_card("characters/reference_sheets/hero_sheet.png", PNG_SHA)
        problems, _ = chk.check_channel("demo")
        self.assertEqual(problems, [])

    def test_missing_file_is_a_problem(self):
        self.write_card("characters/reference_sheets/hero_portrait.jpg", PNG_SHA)
        problems, _ = chk.check_channel("demo")
        self.assertTrue(any("DOES NOT EXIST" in p for p in problems))

    def test_stale_hash_is_a_problem(self):
        self.write_card("characters/reference_sheets/hero_sheet.png", "0" * 64)
        problems, _ = chk.check_channel("demo")
        self.assertTrue(any("HASH MISMATCH" in p for p in problems))

    def test_orphan_sheet_is_a_problem(self):
        self.write_card("characters/reference_sheets/hero_sheet.png", PNG_SHA)
        (self.sheets / "unclaimed_sheet.png").write_bytes(PNG)
        problems, _ = chk.check_channel("demo")
        self.assertTrue(any("unclaimed_sheet.png" in p and "no cast card claims it" in p
                            for p in problems))

    def test_provenance_prose_is_not_treated_as_a_claim(self):
        """The cards cite source-repo paths in prose; only table rows are claims."""
        self.write_card("characters/reference_sheets/hero_sheet.png", PNG_SHA)
        problems, _ = chk.check_channel("demo")
        self.assertEqual(problems, [])

    def test_no_sheets_yet_is_not_a_failure(self):
        """A channel whose sheets 04b has not generated yet is legitimate."""
        shutil.rmtree(self.sheets)
        (self.cards / "CAST-001_HERO.md").write_text(
            "# CAST-001\n\n| Asset | Path | Status |\n|---|---|---|\n"
            "| Voice | `characters/voice/hero.wav` | Not yet generated |\n", encoding="utf-8")
        problems, notes = chk.check_channel("demo")
        self.assertEqual(problems, [])
        self.assertTrue(any("no locked reference images yet" in n for n in notes))

    def test_undeclared_hash_is_a_note_not_a_problem(self):
        self.write_card("characters/reference_sheets/hero_sheet.png", None)
        problems, notes = chk.check_channel("demo")
        self.assertEqual(problems, [])
        self.assertTrue(any("no declared SHA-256" in n for n in notes))

    def test_output_is_ascii_safe(self):
        """The Windows console is cp1252; a non-ASCII marker crashed a real run."""
        src = (ROOT / "tools" / "check_reference_assets.py").read_text(encoding="utf-8")
        for i, line in enumerate(src.splitlines(), 1):
            if "print(" in line:
                self.assertTrue(all(ord(c) < 128 for c in line),
                                f"non-ASCII in printed output at line {i}: {line.strip()}")


class LockedReferences(unittest.TestCase):
    """The second convention: channel_profiles/<slug>/locked-references/."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vidgen_ltx_locked_"))
        self.locked = self.tmp / "demo" / "locked-references"
        self.chars = self.locked / "characters" / "CAST-001"
        self.chars.mkdir(parents=True)
        (self.tmp / "demo" / "channel.json").write_text("{}", encoding="utf-8")
        for name in ("portrait.jpg", "full-body.jpg", "sheet.jpg"):
            (self.chars / name).write_bytes(PNG)
        (self.chars / "PROMOTION.md").write_text("# promoted\n", encoding="utf-8")
        (self.locked / "README.md").write_text(
            "# demo locked references\n\n| Cast | id | files |\n|---|---|---|\n"
            "| `CAST-001/` | Hero | portrait, full-body, sheet |\n", encoding="utf-8")
        self.eps = self.tmp / "_episodes"
        self.manifest = self.eps / "demo" / "EP001" / "visual" / "references" / "manifest.md"
        self.manifest.parent.mkdir(parents=True)
        self._real = chk.CHANNEL_PROFILES_DIR
        self._real_eps = chk.EPISODES_DIR
        chk.CHANNEL_PROFILES_DIR = self.tmp
        chk.EPISODES_DIR = self.eps

    def tearDown(self):
        chk.CHANNEL_PROFILES_DIR = self._real
        chk.EPISODES_DIR = self._real_eps
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _manifest_row(self, sha: str) -> None:
        self.manifest.write_text(
            f"| CAST-001 | Hero | `characters/EP001-CAST001-sheet.jpg` | `{sha}` | "
            f"**COPIED** from `channel_profiles/demo/locked-references/characters/CAST-001/sheet.jpg` |\n",
            encoding="utf-8")

    def test_clean_locked_references_verify(self):
        self._manifest_row(PNG_SHA)
        problems, notes, verified = chk.check_locked_references("demo")
        self.assertEqual(problems, [])
        self.assertEqual(verified, 1)

    def test_overwritten_locked_file_is_caught_via_episode_hash(self):
        self._manifest_row(PNG_SHA)
        (self.chars / "sheet.jpg").write_bytes(PNG + b"-tampered")
        problems, _, _ = chk.check_locked_references("demo")
        self.assertTrue(any("HASH MISMATCH" in p for p in problems))

    def test_missing_promotion_md_is_a_problem(self):
        (self.chars / "PROMOTION.md").unlink()
        problems, _, _ = chk.check_locked_references("demo")
        self.assertTrue(any("PROMOTION.md" in p for p in problems))

    def test_readme_and_disk_disagree(self):
        (self.locked / "characters" / "CAST-002").mkdir()
        for name in ("portrait.jpg", "full-body.jpg", "sheet.jpg"):
            (self.locked / "characters" / "CAST-002" / name).write_bytes(PNG)
        (self.locked / "characters" / "CAST-002" / "PROMOTION.md").write_text("x", encoding="utf-8")
        problems, _, _ = chk.check_locked_references("demo")
        self.assertTrue(any("CAST-002" in p and "README.md" in p for p in problems))

    def test_no_locked_references_dir_is_silent(self):
        shutil.rmtree(self.locked)
        problems, notes, verified = chk.check_locked_references("demo")
        self.assertEqual((problems, notes, verified), ([], [], 0))

    def test_dir_present_but_no_episode_hash_yet_is_a_note(self):
        self.manifest.write_text("nothing relevant here\n", encoding="utf-8")
        problems, notes, verified = chk.check_locked_references("demo")
        self.assertEqual(problems, [])
        self.assertEqual(verified, 0)
        self.assertTrue(any("no episode manifest records a hash" in n for n in notes))


class RealRepo(unittest.TestCase):
    def test_every_channel_in_this_repo_is_clean(self):
        problems = []
        for slug in sorted(p.name for p in chk.CHANNEL_PROFILES_DIR.iterdir()
                           if p.is_dir() and (p / "channel.json").exists()):
            problems.extend(chk.check_channel(slug)[0])
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
