"""Tests for tools/ltx_prompt_manifest.py (04f3) and tools/build_render_package.py (04g).

Each test builds a minimal repo tree in a tempdir: one channel profile, the
negative-prompt base, a copy of the real validator (the review is bound to its
hash), and a two-clip episode. The golden test at the bottom checks the byte
layout against signed-anyway EP002's shipped, rendered package.
"""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_render_package as brp  # noqa: E402
import ltx_prompt_manifest as lpm  # noqa: E402

PROMPTS = (
    "# EP001 clip prompts -- final\n\n"
    "## SC01\n\n[[HERO]]\n\n"
    "GLOBAL:: Continue from the still. A hero stands by a door.\n"
    "BEAT:: 481 :: The hero opens the door.\n\n"
    "## SC02\n\n"
    "GLOBAL:: Continue from the still. The hero steps outside.\n"
    "BEAT:: 481 :: The hero looks up.\n"
)


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Base(unittest.TestCase):
    CLIPS = ("SC01", "SC02", "SC03", "SC04", "SC05")

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="vidgen_ltx_pkg_"))
        (self.root / "tools").mkdir()
        shutil.copy2(ROOT / "tools" / "ltx_prompt_validator.py", self.root / "tools")
        (self.root / "pipeline").mkdir()
        (self.root / "pipeline" / "negative-prompt-base.txt").write_text(
            "duplicate character, on-screen text\n", encoding="utf-8")
        chan = self.root / "channel_profiles" / "demo"
        chan.mkdir(parents=True)
        (chan / "channel.json").write_text(json.dumps({
            "slug": "demo", "models": {"image": "muse-image-1.0"},
            "render": {
                "mode": "i2v", "model": "LTX-2.5", "generation_unit": "clip",
                "clip_duration_seconds": 20, "fps": 24, "aspect_ratio": "16:9",
                "megapixels": 0.98, "spoken_word_band": [32, 36], "style_echo": "photoreal",
                "workflow": "LTX25_T2V_I2V_Two_Stage_Distilled.json", "cfg": 1.2,
                "cfg_refine": 1.0, "cfg_audio": 1.0, "img_compression": 22,
                "negative_prompt_additions": ["cartoon"],
            }}), encoding="utf-8")
        self.ep = self.root / "episodes" / "demo" / "EP001"
        prompts = PROMPTS + "".join(
            f"\n## {c}\n\nGLOBAL:: Continue from the still. Scene {c}.\nBEAT:: 481 :: Hold.\n"
            for c in self.CLIPS[2:])
        self.write("prompts/7-video-prompts.md", prompts)
        self.write("qa/still-gate.md", "all PASS\n")
        self.write("_context/blocking.json", json.dumps({"clips": {
            c: {"chars": {"HERO": {"visible": True}}, "camera": {"movement": "slow push in"}}
            for c in self.CLIPS}}))
        self.write("_context/frame0-requirements.json", json.dumps({"clips": [
            {"clip": c, "characters": ["HERO"], "touched_objects": ["the door"],
             "first_action_performable": True, "continues_from": None} for c in self.CLIPS]}))
        for c in self.CLIPS:
            p = self.ep / "renders" / "stills" / f"{c}.png"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"\x89PNG" + c.encode())
        self.pass_review()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel, text):
        p = self.ep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def pass_review(self, **over):
        doc = {"mode": "strict", "status": "PASS",
               "source_prompts_sha256": _sha((self.ep / lpm.PROMPTS_REL).read_bytes()),
               "validator_sha256": _sha((self.root / "tools" / "ltx_prompt_validator.py").read_bytes())}
        doc.update(over)
        self.write(lpm.REVIEW_REL, json.dumps(doc))

    def build_manifest(self, **kw):
        kw.setdefault("still_gate_pass", True)
        m = lpm.build_manifest("demo", "EP001", root=self.root, **kw)
        (self.ep / lpm.MANIFEST_REL).write_text(json.dumps(m, indent=2), encoding="utf-8")
        return m

    def build_package(self, **kw):
        kw.setdefault("pilots", list(self.CLIPS))
        kw.setdefault("cast", ["Hero"])
        return brp.build_package("demo", "EP001", root=self.root, **kw)


class Manifest(Base):
    def test_builds_every_field_from_disk(self):
        m = self.build_manifest(still_generator="muse-image-1.0")
        sc01 = m["clips"][0]
        self.assertEqual([c["clip"] for c in m["clips"]], list(self.CLIPS))
        self.assertEqual(sc01["index"], 1)
        self.assertEqual(sc01["prompt_sha256"], _sha(
            b"GLOBAL:: Continue from the still. A hero stands by a door.\n"
            b"BEAT:: 481 :: The hero opens the door."))  # [[TAG]] line dropped
        self.assertEqual(sc01["still_sha256"], _sha(b"\x89PNGSC01"))
        self.assertEqual(sc01["camera_movement"], "slow push in")
        self.assertEqual(sc01["still_generator"], "muse-image-1.0")
        self.assertEqual(m["render"]["clip_duration_seconds"], 20)

    def test_refuses_provisional_prompts(self):
        self.write("prompts/7-video-prompts.md", "Every GLOBAL:: line is PROVISIONAL\n" + PROMPTS)
        self.pass_review()
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest()
        self.assertIn("PROVISIONAL", str(ctx.exception))

    def test_refuses_a_review_of_an_older_prompts_file(self):
        self.write("prompts/7-video-prompts.md", PROMPTS + "\n")
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest()
        self.assertIn("different prompts/7-video-prompts.md", str(ctx.exception))

    def test_refuses_a_review_from_an_older_validator(self):
        self.pass_review(validator_sha256="0" * 64)
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest()
        self.assertIn("older ltx_prompt_validator.py", str(ctx.exception))

    def test_refuses_a_legacy_review(self):
        self.pass_review(source_prompts_sha256=None)
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest()
        self.assertIn("predates source_prompts_sha256", str(ctx.exception))

    def test_refuses_without_still_gate_attestation(self):
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest(still_gate_pass=False)
        self.assertIn("--still-gate-pass", str(ctx.exception))

    def test_refuses_a_missing_still(self):
        (self.ep / "renders/stills/SC02.png").unlink()
        with self.assertRaises(lpm.Refused) as ctx:
            self.build_manifest()
        self.assertIn("SC02", str(ctx.exception))


class Package(Base):
    def setUp(self):
        super().setUp()
        self.build_manifest()

    def test_builds_and_verifies(self):
        doc = self.build_package(pilots=["SC01", "SC02", "SC03", "SC04", "SC05"])
        pkg = self.ep / brp.PACKAGE_REL
        master = (pkg / "master-prompt.txt").read_bytes()
        self.assertTrue(master.startswith(b"@@ s1\r\nGLOBAL:: Continue from the still. A hero"))
        self.assertNotIn(b"[[HERO]]", master)
        self.assertEqual((pkg / "negative-prompt.txt").read_bytes(),
                         b"duplicate character, on-screen text, cartoon, second Hero\r\n")
        self.assertEqual(sorted(f.name for f in (pkg / "stills").iterdir()),
                         [f"{c}.png" for c in self.CLIPS])
        self.assertEqual(doc["source_manifest_sha256"],
                         _sha((self.ep / lpm.MANIFEST_REL).read_bytes()))
        self.assertEqual(doc["settings"]["duration_seconds"], 20)

    def test_refuses_a_prompt_edited_after_the_manifest(self):
        text = (self.ep / lpm.PROMPTS_REL).read_text(encoding="utf-8")
        self.write(lpm.PROMPTS_REL, text.replace("looks up", "looks down"))
        self.pass_review()  # even a fresh review does not excuse a stale manifest
        with self.assertRaises(brp.Refused) as ctx:
            self.build_package()
        self.assertIn("SC02: prompt block changed", str(ctx.exception))

    def test_refuses_a_still_swapped_after_the_manifest(self):
        (self.ep / "renders/stills/SC03.png").write_bytes(b"\x89PNGother")
        with self.assertRaises(brp.Refused) as ctx:
            self.build_package()
        self.assertIn("SC03: still changed", str(ctx.exception))

    def test_pilot_rules(self):
        with self.assertRaises(brp.Refused) as ctx:
            self.build_package(pilots=["SC02", "SC03", "SC04", "SC05"])
        msg = str(ctx.exception)
        self.assertIn("at least 5", msg)
        self.assertIn("opening clip SC01", msg)

    def test_cast_is_required(self):
        with self.assertRaises(brp.Refused) as ctx:
            self.build_package(cast=[])
        self.assertIn("--cast", str(ctx.exception))

    def test_existing_package_needs_force(self):
        self.build_package()
        with self.assertRaises(brp.Refused):
            self.build_package()
        self.build_package(force=True)

    def test_verification_catches_a_mispaired_still(self):
        doc = self.build_package()
        pkg = self.ep / brp.PACKAGE_REL
        (pkg / "stills" / "SC02.png").rename(pkg / "stills" / "SC02_take3.png")
        (pkg / "stills" / "s2.png").write_bytes(b"stray")
        errors = brp.verify_package(pkg, doc, lpm.clip_blocks(self.ep / lpm.PROMPTS_REL))
        self.assertTrue(any("SC02" in e for e in errors))


class AppParserMirror(unittest.TestCase):
    def test_scene_number_is_the_prefix_not_the_last_digit_run(self):
        self.assertEqual(brp.app_scene_number("SC07.png"), 7)
        self.assertEqual(brp.app_scene_number("SC07_v2.png"), 7)
        self.assertEqual(brp.app_scene_number("s12.png"), 12)
        self.assertIsNone(brp.app_scene_number("take3_SC07.png"))

    def test_scene_sections_skip_image_blocks_and_tag_lines(self):
        text = "@@ i1\nstill text\n\n@@ s1\n[[A]]\nclip one\n\n@@ s2\nclip two\n"
        self.assertEqual(brp.app_scene_prompts(text), {1: "clip one", 2: "clip two"})


@unittest.skipUnless((ROOT / "episodes/signed-anyway/EP002/exports/ltx-render-package").exists(),
                     "shipped EP002 package not present")
class GoldenEP002(unittest.TestCase):
    """The layout must stay byte-identical to the package that rendered EP002."""

    def test_master_and_negative_match_the_shipped_bytes(self):
        ep = ROOT / "episodes/signed-anyway/EP002"
        pkg = ep / brp.PACKAGE_REL
        blocks = lpm.clip_blocks(ep / lpm.PROMPTS_REL)
        render = json.loads((ROOT / "channel_profiles/signed-anyway/channel.json")
                            .read_text(encoding="utf-8"))["render"]
        self.assertEqual(brp.render_master(lpm.ordered(blocks), blocks),
                         (pkg / "master-prompt.txt").read_bytes())
        self.assertEqual(
            brp.render_negative((ROOT / "pipeline/negative-prompt-base.txt").read_text(encoding="utf-8"),
                                render["negative_prompt_additions"],
                                ["Evelyn", "Adrian", "Elena", "Daniel", "Reyes"]),
            (pkg / "negative-prompt.txt").read_bytes())
        doc = json.loads((pkg / "render-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(brp.verify_package(pkg, doc, blocks), [])


if __name__ == "__main__":
    unittest.main()
