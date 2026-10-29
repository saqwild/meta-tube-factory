# Episode specification

All numeric runtime, speech-rate, aspect-ratio and render settings come from
../channel.json. The active format is a landscape long-form episode of
approximately ten minutes, built from fixed 20-second source clips. Short
excerpts are optional future derivatives, not the active episode format.

## Story beats

1. An everyday external event and a specific question.
2. Entry into the hidden setting with an immediately readable objective.
3. One observable mechanism broken into manageable causal steps.
4. A surprising but supported explanation.
5. Return to the familiar outside-world result.

Avoid arbitrary countdowns and fabricated catastrophes. For a repair story,
the payoff must name the state actually reached; initial adhesion is not a
fully healed wound.

## Script requirements at 03a

- One logline and one viewer takeaway.
- Cast snapshot from CAST.md, including audio-only roles when used.
- Scene/shot beat table with visible action, supported claim IDs, visual
  convention IDs, approximate duration and exact voiceover/radio words.
- For coverage-enabled episodes, an owner-approved `story/coverage-map.json`; its in-scope MUST items must map to beat-table rows and supported claims, while out-of-scope MUST items use their verbatim disclosure.
- Mark exact native LTX-2.5 dialogue windows separately from diegetic soundscape and
  non-diegetic music; all three are generated in the shot unless a reviewed
  repair is explicitly authorized.
- Runtime and spoken-word estimates using channel.json (`render.spoken_word_band`
  per 20-second clip, not a continuous post-track rate).
- A source-based factual statement must match what the planned shot can show.
- Speaker changes must help understanding; leave room for sound and observation.

## Per-shot production unit

Plan one process action per shot. Begin with readable initial geometry and
end with a stable changed state. Keep identity/shape/contact continuity in the
entity state ledger. A whole biological, industrial or chemical transformation
normally requires several shots and explicit time/scale transitions.

The fixed 20-second source-clip length is a generation setting shared by every
channel in this repo. At 04d, record gross source duration, planned in/out
edits, voice timing and final sequence duration separately. Preserve the
causal event when trimming; do not cut away exactly where contact or
transformation should become visible.

## Format selection

The pilot and subsequent full episodes use the active landscape profile.
The nominal generation budget is target_runtime_seconds divided by
render.clip_duration_seconds (600 / 20 = 30 clips nominal). Planned edits may
require more source coverage to retain the final target. Each part must add a
new question, causal step, comparison or supported explanation; repetition is
not additional depth. Do not silently switch an episode to the optional
Shorts settings or mix portrait sources into the long-form master.
