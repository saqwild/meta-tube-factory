# Generic agent launch note

Before work: read `AGENTS.md`, `pipeline/PIPELINE.md`, the active episode's
`episode-state.json` to find `next_stage`, then the matching
`pipeline/stages/<next_stage>.md` contract. Read only that stage's declared inputs. Perform
exactly that stage's task. Write only its declared outputs into the episode's folder. Run:

```bash
python tools/preflight.py complete <channel_slug> <episode_id> <stage_id>
```

(add `--approve` only if you are the human owner and the stage is an owner gate). Stop.

Never invent a stage output the contract doesn't declare. Never read or write outside
`C:\pycode\vidgen-ltx`, except `C:\pycode\app-vidgen-dist` **read-only**, to verify the render app's
real ingest contract and settings.

Nothing here depends on which LLM is driving — if a step in a stage contract seems to assume a
specific tool your platform lacks (e.g. no direct image-gen tool call), do the equivalent
manually and say so in the stage's confirmation note.

## Two things worth knowing before your first stage

**The prompt stages are a loop, not a line.** `04f` drafts the clip prompt and emits a frame-0
requirement block; `04f2` generates the still from that block; `04f3` re-anchors the prompt to
the approved pixels. Each is a separate stage with its own contract. Do not collapse them.

**In i2v the image is the contract; the prompt is only the delta.** If something is wrong, fix
it at the layer it lives in — the still, the conditioning, the render config, the gate. Adding
words to a prompt to compensate for a bad still is the single most common way this pipeline
goes wrong.
