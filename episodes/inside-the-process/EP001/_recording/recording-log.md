# EP001 demo recording log (recorded run, 2026-10-29)

Dual-track evidence for the 3-minute judge demo. Track A = OBS capture
(4 windows: Muse, output folder, Photos, Markdown viewer). Track B =
artifacts in this episode folder. Raw captures stay outside the repo.

| Stage | Track A (process) | Track B (output) |
|---|---|---|
| 00-preflight | Fresh EP001 created, stage completed | episode-state.json |
| 01-ideation | Premise + story definition written | story/premise.md, story/story-definition.md |
| 01b-coverage-scan | Benchmark scan, coverage map, validators PASS, review + scope lock emitted | story/youtube-benchmark.md, story/coverage-map.json, story/coverage-review.json, story/coverage-scope.lock.json |

Notes: this is the recorded re-run after the first session's OBS take
was lost; identical scope and content, restored from Git history.
| 02-research | Live Muse Spark call; sources per COV01-COV07; validator PASS | story/research-notes.md |
| 02a-sourcing | Claim ledger CLM-1 to CLM-12 + visualization ledger VIS-01 to VIS-08; claims bound in coverage-map; validator PASS, verdict CLEARED | story/sources.md |
| 02b-compliance | 14-gate compliance prepared, all PASS, verdict CLEARED, awaiting owner approval | story/compliance.md |
| 03a-writer | Live Muse Wonder call; 12-row script restored final revision, clip split PASS 12/12, coverage PASS | story/characters.md, story/script.md |
| 03b-script-review | Independent spawned reviewer PASS; owner approved, script locked | story/script-review.md |
| 04a-visual-brief | Live Muse Wonder call; 8 scenes, 12 clips = 12 stills budgeted | visual/scene-list.md |
| 04b-character-refs | Locked masters copied byte-identical (SHA-256 verified), zero generation spend | visual/references/manifest.md, visual/references/characters/*.png |
| 04c-scene-refs | First live Muse Image plates (5), ENV004 viewed PASS, PNG converted, environment locks written | visual/references/scenes/*.png, _context/environment-locks.json |
| 04d-shot-plan | blocking.json for 12 clips (camera-relative facing, end states chained), shot-plan.md | visual/shot-plan.md, _context/blocking.json |
| 04e-storyboard | Derived storyboard.html built (12 clips, placeholders pending stills) | exports/storyboard.html |
