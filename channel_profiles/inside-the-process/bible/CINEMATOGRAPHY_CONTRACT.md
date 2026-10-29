# Cinematography Contract

## Visual grammar

Each Micro-Journey alternates between a familiar exterior, a readable entry/cutaway, mechanism-scale observation and an exterior payoff. Camera movement serves orientation or reveals cause and effect; it is not decoration.

## Shot roles

| Role | Purpose |
|---|---|
| Exterior anchor | Establish the familiar object/event and viewer question |
| Entry transition | Disclose that scale/cutaway changes and move into the hidden setting |
| Baseline | Show the system before the main change |
| Approach | Preserve a visible gap and destination before contact |
| Contact / transformation | Hold fixed landmarks so the physical event cannot be mistaken for camera motion |
| Comparison | Show before/after or two states with stable panels and exposure |
| Consequence | Hold long enough for the changed state to be understood |
| Return | Connect the hidden mechanism to the familiar outside result |

## Camera rules

- One primary camera intention per 20-second source clip.
- Use locked or slowly motivated movement for contact, attachment, deformation and comparison.
- A zoom cannot stand in for object growth, spreading or motion.
- State all left/right/front/behind relationships relative to the **camera**, never relative to another character or object — the universal rule in this repo (`AGENTS.md`).
- Preserve at least one fixed environmental landmark across continuity shots.
- Do not mix macro, cellular and molecular scales inside one continuous shot without a visible transition and disclosed convention.
- Keep the main mechanism large enough to read on a phone, but preserve enough surrounding geometry to understand its location.

## Panels and overlays

Two-panel comparisons require stable panel boundaries, exposure and subjects for the full explanatory interval. If a video model blacks out or replaces a panel, use a deterministic editorial composite from the approved plate rather than repeating an unstable generation indefinitely. Labels are added in editing, not requested from LTX-2.5.

## Explorer and capsule

The capsule may establish scale, carry the transition or observe from the edge. It does not occupy a mechanism close-up when it would cover contact geometry. The Explorer uses restrained head turns, hand braces and gaze changes; no superhero poses, repair tools or intervention.

## Edit continuity

- Enter a sequence with state A and leave with an observable state B.
- Adjacent shots inherit object identity, contact landmark, flow direction, lighting side and process state.
- Cut on a completed beat or stable hold, not before the required event becomes visible.
- Preserve 5–20 seconds at the end for the end screen only when the episode plan includes a clean neutral composition.

## Pacing (from the next LTX episode, `STORY_ENGINE.md` §6-7)

- **A visible change about every 5 s of a 20 s clip**, with no static or unchanged stretch longer than about 5 s. A still process is kept alive with camera travel, flow, the Explorer turning, or a light change, never by morphing the frame-0 object into another state inside the clip.
- **Camera movement and cuts follow `pipeline/LTX_I2V_CONTRACT.md` §4 unchanged.** Single take is the default; a declared cut is allowed on process and environment clips only (never on Explorer or "you" clips), with the transition named, state restated and audio continuity stated. See `STORY_ENGINE.md` §7. Any hard cut in a rendered clip that was not declared is reviewed at 05.
- Describe framing as a still composition, not as "from X up to Y", which a video model can read as a pedestal move.

## Production-profile note (LTX)

This is the same visual grammar as the sibling LTX profile, with the clip unit changed from a fixed 15 seconds to this repo's universal fixed 20 seconds (`channel.json` → `render.clip_duration_seconds`). A whole causal sequence spans more or fewer clips than it would have under the LTX profile; replan clip counts from the 20-second unit, not by porting a LTX shot list.
