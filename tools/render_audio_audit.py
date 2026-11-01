#!/usr/bin/env python3
"""Transcribe every ingested render clip and diff it against its approved spoken line.

WHY THIS EXISTS
---------------
`renders/render-manifest.json` (`05-render-ingest`) only verifies duration, resolution,
codec, hash and whether audio is present/silent — never that the clip's actual spoken
audio matches the dialogue it was rendered from. That gap let a real defect through
undetected on EP001 (signed-anyway): two clips silently carried a *different episode's*
dialogue end to end while every structural check passed clean. It was found only by
transcribing the clips and reading the words — this module makes that check repeatable
instead of a one-off manual catch.

(That specific incident turned out to be a transcript-cache collision in `askyt_editor`'s
postprod tooling, not a bad render — but the only reason it was distinguishable from a
real bad render was transcribing the *original* clips directly, bypassing that cache.
This tool always reads straight from the path `render-manifest.json` declares.)

The word-similarity ratio screens for a wholesale wrong-clip swap but is blind to a
one-word meaning flip: "I did not authorize the transfer" vs "I did authorize the transfer"
scores about 0.9. So each dialogue clip also gets a structural check -- the negation multiset
and any spoken digit figures must match the approved line, or the clip FAILs regardless of
the ratio.

RUN
---
    python tools/render_audio_audit.py --channel signed-anyway --episode EP001
    python tools/render_audio_audit.py --channel signed-anyway --episode EP001 --emit-review

Exit 0 = every clip's transcribed audio matches its approved line (or is silent where the
prompt has no quoted dialogue). Exit 1 = at least one FAIL/MISSING/SILENT_BUT_SPOKE. Exit 2 =
setup problem (missing manifest, missing prompts file, no MODEL_API_KEY,
or ffmpeg not on PATH). Transcription is Muse Voice Transcribe via
tools/meta_models.py -- no local speech model.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_paths import EPISODES_DIR  # noqa: E402
from ltx_prompt_validator import QUOTED  # noqa: E402 -- reuse the one quoted-dialogue regex

WORD = re.compile(r"[a-z0-9']+")

DEFAULT_SIMILARITY_THRESHOLD = 0.6
SILENT_WORD_CEILING = 3  # a clip with no quoted dialogue may still catch a stray word or two

# Negation markers. Every "n't" contraction plus "not"/"cannot" collapse to one NOT
# bucket (so "can't" vs "cannot" is not a false mismatch); the standalone quantifier
# negatives are counted on their own. A dialogue clip whose transcript carries a
# different negation multiset than its approved line has almost certainly had its
# meaning flipped -- "I did not authorize" vs "I did authorize" scores ~0.9 on the
# word-similarity ratio but differs here, which is the whole point of this check.
_STANDALONE_NEGATIONS = {"no", "never", "none", "nor", "neither", "without", "nothing", "nobody"}


def _norm_words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def negation_markers(text: str) -> Counter:
    """Multiset of negation markers in `text`. Contractions and 'not'/'cannot' all
    map to the key 'NOT'; quantifier negatives keep their own key."""
    out: Counter = Counter()
    for w in _norm_words(text):
        if w.endswith("n't") or w in ("not", "cannot"):
            out["NOT"] += 1
        elif w in _STANDALONE_NEGATIONS:
            out[w] += 1
    return out


def _digit_numbers(text: str) -> set[str]:
    """Comma-stripped digit runs of >= 2 digits (e.g. '$22,000' -> '22000', '11' -> '11').
    Single digits are skipped -- ASR routinely words them out ('8 minutes' -> 'eight')."""
    return {m.replace(",", "") for m in re.findall(r"\d[\d,]*", text)
            if len(m.replace(",", "")) >= 2}


def structural_reasons(expected: str, transcribed: str) -> list[str]:
    """Meaning-level mismatches the similarity ratio is blind to: a flipped negation,
    or a spoken figure that never made it into the audio."""
    reasons: list[str] = []
    exp_neg, got_neg = negation_markers(expected), negation_markers(transcribed)
    if exp_neg != got_neg:
        reasons.append(
            f"negation mismatch: expected {dict(exp_neg) or '{}'}, heard {dict(got_neg) or '{}'}"
        )
    got_digits = "".join(re.findall(r"\d", transcribed))
    missing = sorted(n for n in _digit_numbers(expected) if n not in got_digits)
    if missing:
        reasons.append(f"number(s) missing from audio: {', '.join(missing)}")
    return reasons


def similarity(expected: str, got: str) -> float:
    """Word-level SequenceMatcher ratio. 1.0 = identical word sequence, 0.0 = disjoint.

    Validated against a real incident: the correct transcript scored 0.76-1.00 across 23
    real dialogue clips; a genuinely wrong clip (a different episode's dialogue entirely)
    scores near 0. 0.6 sits well clear of both, so ASR quirks (homophones, digit spelling)
    don't false-positive and a real mismatch doesn't slip through.
    """
    e, g = _norm_words(expected), _norm_words(got)
    if not e and not g:
        return 1.0
    if not e or not g:
        return 0.0
    return difflib.SequenceMatcher(None, e, g).ratio()


def extract_expected_dialogue(prompts_md_text: str) -> dict[str, str]:
    """{clip_id: expected spoken text} from a `7-video-prompts.md`-shaped file.

    All quoted spans in a clip's block are joined (not just the first) -- a multi-line
    exchange inside one clip is legal. A clip with no quoted dialogue at all is expected to
    be silent; short incidental quotes (< 10 chars, e.g. a stray "OK") are ignored so a
    literal on-screen document quote doesn't get mistaken for spoken audio.
    """
    blocks = re.split(r"(?m)^(?=##\s*SC\d{2,3}\b)", prompts_md_text)
    out: dict[str, str] = {}
    for block in blocks:
        m = re.match(r"##\s*(SC\d{2,3})\b", block.strip(), re.IGNORECASE)
        if not m:
            continue
        clip = m.group(1).upper()
        quotes = [q for q in QUOTED.findall(block) if len(q) >= 10]
        out[clip] = " ".join(quotes)
    return out


@dataclass
class ClipAudit:
    clip: str
    status: str  # PASS, FAIL, SILENT_OK, SILENT_BUT_SPOKE, MISSING
    score: float
    expected: str
    transcribed: str
    reasons: list[str] = field(default_factory=list)


Transcriber = Callable[[Path], str]


def _muse_transcriber(model_name: str = "muse-voice-transcribe-1.0") -> Transcriber:
    """Transcribe via Muse Voice Transcribe (Meta Model API, WAV only).

    Extracts a 16 kHz mono WAV with ffmpeg, then calls meta_models.transcribe.
    model_name is kept for CLI compatibility; the Muse model ID is authoritative.
    """
    import subprocess
    import sys
    import tempfile

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import meta_models

    def _transcribe(path: Path) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "audio.wav"
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", str(wav)],
                capture_output=True, text=True,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"ffmpeg audio extract failed: {proc.stderr[:300]}")
            result = meta_models.transcribe(str(wav))
        if isinstance(result, dict):
            for key in ("transcript", "text", "transcription"):
                if result.get(key):
                    return str(result[key]).strip()
            data = result.get("data") or {}
            if isinstance(data, dict) and data.get("transcript"):
                return str(data["transcript"]).strip()
        return str(result).strip()

    return _transcribe


def audit_clips(
    clips: Sequence[tuple[str, Path]],
    expected: dict[str, str],
    transcribe: Transcriber,
    *,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
) -> list[ClipAudit]:
    """Pure-ish audit loop: no filesystem discovery here, just transcribe-and-compare.

    `clips` is [(clip_id, resolved_file_path), ...]. Kept separate from `review_episode`
    below so tests can drive it with a fake transcriber and without a real episode tree.
    """
    results: list[ClipAudit] = []
    for clip, path in clips:
        exp = expected.get(clip, "")
        if not path.exists():
            results.append(ClipAudit(clip, "MISSING", 0.0, exp, "<no file at declared path>"))
            continue
        got = transcribe(path)
        if not exp:
            words = len(_norm_words(got))
            ok = words <= SILENT_WORD_CEILING
            results.append(ClipAudit(clip, "SILENT_OK" if ok else "SILENT_BUT_SPOKE",
                                      1.0 if ok else 0.0, exp, got))
            continue
        score = similarity(exp, got)
        reasons = structural_reasons(exp, got)
        if score < threshold:
            reasons.insert(0, f"word-similarity {score:.2f} below {threshold:.2f}")
        results.append(ClipAudit(clip, "FAIL" if reasons else "PASS", score, exp, got, reasons))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

import json as _json  # noqa: E402


def review_episode(
    channel_slug: str,
    episode_id: str,
    *,
    root: Path | None = None,
    model_name: str = "muse-voice-transcribe-1.0",
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    emit_review: bool = False,
) -> int:
    ep = EPISODES_DIR / channel_slug / episode_id
    manifest_path = ep / "renders" / "render-manifest.json"
    prompts_path = ep / "prompts" / "7-video-prompts.md"

    if not manifest_path.exists():
        print(f"not found: {manifest_path}\nRun 05-render-ingest first.")
        return 2
    if not prompts_path.exists():
        print(f"not found: {prompts_path}\nRun 04f3-ltx-prompt-final first.")
        return 2

    try:
        transcribe = _muse_transcriber(model_name)
    except RuntimeError as exc:
        print(str(exc))
        return 2

    manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = extract_expected_dialogue(prompts_path.read_text(encoding="utf-8"))

    clips: list[tuple[str, Path]] = []
    for entry in manifest.get("clips", []):
        clip = str(entry.get("clip", "")).upper()
        rel = str(entry.get("path", ""))
        clips.append((clip, (ep / rel) if rel else Path("<no path in manifest>")))
    clips.sort(key=lambda c: c[0])

    results = audit_clips(clips, expected, transcribe, threshold=threshold)

    print(f"render audio audit -- {channel_slug} / {episode_id}  (model={model_name}, "
          f"threshold={threshold})")
    print(f"  {len(results)} clip(s) in manifest, {len(expected)} clip(s) with a prompt block\n")
    for r in results:
        tag = f"score={r.score:.2f}" if r.status in ("PASS", "FAIL") else ""
        print(f"  {r.clip}  {r.status:<17} {tag}")

    bad = [r for r in results if r.status in ("FAIL", "MISSING", "SILENT_BUT_SPOKE")]
    print()
    for r in bad:
        print(f"--- {r.clip} [{r.status}] ---")
        for reason in r.reasons:
            print(f"  reason:      {reason}")
        print(f"  expected:    {r.expected!r}")
        print(f"  transcribed: {r.transcribed!r}")
        print()

    overall = "FAIL" if bad else "PASS"
    print(f"OVERALL: {overall}  ({len(results) - len(bad)}/{len(results)} clips clean)")

    if emit_review:
        import hashlib
        from datetime import datetime, timezone

        doc = {
            "schema_version": 2,
            "episode_id": episode_id,
            "reviewed_at_utc": datetime.now(timezone.utc)
                .isoformat(timespec="seconds").replace("+00:00", "Z"),
            "transcribe_model": "muse-voice-transcribe-1.0",
            "similarity_threshold": threshold,
            "source_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "source_prompts_sha256": hashlib.sha256(prompts_path.read_bytes()).hexdigest(),
            "status": overall,
            "clips": [
                {"clip": r.clip, "status": r.status, "score": r.score,
                 "expected": r.expected, "transcribed": r.transcribed,
                 "reasons": r.reasons,
                 "negations_expected": dict(negation_markers(r.expected)),
                 "negations_heard": dict(negation_markers(r.transcribed))}
                for r in results
            ],
        }
        out = ep / "renders" / "audio-content-audit.json"
        out.write_text(_json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="render_audio_audit.py",
        description="Transcribe every ingested render clip (05-render-ingest's manifest) and "
                    "diff it against its approved spoken line in 7-video-prompts.md. "
                    "Reports only, never rewrites or re-renders.")
    ap.add_argument("--channel", required=True, help="channel slug")
    ap.add_argument("--episode", required=True, help="episode id, e.g. EP001")
    ap.add_argument("--model", default="muse-voice-transcribe-1.0", help="transcribe model (default: muse-voice-transcribe-1.0)")
    ap.add_argument("--threshold", type=float, default=DEFAULT_SIMILARITY_THRESHOLD,
                    help=f"minimum word-similarity to PASS (default: {DEFAULT_SIMILARITY_THRESHOLD})")
    ap.add_argument("--emit-review", action="store_true",
                    help="also write renders/audio-content-audit.json")
    a = ap.parse_args(argv)
    return review_episode(a.channel, a.episode, model_name=a.model, threshold=a.threshold,
                          emit_review=a.emit_review)


if __name__ == "__main__":
    raise SystemExit(main())
