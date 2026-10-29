"""Deterministic checks for owner-locked LTX-2.5 i2v beat prompts.

The validator NEVER rewrites a prompt.  It reports defects so stage 04f3 can
return them to `local_skills/ltx-production-writer` before any render package
is built.  Rule IDs and their rationale are catalogued in
`pipeline/ltx_prompt_validator.md`; every rule this module can emit must be
declared in IMPLEMENTED_RULE_IDS or emitting it raises.

Every clip prompt is the owner-locked PromptRelay-style beat packet: one
`GLOBAL::` continuation anchor plus `BEAT:: <frames> ::` lines totalling 481
(`render.prompt_format == "prompt_relay_beats_v1"`).  The frame labels are a
model-facing pacing convention passed through the current LTX-2.5 graph
unchanged — not the old ComfyUI-PromptRelay node.  See
pipeline/LTX_I2V_CONTRACT.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping, Sequence


RULE_CATALOG_RELATIVE_PATH = "pipeline/ltx_prompt_validator.md"

IMPLEMENTED_RULE_IDS = frozenset(
    {
        # format / owner-locked beat syntax
        "LTXV-D001", "LTXV-D002", "LTXV-D003", "LTXV-D004", "LTXV-D005",
        # positive-only discipline
        "LTXV-D010", "LTXV-D011", "LTXV-D012", "LTXV-D013",
        # required clauses
        "LTXV-D020", "LTXV-D021", "LTXV-D022", "LTXV-D023", "LTXV-D024", "LTXV-D025",
        # dialogue
        "LTXV-D030", "LTXV-D031", "LTXV-D032", "LTXV-D033", "LTXV-D034",
        "LTXV-D035", "LTXV-D036",
        # subject / prose
        "LTXV-D040", "LTXV-D041", "LTXV-D042", "LTXV-D043", "LTXV-D044",
        # multi-shot
        "LTXV-D050", "LTXV-D051",
        # unquoted speech risk / model-facing literalism
        "LTXV-D052", "LTXV-D053",
        # cross-check against locked environment plates
        "LTXV-D054",
        # cross-check against the approved still's confirmed real state
        "LTXV-D055",
        # within-clip prop-state continuity (no invisible re-grab across beats)
        "LTXV-D056",
        # state / continuity
        "LTXV-S001", "LTXV-S002", "LTXV-S003", "LTXV-S004", "LTXV-S005",
        "LTXV-S006",
    }
)

RULE_ID_TOKEN = re.compile(r"\[(LTXV-[DS][0-9]{3})\]")


# ─────────────────────────────────────────────────────────────────────────────
# patterns
# ─────────────────────────────────────────────────────────────────────────────

# Owner-locked PromptRelay-style beat packet (render.prompt_format ==
# "prompt_relay_beats_v1"). The GLOBAL::/BEAT:: labels are a model-facing pacing
# convention passed through the current LTX-2.5 graph unchanged — not the old
# ComfyUI-PromptRelay node. See pipeline/LTX_I2V_CONTRACT.md.
GLOBAL_LINE = re.compile(r"^GLOBAL::\s*(\S.*)$", re.IGNORECASE)
BEAT_LINE = re.compile(r"^BEAT::\s*(\d+)\s*::\s*(\S.*)$", re.IGNORECASE)
BEAT_TOKEN = re.compile(r"^BEAT\s*::", re.IGNORECASE)
GLOBAL_TOKEN = re.compile(r"^GLOBAL\s*::", re.IGNORECASE)
RELAY_TOTAL_FRAMES = 481

# A numeric second-marker of any shape.  LTX-2.5 has no timing syntax at all, so
# every one of these is dead weight that reads as a literal token.
FAKE_TIMING = re.compile(
    r"\(\s*\d+(?:\.\d+)?\s*s(?:ec(?:onds?)?)?\s*\)"          # "(3.0s)"
    r"|\b\d{2}:\d{2}(?:\.\d{1,3})?\b"                          # "00:05.200"
    r"|\bat\s+\d+(?:\.\d+)?\s*seconds?\b"                      # "at 5 seconds"
    r"|\bfrom\s+\d+(?:\.\d+)?\s*s\b"                           # "from 3s"
    r"|\bsecond\s+\d+\b",                                      # "second 4"
    re.IGNORECASE,
)

RENDER_CONFIG_TOKENS = re.compile(
    r"\b\d{1,2}\s*:\s*\d{1,2}\s+(?:aspect|ratio|frame)\b"
    r"|\baspect\s+ratio\b"
    r"|\b\d+\s*fps\b|\bframes?\s+per\s+second\b"
    r"|\b\d{3,4}\s*[x×]\s*\d{3,4}\b"
    r"|\b\d+(?:\.\d+)?\s*(?:mp|megapixels?)\b"
    r"|\b(?:1080p|720p|4k)\b"
    r"|\b~?\d+(?:\.\d+)?\s*(?:s|sec|secs|seconds?)\s+(?:clip|shot|scene|long|duration)\b"
    r"|\bltx[- ]?2(?:\.\d)?\b",
    re.IGNORECASE,
)

# Negation in a POSITIVE prompt.  The model renders the tokens it sees.
NEGATIVE_DIRECTIVE = (
    r"\bno\s+(?:added\s+)?(?:captions?|subtitles?|overlay\s+text|text|logos?|watermarks?)\b",
    r"\bno\s+(?:new|other|extra|additional)\s+(?:characters?|people|figures?|animals?|objects?|props?)\b",
    r"\bno\s+one\s+\w+",
    r"\bnever\b",
    r"\bdo\s+not\b",
    r"\bdoesn't\b|\bdon't\b",
    r"\bwithout\s+(?:adding|changing|moving|duplicating|introducing)\b",
    r"\bavoid\s+\w+ing\b",
    r"\bnothing\s+else\b",
)

MOTION_SUPPRESSION = re.compile(
    r"\bminimal\s+motion\b|\bstatic\s+scene\b|\bstill\s+frame\b",
    re.IGNORECASE,
)
# NB: "Low motion." is the mandated closing token of the GLOBAL:: line in the
# owner-locked beat packet, not a suppression error — it is deliberately absent
# from MOTION_SUPPRESSION.

ONSCREEN_TEXT_REQUEST = re.compile(
    r"\b(?:caption|subtitle|title\s+card|lower\s+third|watermark|on-screen\s+text)\b"
    r"|\btext\s+reads?\b|\bwords?\s+appears?\s+on\s+screen\b",
    re.IGNORECASE,
)

INTERNAL_JARGON = (
    "blocking.json",
    "frame-0 requirement",
    "entity ledger",
    "continuity key",
    "stage 04",
    "pipeline",
    "render package",
    "owner gate",
    "channel.json",
    "[style]",
    "[[",
)

AMBIENT_CLAUSE = re.compile(r"Ambient\s*\(\s*slow,\s*subtle\s*\)\s*:", re.IGNORECASE)
ACOUSTIC_CLAUSE = re.compile(r"Acoustic\s+environment\s*:", re.IGNORECASE)
DIALOGUE_PLACEMENT = re.compile(
    r"clear\s+close\s+dialogue\s+front\s+and\s+cent(?:er|re)", re.IGNORECASE
)

# Camera detection is deliberately two-tier.  A single vocabulary list produces
# false positives on ordinary prose — "Bruno's paw slides along the rail" is not
# a dolly, and "a cozy family look" is not a lens.  Unambiguous camera nouns
# stand alone; ambiguous movement verbs must sit beside a camera subject.
UNAMBIGUOUS_CAMERA = re.compile(
    r"\b(?:doll(?:y|ies|ying)|crane|jib|pedestal|tracking\s+shot|handheld|"
    r"push(?:es|ing)?\s+in|pull(?:s|ing)?\s+(?:back|out)|zoom(?:s|ing)?|"
    r"orbit(?:s|ing)?|arc(?:s|ing)?\s+around|over-the-shoulder)\b",
    re.IGNORECASE,
)
CAMERA_SUBJECT = re.compile(r"\b(?:camera|lens|the\s+frame|the\s+shot)\b", re.IGNORECASE)
CAMERA_MOVEMENT_VERB = re.compile(
    r"\b(?:pan(?:s|ning)?|tilt(?:s|ing)?|truck(?:s|ing)?|slide[sr]?|slides?|"
    r"track(?:s|ing)?|follow(?:s|ing)?|drift(?:s|ing)?|glide[sd]?|glides?|"
    r"begins?|rise[sd]?|rises?|circles?)\b",
    re.IGNORECASE,
)


def _is_camera_sentence(sentence: str) -> bool:
    if UNAMBIGUOUS_CAMERA.search(sentence):
        return True
    return bool(CAMERA_SUBJECT.search(sentence) and CAMERA_MOVEMENT_VERB.search(sentence))

LABELLED_DIALOGUE_BLOCK = re.compile(
    r"^\s*(?:spoken\s+dialogue|dialogue|lines?|speech|voice[- ]over)\s*(?:,[^:\n]{0,60})?\s*:",
    re.IGNORECASE | re.MULTILINE,
)

QUOTED = re.compile(r"[\"“]([^\"“”]{1,600}?)[\"”]")

NARRATOR_WORD = re.compile(r"\bnarrator\b", re.IGNORECASE)

CLOSED_MOUTH = re.compile(
    r"\bmouths?\s+(?:stays?\s+)?closed\b|\bclosed[- ]mouth(?:ed)?\b|\blips?\s+(?:stay\s+)?closed\b",
    re.IGNORECASE,
)

VISIBLE_ACTION_VERB = re.compile(
    r"\b(?:glance[sd]?|look(?:s|ed|ing)?|turn(?:s|ed|ing)?|reach(?:es|ed|ing)?|lift(?:s|ed|ing)?|"
    r"lower(?:s|ed|ing)?|brush(?:es|ed|ing)?|nod(?:s|ded|ding)?|shake[sd]?|tilt(?:s|ed|ing)?|"
    r"lean(?:s|ed|ing)?|wave[sd]?|point(?:s|ed|ing)?|straighten(?:s|ed|ing)?|press(?:es|ed|ing)?|"
    r"grip(?:s|ped|ping)?|rest(?:s|ed|ing)?|settle[sd]?|shift(?:s|ed|ing)?|step(?:s|ped|ping)?|"
    r"drop(?:s|ped|ping)?|raise[sd]?|hold(?:s|ing)?|tighten(?:s|ed|ing)?|droop(?:s|ed|ing)?|"
    r"perk(?:s|ed|ing)?|paw|ears?|tail|shoulders?|head|chin|gaze)\b",
    re.IGNORECASE,
)

CUT_LANGUAGE = re.compile(
    r"\b(?:hard|match|smash|jump|quick)\s+cut\b|\bcuts?\s+to\b|\bdissolves?\s+into\b"
    r"|\bthe\s+view\s+cuts\b|\bcross[- ]?fade[sd]?\b",
    re.IGNORECASE,
)

# LTXV-D052 — an unquoted speech-indicating verb, with no quoted dialogue anywhere in the
# same GLOBAL:: text or BEAT:: text, reads to the model as an actual line to vocalize — even
# though it was authored as narrative shorthand ("Pip tips his head back and says Bruno
# always says Paw Street looks after its own"). Caught live: app-vidgen-dist's relay-to-prose
# compiler (compile_relay_style_prompt, which every render passes through, since LTX-2.5 has
# no native GLOBAL::/BEAT:: understanding) turns that clause into plain chronological prose
# with nothing to mark it as indirect — the model spoke it, then spoke the real quoted line
# again moments later. "tells?/told" is deliberately excluded: "the way he was told" is a
# common, safe past-tense/passive idiom with a materially different risk profile from an
# active "says X" assertion, and was the one false positive found testing this rule.
UNQUOTED_SPEECH_VERB = re.compile(
    r"\b(?:says?|asks?|answers?|repl(?:y|ies|ied)|announces?|whispers?|shouts?|exclaims?|"
    r"states?|remarks?|calls?\s+out)\b",
    re.IGNORECASE,
)

# LTXV-D053 — a numeric camera-motion spec ("pans 45 degrees", "arcs at 2 degrees/sec")
# reads to LTX-2.5 as a literal on-screen token, not a motion instruction; the model has
# no numeric camera control, only natural-language description ("a slow arc around the
# subject"). Adopted from the ltx-2-5-prompter reference skill's pitfall #8, cross-checked
# against every clip in this pipeline (zero prior instances) before enabling as a hard rule.
NUMERIC_CAMERA_SPEC = re.compile(
    r"\d+\s*(?:°|degrees?\b)|\d+\s*(?:fps|/\s*sec\b|per\s+second\b)",
    re.IGNORECASE,
)

# LTXV-D054 — a ground/terrain surface word in a clip's prose that never appears in the
# locked description of any environment or prop plate that clip is tagged with. Caught live
# 2026-10-29: SC06 and SC14 both said a prop was set down "in the grass", inherited almost
# verbatim from the original script (03a/03b, written before the environment was visually
# locked at 04c) — this episode's actual environment is a wooden porch deck with no grass at
# either spot. Deliberately excludes "dirt": it is legitimately ambiguous here (Bruno's
# cardigan carries "porch-dirt ground into the knees and elbows" as a wardrobe stain, not a
# ground claim), and was the one likely false positive found scoping this rule. Requires the
# per-episode `_context/environment-locks.json` sidecar (04c) to run at all — an episode
# without one skips this rule rather than failing on a missing optional input.
GROUND_SURFACE_WORD = re.compile(
    r"\b(?:grass|lawn|meadow|gravel|sand|pavement|sidewalk|asphalt)\b",
    re.IGNORECASE,
)
CLIP_ENV_TAG = re.compile(r"\[\[((?:ENV|PROP)\d{2,4})\]\]")

# LTXV-D056 — a prop already set at rest in an earlier BEAT re-appears "in his/her paws" in a
# later BEAT of the SAME clip with no explicit pickup verb between the two. Caught live
# 2026-10-29: SC06's opening beat had Fin "set the wrench down"; his speaking beat two lines
# later re-described it as "in his paws" and had him "set the wrench down" a second time — an
# invisible re-grab the model had to invent between beats, which is exactly the kind of gap a
# generation model fills with whatever nearby object it associates with "picking something up"
# (it picked the flashlight instead, on the actual render). The state-before/gesture clauses for
# a later beat must be written from the object's CURRENT rested state, not re-copied from an
# earlier draft of the clip. `PICKUP_VERB` is the escape hatch for a clip that legitimately does
# pick the object back up — write the pickup explicitly and this rule clears.
REST_VERB = re.compile(
    r"\b(?:sets?|puts?|lays?|places?)\b[^.]{0,30}\bdown\b|\brest(?:s|ing)?\s+(?:flat\s+)?(?:down\s+)?on\b",
    re.IGNORECASE,
)
HOLD_PHRASE = re.compile(r"\bin\s+(?:his|her|their)\s+paws?\b", re.IGNORECASE)
PICKUP_VERB = re.compile(
    r"\bpicks?\s+(?:it\s+)?(?:back\s+)?up\b|\breaches?\s+for\b|\bretrieves?\b|\blifts?\s+it\b|\bgrabs?\b",
    re.IGNORECASE,
)

AUDIO_CONTINUITY = re.compile(
    r"\b(?:continues?|carries|persists?|drops?|fades?|remains?|holds?)\b[^.]{0,60}"
    r"\b(?:across|through|over)\s+the\s+cut\b"
    r"|\b(?:across|through)\s+the\s+cut\b[^.]{0,60}\b(?:continues?|remains?|drops?)\b",
    re.IGNORECASE,
)

# Idioms / abstract verbs LTX reads literally.  Curated; grows only by escalation
# from a real render failure, never speculatively.
LITERAL_READER_TRAPS = (
    r"\bcatch(?:es|ing)?\s+(?:his|her|their|the)\s+eye\b",
    r"\bwithdraw(?:s|ing)?\b",
    r"\bholds?\s+there\b",
    r"\bthe\s+way\s+it\s+came\b",
    r"\btakes?\s+in\s+the\s+(?:room|scene|sight)\b",
    r"\bdrinks?\s+in\b",
    r"\bhangs?\s+in\s+the\s+air\b",
    r"\bmelts?\s+away\b",
    r"\bbreaks?\s+into\s+a\s+smile\b",
    r"\bsomething\s+shifts?\b",
    r"\bbeat\s+passes\b",
)

DURATION_FILLER = re.compile(
    r"(?:^|[,;.]\s*)(?:a\s+long\s+beat|a\s+beat|for\s+a\s+while|a\s+moment\s+passes|"
    r"time\s+passes)\s*(?=[,;.]|$)",
    re.IGNORECASE,
)

# Bare collective/species words that render as photoreal humans on an
# anthropomorphic channel unless explicitly qualified.
BARE_CROWD = re.compile(
    r"\b(?:neighbou?rs?|kids?|children|adults?|people|villagers?|crowd|shoppers?|"
    r"passersby|bystanders?|customers?|guests?|families)\b",
    re.IGNORECASE,
)
ANTHRO_QUALIFIER = re.compile(r"anthropomorphic", re.IGNORECASE)

# Terminal punctuation, optionally followed by a closing quote — English puts the
# full stop inside the quotation marks, so `…debatable." Clover…` ends a sentence
# just as `…debatable. Clover…` does.
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|(?<=[.!?][\"”])\s+")
WORD = re.compile(r"\b[\w'’-]+\b")


# ─────────────────────────────────────────────────────────────────────────────
# result type
# ─────────────────────────────────────────────────────────────────────────────

def _rule_message(rule_id: str, message: str) -> str:
    if rule_id not in IMPLEMENTED_RULE_IDS:
        raise ValueError(f"validator emitted undeclared rule ID: {rule_id}")
    return f"[{rule_id}] {message}"


@dataclass
class ClipReview:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts: dict[str, object] = field(default_factory=dict)
    # rule IDs whose check could NOT run for want of an optional input (no
    # voice-signatures.json, no spoken_word_band, no cast source). "not checked"
    # is not "passed" — the CLI surfaces these per clip.
    skipped: list[str] = field(default_factory=list)

    def _skip(self, *rule_ids: str) -> None:
        for r in rule_ids:
            if r not in IMPLEMENTED_RULE_IDS:
                raise ValueError(f"validator marked undeclared rule ID skipped: {r}")
            if r not in self.skipped:
                self.skipped.append(r)

    @property
    def passed(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, object]:
        emitted = sorted(
            {
                match.group(1)
                for message in (*self.errors, *self.warnings)
                if (match := RULE_ID_TOKEN.match(message))
            }
        )
        facts = dict(self.facts)
        facts["emitted_rule_ids"] = emitted
        return {
            "status": "PASS" if self.passed else "FAIL",
            "errors": self.errors,
            "warnings": self.warnings,
            "skipped": sorted(self.skipped),
            "facts": facts,
        }


def _error(review: ClipReview, rule_id: str, message: str) -> None:
    review.errors.append(_rule_message(rule_id, message))


def _warning(review: ClipReview, rule_id: str, message: str) -> None:
    review.warnings.append(_rule_message(rule_id, message))


@dataclass(frozen=True)
class RelayPrompt:
    global_text: str
    beats: tuple[tuple[int, str], ...]

    @property
    def model_text(self) -> str:
        """GLOBAL text plus every beat's text, newline-joined — the frame labels
        are stripped, so every downstream prose rule reads only model-facing words."""
        return "\n".join((self.global_text, *(text for _, text in self.beats)))


def _parse_relay(prompt: str) -> tuple[RelayPrompt | None, list[tuple[str, str]]]:
    """Parse the strict, owner-locked PromptRelay-style beat packet.

    Returns (RelayPrompt | None, [(rule_id, message), ...]). A prompt that is not
    in beat form at all fails LTXV-D001; a malformed beat or a frame total other
    than 481 fails LTXV-D002.
    """
    lines = [line.strip() for line in prompt.splitlines() if line.strip()]
    errors: list[tuple[str, str]] = []
    if not lines:
        return None, [("LTXV-D001", "prompt is empty; it needs one GLOBAL:: line and BEAT:: lines")]
    first = GLOBAL_LINE.fullmatch(lines[0])
    if not first:
        errors.append(("LTXV-D001", "first non-empty line must be GLOBAL:: <continuation anchor>"))
        global_text = ""
        start = 0
    else:
        global_text = first.group(1)
        start = 1
    beats: list[tuple[int, str]] = []
    for line in lines[start:]:
        if GLOBAL_TOKEN.match(line):
            errors.append(("LTXV-D001", "a relay prompt must contain exactly one GLOBAL:: line"))
            continue
        match = BEAT_LINE.fullmatch(line)
        if match:
            frames = int(match.group(1))
            if frames <= 0:
                errors.append(("LTXV-D002", "every BEAT:: duration must be a positive integer frame count"))
            else:
                beats.append((frames, match.group(2)))
        elif BEAT_TOKEN.match(line):
            errors.append(("LTXV-D002", "BEAT:: must use exactly BEAT:: <positive integer frames> :: <text>"))
        else:
            errors.append(("LTXV-D001", "relay prompts may contain only GLOBAL:: and BEAT:: lines"))
    if not beats:
        errors.append(("LTXV-D001", "prompt has no valid BEAT:: blocks"))
    elif sum(frames for frames, _ in beats) != RELAY_TOTAL_FRAMES:
        errors.append((
            "LTXV-D002",
            f"BEAT:: frame counts total {sum(frames for frames, _ in beats)}, expected "
            f"{RELAY_TOTAL_FRAMES} for the locked 20-second / 24-fps packet",
        ))
    return (RelayPrompt(global_text, tuple(beats)) if global_text and beats else None), errors


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sentences(prompt: str) -> list[str]:
    """Split into sentences WITHOUT breaking inside quoted dialogue.

    Dialogue routinely ends on `!` or `?`, and a naive split on terminal
    punctuation cuts mid-quote. The fragments that result start with an
    unbalanced quote mark and glue a speech tail onto the next clause, which
    made a character action read as a camera move (`LTXV-D025`) and hid the
    real final beat (`LTXV-D041`). Found against real clip-prompt drafts, 2026-10-29.

    Quoted spans are masked to same-length filler so offsets still line up with
    the original text; the returned sentences are sliced from the original, so
    nothing is rewritten.
    """
    def mask(match: "re.Match[str]") -> str:
        body = match.group(0)
        inner = body[1:-1]
        # Keep a quote's FINAL terminal mark visible: it ends the outer sentence
        # too. Everything else inside the quote is hidden from the splitter.
        if inner and inner[-1] in ".!?":
            inner = "\x00" * (len(inner) - 1) + inner[-1]
        else:
            inner = "\x00" * len(inner)
        return body[0] + inner + body[-1]

    text = prompt.strip()
    masked = QUOTED.sub(mask, text)
    out: list[str] = []
    start = 0
    for match in SENTENCE_SPLIT.finditer(masked):
        out.append(text[start:match.start()].strip())
        start = match.end()
    out.append(text[start:].strip())
    return [s for s in out if s]


def strip_dialogue(prompt: str) -> str:
    """Prose with quoted speech removed — what most positive-text rules read."""
    return QUOTED.sub(" ", prompt)


def spoken_words(prompt: str) -> int:
    return sum(len(WORD.findall(match.group(1))) for match in QUOTED.finditer(prompt))


def _names_a_character(sentence: str, first_names: Sequence[str]) -> bool:
    lowered = sentence.lower()
    return any(re.search(rf"\b{re.escape(n.lower())}\b", lowered) for n in first_names)


# ─────────────────────────────────────────────────────────────────────────────
# main text validation
# ─────────────────────────────────────────────────────────────────────────────

def validate_prompt(
    prompt: str,
    *,
    character_first_names: Sequence[str] = (),
    visible_character_count: int | None = None,
    voice_signatures: Mapping[str, str] | None = None,
    spoken_word_band: tuple[int, int] | None = None,
    max_words: int = 450,
    sentence_band: tuple[int, int] = (4, 8),
    declared_cuts: int = 0,
    anthropomorphic_channel: bool = False,
    style_echo: str = "",
    props: Sequence[Mapping[str, object]] = (),
) -> ClipReview:
    """Validate one render-ready owner-locked LTX-2.5 beat prompt."""
    review = ClipReview()
    relay, format_errors = _parse_relay(prompt)
    for rule_id, message in format_errors:
        _error(review, rule_id, message)
    model_text = relay.model_text if relay else prompt
    prose = strip_dialogue(model_text)
    sentences = _sentences(model_text)
    total_words = len(WORD.findall(model_text))
    spoken = spoken_words(model_text)

    review.facts["total_word_count"] = total_words
    review.facts["spoken_word_count"] = spoken
    review.facts["sentence_count"] = len(sentences)
    review.facts["has_dialogue"] = spoken > 0
    review.facts["relay_beat_count"] = len(relay.beats) if relay else 0
    review.facts["relay_frame_total"] = sum(frames for frames, _ in relay.beats) if relay else 0

    # ── format / owner-locked beat syntax ─────────────────────────────────────
    if (match := FAKE_TIMING.search(prose)):
        _error(review, "LTXV-D002",
               f"prompt contains an unstructured numeric timing marker {match.group(0)!r}; "
               "timing belongs only in the locked BEAT:: frame labels")
    if (match := RENDER_CONFIG_TOKENS.search(prose)):
        _error(review, "LTXV-D003",
               f"render configuration belongs in the graph, never the prompt text: {match.group(0)!r}")
    if total_words > max_words:
        _warning(review, "LTXV-D004",
                 f"prompt is {total_words} words, past the runaway tripwire of {max_words}; "
                 "check for a repeated room inventory or duration filler — LTX-2.5 has no vendor "
                 "word ceiling, so never trim a load-bearing identity, audio or camera anchor to fit it")
    low, high = sentence_band
    if relay is None and spoken == 0 and not (low <= len(sentences) <= high):
        # In the owner-locked beat packet the BEAT:: structure IS the length
        # control; sentence-counting a GLOBAL + N beats is not meaningful.
        _warning(review, "LTXV-D005",
                 f"non-dialogue clip has {len(sentences)} sentences; single-take guidance is {low}-{high}")

    # ── positive-only discipline ──────────────────────────────────────────────
    for pattern in NEGATIVE_DIRECTIVE:
        if (match := re.search(pattern, prose, re.IGNORECASE)):
            _error(review, "LTXV-D010",
                   f"negation in a positive prompt: {match.group(0)!r} — the model renders the "
                   "tokens it sees; suppression belongs in the negative prompt only")
    if MOTION_SUPPRESSION.search(prose):
        _error(review, "LTXV-D011",
               "blanket motion-suppression token present; describe the exact plausible motion instead")
    if ONSCREEN_TEXT_REQUEST.search(prose):
        _error(review, "LTXV-D012",
               "on-screen text/caption requested; spelling is not guaranteed across frames — "
               "titles and labels are a post-production pass")
    lowered = model_text.lower()
    for phrase in INTERNAL_JARGON:
        if phrase in lowered:
            _error(review, "LTXV-D013", f"internal pipeline jargon leaked into the prompt: {phrase!r}")

    # ── required clauses ──────────────────────────────────────────────────────
    ambient = AMBIENT_CLAUSE.search(model_text)
    acoustic = ACOUSTIC_CLAUSE.search(model_text)
    if not ambient:
        _error(review, "LTXV-D020",
               "missing the required 'Ambient (slow, subtle):' visual-motion sentence")
    if not acoustic:
        _error(review, "LTXV-D021",
               "missing the required 'Acoustic environment:' sound sentence")
    if ambient and acoustic:
        for sentence in sentences:
            if AMBIENT_CLAUSE.search(sentence) and ACOUSTIC_CLAUSE.search(sentence):
                _error(review, "LTXV-D022",
                       "ambient motion and acoustic environment are merged into one sentence; "
                       "visual motion and sound are two separate clauses")
                break
    if acoustic and spoken > 0 and not DIALOGUE_PLACEMENT.search(model_text):
        _error(review, "LTXV-D023",
               "a clip with dialogue must state the mix note 'clear close dialogue front and center'")

    camera_sentences = [s for s in sentences if _is_camera_sentence(s)]
    if not camera_sentences:
        _error(review, "LTXV-D024",
               "no camera movement stated; a fully locked camera over a settled character reads "
               "as a dead freeze-frame")
    for sentence in camera_sentences:
        if QUOTED.search(sentence):
            _error(review, "LTXV-D025",
                   "camera movement shares a sentence with a quoted line; they are two separate clauses")
            break

    # ── dialogue ──────────────────────────────────────────────────────────────
    if LABELLED_DIALOGUE_BLOCK.search(prompt):
        _error(review, "LTXV-D030",
               "labelled dialogue block present; a dialogue header reads as a caption track — "
               "fold each line into the speaker's action")
    for match in QUOTED.finditer(model_text):
        carrier = model_text[max(0, match.start() - 240):match.start()]
        tail = carrier.rsplit(".", 1)[-1]
        if not VISIBLE_ACTION_VERB.search(tail):
            _error(review, "LTXV-D031",
                   f"quoted line has no visible action attached to its speaker: "
                   f"{match.group(1)[:48]!r}")
    if voice_signatures:
        first_quote = QUOTED.search(model_text)
        for name, signature in voice_signatures.items():
            occurrences = len(re.findall(re.escape(signature), model_text, re.IGNORECASE))
            if occurrences == 0:
                if first_quote and re.search(rf"\b{re.escape(name)}\b", model_text, re.IGNORECASE):
                    _error(review, "LTXV-D032",
                           f"{name}'s first line is missing the inline voice signature")
            elif occurrences > 1:
                _error(review, "LTXV-D033",
                       f"{name}'s voice signature is stated {occurrences} times; inline on the "
                       "first line only")
    elif spoken > 0:
        review._skip("LTXV-D032", "LTXV-D033")  # no voice-signatures.json to check against
    if spoken_word_band is None and spoken > 0:
        review._skip("LTXV-D034")  # channel declares no render.spoken_word_band
    elif spoken_word_band and spoken > 0:
        lo, hi = spoken_word_band
        if not (lo <= spoken <= hi):
            _error(review, "LTXV-D034",
                   f"clip carries {spoken} spoken words against the channel band {lo}-{hi}")
    if NARRATOR_WORD.search(prose):
        _error(review, "LTXV-D035",
               "the word 'Narrator' binds a voice to nothing visible; describe an off-screen "
               "background voice-over instead")
    if visible_character_count is None and spoken > 0:
        review._skip("LTXV-D036")  # no blocking.json / frame0 cast count to check against
    elif visible_character_count is not None and visible_character_count >= 2 and spoken > 0:
        if not CLOSED_MOUTH.search(prose):
            _error(review, "LTXV-D036",
                   "2+ visible characters with dialogue but no explicit closed-mouth clause for "
                   "the non-speakers")

    # ── subject / prose ───────────────────────────────────────────────────────
    if not character_first_names:
        review._skip("LTXV-D040", "LTXV-D041")  # no cast source (blocking.json / frame0)
    if character_first_names and sentences:
        # In the locked packet the GLOBAL:: line is the opening anchor and the
        # last BEAT:: is the explicit productive tail (its Acoustic clause stays
        # part of that same timed beat). Fall back to sentence slicing only for a
        # prompt that failed to parse as a relay at all.
        opening = relay.global_text if relay else sentences[0]
        # No one visible at frame 0: the rule inverts. Naming an off-frame character in the picture text tells the
        # model a person is near, and with no identity in frame it draws strangers (inside-the-process EP001
        # SC13/SC15/SC29, 2026-10-29). A voice may still speak, in a dialogue beat, as audio only.
        nobody_visible = visible_character_count == 0
        if nobody_visible:
            if _names_a_character(strip_dialogue(opening), character_first_names):
                _error(review, "LTXV-D040",
                       "no character is visible at frame 0, yet the opening names one; an off-frame "
                       "character in the picture text makes the model draw a person - describe the "
                       "empty view instead")
        elif not _names_a_character(opening, character_first_names):
            _error(review, "LTXV-D040",
                   "the first sentence does not name a character as its subject")
        final_beat = relay.beats[-1][1] if relay and relay.beats else None
        if final_beat is None and not relay:
            _rest = list(sentences)
            if style_echo and _rest and style_echo.strip().rstrip(".").lower() in _rest[-1].lower():
                _rest.pop()
            while _rest and (ACOUSTIC_CLAUSE.match(_rest[-1]) or AMBIENT_CLAUSE.match(_rest[-1])):
                _rest.pop()
            final_beat = _rest[-1] if _rest else None
        if final_beat is None:
            _error(review, "LTXV-D041", "the clip has no final action beat")
        elif nobody_visible:
            if _names_a_character(strip_dialogue(final_beat), character_first_names):
                _error(review, "LTXV-D041",
                       "no character is visible at frame 0, yet the final beat names one; the model "
                       "reveals a stranger - end on what the frame shows")
        elif not _names_a_character(final_beat, character_first_names):
            _error(review, "LTXV-D041",
                   "the final action beat does not name a character as its subject")
    if anthropomorphic_channel:
        for match in BARE_CROWD.finditer(prose):
            window = prose[max(0, match.start() - 90):match.end() + 40]
            if not ANTHRO_QUALIFIER.search(window):
                _error(review, "LTXV-D042",
                       f"unqualified collective {match.group(0)!r} renders as photoreal humans; "
                       "state 'anthropomorphic animal' explicitly")
                break
    for pattern in LITERAL_READER_TRAPS:
        if (match := re.search(pattern, prose, re.IGNORECASE)):
            _error(review, "LTXV-D043",
                   f"LTX reads literally: {match.group(0)!r} is an idiom or abstract verb — "
                   "use a concrete photographable action")
    if (match := DURATION_FILLER.search(prose)):
        _warning(review, "LTXV-D044",
                 f"duration filler with no filmable content: {match.group(0).strip(' ,;.')!r}")

    # ── multi-shot ────────────────────────────────────────────────────────────
    cuts = list(CUT_LANGUAGE.finditer(prose))
    review.facts["observed_cut_phrases"] = [m.group(0) for m in cuts]
    if declared_cuts == 0 and cuts:
        _error(review, "LTXV-D050",
               f"single-take clip contains unmarked cut language: {cuts[0].group(0)!r}")
    if declared_cuts:
        if len(cuts) != declared_cuts:
            _error(review, "LTXV-D051",
                   f"{declared_cuts} cut(s) declared but {len(cuts)} named in prose")
        if not AUDIO_CONTINUITY.search(prose):
            _error(review, "LTXV-D051",
                   "a declared cut must state whether music, dialogue and ambience continue across it")

    # ── unquoted speech risk ─────────────────────────────────────────────────
    if relay:
        segments = [("GLOBAL::", relay.global_text)] + [
            (f"BEAT:: {frames} ::", text) for frames, text in relay.beats
        ]
        for label, segment_text in segments:
            m = UNQUOTED_SPEECH_VERB.search(segment_text)
            if m and not QUOTED.search(segment_text):
                _error(review, "LTXV-D052",
                       f"{label} names speech ({m.group(0)!r}) with no quoted line anywhere "
                       f"in the same segment — an unquoted 'X says Y' clause is read as an "
                       f"actual line by the model and duplicates when the real quote follows; "
                       f"rewrite as physical/atmospheric description only")

    if (m := NUMERIC_CAMERA_SPEC.search(prose)):
        _error(review, "LTXV-D053",
               f"numeric camera-motion spec {m.group(0)!r} reads as a literal on-screen "
               f"token; LTX-2.5 has no numeric camera control — describe the motion in "
               f"natural language instead (\"a slow arc\", not a measured angle or rate)")

    # ── within-clip prop-state continuity (no invisible re-grab across beats) ─────────────────
    if not props:
        review._skip("LTXV-D056")  # no blocking.json props[] to check against
    elif relay and relay.beats:
        for prop in props:
            name = str((prop or {}).get("name", "")).strip()
            if not name:
                continue
            noun = name.split()[-1].lower()
            if len(noun) < 3:
                continue
            noun_re = re.compile(r"\b" + re.escape(noun) + r"\b", re.IGNORECASE)
            rested_in_beat: int | None = None
            for i, (frames, text) in enumerate(relay.beats):
                if not noun_re.search(text):
                    continue
                if rested_in_beat is not None and HOLD_PHRASE.search(text) and not PICKUP_VERB.search(text):
                    _error(review, "LTXV-D056",
                           f"{name!r} was already set at rest in an earlier BEAT (frame "
                           f"{relay.beats[rested_in_beat][0]}) but BEAT {frames} describes it "
                           f"'in his/her paws' again with no pickup verb between — this forces "
                           f"an invisible re-grab the model fills with whatever object is at "
                           f"hand; write this beat from the object's current rested state, or "
                           f"add an explicit pickup verb if it is genuinely picked back up")
                if REST_VERB.search(text):
                    rested_in_beat = i

    return review


def validate_environment_consistency(
    prompt: str,
    still_chunk: str | None,
    env_locks: Mapping[str, str],
) -> list[str]:
    """LTXV-D054 — a ground/terrain word in the clip's prose must appear in the locked
    description of at least one environment/prop plate the clip is tagged with.

    `still_chunk` is the clip's full `## SCnn ...` block from `6-image-prompts.md` (kept,
    not stripped, so its `[[ENVnnn]]`/`[[PROPnnn]]` tag line is still there — the same tag
    line the writer put on the video prompt, since both are authored against the same
    blocking). `env_locks` is `{tag: locked_string}` from `_context/environment-locks.json`;
    an episode without that optional sidecar skips this rule entirely rather than failing.
    """
    if not env_locks or not still_chunk:
        return []
    tags = CLIP_ENV_TAG.findall(still_chunk)
    if not tags:
        return []
    locked_text = " ".join(env_locks.get(t, "") for t in tags).lower()
    if not locked_text.strip():
        return []
    prose = strip_dialogue(prompt).lower()
    errors: list[str] = []
    for m in GROUND_SURFACE_WORD.finditer(prose):
        word = m.group(0).lower()
        if word not in locked_text:
            errors.append(_rule_message(
                "LTXV-D054",
                f"{word!r} is not in the locked description of this clip's tagged "
                f"environment/prop plate(s) ({', '.join(tags)}); i2v renders what the plate "
                f"actually shows, not what the prose assumes — verify the ground surface "
                f"against the plate before keeping this word"))
    return errors


def validate_still_grounding_facts(
    prompt: str,
    clip: str,
    still_facts: Sequence[Mapping[str, str]],
) -> list[str]:
    """LTXV-D055 — a clip's prose must not revert to a character/state phrasing that a
    confirmed real observation of the APPROVED still already overrode.

    `still_facts` is the list of fact records from `_context/frame0-still-facts.json`
    whose `clip` matches this one (each: `character`, `detail`, `confirmed_state_pattern`,
    `contradicting_pattern`, `source`). These are hand-recorded, one at a time, only when
    a real still-vs-prompt deviation was directly confirmed against the rendered pixel
    (never guessed) — e.g. Bruno's glasses rendering on-face instead of on-chain in
    SC02/SC09, or SC28 showing him fully settled rather than the "perched forward" the
    still-prompt originally asked for. The 04f3 builder already sources these overrides by
    hand; this rule makes a silent regression (a rebuild that drops the override) a hard
    validator failure instead of something only caught by re-eyeballing every pixel again.
    An episode with no sidecar, or a clip with no fact records, skips silently — this is
    NOT a substitute for the still-gate review, only a guard against losing its findings.
    """
    if not still_facts:
        return []
    prose = strip_dialogue(prompt)
    errors: list[str] = []
    for fact in still_facts:
        contradicting = fact.get("contradicting_pattern")
        if not contradicting:
            continue
        if re.search(contradicting, prose, re.IGNORECASE):
            errors.append(_rule_message(
                "LTXV-D055",
                f"{fact.get('character', '?')}'s {fact.get('detail', 'state')} clause matches "
                f"{contradicting!r} — this contradicts the confirmed real state of the "
                f"APPROVED still for {clip} ({fact.get('source', 'see frame0-still-facts.json')}); "
                f"the still-gate override for this fact appears to have been dropped"))
    return errors


# ─────────────────────────────────────────────────────────────────────────────
# state / continuity validation
# ─────────────────────────────────────────────────────────────────────────────

FRAME0_REQUIRED_KEYS = frozenset(
    {"clip", "touched_objects", "characters", "frame0_state", "props_at_rest",
     "first_action_performable", "continues_from"}
)

CHARACTER_STATE_KEYS = frozenset(
    {"pos", "facing", "gaze", "pose", "expression", "mouth", "hands"}
)


def validate_frame0_requirements(
    prompt: str,
    block: Mapping[str, object],
    *,
    blocking_characters: Sequence[str] = (),
) -> list[str]:
    """LTXV-S001/S002/S003 — the block is complete, and it covers the prose."""
    errors: list[str] = []
    missing = FRAME0_REQUIRED_KEYS - set(block)
    if missing:
        errors.append(_rule_message(
            "LTXV-S001",
            f"frame-0 requirement block is missing field(s): {sorted(missing)}"))
        return errors

    states = block.get("frame0_state")
    if not isinstance(states, Mapping) or not states:
        errors.append(_rule_message("LTXV-S001", "frame0_state must be a non-empty mapping"))
        return errors
    for name, raw in states.items():
        if not isinstance(raw, Mapping):
            errors.append(_rule_message("LTXV-S001", f"{name}: frame0_state entry must be a mapping"))
            continue
        gaps = CHARACTER_STATE_KEYS - set(raw)
        if gaps:
            errors.append(_rule_message(
                "LTXV-S001", f"{name}: frame-0 state is missing {sorted(gaps)}"))
        if str(raw.get("mouth", "")).strip() == "":
            errors.append(_rule_message(
                "LTXV-S001", f"{name}: frame-0 mouth state must be stated explicitly"))

    if block.get("first_action_performable") is not True:
        errors.append(_rule_message(
            "LTXV-S001",
            "the clip's first action must be performable from this frozen instant; "
            "re-roll the still rather than rewording the clip"))

    prose = strip_dialogue(prompt).lower()
    touched = block.get("touched_objects")
    if not isinstance(touched, Sequence) or isinstance(touched, (str, bytes)):
        errors.append(_rule_message("LTXV-S002", "touched_objects must be a list"))
    else:
        resting = block.get("props_at_rest")
        resting_keys = {str(k).lower() for k in resting} if isinstance(resting, Mapping) else set()
        for obj in touched:
            name = str(obj).strip().lower()
            if not name:
                continue
            if name not in resting_keys:
                errors.append(_rule_message(
                    "LTXV-S002",
                    f"{obj!r} is touched by the action but has no frame-0 resting state; "
                    "i2v never invents objects"))
            head = re.sub(r"^(?:the|a|an)\s+", "", name)
            if head and head not in prose:
                errors.append(_rule_message(
                    "LTXV-S002",
                    f"{obj!r} is declared touched but never named in the clip prose"))

    declared = block.get("characters")
    if blocking_characters and isinstance(declared, Sequence) and not isinstance(declared, (str, bytes)):
        if sorted(str(c) for c in declared) != sorted(blocking_characters):
            errors.append(_rule_message(
                "LTXV-S003",
                f"clip cast {sorted(str(c) for c in declared)} disagrees with blocking.json "
                f"{sorted(blocking_characters)}"))

    # A character who is off-screen at frame 0 must not be written as entering the frame. i2v has no identity
    # to condition on, so it invents a new person (inside-the-process EP001 SC29, 2026-10-29: "the Explorer
    # leans back into frame" rendered a different man with a visible face). Presence changes across a cut.
    for name, raw in states.items():
        if not isinstance(raw, Mapping) or not _is_off_screen(raw.get("pose")):
            continue
        who = re.escape(str(name).lower())
        for sentence in re.split(r"(?<=[.;])\s+", prose):
            if re.search(rf"\b{who}\b", sentence) and OFFSCREEN_ENTRY.search(sentence):
                errors.append(_rule_message(
                    "LTXV-S003",
                    f"{name} is off-screen at frame 0 but the prose brings them into frame "
                    f"({OFFSCREEN_ENTRY.search(sentence).group(0)!r}); i2v invents a new identity - "
                    "change who is on screen across a cut instead"))
                break
    return errors


OFFSCREEN_ENTRY = re.compile(
    r"\b(?:(?:leans?|steps?|walks?|moves?|comes?|slides?)\s+(?:back\s+)?into\s+(?:the\s+)?(?:frame|view|shot)|"
    r"enters?\s+(?:the\s+)?(?:frame|shot)|appears?\s+(?:in|at)\s+(?:the\s+)?(?:frame|edge))\b",
    re.IGNORECASE)


def _is_off_screen(pose: object) -> bool:
    text = str(pose or "").lower()
    return "off-screen" in text or "not drawn in frame" in text


STILL_HEADER = re.compile(r"^##\s*(SC\d{2,3})\b", re.IGNORECASE | re.MULTILINE)
MOTION_VERB = re.compile(
    r"\b(?:reach(?:es|ing)|lift(?:s|ing)|rais(?:es|ing)|lower(?:s|ing)|throw(?:s|ing)|"
    r"walk(?:s|ing)|run(?:s|ning)|turn(?:s|ing)\s+toward|swing(?:s|ing)|open(?:s|ing)|"
    r"clos(?:es|ing)|pour(?:s|ing)|hand(?:s|ing)\s+over|pick(?:s|ing)\s+up|"
    r"set(?:s|ting)\s+down|begin(?:s|ning)|start(?:s|ing)\s+to|mid-(?:step|stride|motion|air))\b",
    re.IGNORECASE,
)
# "opening" is also a noun ("an arched opening", "whose opening is dim grey"), common in locked
# environment strings that must be copied verbatim. It reads as a noun only when a determiner or
# possessive, optionally plus one adjective, sits right before it. "The blades are opening"
# still fails.
NOUN_OPENING = re.compile(
    r"\b(?:a|an|the|its|their|his|her|whose|this|that|each|one)\s+(?:[a-z-]+\s+)?$", re.IGNORECASE)


def _still_motion_verb(prose: str):
    for m in MOTION_VERB.finditer(prose):
        if m.group(0).lower() == "opening" and NOUN_OPENING.search(prose[max(0, m.start() - 40):m.start()]):
            continue
        return m
    return None


def validate_still_covers_requirements(
    still_prompt: str,
    block: Mapping[str, object],
    *,
    clip_id: str | None = None,
) -> list[str]:
    """LTXV-S006 — the STILL prompt is bound to the right clip and contains
    everything that clip's action will touch.

    LTXV-S002 checks the clip prose against its own requirement block. This is
    the other half: without it, a still can be authored against the wrong clip,
    or omit an object the clip reaches for, and nothing catches it until a
    render has been spent.
    """
    errors: list[str] = []

    declared = str(block.get("clip", "")).strip().lower()
    header = STILL_HEADER.search(still_prompt)
    found = header.group(1).lower() if header else None
    target = (clip_id or declared).lower()
    if target:
        if found is None:
            errors.append(_rule_message(
                "LTXV-S006",
                f"still prompt has no '## {target}' header, so it cannot be bound to a clip"))
        elif found != target:
            errors.append(_rule_message(
                "LTXV-S006",
                f"still prompt is headed {found!r} but carries the requirement block for "
                f"{target!r}; the still would condition the wrong clip"))

    # The `## SC07 | pose:` header and the `[[TAG]]` line are packet metadata, not
    # text the image model sees. Leaving them in would let a character satisfy the
    # prose checks by appearing only as a reference tag — precisely the defect
    # worth catching, since a tag binds identity but stages nothing.
    body = re.sub(r"^##\s*SC\d{2,3}\b.*$", " ", still_prompt, flags=re.IGNORECASE | re.MULTILINE)
    body = re.sub(r"\[\[[A-Za-z0-9_]+\]\]", " ", body)
    prose = strip_dialogue(body).lower()
    touched = block.get("touched_objects")
    if isinstance(touched, Sequence) and not isinstance(touched, (str, bytes)):
        for obj in touched:
            head = re.sub(r"^(?:the|a|an)\s+", "", str(obj).strip().lower())
            if head and head not in prose:
                errors.append(_rule_message(
                    "LTXV-S006",
                    f"{obj!r} is touched by the clip's action but never appears in the still "
                    "prompt; i2v never invents objects"))

    if (m := _still_motion_verb(prose)):
        errors.append(_rule_message(
            "LTXV-S006",
            f"still prompt contains the motion verb {m.group(0)!r}; frame-0 is a settled "
            "STATE, never mid-action"))

    states = block.get("frame0_state")
    if isinstance(states, Mapping):
        for name in states:
            if name and str(name).split("_")[0].lower() not in prose:
                errors.append(_rule_message(
                    "LTXV-S006",
                    f"{name} is in the clip's frame-0 state but is not named in the still prompt"))
    return errors


def validate_continuity(
    clips: Sequence[tuple[str, Mapping[str, object]]],
) -> dict[str, list[str]]:
    """LTXV-S004 — a continuing entity opens where the previous clip left it."""
    failures: dict[str, list[str]] = {}
    previous_id: str | None = None
    previous_end: Mapping[str, object] = {}
    for clip_id, block in clips:
        continues = block.get("continues_from")
        if continues:
            if previous_id is None:
                failures.setdefault(clip_id, []).append(_rule_message(
                    "LTXV-S004", "declares continuity but has no preceding clip"))
            elif str(continues) != previous_id:
                failures.setdefault(clip_id, []).append(_rule_message(
                    "LTXV-S004",
                    f"declares continuity from {continues!r} but the preceding clip is {previous_id!r}"))
            else:
                opening = block.get("frame0_state")
                if isinstance(opening, Mapping) and isinstance(previous_end, Mapping):
                    for name, state in opening.items():
                        prior = previous_end.get(name)
                        if not isinstance(prior, Mapping) or not isinstance(state, Mapping):
                            continue
                        # A cut may change who is on screen; only an in-shot handoff must match.
                        if _is_off_screen(prior.get("pose")) != _is_off_screen(state.get("pose")):
                            continue
                        for key in ("pos", "pose", "hands"):
                            if key in prior and key in state and prior[key] != state[key]:
                                failures.setdefault(clip_id, []).append(_rule_message(
                                    "LTXV-S004",
                                    f"{name}: opening {key}={state[key]!r} conflicts with "
                                    f"{previous_id}'s end {key}={prior[key]!r}"))
        end_state = block.get("end_state")
        previous_end = end_state if isinstance(end_state, Mapping) else {}
        previous_id = clip_id
    return failures


# A still that declares the END state while the clip performs the transition INTO
# it.  High precision by design: a CLOSED door plus opens-in-clip is a legal
# start-state transition and passes.
STATE_TRANSITION_PAIRS = (
    (r"\bdoor\s+(?:is\s+)?(?:already\s+)?open\b", r"\b(?:knocks?|opens?\s+the\s+door|pushes?\s+the\s+door\s+open)\b", "door"),
    (r"\blamp\s+(?:is\s+)?lit\b|\bcandle\s+(?:is\s+)?lit\b", r"\b(?:strikes?\s+a\s+match|lights?\s+the\s+(?:lamp|candle))\b", "lamp/candle"),
    (r"\b(?:seated|sitting|sits)\b", r"\bsits?\s+down\b|\blowers?\s+(?:him|her|them)self\s+(?:in)?to\b", "seating"),
    (r"\bbroken\b|\bshattered\b|\bcracked\b", r"\bbreaks?\b|\bshatters?\b|\bcracks?\b", "breakage"),
    (r"\bheld\s+in\b|\bholding\b|\bin\s+(?:his|her|their)\s+(?:paws?|hands?)\b", r"\bpicks?\s+(?:it\s+)?up\b|\blifts?\s+it\s+from\b", "held prop"),
    (r"\balready\s+placed\b|\bresting\s+on\s+the\s+table\b", r"\bplaces?\s+it\b|\bsets?\s+it\s+down\b", "placement"),
)


def validate_state_transition(still_prompt: str, clip_prompt: str) -> list[str]:
    """LTXV-S005 — the still must not already show the end of an action the clip performs."""
    errors: list[str] = []
    still = strip_dialogue(still_prompt)
    clip = strip_dialogue(clip_prompt)
    for still_pattern, clip_pattern, label in STATE_TRANSITION_PAIRS:
        if re.search(still_pattern, still, re.IGNORECASE) and re.search(clip_pattern, clip, re.IGNORECASE):
            errors.append(_rule_message(
                "LTXV-S005",
                f"the still already shows the completed {label} state while the clip performs the "
                "transition into it; i2v cannot re-enact a finished action"))
    return errors


# ─────────────────────────────────────────────────────────────────────────────
# CLI — validate one episode's clip prompts (04f3 steps 3-4)
# ─────────────────────────────────────────────────────────────────────────────
#
# The library above never touches the filesystem.  This section does: it reads
# an episode's `prompts/7-video-prompts.md`, its `_context/` artifacts and the
# channel profile, runs `validate_prompt` plus every cross-check that has the
# inputs it needs, prints a per-clip verdict and exits non-zero on any error.

import argparse as _argparse
import hashlib as _hashlib
import json as _json
import sys as _sys
from datetime import datetime as _datetime, timezone as _timezone
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parent.parent
_CLIP_HEADER = re.compile(r"^##\s*(SC\d{2,3})\b", re.IGNORECASE)
_TAG_ONLY_LINE = re.compile(r"^\s*(?:\[\[[A-Za-z0-9_]+\]\]\s*)+$")


def _iter_clip_blocks(md_text: str):
    """Yield (clip_id, body) from `## SCnn` blocks; a leading `[[TAG]]` line is
    packet metadata and is dropped."""
    clip: str | None = None
    buf: list[str] = []
    for line in md_text.splitlines():
        m = _CLIP_HEADER.match(line.strip())
        if m:
            if clip:
                yield clip, "\n".join(buf).strip()
            clip, buf = m.group(1).upper(), []
            continue
        if clip is not None and not _TAG_ONLY_LINE.match(line):
            buf.append(line)
    if clip:
        yield clip, "\n".join(buf).strip()


def _split_still_prompts(md_text: str) -> dict[str, str]:
    """{clip_id: full `## SCnn …` chunk} — the header is kept so
    validate_still_covers_requirements can bind the still to its clip."""
    out: dict[str, str] = {}
    for chunk in re.split(r"(?m)^(?=##\s*SC\d{2,3}\b)", md_text):
        m = re.match(r"^##\s*(SC\d{2,3})\b", chunk.strip(), re.IGNORECASE)
        if m:
            out[m.group(1).upper()] = chunk.strip()
    return out


def _first_name(raw: object) -> str:
    return str(raw).split("_")[0].strip()


def _sha256_file(path: _Path) -> str:
    return _hashlib.sha256(path.read_bytes()).hexdigest()


# S-rule families keyed by the input each needs. Used to report, per clip, which
# rules were actually checkable given the inputs on disk.
_S_RULES_NEED_FRAME0 = frozenset({"LTXV-S001", "LTXV-S002", "LTXV-S003", "LTXV-S004"})
_S_RULES_NEED_FRAME0_AND_STILL = frozenset({"LTXV-S005", "LTXV-S006"})


def review_episode(
    channel_slug: str,
    episode_id: str,
    *,
    root: _Path | None = None,
    emit_review: bool = False,
    strict: bool = False,
) -> int:
    """Validate an episode's clip prompts.

    Two modes:
      * **draft** (default) — run every check the inputs on disk allow, and report
        per clip which rules could NOT be checked (no blocking.json, no
        frame0-requirements block, no still). A draft run can PASS with missing
        inputs; the emitted review is stamped ``mode: "draft"``.
      * **strict** (``--strict``, run by 04f3) — every clip must have a
        blocking.json entry, a frame0-requirements block, and a still prompt.
        Any gap FAILs that clip and the run. The emitted review is stamped
        ``mode: "strict"`` and only a strict review may clear the 04f3 gate.

    Return 0 if clean, 1 on any error (rule violation or, in strict mode, an
    input gap), 2 on a setup problem (missing profile / prompts file).
    """
    root = root or _REPO_ROOT
    ep = root / "episodes" / channel_slug / episode_id
    chan_path = root / "channel_profiles" / channel_slug / "channel.json"
    if not chan_path.exists():
        print(f"no channel profile: {chan_path}")
        return 2
    channel = _json.loads(chan_path.read_text(encoding="utf-8"))
    render = channel.get("render", {}) or {}

    prompts_md = ep / "prompts" / "7-video-prompts.md"
    if not prompts_md.exists():
        print(f"not found: {prompts_md}\nRun 04f (draft), then 04f3 (final), first.")
        return 2
    clip_prompts = dict(_iter_clip_blocks(prompts_md.read_text(encoding="utf-8")))
    if not clip_prompts:
        print(f"no '## SCnn' clip blocks in {prompts_md}")
        return 2

    blocking: dict[str, dict] = {}
    bpath = ep / "_context" / "blocking.json"
    if bpath.exists():
        raw = _json.loads(bpath.read_text(encoding="utf-8")).get("clips", {})
        if isinstance(raw, dict):
            blocking = {str(k).upper(): v for k, v in raw.items()}

    frame0: dict[str, dict] = {}
    fpath = ep / "_context" / "frame0-requirements.json"
    if fpath.exists():
        for blk in _json.loads(fpath.read_text(encoding="utf-8")).get("clips", []):
            frame0[str(blk.get("clip", "")).upper()] = blk

    still_prompts: dict[str, str] = {}
    spath = ep / "prompts" / "6-image-prompts.md"
    if spath.exists():
        still_prompts = _split_still_prompts(spath.read_text(encoding="utf-8"))

    voice_sigs: dict[str, str] = {}
    vpath = ep / "_context" / "voice-signatures.json"
    if vpath.exists():
        raw = _json.loads(vpath.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            voice_sigs = {str(k): str(v) for k, v in raw.items()}

    env_locks: dict[str, str] = {}
    epath = ep / "_context" / "environment-locks.json"
    if epath.exists():
        raw = _json.loads(epath.read_text(encoding="utf-8")).get("environments", {})
        if isinstance(raw, dict):
            env_locks = {str(k).upper(): str(v) for k, v in raw.items()}

    still_facts: dict[str, list[dict]] = {}
    sfpath = ep / "_context" / "frame0-still-facts.json"
    if sfpath.exists():
        raw = _json.loads(sfpath.read_text(encoding="utf-8")).get("facts", [])
        if isinstance(raw, list):
            for fact in raw:
                if isinstance(fact, dict) and fact.get("clip"):
                    still_facts.setdefault(str(fact["clip"]).upper(), []).append(fact)

    band = render.get("spoken_word_band")
    band = (band[0], band[1]) if isinstance(band, list) and len(band) == 2 else None
    try:
        max_words = int(render.get("max_prompt_words") or 450)
    except (TypeError, ValueError):
        max_words = 450
    style_echo = str(render.get("style_echo", ""))
    anthro = any("anthropomorphic" in str(x).lower()
                 for x in channel.get("hard_safety_floor", []) or [])

    episode_names: set[str] = set()
    for v in blocking.values():
        for n in (v.get("chars") or {}):
            episode_names.add(_first_name(n))
    for blk in frame0.values():
        for n in (blk.get("frame0_state") or {}):
            episode_names.add(_first_name(n))

    order = sorted(clip_prompts)
    reports: list[dict] = []
    any_error = False

    for clip in order:
        prompt = clip_prompts[clip]
        blk_b = blocking.get(clip, {}) or {}
        chars = blk_b.get("chars") or {}
        visible = [k for k, s in chars.items()
                   if not isinstance(s, dict) or s.get("visible", True)]
        vis_names = sorted({_first_name(n) for n in visible})
        # blocking lists every character with a visible flag; an all-off-screen clip is 0 visible, not a
        # fallback to frame0's cast size (that miscount hid the off-frame-character problem, 2026-10-29)
        vcount = (len(visible) if chars
                  else (len(frame0.get(clip, {}).get("frame0_state", {})) or None))

        review = validate_prompt(
            prompt,
            character_first_names=sorted(episode_names) or vis_names,
            visible_character_count=vcount,
            voice_signatures=voice_sigs or None,
            spoken_word_band=band,
            max_words=max_words,
            anthropomorphic_channel=anthro,
            style_echo=style_echo,
            props=blk_b.get("props") or (),
        )
        rd = review.as_dict()
        errors = list(review.errors)
        warnings = list(review.warnings)

        blk_f = frame0.get(clip)
        still = still_prompts.get(clip)
        # which inputs are missing for this clip
        input_gaps = []
        if clip not in blocking:
            input_gaps.append("blocking.json")
        if blk_f is None:
            input_gaps.append("frame0-requirements")
        if not still:
            input_gaps.append("6-image-prompts.md still")

        # which rules could NOT be checked, for want of an input
        skipped = set(review.skipped)
        if blk_f is None:
            skipped |= _S_RULES_NEED_FRAME0 | _S_RULES_NEED_FRAME0_AND_STILL
        elif not still:
            skipped |= _S_RULES_NEED_FRAME0_AND_STILL
        if not env_locks:
            skipped.add("LTXV-D054")
        if not still_facts:
            skipped.add("LTXV-D055")

        if blk_f is not None:
            errors += validate_frame0_requirements(
                prompt, blk_f, blocking_characters=vis_names)
            if still:
                errors += validate_still_covers_requirements(still, blk_f, clip_id=clip)
                errors += validate_state_transition(still, prompt)
        if env_locks:
            errors += validate_environment_consistency(prompt, still, env_locks)
        if still_facts.get(clip):
            errors += validate_still_grounding_facts(prompt, clip, still_facts[clip])

        strict_fail = bool(strict and input_gaps)
        if errors or strict_fail:
            any_error = True
        reports.append({
            "clip": clip,
            "status": "FAIL" if (errors or strict_fail) else "PASS",
            "display": "FAIL" if (errors or strict_fail)
                       else ("WARN" if warnings else "PASS"),
            "checked_rule_ids": sorted(IMPLEMENTED_RULE_IDS - skipped),
            "skipped_rule_ids": sorted(skipped),
            "input_gaps": input_gaps,
            "errors": errors,
            "warnings": warnings,
            "facts": rd["facts"],
        })

    if frame0:
        seq = [(c, frame0[c]) for c in order if c in frame0]
        for c, msgs in validate_continuity(seq).items():
            for r in reports:
                if r["clip"] == c and msgs:
                    r["errors"] += msgs
                    r["status"] = r["display"] = "FAIL"
                    any_error = True

    mode = "strict" if strict else "draft"
    print(f"LTX prompt review ({mode}) -- {channel_slug} / {episode_id}")
    print(f"  {len(order)} clip(s) · max_words={max_words} · "
          f"band={band or 'none'} · anthropomorphic={anthro}")
    clips_with_gaps = [(r["clip"], r["input_gaps"]) for r in reports if r["input_gaps"]]
    if clips_with_gaps:
        label = "MISSING INPUT (fails strict)" if strict else "missing input (draft: skipped, not failed)"
        for clip, gaps in clips_with_gaps:
            print(f"  {label}: {clip} -- {', '.join(gaps)}")
    print()
    for r in reports:
        f = r["facts"]
        print(f"  {r['clip']}  {r['display']:<4}  "
              f"[{f.get('total_word_count', '?')}w / {f.get('spoken_word_count', '?')} spoken]"
              + (f"  skipped:{len(r['skipped_rule_ids'])}" if r["skipped_rule_ids"] else ""))
        for e in r["errors"]:
            print(f"      ERROR  {e}")
        if strict and r["input_gaps"]:
            print(f"      ERROR  strict mode: no {', no '.join(r['input_gaps'])}")
        for w in r["warnings"]:
            print(f"      warn   {w}")
    print()
    overall = "FAIL" if any_error else "PASS"
    print(f"OVERALL: {overall} ({mode})  "
          f"({sum(1 for r in reports if r['status'] == 'PASS')}/{len(reports)} clips clean)")
    if not strict and clips_with_gaps:
        print("  NOTE: draft run -- rules needing the missing inputs were NOT checked. "
              "04f3 must run --strict.")

    if emit_review:
        # The review is bound to the file it actually read. It used to record a
        # `source_manifest_sha256` that silently fell back to hashing this file
        # when no manifest existed yet (always true at 04f3, which writes the
        # manifest AFTER the review) -- so the recorded hash never matched the
        # manifest it was named after. The manifest binds itself to the prompt
        # blocks by per-clip hash; the review binds to the prompts file here.
        catalog = root / RULE_CATALOG_RELATIVE_PATH
        doc = {
            "schema_version": 2,
            "episode_id": episode_id,
            "mode": mode,
            "reviewed_at_utc": _datetime.now(_timezone.utc)
                .isoformat(timespec="seconds").replace("+00:00", "Z"),
            "source_prompts_sha256": _sha256_file(prompts_md),
            "validator_sha256": _sha256_file(_Path(__file__).resolve()),
            "rule_catalog_sha256": (_sha256_file(catalog) if catalog.exists()
                                    else "0" * 64),
            "status": overall,
            "strict_input_gaps": {
                r["clip"]: r["input_gaps"] for r in reports if r["input_gaps"]
            },
            "clips": [
                {k: r[k] for k in ("clip", "status", "checked_rule_ids",
                                   "skipped_rule_ids", "input_gaps",
                                   "errors", "warnings", "facts")}
                for r in reports
            ],
        }
        out = ep / "_context" / "ltx-prompt-review.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}")

    return 1 if any_error else 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = _argparse.ArgumentParser(
        prog="ltx_prompt_validator.py",
        description="Validate an episode's LTX-2.5 clip prompts. Reads "
                    "prompts/7-video-prompts.md and the _context/ artifacts; "
                    "reports only, never rewrites. Use --strict for 04f3 (requires "
                    "a blocking.json entry, a frame0-requirements block, and a still "
                    "per clip); without it the run is a draft and reports which "
                    "checks it could not run.")
    ap.add_argument("--channel", required=True, help="channel slug")
    ap.add_argument("--episode", required=True, help="episode id, e.g. EP001")
    ap.add_argument("--strict", action="store_true",
                    help="final-validation mode: fail on any clip missing an input (04f3)")
    ap.add_argument("--emit-review", action="store_true",
                    help="also write _context/ltx-prompt-review.json")
    a = ap.parse_args(argv)
    return review_episode(a.channel, a.episode, emit_review=a.emit_review, strict=a.strict)


if __name__ == "__main__":
    raise SystemExit(main())
