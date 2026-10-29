# 04d — shot plan and blocking spec

## Why this stage carries more weight than it used to

Under the previous engine this stage wrote a prose shot breakdown and the prompt stage decided
the rest. Under LTX-2.5 i2v, **two artifacts must agree about geometry** — the clip prompt and
the frame-0 still — and if each decides pose, gaze and prop state independently they will
disagree. The classic symptom is a still where a character faces the camera and a clip that
says "he looks at her".

So this stage decides geometry **once**, in a structured, machine-checkable file. Both prompt
stages are projections of it and neither may re-decide it.

## Inputs

`visual/scene-list.md`, `visual/references/manifest.md`, `story/script.md`,
`channel_profiles/<slug>/channel.json` → `render`.

## Task

### 1. The clip breakdown

Break the episode into **clips**. The clip is the generation unit: a fixed **20 seconds** for
both channels, one still and one prompt each. `channel.json` → `render.clip_duration_seconds`
is authoritative; do not carry a duration figure over from a sibling pipeline.

Per clip, record which references apply, the camera framing **described relative to the
camera**, and the dialogue it carries. Facing is never described relative to another character
— that is the rule that disqualifies bench, podium and head-of-table geometry, which puts a
speaking character's back to the lens.

Check the spoken-word budget as you break: at the channel's planning pace, a 20-second clip
carries a band of quoted words declared in `channel.json` → `render.spoken_word_band`. A clip
that needs materially more dialogue than that is a clip that needs splitting, and this is the
cheapest place to discover it.

### 2. The blocking spec — `_context/blocking.json`

The geometry authority. Scene-keyed, structured so the gates parse fields instead of regexing
prose:

```json
{
  "SC07": {
    "chars": {
      "BRUNO": {"pos": "left", "facing": "camera-left three-quarter", "gaze": "at Pip",
                "pose": "standing at the fence, one paw on the post",
                "expression": "guarded", "mouth": "closed", "hands": "empty",
                "cue": "burnt-orange cardigan", "visible": true},
      "PIP":   {"pos": "right", "facing": "camera", "gaze": "up at Bruno",
                "pose": "seated in the mud", "expression": "hopeful",
                "mouth": "closed", "hands": "empty",
                "cue": "red bandana", "visible": true}
    },
    "props": [
      {"name": "the trowel", "detail": "one flat dent beneath the handle",
       "resting_state": "lying flat in the garden bed, blade half-buried"},
      {"name": "the watering can", "detail": "a chipped enamel rim",
       "resting_state": "on its side, spout pointing camera-right"}
    ],
    "camera": {"shot": "medium two-shot", "movement": "slow dolly in"},
    "anchors": ["Bruno reaches for the trowel", "Bruno grumbles", "Pip's ears droop"],
    "end_state": {
      "BRUNO": {"pos": "left", "pose": "standing at the fence", "hands": "empty"},
      "PIP":   {"pos": "right", "pose": "seated in the mud", "hands": "empty"}
    },
    "frame0": "rest"
  }
}
```

Field rules that are not optional:

- **`expression` is its own field**, separate from `pose`. An emotional read folded into a
  posture string cannot be independently reviewed, and it is exactly what the clip QA
  checklist's performance column checks against.
- **`mouth` defaults to `closed` for every character.** Override only for a genuine
  cold-open/reveal peak, and say so explicitly.
- **`hands` ends empty**, and a prop that will be "placed" during the clip is already at its
  placed `resting_state` — a prop seeded mid-placement lingers or duplicates in the render.
- **`camera.movement` is decided here**, not at the prompt stage. A locked camera over a
  settled character reads as a dead freeze-frame; pick the movement the scene calls for from
  the table in `LTX_I2V_CONTRACT.md`.
- **`end_state` feeds the next clip's continuity check** (`LTXV-S004`). A continuing
  character's next opening state must equal it.
- Only characters marked `visible: true` are drawn in frame.

## Output

`episodes/<slug>/EPxxx/visual/shot-plan.md` and
`episodes/<slug>/EPxxx/_context/blocking.json`.

## Forbidden

Do not write LTX prose prompts or still prompts here — those are `04f` and `04f2`. Do not
describe facing relative to another character under any circumstance. Do not leave `mouth`,
`expression`, `hands` or `camera.movement` unset and expect a downstream stage to invent them —
that is precisely the drift this stage exists to prevent.

## Stop condition

Every clip in the episode has a `blocking.json` entry with every required field populated, and
every continuing character's `end_state` is consistent with the following clip's opening.
