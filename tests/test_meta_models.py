import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import meta_models as mm


def fake_capture(seen, body=b'{"id":"r1"}'):
    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return body
    def fake_urlopen(req, timeout=0):
        seen["url"] = req.full_url
        seen["auth"] = req.headers.get("Authorization")
        seen["ctype"] = req.headers.get("Content-type") or req.headers.get("Content-Type")
        seen["data"] = req.data
        return FakeResp()
    return fake_urlopen


class AllocationTest(unittest.TestCase):
    def test_user_allocation_official_ids(self):
        # Requested short names resolve to official Model API IDs (docs/models).
        self.assertEqual(mm.resolve_role("reasoning"), "muse-spark-1.3")
        self.assertEqual(mm.resolve_role("creative"), "muse-wonder-1.0")
        self.assertEqual(mm.resolve_role("image"), "muse-image-1.0")
        self.assertEqual(mm.resolve_role("segment"), "sam-3.1")
        self.assertEqual(mm.resolve_role("transcribe"), "muse-voice-transcribe-1.0")

    def test_stage_allocation(self):
        self.assertEqual(mm.model_for_stage("03a-writer"), "muse-wonder-1.0")
        self.assertEqual(mm.model_for_stage("04f2-frame0-stills"), "muse-image-1.0")
        self.assertEqual(mm.model_for_stage("04h-ltx-pilot-qa"), "sam-3.1")
        self.assertEqual(mm.model_for_stage("05a-render-qa"), "muse-voice-transcribe-1.0")
        self.assertEqual(mm.model_for_stage("01b-coverage-scan"), "muse-spark-1.3")

    def test_unknown_and_open_weight(self):
        with self.assertRaises(ValueError):
            mm.resolve_role("nope")
        with self.assertRaises(ValueError):
            mm.model_for_stage("99-nope")
        # Glimmer / Spark Open are self-hosted only: no Model API ID.
        with self.assertRaises(ValueError):
            mm.resolve_role("local_fast")
        with self.assertRaises(ValueError):
            mm.resolve_role("local_open")


class CallTest(unittest.TestCase):
    def test_responses_create(self):
        seen = {}
        with patch.dict("os.environ", {"MODEL_API_KEY": "test-key"}):
            with patch.object(mm.urllib.request, "urlopen", fake_capture(seen)):
                out = mm.responses_create("muse-spark-1.3", "hi")
        self.assertEqual(out, {"id": "r1"})
        self.assertTrue(seen["url"].endswith("/responses"))
        self.assertEqual(seen["auth"], "Bearer test-key")
        self.assertEqual(json.loads(seen["data"])["model"], "muse-spark-1.3")

    def test_image_generate(self):
        seen = {}
        with patch.dict("os.environ", {"MODEL_API_KEY": "test-key"}):
            with patch.object(mm.urllib.request, "urlopen", fake_capture(seen)):
                mm.image_generate("a fox", size="1536x1024")
        self.assertTrue(seen["url"].endswith("/images/generations"))
        body = json.loads(seen["data"])
        self.assertEqual(body["model"], "muse-image-1.0")
        self.assertEqual(body["prompt"], "a fox")

    def test_segment(self):
        seen = {}
        with patch.dict("os.environ", {"MODEL_API_KEY": "test-key"}):
            with patch.object(mm.urllib.request, "urlopen", fake_capture(seen)):
                mm.segment("https://example.com/p.png", "glasses")
        self.assertTrue(seen["url"].endswith("/responses"))
        body = json.loads(seen["data"])
        self.assertEqual(body["model"], "sam-3.1")
        self.assertEqual(body["input"][0]["content"][0]["text"], "glasses")

    def test_transcribe_multipart(self):
        seen = {}
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fh:
            fh.write(b"RIFFfake")
            path = fh.name
        with patch.dict("os.environ", {"MODEL_API_KEY": "test-key"}):
            with patch.object(mm.urllib.request, "urlopen", fake_capture(seen, b'{"transcript":"hi"}')):
                out = mm.transcribe(path, session_id="s1")
        self.assertEqual(out, {"transcript": "hi"})
        self.assertIn("/asr/transcribe?sessionId=s1", seen["url"])
        self.assertIn("multipart/form-data", seen["ctype"])
        self.assertIn(b"muse-voice-transcribe-1.0", seen["data"])
        self.assertIn(b'name="audio"', seen["data"])

    def test_config_never_prints_key(self):
        with patch.dict("os.environ", {"MODEL_API_KEY": "secret-value"}):
            self.assertNotIn("secret-value", json.dumps(mm.config_summary()))
            self.assertTrue(mm.config_summary()["key_present"])

    def test_smoke_without_key_is_clean_error(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch.object(mm, "_load_dotenv", lambda: None):
                self.assertEqual(mm.main(["smoke"]), 1)


if __name__ == "__main__":
    unittest.main()
