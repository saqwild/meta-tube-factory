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
| 04f-ltx-prompt-draft | 12 draft prompts + frame0 requirements, validator PASS 12/12 (draft) after 3 fix rounds | prompts/7-video-prompts.md, _context/frame0-requirements.json |
| 04f2-frame0-stills | 12 Muse Image stills generated; Explorer set regenerated adult proportions; gate PASS with visor deviation logged | renders/stills/SC01-SC12.png, qa/still-gate.md |
| 04f3-ltx-prompt-final | GLOBAL re-anchored (gold visor), strict validator PASS 12/12, manifest built | _context/ltx-prompt-manifest.json |
| 04g-ltx-render-package | Render package built, pilots SC01,SC02,SC05,SC08,SC12 | exports/ltx-render-package/ |
| 04f2 owner QA revision | SC01/SC12 CAST-002 face fix + Explorer opaque visor fix, all 12 regenerated, SC01/SC06 viewed PASS | renders/stills/*.png, qa/still-gate.md |
| 04f3/04g rebuild | Strict PASS 12/12, manifest + render package rebuilt with new hashes | _context/ltx-prompt-manifest.json, exports/ltx-render-package/ |
| 04h pilot QA (part) | SC01 rendered clip FAIL cloth inversion (frames checked); prompt fix at 04f3, package rebuilt | qa/pilot-qa.md, qa/frames-s01/ |
| 04h pilot QA (owner) | SC02/SC03/SC04 viewed PASS; SC01 re-render pending; tail dead silence to trim at 06a | qa/pilot-qa.md |
