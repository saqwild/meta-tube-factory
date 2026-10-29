# 01b — coverage scan (`inside-the-process` only)

Decide, before any research, **what a complete explanation of this episode's process must
answer** — and have the owner approve it. The authority for this stage is
`pipeline/process_coverage.md`; read it first.

This stage exists because inside-the-process EP001 reached its frame-0 stills before anyone
noticed it never showed what glass is made of. Every stage had done its own job; none owned
completeness. This one does.

## Inputs

`story/premise.md` (its **full process chain** and **declared scope** — see `01-ideation`),
`channel_profiles/inside-the-process/channel.json`, `pipeline/process_coverage.md`,
`pipeline/youtube_benchmark.md`. Public web and YouTube reading is allowed at this stage.

## Task

1. **Classify the process** into one archetype (`manufactured_product`, `biological_process`,
   `natural_phenomenon`, `system_infrastructure`, or `other` with declared custom dimensions).
2. **Write the process chain first, then the scope.** List every state from the *true*
   raw/original starting substance to the finished result in use; only then choose where the
   episode starts and ends. A chain that begins at an already-transformed state ("molten
   glass") is the failure this stage exists to catch.
3. **Run the YouTube market and coverage scan** (`pipeline/youtube_benchmark.md`, including
   §4 *Coverage topic scan*) and record every topic the three benchmark videos cover.
4. **Write five or more naive-viewer questions** — what a curious 14-year-old would ask — before
   looking at your own item list, so they are an independent check on it.
5. **Build `story/coverage-map.json`**: one item per concrete question, each with a dimension,
   `MUST`/`OPTIONAL` priority and `in`/`out` scope. Every required dimension gets a MUST item;
   every benchmark topic and naive-viewer question maps to an item; a topic covered by two or
   more benchmarks maps to a MUST item. An out-of-scope MUST item gets a `reason` and the exact
   on-screen `disclosure`.
6. **Validate and emit the review and the scope lock:**
   ```bash
   python tools/youtube_benchmark_validator.py episodes/inside-the-process/EPxxx
   python tools/coverage_validator.py --channel inside-the-process --episode EPxxx \
       --stage 01b-coverage-scan --emit-review
   ```

## Output

- `story/youtube-benchmark.md` — the market brief and coverage topic scan (validated).
- `story/coverage-map.json` — schema `pipeline/schemas/coverage-map.schema.json`.
- `story/coverage-review.json` — the validator's verdict, bound to the hashes it read.
- `story/coverage-scope.lock.json` — the scope the owner approves. Later stages may add items
  but may not remove, demote or scope-out a locked one without reopening `01b`.

## Forbidden

No research notes, claims, dialogue or visual work. Do not let a benchmark video decide a fact —
it is evidence of what viewers **expect answered**, never of what is **true**. Do not treat
leaving an essential topic out as "differentiation": the channel differentiates on how it
explains, never on what it leaves out. Do not store third-party transcripts.

## Stop condition

**Owner gate.** The owner reads the process chain, the scope boundary and the MUST list and
approves them with `preflight.py complete ... --approve`. The completion gate refuses unless
`story/coverage-review.json` is a PASS for this stage and nothing it read has changed since.
