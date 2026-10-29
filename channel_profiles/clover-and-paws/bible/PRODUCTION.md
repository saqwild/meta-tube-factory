# Episode Production Operating Procedure — Clover & Bruno Stories
**Status**: LOCKED FINAL 2026-10-29
**Channel**: Clover & Bruno Stories @cloverandbruno
**Replaces**: previous prototype 8-11 min tribunal SOP — ABANDONED

## Production objective

Deliver 3-4 episodes per week after pilot batch stabilizes: 2-3 Shorts 160-180s (growth driver) + 1 Long 9:30 target (9:00-15:00 allowed) per week, with 2-week buffer. Launch with 4-episode buffer covering all 5 arcs (Cozy, Stand Tall, Rescue Dash, Road & Muscle, Spy Agency). Do not make weekly cadence dependent on same-day generation.

## Stage gates — cat & dog family

| Stage | Output | Pass condition |
|---|---|---|
| 1. Story design | Approved SCRIPT_BRIEF.md | Type A/B/C + Arc A-E, polite request + Bruno No + soft yes, chore visible by 0:10, fictional-composite check, co-appearance check |
| 2. Script | Timed dialogue script | Shorts 160-180s / Longs 9:30, natural clip-sized lines, Bruno first line No, Clover always polite, visual prop beats |
| 3. Shot plan | Numbered shot manifest | Labels, speakers, eyelines (Clover left up, Bruno right down), action, sound, continuity, max chars (3 Shorts / 6 Longs) |
| 4. References | Character/set/prop pack | Identity and wardrobe approved (Clover orange onesie, Bruno 70y gray + burnt-orange cardigan and glasses-on-a-chain), no real likeness/logo, hash-bound |
| 5. Prompt compile | Photoreal 6-section prompts | Unified photoreal engine, labels stable, dialogue/timing match shot duration, Bruno never-yes-first enforced |
| 6. Proof render | 0.4 MP clips | Performance (Clover soft, Bruno raspy grumpy), identity, blocking, audio pass |
| 7. Final render | 0.98 MP clips / 4K | Technical QC pass, warm lighting, fur detail, no distress |
| 8. Edit | Picture lock | Retention structure (0:10 chore, 0:45 Bruno No, 2:00 soft yes), prop inserts, mix and captions pass |
| 9. Package | Title, thumbnail, metadata | Promise accurate, both cat and dog faces for Duo, disclosure present, mobile legibility, hashtags #catanddog #cloverandbruno |
| 10. Publish/review | Live upload + scorecard + YPP evidence pack | Authorship archive complete, altered content=Yes, not made for kids, 48h/7d/28d metrics logged |

## Recommended weekly cadence after launch — cat & dog

| Day | Work |
|---|---|
| Monday | Story briefs x3: pick Arc rotation (e.g., Cozy, Rescue Dash, Spy), title premise, co-appearance |
| Tuesday | Scripts + table read: lock Bruno No line + soft yes line + Clover polite line |
| Wednesday | Reference/shot planning + proof batch (kitchen/porch/market/garage) |
| Thursday | Final generation + pickups (prop close-ups: bike pump, bag, oil can, magnifier) |
| Friday | Edit, sound, captions, QC — check Bruno never-yes-first, Clover polite, max chars |
| Saturday | Thumbnail (both faces for Duo) + metadata + compliance sign-off (Altered Yes, Not kids) |
| Sunday | Long publish 9:30 + Short funnel next day via Related Video |

First month: two-week production cycle while building reference packs for CAST-001 to CAST-007 (portrait + full-body + six-panel). Measure rerender rate for Bruno says yes first = fail.

## Shot manifest minimum fields — cat & dog

episode_id, shot_id, duration, story_beat, type (A Duo 70% / B Clover 15% / C Bruno 15%), arc (A-E), subjects, speaker_ids, dialogue, composition, camera, facing, eyeline, primary_action (Clover holds bike / Bruno crosses arms / Fin lifts), hero_prop (bike, bag, pump, oil can, magnifier), sound (porch creak, bag rustle), continuity_in, continuity_out, location (kitchen/porch/market/garage/bridge/park/lake), model_route, draft_status, final_status, rejection_reason

## Batch strategy — cozy + action

- Batch by set and lighting first: all kitchen warm, then porch, then market, then garage, then outdoor rescue locations
- Proof dialogue before silent inserts because Bruno grumpy voice failures expensive late
- Generate critical hero-prop close-ups separately (bike tire flat vs inflated, heavy bag, oil can, magnifier)
- Reserve 20-30% GPU time for pickups until first 4 episodes establish rate, especially for Rescue Dash tree/cart physics
- Keep accepted and rejected clips; rejection data required to improve prompts (e.g., Bruno says yes first = auto-reject)
- Outdoor arcs (Rescue, Road, Spy) batch together to show places around Paw Street

## Human review roles — cat & dog

One person may hold multiple roles, but each check explicit:

- story editor: wish/chore clarity, polite vs grumpy contrast, Bruno No within 45s, soft yes, payoff warmth
- co-appearance reviewer: departures from the CAST.md §4 defaults are declared and reasoned
- continuity reviewer: fur, wardrobe (orange onesie / burnt-orange cardigan + glasses-on-a-chain), age 70y, paws, props, eyelines, shot state
- sound/editorial reviewer: Clover soft polite + Bruno raspy grumpy clear, room tone warm continuous, captions match
- compliance reviewer: fiction, synthetic disclosure Yes, not made for kids, no graphic violence, no distress bait, max chars, model rights

## Definition of done — cat & dog family

Episode done only when video, thumbnail (both cat+dog for Duo) and title make same promise; final cut passes EPISODE_SPEC.md (160-180s Shorts / 9:30 Longs, Bruno No within 45s, soft yes by 2:00 Shorts / 6:00 Longs); disclosure present (AI-generated original stories. Not real footage. Photoreal anthropomorphic cat and dog family stories — Kitten Clover and Grumpy Dog Bruno.); altered content=Yes, not made for kids; YPP Authorship Evidence Pack complete; all source assets archived under episode ID with hash-bound references; thumbnail shows both faces for Duo.

## Arc rotation guardrail

Maintain rolling 5-episode matrix: Cozy, Stand Tall, Rescue Dash, Road & Muscle, Spy Agency — ensure no arc repeats twice in row, keep cozy 20% base, action 50% of Duo. Log arc type per episode to avoid template repetition flagged as inauthentic.
