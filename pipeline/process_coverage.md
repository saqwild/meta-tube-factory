# Process coverage — what a complete explanation must answer

**Channel:** `inside-the-process` (Explained From Within) only. Added 2026-10-29.

## Why this exists

EP001 ("how molten glass becomes a bottle") cleared premise, research, sourcing, compliance,
script and an independent script review, then reached the frame-0 stills — and only there did
the owner notice the episode never showed what glass is made of. Nothing upstream was wrong on
its own terms. Every stage faithfully processed what the previous one handed it:

1. **The premise narrowed the question.** It asked "how does *molten glass* become this shape" —
   a question that starts after melting. Research then covered forming, the claim ledger
   followed the research, and the script followed the ledger.
2. **The YouTube benchmark saw the gap and steered away from it.** All three top videos covered
   ingredients (the highest-viewed spent ~4 minutes on raw-material batching; another had an
   uploader chapter literally called "Ingredients"). The brief read that as something to
   *differentiate from*.
3. **The writer's beat filter dropped it.** Beats had to be "both causally necessary **and**
   likely to change understanding" — "it starts as sand" is necessary but unsurprising, so it
   failed the *and*.

No stage owned the question **"what must a complete explanation of this topic contain?"** This
file is that owner. The answer is written down once, at `01b`, as `story/coverage-map.json`,
approved by the owner, and every later stage is checked against it by
`tools/coverage_validator.py`.

## The rule

> Every **MUST** item is either explained on screen, backed by an approved claim, or declared
> **out of scope** with a reason and an on-screen disclosure. Nothing essential is silently
> skipped. Interest ranking decides how much time an item gets — never whether it appears.

A 10-minute episode cannot give every item equal depth, and it does not need to: an essential,
unsurprising item (the raw materials) may get one clip while the surprising one gets four.

## Topic archetypes and required dimensions

Pick the one archetype that fits the episode's process (`archetype` in the map). Every
**required dimension** of that archetype needs at least one **MUST** item. The guiding question
is what a curious general viewer would ask; write items as concrete questions for *this* topic.

### `manufactured_product` — bottle, battery, chocolate, pencil, tyre

| Dimension | Guiding question | Glass bottle | Lithium-ion battery |
|---|---|---|---|
| `composition` | What is the finished thing made of — and if it has parts, what does each part do? | soda-lime glass: a silica network with soda and lime | cathode, anode, electrolyte, separator, current collectors, casing — and the job of each |
| `raw_materials` | What raw substances does it start from, and where do they come from? | silica sand, soda ash, limestone, recycled cullet | lithium/nickel/cobalt compounds, graphite, aluminium and copper foil, solvent |
| `preparation` | How are those raw materials prepared or combined before the main transformation? | weighing, batching, melting, fining | slurry mixing, electrode coating, drying, calendering |
| `transformation` | What are the main steps that turn it into its final form (state A → state B)? | gob → parison → blow mold → bottle | electrode stacking/winding, electrolyte fill, sealing, formation charging |
| `conditions` | What conditions make each step work — temperature, pressure, time, force — and why? | ~1,500 °C melt, working viscosity, compressed air | dry room, formation voltage/current, ageing time |
| `quality_control` | How is it finished and checked, and what defects are caught? | annealing lehr, inspection for cracks/stones | capacity grading, leak and short testing |
| `product_in_use` | How does the finished thing work or get used — connecting back to the familiar object? | holds a drink; why it doesn't shatter | ions shuttle anode ↔ cathode as it charges and discharges |

### `biological_process` — blood clotting, digestion, a vaccine response

| Dimension | Guiding question |
|---|---|
| `anatomy` | Which structures are involved — organs, tissues, cells, molecules — and what does each do? |
| `trigger` | What starts the process? |
| `sequence` | What happens, in order? |
| `agents_and_signals` | Which cells and molecules do the work, and how are they coordinated? |
| `regulation` | What keeps it in check, and what stops it? |
| `outcome` | What state is actually reached — and what it is *not* yet (initial plug ≠ healed wound)? |
| `misconception` | Which common belief does the episode correct? |

### `natural_phenomenon` — lightning, rain, a volcanic eruption

| Dimension | Guiding question |
|---|---|
| `ingredients` | Which materials and conditions must be present? |
| `energy_source` | Where does the energy come from? |
| `sequence` | What happens, in order? |
| `outcome` | What is the result? |
| `scale_and_frequency` | How big, how often, where? |
| `misconception` | Which common belief does the episode correct? |

### `system_infrastructure` — tap water, electricity to a socket, a parcel's journey

| Dimension | Guiding question |
|---|---|
| `source` | Where does it start? |
| `stages` | What treatment or transformation stages does it pass through? |
| `distribution` | How does it travel? |
| `endpoint` | How does it reach and serve the user? |
| `controls` | What monitoring, safety and failsafes keep it working? |

### `other`

Only when none of the above fits. Declare at least four `custom_dimensions` (each an `id` and a
guiding `question`); each then needs a MUST item exactly like a built-in dimension.

## Priority, scope and disclosure

- **MUST** — a curious general viewer would feel the explanation is incomplete without it.
  **OPTIONAL** — enrichment; include it if time allows.
- **scope `in`** — the episode explains it. **scope `out`** — genuinely beyond this episode (too
  far upstream, its own multi-step process). An out-of-scope MUST item needs a `reason` and a
  `disclosure`: the exact words the episode says on screen so the viewer knows the gap is
  deliberate. The disclosure must appear verbatim in `story/script.md`.
- Narrowing scope **after** the owner approves `01b` — removing a MUST item, demoting it to
  OPTIONAL, or moving it out of scope — fails the validator until `01b` is reopened and
  re-approved. Adding items is always allowed.

## Where the items come from — three independent sources

1. **The archetype** (above) — first principles for this kind of process.
2. **The YouTube coverage scan** at `01b` (`pipeline/youtube_benchmark.md` §4) — which topics
   the highest-viewed videos on this topic actually cover. A topic covered by **two or more**
   benchmark videos is something viewers expect answered: it must map to a MUST item (in or out
   of scope). Competitor videos are a **coverage checklist, never a factual source** — facts
   still come only from `02a`'s claim ledger.
3. **Naive-viewer questions** — at least five questions a curious 14-year-old would ask about
   this topic, each mapped to an item.

## `story/coverage-map.json`

Schema: `pipeline/schemas/coverage-map.schema.json`. Created at `01b`; later stages fill in
their own fields and never delete what an earlier stage approved.

```json
{
  "schema_version": 1,
  "episode_id": "EP002",
  "topic": "how a glass bottle is made",
  "archetype": "manufactured_product",
  "process_chain": ["quarried sand, soda ash, limestone, cullet", "batch", "melt", "gob",
                    "parison", "blown bottle", "annealed bottle", "inspected bottle", "bottle in use"],
  "scope": {"starts_at": "raw materials arriving at the plant", "ends_at": "an inspected bottle ready to fill"},
  "items": [
    {"id": "COV01", "dimension": "composition", "priority": "MUST", "scope": "in",
     "question": "What is bottle glass actually made of?",
     "claim_ids": ["CLM-12"], "script_rows": ["3"]},
    {"id": "COV02", "dimension": "raw_materials", "priority": "MUST", "scope": "out",
     "question": "Where does the sand come from?",
     "reason": "Quarrying is its own process and a separate episode.",
     "disclosure": "the sand itself was mined long before it reached this plant"}
  ],
  "benchmark_topics": [
    {"topic": "raw-material batching", "seen_in": ["B01", "B02", "B03"], "item": "COV01"}
  ],
  "naive_viewer_questions": [
    {"question": "What is glass made of?", "item": "COV01"}
  ]
}
```

| Field | Written at | Meaning |
|---|---|---|
| `archetype`, `process_chain`, `scope`, `items[].id/dimension/priority/scope/question/reason/disclosure` | `01b` | what the episode must answer — **owner-approved** |
| `benchmark_topics`, `naive_viewer_questions` | `01b` | the evidence for the item list |
| `items[].claim_ids` | `02a` | approved `CLM-nn` rows in `story/sources.md` that support the item |
| `items[].script_rows` | `03a` | `#` values of the rows in `story/script.md`'s beat table that explain it |

## What each stage must satisfy

Run after each stage's work, before `preflight.py complete`:

```bash
python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage <stage_id> --emit-review
```

The review (`story/coverage-review.json`) is what that stage's completion gate reads; it is
bound to the hashes of the files it read, so any later edit makes it stale. Checks are
cumulative:

| Stage | Adds these checks |
|---|---|
| `01b-coverage-scan` | valid map; every required dimension has a MUST item; ≥3-step process chain; ≥5 naive-viewer questions, each mapped; every benchmark topic mapped, and every topic seen in ≥2 benchmarks mapped to a MUST item; B01–B03 each contributed topics; out-of-scope MUST items carry a reason and a disclosure; the YouTube benchmark itself validates. Writes `story/coverage-scope.lock.json`. |
| `02-research` | every in-scope MUST item's id (`COV01`…) is cited in `story/research-notes.md` |
| `02a-sourcing` | every in-scope MUST item has `claim_ids`, and each is a `SUPPORTED` or `QUALIFIED` row of `story/sources.md`'s claim ledger |
| `03a-writer` (and `03b` re-check) | every in-scope MUST item names `script_rows` that exist in the beat table and carry at least one of its claim IDs; every out-of-scope disclosure appears in `story/script.md` |

At every stage after `01b`, the map is also compared with the scope lock — see *Priority, scope
and disclosure*.
