# Pre-writer YouTube topic-market brief

Ported from the sibling repo `sibling-repo` on 2026-10-29. In this repo it
runs at **`01b-coverage-scan` for `inside-the-process` only** — before any
research, so what the top videos cover can shape what the episode researches.
(It ran at `03a-writer` until 2026-10-29; episodes created before then still
run it there.) `signed-anyway` and `clover-and-paws` do not run it.

It supplies two things a general scriptwriting skill cannot:

1. a dated, topic-specific view of current audience **packaging** (§1–§3);
2. a **coverage topic list** — which parts of the process the highest-viewed
   videos actually explain (§4), fed into `story/coverage-map.json` as evidence
   of what viewers expect to have answered.

It does **not** supply story structure, factual claims, visual sequences,
dialogue, CTA wording, or a competitor-derived script blueprint. The local
story-writer skill remains the sole author of the episode's original narrative
structure, and `02a`'s claim ledger the sole factual authority.

**Why the coverage list exists.** EP001's benchmark recorded that all three top
videos covered ingredients — one spent ~4 minutes on raw-material batching,
another had a chapter literally called "Ingredients" — and then read that as
something to differentiate *away* from. The episode shipped its script without
raw materials until the owner caught it at the stills. What the top videos
consistently cover is what viewers expect answered.

## Required artifact

Write `episodes/inside-the-process/EPxxx/story/youtube-benchmark.md` and run:

```text
python tools/youtube_benchmark_validator.py episodes/inside-the-process/EPxxx
```

The validator must pass before `01b` completes (`tools/coverage_validator.py`
runs it too).

Do not save third-party transcripts in the repository. Record only original
analysis, short attributed opening excerpts when needed, timestamps, public
URLs, current metadata, and retrieval status. An opening quotation must remain
within normal short-quotation limits; paraphrase the rest.

## 1. Research — live, topic-specific market scan

Use current public YouTube search and metadata. The default tool is the
installed `search-youtube` CLI. Search four to six distinct query variants
drawn from the episode premise, not one exact query repeated.

For every search, record:

- query text;
- research date/time and tool used;
- result count requested;
- relevant candidate title, public URL, channel, duration, current visible
  view count, and upload date when available;
- direct-relevance decision and reason.

Deduplicate by video ID, remove results that only share broad words, then rank
the directly relevant candidates by their current visible view count. The
market-scan set is the **three highest-viewed directly relevant videos with a
retrievable opening-caption sample** in the recorded search snapshot. If a
higher-viewed direct candidate has no usable captions, list it in the
exclusions table with the retrieval attempt and reason, then continue down the
ranked snapshot until three eligible videos are available.

This does not claim the set is the absolute three most-viewed videos on
YouTube. It is the top eligible set in a timestamped, topic-specific search
snapshot.

For §2, use captions only to inspect the **first 60–90 seconds**, plus explicit
chapters or closing metadata if available — do not perform a whole-transcript
story analysis. (§4 may read further, for one narrow purpose only.) Prefer
creator-provided English captions, then English
auto-captions, then the spoken-language transcript when analysis can be
performed reliably. Record the language and retrieval method. If no usable
opening sample is available, the video cannot be one of B01–B03.

## 2. Compact market scan — one record for each benchmark

The file needs one section each for `B01`, `B02`, and `B03`. For each, include
these exact fields:

- `Source video URL`
- `Current view snapshot`
- `Duration`
- `Opening-caption sample status`
- `Opening evidence`
- `Opening behavior`
- `Format signal`

Use only the title, visible metadata, opening-caption sample, and explicit
chapters/descriptive structure to identify:

- **Opening evidence:** a short attributed opening quotation or a faithful
  paraphrase labelled as such, with timestamp. Do not reproduce long
  transcript text.
- **Opening behavior:** how the title/promise is confirmed or delayed during
  the first 60–90 seconds.
- **Format signal:** brief, observable pacing or organization evidence such as
  duration, chapters, a stepwise frame, continuous demonstration, or a visible
  question-to-answer handoff. This is not inferred retention analytics.

Do not extract a full emotional arc, body structure, retention-trick catalog,
or CTA. The generic/local story-writing skill handles those craft decisions.

## 3. Topic-market brief — inform, do not prescribe

Add `## Topic-market brief` with these exact fields:

- `Audience promise to meet`
- `Current format signal`
- `Explained From Within differentiation`

These three fields describe the viewer's likely expectation, a current
observable convention, and the original value this channel will add. They are
inputs to the writer's foundation; they must not prescribe a scene sequence,
wording, emotional arc, CTA, title, or visual treatment.

**Differentiation is how the channel explains, never what it leaves out.** The
inside view, the causal "why", the stricter sourcing — those differentiate. A
topic the benchmarks consistently cover (§4) is a viewer expectation to meet,
not a crowded area to avoid.

## 4. Coverage topic scan — what the top videos actually explain

Add `## Coverage topic scan`. For each of B01–B03, read the video's uploader
chapters and, where available, its **full** captions — for one purpose only:
listing the **topics and process steps it covers** (nouns and steps such as
"raw-material batching", "melting", "blow-and-blow forming", "annealing",
"inspection"). Do not extract its structure, order, wording, hook, arc or claims.

Record in the file, one line per video:

```text
- B01 topic source: <uploader chapters / full English captions / auto-captions>, read <date>
```

Record the topics themselves **only** in `story/coverage-map.json` →
`benchmark_topics`, each with the videos it was `seen_in` and the coverage item
it maps to (`pipeline/process_coverage.md`). A topic seen in two or more
benchmarks must map to a MUST item. No transcript text is stored anywhere.

Record the following under `## Originality and evidence boundaries`:

- the writer **must not copy** title phrasing, opening lines, dialogue,
  structure, footage, graphics, music, thumbnails, CTA, or factual claims;
- the approved source ledger remains the only factual authority;
- the market brief is not a substitute for scientific or industrial evidence.

## Failure and refresh rules

- Fewer than three directly relevant, opening-caption-retrievable videos:
  expand queries and record the gap; do not draft the script until the
  condition is met.
- Opening captions unavailable: record the retrieval attempt and exclusion;
  do not fabricate the analysis.
- Market brief older than 30 days at the time of writing: rerun the search
  snapshot.
- Later title, thumbnail, metadata, or render choices may consider the brief,
  but must remain original and comply with the source/compliance ledgers.
