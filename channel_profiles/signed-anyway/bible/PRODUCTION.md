# Episode Production Operating Procedure

## Production objective

Deliver one authored 8–11 minute case per week after the pilot batch stabilizes, targeting 9:30, with two Shorts that funnel to it. Launch with a two-episode buffer; do not make weekly cadence dependent on same-day generation.

## Stage gates

| Stage | Output | Pass condition |
|---|---|---|
| 1. Case design | Approved `SCRIPT_BRIEF.md` | Two defensible verdicts, seeded reversal, fictional-composite check |
| 2. Script | Timed dialogue script | 8–11 minute read targeting 9:30, natural clip-sized lines, visual evidence beats |
| 3. Shot plan | Numbered shot manifest | Labels, speakers, eyelines, action, sound and continuity defined |
| 4. References | Character/set/prop pack | Identity and wardrobe approved; no real likeness/logo |
| 5. Prompt compile | One continuous-prose clip prompt per clip | Frame-0 honoured; dialogue fits the fixed 20-second clip |
| 6. Proof render | 0.4 MP clips | Performance, identity, blocking and audio pass |
| 7. Final render | 0.98 MP clips | Technical QC pass and license route confirmed |
| 8. Edit | Picture lock | Retention structure, evidence graphics, mix and captions pass |
| 9. Package | Title, thumbnail, metadata | Promise accurate; disclosure present; mobile legibility pass |
| 10. Publish/review | Live upload + scorecard + YPP evidence pack | Authorship archive complete; 48-hour, 7-day and 28-day metrics logged |

## Recommended weekly cadence after launch

| Day | Work |
|---|---|
| Monday | Case brief, plausibility check, title premise |
| Tuesday | Script and table read; lock reversal and verdict |
| Wednesday | Reference/shot planning and proof batch |
| Thursday | Final generation and pickups |
| Friday | Edit, evidence graphics, sound, captions and QC |
| Saturday | Thumbnail/metadata, compliance sign-off, schedule |
| Sunday | Long-form publish; verdict Short follows after 24–48 hours |

For the first month, use a two-week production cycle while building reusable references and measuring rerender rate. Speed claims should be based on logged approved output, not raw generation time.

## Shot manifest minimum fields

`episode_id`, `shot_id`, `duration`, `story_beat`, `subjects`, `speaker_ids`, `dialogue`, `composition`, `camera`, `facing`, `eyeline`, `primary_action`, `hero_prop`, `sound`, `continuity_in`, `continuity_out`, `model_route`, `draft_status`, `final_status`, `rejection_reason`.

## Batch strategy

- Batch by set and lighting first, then by character pairing.
- Proof dialogue before silent inserts because dialogue failures are more expensive to restructure late.
- Generate critical hero-prop close-ups separately.
- Reserve 20–30% GPU time for pickups until the first four episodes establish a measured rate.
- Keep accepted and rejected clips; rejection data is required to improve prompts.

## Human review roles

One person may hold multiple roles, but each check remains explicit:

- story editor: dilemma, causality, reversal, verdict fairness;
- financial plausibility reviewer: mechanism and numbers;
- continuity reviewer: face, wardrobe, props, eyelines and shot state;
- sound/editorial reviewer: dialogue, room tone, pacing and captions;
- compliance reviewer: fiction, disclosures, sponsor and model rights.

## Definition of done

An episode is done only when the video, thumbnail and title make the same promise; the final cut passes `EPISODE_SPEC.md`; the disclosure is present; the model-licence gate is PASS; the YPP Authorship Evidence Pack is complete; and all source assets are archived under the episode ID.
