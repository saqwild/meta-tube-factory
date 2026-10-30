# EP001 sources - How Bread Rises (02a-sourcing, Branch B)

Gate: bible/SCIENCE_AND_SOURCING.md. Public web reading is required at
this stage; claims below are bounded, paraphrased, and cited to direct
pages. No transcript text is copied. Reviewer scope: source-based
editorial verification within existing gates (no health-actionable
claims are made; no clinician review claimed).

## Claim ledger

| Claim ID | Exact bounded claim | Direct source URL and location | What it supports | Limits/variability | Status |
|---|---|---|---|---|---|
| CLM-1 | Yeast (Saccharomyces cerevisiae) ferments dough sugars and produces carbon dioxide gas and ethanol; the ethanol largely bakes off. | https://science.howstuffworks.com/innovation/edible-innovations/bread.htm (How Bread Works, yeast section) | The rise mechanism, COV04 | Yeast strain and dough formula change gas rate. | SUPPORTED |
| CLM-2 | Kneading develops flour proteins into a long, elastic gluten network that traps gas; without it, gas escapes and bread stays dense. | https://science.howstuffworks.com/innovation/edible-innovations/bread.htm (gluten experiment); https://phys.org/news/2023-11-gluten-complex-chemistry-fluffy-goods.html | Kneading and trapping, COV03/COV04 | Flour protein content varies by wheat and milling. | SUPPORTED |
| CLM-3 | Carbon dioxide bubbles inflate the stretching gluten network; the expansion of many trapped bubbles is the visible rise. | https://phys.org/news/2023-11-gluten-complex-chemistry-fluffy-goods.html (network traps gases during rising) | Bubble rise, surprise beat, COV04 | Bubble count language ("millions") is order-of-magnitude, not measured for this loaf; script must say "millions of tiny bubbles" as an image, not a count. | QUALIFIED |
| CLM-4 | In the oven, trapped gas and water vapour expand (oven spring), yeast is killed by heat, starch gelatinizes, and the foam sets into crumb. | https://www.pizzablab.com/learning-and-resources/baking/dough-baking-processes/ (baking stage table) | Oven transformation, COV04/COV05 | Stage temperatures are ranges for typical wheat loaves, not guarantees. | SUPPORTED |
| CLM-5 | Wheat starch gelatinization runs roughly 65-82C, and surface Maillard browning develops above about 140C. | https://dev.bakerpedia.com/processes/thermal-profiling/ (gelatinization onset/conclusion; crust colour) | Conditions narration, COV05 | Exact values vary with formula, hydration and oven; script uses "about" wording. | QUALIFIED |
| CLM-6 | Fermentation speeds with warmth and slows in the cold; time and temperature trade speed against flavour development. | https://www.sustainweb.org/realbread/articles/jul21-bread-science-101/ (bread science overview) | Conditions and practical segment, COV05 | Kitchen conditions vary; no universal timing is promised. | SUPPORTED |
| CLM-7 | The yeast in finished bread is dead; baking kills it. | https://www.pizzablab.com/learning-and-resources/baking/dough-baking-processes/ (yeast thermal death in stage table) | Objection beat ("is the yeast still alive?"), COV06 | None material; thermal death is gradual, script says "the heat kills the yeast as the loaf bakes". | SUPPORTED |
| CLM-8 | Doneness is judged by crust colour, internal temperature, and sound/texture cues; under-baked crumb stays gummy, and cooling finishes crumb set. | https://dev.bakerpedia.com/processes/thermal-profiling/ ; https://www.sustainweb.org/realbread/articles/jul21-bread-science-101/ | Quality control and cooling, COV06/COV07 | Internal-temperature targets vary by loaf type; script gives no single universal number. | QUALIFIED |


| CLM-9 | Salt slows yeast fermentation slightly and tightens the gluten network, helping dough hold gas and shape. | https://www.sustainweb.org/realbread/articles/jul21-bread-science-101/ (ingredients/salt function) | Salt role in row 2, COV02 | Amount varies by recipe; script makes no universal quantity claim. | SUPPORTED |
| CLM-10 | Baker's yeast is a living single-celled organism sold dry and dormant; warm water and dough reactivate it. | https://science.howstuffworks.com/innovation/edible-innovations/bread.htm (yeast as living leavening) | Yeast identity and activation, row 2, COV02 | Strain products vary; no medical or probiotic claim is made. | SUPPORTED |
| CLM-11 | Shaping presses out oversized gas bubbles and redistributes smaller ones; a tightened surface helps the shaped loaf hold its form during proofing. | https://www.sustainweb.org/realbread/articles/jul21-bread-science-101/ (shaping/proving overview) | Shaping beat, row 6, COV03 | Technique varies by loaf style; script describes this loaf only. | QUALIFIED |
| CLM-12 | After cooling, crumb firms further as starch recrystallizes (staling) over hours to days; the crust softens as moisture migrates outward. | https://www.sustainweb.org/realbread/articles/jul21-bread-science-101/ (cooling/storage overview) | Storage and crumb-vs-crust, rows 11-12, COV01/COV07 | Rate varies with storage and formula; no storage guarantee is promised. | QUALIFIED |
## Visualization ledger

| Visual ID | Planned illustration | Factual support/claim IDs | Scale/time/color/cutaway convention | Fiction or metaphor | Audience clarification |
|---|---|---|---|---|---|
| VIS-01 | Explorer and capsule travelling inside the dough mass | CLM-1, CLM-2 | Magnified interior, fictional scale | Fiction (device) | On-screen disclosure: fictional Explorer, simplified scale. |
| VIS-02 | Dough as a foam city: gluten scaffolding, gas-balloon bubbles | CLM-2, CLM-3 | Explanatory metaphor, bubbles enlarged | Metaphor | Narration names it as a picture for the network, not literal appearance. |
| VIS-03 | Bubbles inflating and stretching during fermentation | CLM-1, CLM-3 | Time compressed (hours shown in seconds) | Representation | Disclosure line names time compression. |
| VIS-04 | Oven spring: bubbles expand, then structure locks solid | CLM-4, CLM-5 | Time compressed, interior cutaway | Representation | No claim of real oven-camera footage. |
| VIS-05 | Crust browning and steam escaping at the surface | CLM-5, CLM-8 | Surface view, natural colour | Representation | Browning is shown as colour change, not a chemical diagram. |
| VIS-06 | COV08 disclosure card over the mixing bowl opening | Approved scope, coverage-map COV08 | Text added in post, not generated | Neither | Exact disclosure: "the flour began as wheat in a field long before it reached this bowl". |

| VIS-07 | Yeast as workers/breathers, rise as engine, colour as receipt, patience as ingredient (spoken metaphors) | CLM-1, CLM-10 | Spoken metaphor, no visual change | Metaphor | Mechanism wording stays literal in the same lines. |
| VIS-08 | Time-compression card: hours of fermentation shown in seconds | CLM-6 | Post-produced text card, stage 06a | Neither | Exact line planned: "Hours of rising, shown here in seconds." |
## Coverage binding

claim_ids are filled in story/coverage-map.json for COV01-COV07, then
checked by tools/coverage_validator.py at stage 02a-sourcing.

OVERALL VERDICT: **CLEARED**
