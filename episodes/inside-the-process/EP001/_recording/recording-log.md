# EP001 demo recording log

Dual-track evidence for the 3-minute judge demo. Track A = OBS window
capture of the Muse window (Factory scene). Track B = artifacts in
this episode folder as they are created. Editor (Remotion, demo-video/)
matches tracks by stage and timestamp. Raw captures stay outside the
repo; selected clips and this log are committed.

| Stage | Date | Track A (process) | Track B (output) |
|---|---|---|---|
| 00-preflight | 2026-10-29 | preflight new, EP001 created | episode-state.json |
| 01-ideation | 2026-10-29 | premise + story definition written, stage completed | story/premise.md, story/story-definition.md |
| 01b-coverage-scan | 2026-10-29 | YouTube benchmark scan (4 queries), coverage map written, validators PASS, review + scope lock emitted | story/youtube-benchmark.md, story/coverage-map.json, story/coverage-review.json, story/coverage-scope.lock.json |
| 02-research | 2026-10-29 | Live Muse Spark synthesis call; web sources per COV01-COV07; coverage validator PASS | story/research-notes.md |

## Notes

- Benchmark eligibility: Susanna Z and SciShow Kids excluded (no usable
  English opening-caption sample on 2026-10-29); B01-B03 are the top
  eligible directly relevant videos. No transcript text is stored.
- Next: owner approves 01b scope lock, then 02-research.
