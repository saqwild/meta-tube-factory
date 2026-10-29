# 02a — sourcing

Appears in a channel's `pipeline_stages` when that channel's relationship to
real-world fact is load-bearing. **Two channel types use this stage**, and
the branch is chosen by the channel, not by the agent.

| Channel type | The test | Currently |
|---|---|---|
| **Fiction over real mechanism** | Non-depiction — keep the real out of the invented | `signed-anyway` |
| **Factual, with cast** | Traceability — keep the unsourced out of the real, claim-ledger/visualization-ledger shape | `inside-the-process` |

Read the channel's own accuracy or compliance gate in `bible/` before starting;
it defines the verdict this stage must produce.

## Inputs

`story/research-notes.md`, `story/premise.md`, and the channel's gate document
(`bible/SCIENCE_AND_SOURCING.md` for inside-the-process, `bible/COMPLIANCE_GATE.md` for a
fiction channel).

---

## Branch A — fiction over real mechanism (`signed-anyway`)

### Task

Separate **researched mechanism facts** (how this kind of financial/ethical
situation plausibly works) from **invented story elements** (the specific
characters, company, and events of this episode, all fictional). Record every
direct public source URL actually relied on. State explicitly what boundary
keeps the premise from depicting or implying a real person, company, or event
— a disguised retelling of a real case is not acceptable here even if no name
is used.

### Forbidden

No dialogue, no titles, no prompts. Do not carry a real transcript, quote, or
recognizable case sequence into canon.

---

## Branch B — factual, with cast (`inside-the-process`)

### Task

Trace every claim the episode will make to a source. Public web reading is
**required** at this stage, not merely permitted: peer-reviewed literature,
standards bodies, government and university technical publications,
manufacturer process documentation and scientific institutions.

Write both ledgers `SCIENCE_AND_SOURCING.md` specifies in `story/sources.md`:

1. A **claim ledger** — one row per central factual claim: `Claim ID`, the
   exact bounded claim, a direct source URL and location, what it supports,
   limits/variability, and a status of `SUPPORTED`, `QUALIFIED` or
   `UNRESOLVED`. Do not treat a generic homepage as evidence for a detailed
   mechanism; state the actual product/process variant when manufacturers use
   different methods.
2. A **visualization ledger** — one row per planned illustration: `Visual ID`,
   the planned illustration, the factual support/claim IDs it rests on, its
   scale/time/color/cutaway convention, whether it is fiction or metaphor, and
   any audience clarification needed. The Explorer and capsule belong in the
   fictional-device column; a receptor rendered as a docking bay or ions shown
   as colored particles is an explanatory representation, not a claim of
   literal appearance.
3. **Bind the coverage map** (episodes that ran `01b-coverage-scan`): fill each
   item's `claim_ids` in `story/coverage-map.json`. Every in-scope MUST item
   needs at least one `SUPPORTED` or `QUALIFIED` claim; then run
   `python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage 02a-sourcing --emit-review`.
   A MUST item no source can support blocks the stage like any central
   `UNRESOLVED` claim.

### Source rules

Vendor blogs, retailer pages, brand-history pages and content farms are not
acceptable as a sole source. Several such pages agreeing is **not**
corroboration — it usually means one was copied. Wikipedia may be used only as
an index to locate a primary source, which must then be read directly. Do not
infer a figure by arithmetic from two sources that were not measuring the same
thing. Escalate disputed, uncertain or health-actionable claims to a suitably
qualified reviewer per `channel.json` → `science.qualified_review`; record the
actual reviewer scope.

### Forbidden

No dialogue, no titles, no prompts. Do not copy transcripts or imply real
footage, proprietary access, factual verification or expert review that did
not occur. Mark an unresolved claim explicitly rather than inventing support
or softening it until it reads as opinion — any central `UNRESOLVED` claim
blocks script clearance.

---

## Output

`episodes/<slug>/EPxxx/story/sources.md`, closing with the verdict line the
channel's gate specifies (for a factual channel,
`OVERALL VERDICT: **CLEARED**` or `**BLOCKED**`).

## Stop condition

Owner approval required before the next stage may begin.
