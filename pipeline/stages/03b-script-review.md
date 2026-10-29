# 03b — script review

**Never run by whatever performed `03a-writer`.** Author and grader must be
different sessions/actors — this is a universal rule, not channel-specific.

## Inputs

`story/script.md`, `story/characters.md`, `channel_profiles/<slug>/channel.json`
→ `format`/`script` numbers.

For `inside-the-process`, also read the topic-market brief in
`story/youtube-benchmark.md` and verify the script's writer self-audit against
`local_skills/explained-from-within-story-writer/SKILL.md`. Read
`story/coverage-map.json` only **after** the blind naive-viewer test below.

## Task

Independent craft verdict: does the script hit runtime, does every scene earn
its place, does dialogue avoid the channel's forbidden moves (e.g.
signed-anyway: no omniscient narrator, no legal/financial-advice tutorial,
two-defensible-verdicts requirement; clover-and-paws: no plotless compilation,
Clover never on screen without a parent, Bruno's first answer is always No with
attitude before any reluctant yes, and the hard-safety-floor checks — no real
people/brands, no peril, every background character explicitly anthropomorphic).

For `inside-the-process` (a factual-process profile), also read
`story/sources.md`, `story/compliance.md` and the channel's QA/science bible.
Review claim support, visual simplifications, expert-review status,
narration/action agreement, and the distinction between initial repair and
completed healing where relevant. Do not require financial verdicts, multiple
physical speakers or animal-family rules from another channel. A factual
failure yields `REVISE`. Also reject a draft that copies benchmark packaging,
wording or structure closely, turns the generic craft guide into unsupported
factual claims, omits the required causal/audience/payoff self-audit, sends
LTX prompt prose to this story stage, or reuses the sibling LTX profile's
already-produced episode as source material.

**Completeness — two independent checks (`inside-the-process`):**

1. **Blind naive-viewer test, done FIRST.** Before opening `script.md` or
   `coverage-map.json`, read only the premise's viewer question and write down
   at least five questions a curious 14-year-old would ask about this topic
   ("what is it made of?", "why doesn't it crack?"). Record them in
   `script-review.md` exactly as written, *then* read the script and mark each
   answered (with the beat-table row) or unanswered. Writing the questions
   after reading the script lets the script decide what seems important — the
   same reason the still gate never shows the claim first. An unanswered
   question that a general viewer needs is a `REVISE`, unless the coverage map
   already declares it out of scope with an on-screen disclosure.
2. **Mechanical coverage re-check** (episodes that ran `01b-coverage-scan`):
   ```bash
   python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage 03b-script-review --emit-review
   ```
   A FAIL is a `REVISE`. The completion gate also refuses `03b` unless this
   review is a fresh PASS.

**Story-engine checks (`inside-the-process`, from the next LTX episode, `bible/STORY_ENGINE.md`):** also check that
the arc lands at its targets (§3), narration stays second person, the master metaphor is set up early and paid off with the Explorer
inside it, the objection comes before the practical section, the practical section is explanation and not instruction (§11), the
outside share is about 20-25%, the Explorer's lines are helmet-radio voice-over only in rows where the Explorer is visible, and every
metaphor appears in the visualization ledger. Follow-up rounds after a `REVISE` stay verification-only, as above.

EP001 passed an independent review without ever showing what glass is made
of; the reviewer was only asked whether the script was well made, not whether
it was complete. These two checks are that question.

## Follow-up rounds (after a `REVISE`)

A round that follows a `REVISE` is **verification-only**. The reviewer checks that
each required and accepted advisory fix was applied as described, stays inside its
cited claim's Limits, and introduces no new factual or clip-boundary defect in the
edited text. The reviewer also re-runs the mechanical checks (the coverage
validator, which includes `tools/clip_split_check.py`). The reviewer does not
re-read the whole script or re-run the blind test, and does not look for new
advisories elsewhere. Anything noticed in passing is listed as non-blocking and
does not change the verdict.

A **full** review (everything above) is needed again only when the revision
changes the script substantially: a row added, removed or reordered, a claim
added or re-scoped, or a coverage item moved. Reason: inside-the-process EP001
ran 15 rounds. Once Round 13 had approved the substance, each whole-script
re-read still surfaced a fresh advisory and prompted another round, while the
claims themselves no longer changed.

## Output

`episodes/<slug>/EPxxx/story/script-review.md` — `PASS` or `REVISE` with
specifics. A `REVISE` returns the episode to `03a-writer`.

## Stop condition

**Owner gate.** Script is locked before any visual/render work begins.
