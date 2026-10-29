# 02b — compliance gate

Appears in a channel's `pipeline_stages` when that channel declares a `compliance` block in
`channel.json` needing a **pre-script** gate. Both channels currently declare one, and the two
are not the same shape — read the channel's own block rather than assuming.

## Inputs

- `story/premise.md`
- `channel_profiles/<slug>/channel.json` → `compliance`, `hard_safety_floor`,
  `metadata_validation`
- the channel's compliance reference doc in its bible (`COMPLIANCE_GATE.md`)
- `story/sources.md` **only where the channel runs `02a-sourcing`** — a channel without that
  stage has no sources file, and its absence is not a finding

## Task

Apply the channel's own declared checklist to the premise and record a **per-gate verdict**, not
a single overall impression. Every channel gets:

- non-depiction of a real person, company, product, brand or event
- the `hard_safety_floor` items, each checked individually
- originality against prior episodes on that channel
- the synthetic-media disclosure requirement

Plus whatever else that channel declares. A financial-drama channel adds mechanism plausibility
and a two-defensible-verdicts test; a family channel adds its own character and safety rules.

**Run before a script exists.** That is the point of the stage: a premise that cannot clear
compliance should never absorb writing effort, and a gate applied after a script is written is a
gate under pressure to pass.

## Output

`episodes/<slug>/EPxxx/story/compliance.md`, with a per-gate table and an explicit overall
verdict: **`CLEARED`** or **`BLOCKED`**.

## Forbidden

No dialogue, no scenes, no prompts. Do not narrow a gate so the premise fits it. A `BLOCKED`
verdict must never be silently downgraded — it stops the episode with no further stage
authorized until the owner resolves it, by revising the premise and re-running from
`01-ideation`, or by cancelling.

## Stop condition

**Owner gate.** `03a-writer` may not start without a recorded `CLEARED` verdict here. An agent
may prepare the verdict document; a human approves it.
