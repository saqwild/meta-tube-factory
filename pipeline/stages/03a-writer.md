# 03a — writer

## Inputs

`story/premise.md`, `story/research-notes.md` (+ `story/sources.md` /
`story/compliance.md` where the channel has those stages), the channel's cast
registry (`channel_profiles/<slug>/channel.json` → `cast`, plus the read-only
reference bible for full cast bios/voice).

### Channel-specific story-writer authority

For `inside-the-process`, read the owner-approved `story/coverage-map.json` and
the YouTube benchmark (`story/youtube-benchmark.md`), both produced at
`01b-coverage-scan`. If the benchmark is more than 30 days old, re-run its
search snapshot first (`pipeline/youtube_benchmark.md`). The brief informs the
writer's audience promise, current format signal and differentiation only; it
does not prescribe the episode's story structure or dialogue. The coverage map
is binding: **every in-scope MUST item gets at least one beat-table row that
explains it** (record the row numbers in its `script_rows`), and every
out-of-scope MUST item's `disclosure` is spoken on screen verbatim. Before
handoff:

```text
python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage 03a-writer --emit-review
```

That check includes `tools/clip_split_check.py`. Each beat-table row's
dialogue must divide into the row's clips (the `Duration` cell's "(N clips)")
at clean pauses, with every clip inside `channel.json`
`render.spoken_word_band`. Each clip's audio is a separate delivery, so a
boundary mid-phrase is heard as a broken line. Run it on its own while
drafting: `python tools/clip_split_check.py --channel inside-the-process --episode EPxxx`.

Episodes created before 2026-10-29 (no `01b` in their sequence) instead
create and pass the benchmark here, as before:
`python tools/youtube_benchmark_validator.py episodes/inside-the-process/EPxxx`.
No other channel in this repo runs either gate.

`local_skills/explained-from-within-story-writer/SKILL.md` is the sole story
writer at this stage for `inside-the-process`. It uses the locally copied
`local_skills/youtube-scriptwriting/` skill as its general craft library, then
applies the channel's factual-process, native-audio, runtime and originality
rules. It does not replace the mode-specific LTX production writer at `04f`.

## Task

Select the episode's cast (snapshot names/IDs from the registry; a channel
that forbids one performer in two roles per episode must be respected), then
write the full script/story package: scene-by-scene beats, dialogue, and a
runtime estimate against the channel's `format` numbers in `channel.json`.

For `inside-the-process`, follow the local story writer's required foundation,
causal-outline, script-table and self-audit workflow before handoff to 03b.

## Output

`episodes/<slug>/EPxxx/story/characters.md` (cast snapshot),
`episodes/<slug>/EPxxx/story/script.md` (full script with runtime estimate).
For `inside-the-process`, also `story/coverage-map.json` with every item's
`script_rows` filled and a fresh `story/coverage-review.json` for this stage
(or, for a pre-2026-10-29 episode, `story/youtube-benchmark.md`).

## Factual-process and post-audio requirements

For profiles declaring `science.evidence_mode: factual_process` (currently
`inside-the-process`), also read the local `EPISODE_SPEC.md` and
`SCIENCE_AND_SOURCING.md`. Bind each explanatory beat to approved claim/
visualization IDs. Keep narration, radio lines, generated ambience and
visible action in separate script columns. Where `audio.native_generated_dialogue`
is false, speech is authored for post production and must not be passed as
native LTX-2.5 dialogue. Audio-only cast members have no generated physical
appearance.

### `inside-the-process` — story engine (`bible/STORY_ENGINE.md`)

- First confirm or revise `story/story-definition.md` against the cleared `02a` claims. Any fact the sources do not support leaves the sheet.
- Write to the arc in §3, as shares of runtime on this episode's clip grid: hook in the first ~7%; struggle through ~25-40%; climax at
  ~43-50% with the master metaphor paid off inside it; objection at ~53-58%; practical at ~70-85% (explanation, never instruction);
  caveats; a callback plus a clock-tied comment question at the end.
- Narration: Control speaks to "you" throughout. About 20-25% of clips are outside ones showing the recurring "you" figure; the rest are inside.
- Each clip's visible action names a visible change about every 5 s (§6). A declared cut is allowed only as `STORY_ENGINE.md` §7 and
  `LTX_I2V_CONTRACT.md` §4 describe.
- The Explorer's lines are a helmet-radio voice-over, only in rows where the Explorer is visible (`VISUAL_STYLE_CONTRACT.md` voice rule).

## Forbidden

Do not perform `03b-script-review` yourself — a different actor (different
agent session or a human) must grade it. Do not invent a cast member outside
the registry without flagging it as episode-local per the channel's rule.
For `inside-the-process`, do not copy or closely paraphrase a benchmark's
title, opening, dialogue, structure, visual sequence, thumbnail or CTA. The
episode's approved source ledger remains the only authority for factual
process claims.
