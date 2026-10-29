# Claude launch note

No Claude-specific behavior. Follow `adapters/generic/AGENT.md` exactly.

Skill routing:

| stage | prompt writer | generator |
|---|---|---|
| `04b` / `04c` — reference sheets and plates | — | the `muse-image` skill |
| `04f` / `04f3` — clip prompts | `local_skills/ltx-production-writer/SKILL.md`, **sole writer** | none — LTX renders at `04h`/`05` |
| `04f2` — frame-0 stills | `local_skills/frame0-still-writer/SKILL.md`, **sole writer** | `muse-image`, working down `prompts/6-image-agent-packet.md` one clip at a time |

Writing the prompt and generating the image are two different jobs. The writer skills never
generate; `muse-image` never authors a prompt from scratch here — it renders the text the
writer produced. One generator per episode, declared and held: mixing them is the fastest route
to cast drift.

The global **`ltx25-prompting`** skill runs only at the end of `04f3`, as a read-only syntax and
conformance check. It never drafts, enhances, paraphrases or rewrites, and where it disagrees
with `pipeline/LTX_I2V_CONTRACT.md` the contract wins — it is a generic vendor-syntax guide and
does not carry this pipeline's render-validated findings.

Do not invoke `prompt-master`, `video-prompting`, or `flux-best-practices` anywhere in this
repo. The first two do not implement this repository's owner-locked PromptRelay-style beat format; the third is for a generator this
pipeline does not use.
