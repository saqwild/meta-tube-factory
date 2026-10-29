# YouTube Packaging and SEO Contract

> **Canonical visual rules:** `VISUAL_STYLE_CONTRACT.md` controls the image style. This document controls discovery language, title-description derivation, thumbnail promise and metadata validation. Shared brand-level SEO doctrine, ported from the sibling `sibling-repo` profile 2026-10-29 — nothing below is render-engine-specific. Section 11 of the source document (a worked derivation of the LTX profile's already-shipped EP001) was dropped here, since this profile's own first episode has not been chosen yet; sections renumbered accordingly.

## 1. Locked channel classification

| Field | Decision |
|---|---|
| Channel | **Explained From Within** (`@explainedfromwithin`; claimed 2026-10-29) |
| Category | **Education** |
| Format | Long-form factual process explanation with a fictional miniature Explorer |
| Audience | General-audience curious teens and adults; not child-directed |
| Runtime | Approximately 9–11 minutes; current target 10 minutes |
| Discovery model | Search-supported educational browse: an established mechanism phrase plus a familiar event/object and the recurring inside viewpoint |
| Channel promise | How things work—and how they are made—seen from the inside |

The Explorer and capsule are fictional storytelling devices. The physical process is a sourced explanation. Never package an episode as literal microscopic footage, hidden-camera factory footage, a medical diagnosis, a treatment tutorial or a comprehensive mechanism when the episode only covers a bounded part.

## 2. Discovery strategy

Package the **familiar trigger or object** and the **hidden causal mechanism**. The channel name, Explorer and internal series labels support recognition but do not replace the viewer’s query.

### Keyword families

| Pillar | Primary phrase families | Supporting language |
|---|---|---|
| Inside Your Body | `[mechanism] explained`, `how [body process] works`, `what happens when [ordinary body event]` | platelet plug formation, blood clotting process, how breathing works, digestion explained, immune response, wound healing stages |
| Inside Materials | `how [material] forms`, `why [material] changes`, `[material process] explained` | how concrete sets, glass tempering process, rust formation, crystal growth, material science |
| Inside Manufacturing | `how [object] is made`, `[object] manufacturing process`, `how [input] becomes [output]` | glass bottle manufacturing, aluminum can making, paper recycling process, ceramic firing, injection molding |
| Inside Technology | `how [device/process] works`, `what happens inside [device]`, `[technology] explained` | how batteries charge, lithium-ion battery explained, data storage, camera sensor, electric motor |
| Format/brand | `how things work`, `scientific visualization`, `3D process animation` | inside view, process visualization, mechanism explained, Explained From Within |

Use exactly one primary phrase per episode. Add two to four supporting phrases only when they describe content actually present in the approved script and visuals.

### Finalized-video keyword deliverable

Every finalized video must include a distinct, ready-to-use set of **10–15
video-specific keyword phrases**. This is a required deliverable, not an
optional research note or a copy of the channel keyword bank.

The set must include:

1. the exact primary phrase;
2. one or two natural viewer-language variants;
3. familiar trigger/object queries;
4. mechanism-specific queries supported by the final script and visuals; and
5. only the minimum relevant pillar, format and channel anchors needed to
   complete the YouTube Tags field.

Save the set under `## Video-specific keywords — ready to use` in the episode
`metadata/package.md`. Mirror the same ordered set into the final upload sheet
and machine-readable upload JSON. Do not paste it as a keyword dump into the
public description; the title and description must use important phrases
naturally under §§4–5.

## 3. Keyword evidence and data integrity

YouTube ordinary search does not expose reliable public monthly query volume. Never convert result counts, views or autocomplete into monthly search volume. Record monthly volume only from a named provider such as YouTube Studio Research, Google Trends set to YouTube Search, or an approved keyword platform; include geography, date range and source.

### Required episode research

Before a final title is approved:

1. Generate four to six plain-language queries for the episode mechanism, familiar trigger and likely viewer question.
2. Sample at least ten YouTube results per query.
3. Record capture date, query, sample size, relevant-result count, intent, repeated title language, obvious mismatch clusters and representative URLs.
4. Separate search intent. A medically actionable query, product-support query or children’s query is not interchangeable with a general explanation query.
5. Record upload dates only when the source returns them. Missing dates are `unavailable`, never zero or recent.
6. Choose the primary phrase by factual fit and viewer intent. Views support context but do not prove keyword demand.
7. Save the decision under `episodes/<slug>/EPxxx/metadata/keyword-research.md`.

For broad or competitive topics, run an evergreen pass without an age filter and an active-competition pass covering the last 12 months. If valid dates are unavailable for at least 90% of the sample, record the active pass as unavailable and make no freshness claim.

## 4. Keyword-to-title contract

### Preferred formulas

- **How [primary mechanism] Works Inside [familiar object/event]**
- **How [mechanism entity] [does the action] Inside [familiar object/event]**
- **What Happens Inside [object/body] When [familiar trigger]?**
- **How [input] Becomes [output]—From the Inside**
- **[Primary mechanism]: Inside [familiar object/event]**

### Rules

1. Derive every title from the episode’s recorded primary phrase; name the phrase and formula in the metadata package.
2. Put the exact phrase or a natural grammatical variant within the first 40 characters where practical.
3. Pair the mechanism with a concrete familiar object/event. Do not title an episode only with the series or channel name.
4. Keep titles at 70 characters or fewer.
5. Match the episode’s true scope. Do not promise full wound healing, the complete coagulation cascade, a full factory line or an entire device architecture when those are not shown.
6. A number, duration, percentage or superlative must be sourced and visible in the episode.
7. Do not lead with `AI generated`, episode numbers, the channel name or the Explorer.
8. Ban false-access language such as `actual footage`, `secret footage`, `caught on camera` and `microscope footage` for synthetic scenes.
9. Avoid alarmist health framing, emergency advice, miracle language and unsupported certainty.
10. A browse variant may emphasize curiosity, but it must retain the primary mechanism or an unambiguous natural variant.
11. From the next LTX episode, **timeline test variants** (`STORY_ENGINE.md` §2), such as "What Happens To Your Body When You… (Hour by Hour)", are allowed as the launch title or an A/B variant **only** when they satisfy rules 1–10. They must carry the primary phrase or a natural variant within 40 characters, and the video must actually run on that clock. Do not promise "hour by hour" for a video that jumps from minutes to weeks.

## 5. Keyword-to-description contract

The first two visible lines must contain the primary phrase naturally and state the episode payoff. The source and visualization disclosures are part of the value proposition, not generic footer text.

```text
[Sentence 1: exact primary phrase + causal scope shown in the episode.]
[Sentence 2: familiar trigger/object + inside-view payoff + key boundary or distinction.]

CHAPTERS
0:00 [Familiar trigger]
[timestamps derived from the final edit]

[One short paragraph explaining the mechanism with two to four approved supporting phrases used naturally.]

[Exact synthetic-visualization disclosure from channel.json]

VISUALIZATION CONVENTIONS
[Episode-specific scale, timing, color, cutaway and fictional-guide conventions.]

SOURCES
[Direct public URLs used by the final script.]

[Educational/medical boundary when relevant.]

[One-sentence channel promise.]

[Required channel hashtags] [one or two episode-specific hashtags]
```

### Description rules

- Use the exact primary phrase in the first 25 words.
- Use each supporting phrase only when natural; do not stack synonyms for density.
- Explain the bounded process before discussing production methods.
- Include direct source URLs for factual-process episodes.
- State relevant simplifications: magnification, time compression, false color, conceptual cutaway, visibility enhancement and fictional guide.
- Do not describe all science as fictional merely because the guide is fictional.
- Do not imply access to a real patient, factory, microscope or proprietary device.
- Put chapters before the long source list so navigation remains visible.
- Keep the full description below 5,000 characters and validate the actual copy block, not the surrounding package.

## 6. Chapters, cards and end screens

- Chapters start at `0:00`, contain at least three entries and remain at least ten seconds apart.
- Labels use familiar questions and mechanism stages; avoid unsupported claims.
- Derive timestamps from the assembled master, not only the script, after editorial transitions are final.
- Do not add irrelevant cards merely to fill recommended positions.
- For a launch channel, omit cards until a relevant published video or playlist exists; add them retroactively.
- Reserve the final 5–20 seconds for a subscribe element and, when available, one related video or playlist.

## 7. Tags and hashtags

Tags are secondary metadata. Use 10–15 relevant tags and stay below 500 characters.

### Channel-level tag bank

`how things work, how things are made, scientific visualization, 3D process animation, process explained, inside the human body, material science explained, manufacturing process, how technology works, engineering animation, inside view, hidden processes, Explained From Within`

### Episode tag stack

The episode tag stack is the YouTube Tags-field implementation of the required
video-specific keyword set. It must be ready to copy without additional
research or cleanup.

1. exact primary phrase;
2. one or two natural grammatical variants;
3. two to four approved supporting phrases;
4. familiar object/event phrase;
5. pillar phrase;
6. format phrase;
7. `Explained From Within`.

Use three to five hashtags. `#ExplainedFromWithin` and `#HowThingsWork` are required. Add one or two episode-specific hashtags; never exceed 15.

## 8. Title-thumbnail split

The title carries the **mechanism and familiar trigger**. The primary thumbnail carries the episode's **visible causal journey**.

### Default primary — four-panel causal ladder

Every new primary thumbnail uses a left-to-right four-panel layout unless an episode-specific exception is documented and owner-approved:

| Panel | Job | Rule |
|---|---|---|
| 1. Text promise | State the transformation in viewer language | Use a short phrase such as `FROM SAND TO BOTTLE`; it clarifies the visual story and must not merely repeat the entire title. |
| 2. Input / trigger | Show where the process starts | Use an actual episode state: material input, body trigger, charge source, or familiar before-state. |
| 3. In-process state | Show the decisive mechanism or material change | Use the most legible accepted process frame; this is the evidence panel, not generic spectacle. |
| 4. Visible outcome | Show the resulting object, state, or payoff | Use the actual explained result, never an unsupported or universal end state. |

The primary phrase must normally use six or fewer content words. A context line of up to three words and the fixed three-word `EXPLAINED FROM WITHIN` footer are allowed when each remains readable at phone size. Add type in the compositor; do not rely on a text-to-image model for spelling.

Use accepted episode frames or approved stills for all three evidence panels. A title that promises `from X to Y` must show both states and an authentic in-process bridge. Do not use a single outcome image with a transformation claim.

The alternate thumbnail remains materially different, usually a single decisive interaction or a no-text mechanism close-up. It is an upload-testing fallback, not a reason to weaken the four-panel primary.

| Element | Rule |
|---|---|
| Explorer | Optional scale cue; always secondary to the process states |
| Medical imagery | Non-graphic; no fear, pain or emergency framing |
| Accuracy | Every panel must appear in the accepted episode and fit the documented scope |
| Output | 16:9; master at least 1280×720 and below YouTube's upload limit |
| Tests | Critical content inside the safe area; legible at 10% scale and on a phone |

An exception is allowed only when the topic has no honest input → process → outcome progression. Record the reason, proposed alternate hierarchy, and owner decision in `metadata/package.md` before upload.
### Required production-ready thumbnail brief

Every finalized video's `metadata/package.md` must contain enough information
to generate the thumbnail without another creative-planning pass:

1. **Production mode:** image generation, existing-scene composite, or hybrid.
2. **Reference manifest:** the role and stable project path for every required
   image. If no reference is required, state `None`. Never depend on a temp,
   clipboard or Downloads path. Extract any required video frame into
   `metadata/thumbnail-references/` first.
3. **Full visual prompt:** a copy-ready prompt defining subject, action,
   composition, camera/viewpoint, lighting, palette, hierarchy, mood and
   factual boundaries.
4. **Exact typography specification:** exact visible text, capitalization,
   font family and weight, pixel size at the declared master resolution, hex
   colors, stroke, shadow, line spacing, alignment, bounding box and position.
   State `No text` when appropriate.
5. **Layout coordinates:** master dimensions, panel proportions, subject focal
   zones, divider coordinates and central-safe-area requirements.
6. **Negative instructions:** forbidden imagery, extra text, logos, gore,
   misleading final states, unsupported scale and literal-footage cues.
7. **Output contract:** aspect ratio, pixel dimensions, color space, file type,
   quality/size limit and mobile-size validation.
8. **Alternate concept:** a second complete prompt and typography specification,
   not merely a one-line idea.

The copy-ready prompt must mention the exact text specification even when the
recommended production method generates the clean image first. For reliable
spelling and brand consistency, add text deterministically in the compositor
after image generation whenever possible.

Create the four-panel causal-ladder primary and one materially different alternate before upload. Test the full package—title and thumbnail together—because a high click-through rate with weak retention signals a mismatched promise.

## 9. Episode workflow

1. Start with a familiar trigger/object and one hidden causal process.
2. Assign one pillar and write four to six viewer queries.
3. Run the required live YouTube sample and log the evidence.
4. Choose one primary phrase by relevance and intent; record rejected phrases and why.
5. Generate three title options using §4 formulas before script lock when possible.
6. Confirm the approved script can visibly and verbally pay off every title term.
7. After picture lock, select the final title and write the description from the primary/supporting keyword stack.
8. Derive chapter labels from the final timeline.
9. Build and save the required 10–15 video-specific keyword set from §2, then map that ordered set into the Tags field using §7.
10. Validate title, description, hashtags, disclosures and banned terms against `channel.json`, including with `tools/metadata_validator.py`.
11. Upload corrected captions and verify spelling of the primary mechanism.
12. Save the final package and keyword research log under the episode ID.

## 10. Launch episode examples

| Pillar | Familiar trigger/object | Primary phrase candidate | Honest title direction |
|---|---|---|---|
| Inside Your Body | Minor paper cut | platelet plug formation | How a Platelet Plug Forms Inside a Tiny Cut |
| Inside Manufacturing | Molten glass becoming a bottle | glass bottle manufacturing process | How Molten Glass Becomes a Bottle—From the Inside |
| Inside Technology | Phone connected to a charger | how lithium-ion batteries charge | How a Phone Battery Charges From the Inside |
| Inside Materials | Wet concrete hardening | how concrete sets | How Concrete Sets From the Inside |
| Inside Your Body | Swallowed food | digestion explained | Digestion Explained From Inside the Stomach |
| Inside Materials | Iron exposed to moisture | how rust forms | How Rust Forms From the Inside |

These are query and title candidates, not validated demand forecasts or cleared scientific claims. Each episode must complete research and compliance before production. Note the first row is the topic the sibling LTX profile already shipped as its own EP001 — still valid as a candidate here if `01-ideation` chooses it, but not a default.

## 11. Pre-upload QC

### Keyword and promise

- [ ] Keyword research log exists and names one primary phrase.
- [ ] Final title records the formula and exact/natural primary phrase used.
- [ ] Primary phrase or natural variant appears within the first 40 title characters.
- [ ] Exact primary phrase appears within the first 25 description words.
- [ ] Title and thumbnail promise only mechanisms visible in the accepted episode.
- [ ] Supporting phrases match approved script content.

### Accuracy and disclosure

- [ ] Category is Education.
- [ ] Made for kids is No.
- [ ] Altered or synthetic content is Yes.
- [ ] Exact channel disclosure appears in the description.
- [ ] Sources are direct public URLs used by the final script.
- [ ] Visualization conventions identify relevant scale, timing, color and cutaway simplifications.
- [ ] No diagnosis, treatment advice, fake-footage claim or unsupported timeline appears.

### Metadata and thumbnail

- [ ] Title is 70 characters or fewer and contains no banned pattern.
- [ ] Description is below 5,000 characters and contains both required hashtags.
- [ ] A dedicated 10–15 phrase video-specific keyword block exists and includes the primary phrase.
- [ ] The same ordered keyword set is mirrored into the upload sheet/JSON and mapped into Tags below 500 characters.
- [ ] Chapters start at 0:00 and match the final assembled master.
- [ ] Thumbnail brief contains a complete copy-ready visual prompt, exact typography/layout/output specifications and a full alternate prompt.
- [ ] Every required reference image has a stable existing path under `metadata/thumbnail-references/`; temporary paths are prohibited.
- [ ] Primary thumbnail follows the four-panel causal ladder, uses only accepted process states, and shows input → process → outcome.
- [ ] Primary transformation phrase uses six or fewer content words; optional context and fixed brand footer follow the documented limits.
- [ ] Any primary-layout exception is documented in `metadata/package.md` and owner-approved before upload.
- [ ] Final thumbnail matches the brief and remains readable at 10% scale.
- [ ] Captions are checked against the authorized dialogue.

## 12. Post-publish learning

Review at 48 hours, 7 days and 28 days. Compare like traffic sources and episode formats.

| Question | Evidence |
|---|---|
| Did the search phrase reach the intended audience? | YouTube Search terms, impressions and CTR for Search traffic |
| Did the title-thumbnail promise match? | Retention at 0:15, 0:30 and first mechanism payoff |
| Did the explanation sustain attention? | Average view duration, percentage viewed and chapter-level retention |
| Did the inside viewpoint differentiate the episode? | Browse/Suggested neighbors, comments mentioning the visualization, returning viewers |
| Did viewers continue? | End-screen click rate, playlist starts and second-video views |
| Was the production viable? | Cost and generation time per accepted second; rerender and editorial-repair count |

Do not set universal success thresholds from one pilot. Use the first four comparable long-form uploads to establish the channel baseline, then change one major packaging variable at a time. Where useful, compare against the sibling LTX profile's baseline (same brand, different render stack) rather than starting a baseline from zero.

## 13. Change control

This document cannot override `CHANNEL_STRATEGY.md`, `SCIENCE_AND_SOURCING.md`, `VISUAL_STYLE_CONTRACT.md`, `COMPLIANCE_GATE.md` or `channel.json`. Changing the audience, category, factual-process model, synthetic disclosure, required hashtags or channel pillars requires an explicit channel-level decision rather than a silent SEO edit.
