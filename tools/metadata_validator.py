#!/usr/bin/env python3
"""Validate a `06-distribution-metadata` package against its channel's
`metadata_validation` constants.

WHY THIS EXISTS
---------------
Every other gated stage in this pipeline (04f3's clip prompts, reference
assets, preflight) has a deterministic checker that survives past the one
episode it was written for. `06-distribution-metadata` did not: EP001's
`metadata/package.md` was validated once, by hand, with a throwaway script
run against `channel.json` and thrown away. The next episode got no such
check unless someone remembered to write one again. This module is that
check, made permanent.

It is a checker, never an author: it reads a finished `package.md`, reads
the channel's `metadata_validation` (and relevant `youtube`) block, and
reports pass/fail per constant. It never rewrites the package.

RUN
---
    python tools/metadata_validator.py --channel signed-anyway --episode EP001
    python tools/metadata_validator.py --channel signed-anyway --episode EP001 --emit-review

Exit 0 = every implemented constant satisfied. Exit 1 = at least one FAIL.
Exit 2 = setup problem (missing channel profile or package.md, or the
package's Title/Description sections could not be parsed).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

sys.path.insert(0, str(Path(__file__).resolve().parent))

from project_paths import CHANNEL_PROFILES_DIR, EPISODES_DIR  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# rule catalog — every rule this module can emit must be declared here or
# emitting it raises. Mirrors tools/ltx_prompt_validator.py's own discipline.
# ─────────────────────────────────────────────────────────────────────────────

IMPLEMENTED_RULE_IDS = frozenset(
    {
        "META-D001",  # title exceeds title_max_chars / title_max_characters
        "META-D002",  # banned title pattern present
        "META-D003",  # required disclosure term missing from description
        "META-D004",  # banned description term present
        "META-D005",  # required hashtag missing from description
        "META-D006",  # Title section missing or unparseable
        "META-D007",  # Description section missing or unparseable
        "META-D008",  # youtube.description_line_required not present verbatim
        "META-W001",  # metadata_validation key present but not implemented here
        "META-W002",  # metadata_validation.title_max_chars disagrees with youtube.title_max_characters
    }
)

# Keys this module knows how to check. Anything else found in a channel's
# `metadata_validation` block is a real constraint this tool is silently
# blind to unless it is surfaced — so it is surfaced, as META-W001, rather
# than skipped without a trace.
KNOWN_METADATA_VALIDATION_KEYS = frozenset(
    {
        "required_disclosure_terms",
        "banned_description_terms",
        "banned_title_patterns",
        "title_max_chars",
        "required_hashtags",
    }
)


def _rule_message(rule_id: str, message: str) -> str:
    if rule_id not in IMPLEMENTED_RULE_IDS:
        raise ValueError(f"validator emitted undeclared rule ID: {rule_id}")
    return f"[{rule_id}] {message}"


@dataclass
class Review:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts: dict[str, object] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not self.errors


def _error(review: Review, rule_id: str, message: str) -> None:
    review.errors.append(_rule_message(rule_id, message))


def _warning(review: Review, rule_id: str, message: str) -> None:
    review.warnings.append(_rule_message(rule_id, message))


# ─────────────────────────────────────────────────────────────────────────────
# package.md parsing — no filesystem here, pure text in / dataclass out
# ─────────────────────────────────────────────────────────────────────────────

_SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_FENCE = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)
_BOLD = re.compile(r"\*\*(.+?)\*\*")


@dataclass
class PackageFields:
    title: str | None
    description: str | None


def _extract_section(md_text: str, heading: str) -> str | None:
    """Text between `## {heading}` and the next `##` heading (or EOF)."""
    headings = list(_SECTION.finditer(md_text))
    for i, m in enumerate(headings):
        if m.group(1).strip().lower() == heading.strip().lower():
            start = m.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(md_text)
            return md_text[start:end]
    return None


def parse_package(md_text: str) -> PackageFields:
    title = None
    title_section = _extract_section(md_text, "Title")
    if title_section:
        m = _BOLD.search(title_section)
        if m:
            title = m.group(1).strip()

    description = None
    desc_section = _extract_section(md_text, "Description")
    if desc_section:
        m = _FENCE.search(desc_section)
        if m:
            description = m.group(1).strip("\n")

    return PackageFields(title=title, description=description)


# ─────────────────────────────────────────────────────────────────────────────
# validation
# ─────────────────────────────────────────────────────────────────────────────

def validate_package(fields: PackageFields, channel: Mapping[str, object]) -> Review:
    review = Review()
    mval = channel.get("metadata_validation", {}) or {}
    yt = channel.get("youtube", {}) or {}

    for key in mval:
        if key not in KNOWN_METADATA_VALIDATION_KEYS:
            _warning(review, "META-W001",
                     f"channel.json declares metadata_validation.{key!r} but this validator "
                     "does not implement it -- check it by hand")

    # ── title ──────────────────────────────────────────────────────────────
    if fields.title is None:
        _error(review, "META-D006",
               "package.md's '## Title' section has no bold **title** line to parse")
    else:
        review.facts["title"] = fields.title
        review.facts["title_length"] = len(fields.title)

        max_chars = mval.get("title_max_chars")
        yt_max_chars = yt.get("title_max_characters")
        if max_chars is not None and yt_max_chars is not None and max_chars != yt_max_chars:
            _warning(review, "META-W002",
                     f"metadata_validation.title_max_chars ({max_chars}) disagrees with "
                     f"youtube.title_max_characters ({yt_max_chars})")
        limit = max_chars if max_chars is not None else yt_max_chars
        if limit is not None:
            review.facts["title_max_chars"] = limit
            if len(fields.title) > limit:
                _error(review, "META-D001",
                       f"title is {len(fields.title)} characters, over the {limit}-character limit")

        for pattern in mval.get("banned_title_patterns", []) or []:
            if str(pattern).lower() in fields.title.lower():
                _error(review, "META-D002", f"title contains banned pattern {pattern!r}")

    # ── description ───────────────────────────────────────────────────────
    if fields.description is None:
        _error(review, "META-D007",
               "package.md's '## Description' section has no fenced ```text``` block to parse")
    else:
        review.facts["description_length"] = len(fields.description)
        lowered = fields.description.lower()

        for term in mval.get("required_disclosure_terms", []) or []:
            if str(term).lower() not in lowered:
                _error(review, "META-D003",
                       f"required disclosure term missing from description: {term!r}")

        for term in mval.get("banned_description_terms", []) or []:
            if str(term).lower() in lowered:
                _error(review, "META-D004", f"description contains banned term {term!r}")

        required_hashtags = list(mval.get("required_hashtags", []) or [])
        for tag in yt.get("required_hashtags", []) or []:
            if tag not in required_hashtags:
                required_hashtags.append(tag)
        for tag in required_hashtags:
            if str(tag).lower() not in lowered:
                _error(review, "META-D005", f"required hashtag missing from description: {tag!r}")

        required_line = yt.get("description_line_required")
        if required_line:
            normalized_desc = re.sub(r"\s+", " ", fields.description).strip()
            normalized_line = re.sub(r"\s+", " ", str(required_line)).strip()
            if normalized_line not in normalized_desc:
                _error(review, "META-D008",
                       f"youtube.description_line_required not present verbatim in description: "
                       f"{required_line!r}")

    return review


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def review_metadata(
    channel_slug: str,
    episode_id: str,
    *,
    root: Path | None = None,
    emit_review: bool = False,
) -> int:
    chan_path = CHANNEL_PROFILES_DIR / channel_slug / "channel.json"
    if not chan_path.exists():
        print(f"no channel profile: {chan_path}")
        return 2
    import json
    channel = json.loads(chan_path.read_text(encoding="utf-8"))

    package_path = EPISODES_DIR / channel_slug / episode_id / "metadata" / "package.md"
    if not package_path.exists():
        print(f"not found: {package_path}\nRun 06-distribution-metadata first.")
        return 2

    fields = parse_package(package_path.read_text(encoding="utf-8"))
    review = validate_package(fields, channel)

    print(f"metadata review -- {channel_slug} / {episode_id}")
    if "title" in review.facts:
        print(f"  title: {review.facts['title']!r} ({review.facts['title_length']} chars"
              f"{', limit ' + str(review.facts['title_max_chars']) if 'title_max_chars' in review.facts else ''})")
    if "description_length" in review.facts:
        print(f"  description: {review.facts['description_length']} chars")
    print()
    for e in review.errors:
        print(f"  ERROR  {e}")
    for w in review.warnings:
        print(f"  warn   {w}")
    print()
    overall = "PASS" if review.passed else "FAIL"
    print(f"OVERALL: {overall}")

    if emit_review:
        import hashlib
        import json as _json
        from datetime import datetime, timezone

        doc = {
            "schema_version": 1,
            "episode_id": episode_id,
            "reviewed_at_utc": datetime.now(timezone.utc)
                .isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source_package_sha256": hashlib.sha256(package_path.read_bytes()).hexdigest(),
            "validator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "status": overall,
            "errors": review.errors,
            "warnings": review.warnings,
            "facts": review.facts,
        }
        out = package_path.parent / "validation.json"
        out.write_text(_json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    return 0 if review.passed else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="metadata_validator.py",
        description="Validate an episode's 06-distribution-metadata package.md against "
                    "its channel's metadata_validation constants. Reports only, never rewrites.")
    ap.add_argument("--channel", required=True, help="channel slug")
    ap.add_argument("--episode", required=True, help="episode id, e.g. EP001")
    ap.add_argument("--emit-review", action="store_true",
                    help="also write metadata/validation.json beside package.md")
    a = ap.parse_args(argv)
    return review_metadata(a.channel, a.episode, emit_review=a.emit_review)


if __name__ == "__main__":
    raise SystemExit(main())
