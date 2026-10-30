# Frame-0 Agent Packet — inside-the-process / EP001

For whoever generates the stills. Per clip: the exact prompt to submit, then that
clip's own validation rules — the staging claims the prompt already makes, turned
into checks.

Workflow: (1) generate a candidate from the prompt as written, (2) check the RESULT
first for the hard blockers below, then use the validation-rules lines as a useful
continuity checklist, (3) correct or re-roll only a hard blocker, and (4) finalise
the first clear, story-usable candidate. Retain other candidates; the post-render
still gate remains a separate check.

## Rules for this packet

### Acceptance threshold

- **Hard blockers:** a required character, setting landmark, or prop touched in the
  following clip is missing, materially wrong, duplicated, or impossible to act from;
  the image starts in the middle of an action; or an unwanted performer, unsafe beat,
  or obvious continuity contradiction changes the story.
- **Tolerate without a re-roll:** a slightly open-looking or partly occluded mouth when
  nobody is visibly speaking; empty paws partly hidden in a pocket or behind the body
  when no prop is held; small eyeline or expression variation; or a tiny surface mark
  that is not readable at the shot's framing. Record it only when useful.
- Do not spend another generation merely to perfect one of those tolerated details.

- Every character reference is declared by the `[[TAG]]` line directly below its clip
  header. Those tagged reference assets already exist — use the listed tags as the
  reference bindings and do not invent a replacement identity.
- `## SC<NN> | pose: …` is packet metadata, **not** text to submit to the image model.
  The prompt begins after it: the `[[TAG]]` line, then the prose.
- The two `frame-0 fwd` / `performable` lines are the ones that protect the render.
  Every listed object must be VISIBLE and at its resting state, because the clip's
  action touches it and image-to-video never invents objects. If the first action is
  not performable from the frozen instant, **re-roll the still — do not reword the
  clip.**
- Save the approved keep as `SC<NN>.png` in `renders/stills/` — exactly that name. The
  render app binds a still to its clip by the scene number PREFIXING the filename stem;
  any other name is skipped and a second file for the same number is ambiguous.

[STYLE] = Photorealistic cinematic scientific visualization, restrained exploration-film aesthetic, controlled directional light with readable depth, practical ivory-and-orange explorer equipment with restrained cyan navigation accents, explicitly photoreal and not illustrated or cel-shaded

---

## SC01 | pose: the adult holding the linen cloth beside the risen dough
[[CAST-002-SHEET]]
The complete visible cast contains exactly 1 character: the adult. Medium wide shot. Warm home kitchen counter, a pale dough ball under a linen cloth beside a glass mixing bowl, soft daylight, polished home realism. one adult in plain home clothes stands at the counter, facing camera three-quarter, gaze at the risen dough, expression surprised, mouth closed and relaxed at frame zero, one hand holding the linen cloth. The dough ball rests in the glass bowl, pale and doubled in size. Warm morning mood, soft shadows, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC01 validation rules:
     n1 contact    : hand holding the linen cloth
     n2 mouth      : mouth closed and relaxed at frame zero, one hand hol
     n3 states     : holding
     n4 frame-0 fwd: these must be VISIBLE and at rest — the linen cloth, the dough ball
     n5 performable: is the clip's first action performable from this frozen instant?

---

## SC02 | pose: the Explorer standing in the wet mixed dough, capsule behind
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium shot. Macro interior inside just-mixed bread dough, wet shaggy flour mass with dry flour pockets and water sheen, pale golden tones, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, standing inside the mass, facing camera three-quarter, gaze at the wet mass around him, expression curious as its own clause, mouth closed and relaxed at frame zero, hands empty. A small ivory-and-orange capsule with a cyan light ring rests in the dough behind him. Curious first-entry mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC02 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside just-mixed bread dough, wet shaggy flour mass wit
     n3 containment: inside the mass, facing camera three-quarter, gaze at th
     n4 states     : empty, standing
     n5 frame-0 fwd: these must be VISIBLE and at rest — the capsule
     n6 performable: is the clip's first action performable from this frozen instant?

---

## SC03 | pose: the Explorer standing among aligning gluten strands
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium close shot. Macro interior inside bread dough, foam city of pale golden bubbles held in a translucent elastic gluten network, warm soft light, ivory and orange tones with subtle cyan accent light, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, standing among aligning strands, facing camera, gaze at the forming strands, expression focused as its own clause, mouth closed and relaxed at frame zero, hands empty. Quiet weaving mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC03 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough, foam city of pale golden bubbles hel
     n3 states     : empty, held, standing

---

## SC04 | pose: the Explorer in the foam city as first bubbles form
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium wide shot. Macro interior inside bread dough, foam city of pale golden bubbles held in a translucent elastic gluten network, warm soft light, ivory and orange tones with subtle cyan accent light, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, standing in the foam, facing camera three-quarter, gaze at the first tiny bubbles, expression amazed as its own clause, mouth closed and relaxed at frame zero, hands empty. Wonder mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC04 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough, foam city of pale golden bubbles hel
     n3 states     : empty, held, standing

---

## SC05 | pose: the Explorer rising with the inflating foam city
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Wide shot. Macro interior inside bread dough, foam city of pale golden bubbles held in a translucent elastic gluten network, warm soft light, ivory and orange tones with subtle cyan accent light, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, settled on the stretching mass, facing camera, gaze up at the inflating bubbles, expression delighted as its own clause, mouth closed and relaxed at frame zero, hands empty. Uplifting swell mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC05 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough, foam city of pale golden bubbles hel
     n3 placement  : on the stretching mass
     n4 states     : empty, held

---

## SC06 | pose: the Explorer braced inside the shaped loaf
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium shot. Macro interior inside bread dough, foam city of pale golden bubbles held in a translucent elastic gluten network, warm soft light, ivory and orange tones with subtle cyan accent light, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, braced inside the shaped loaf, facing camera three-quarter, gaze at the redistributed bubbles, expression steady as its own clause, mouth closed and relaxed at frame zero, hands empty. Settled shaping mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC06 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough, foam city of pale golden bubbles hel
     n3 containment: inside the shaped loaf, facing camera three-quarter, gaz
     n4 states     : empty, held

---

## SC07 | pose: the Explorer inside the doming proofed loaf
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium wide shot. Macro interior inside bread dough, foam city of pale golden bubbles held in a translucent elastic gluten network, warm soft light, ivory and orange tones with subtle cyan accent light, magnified scale. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, inside the doming loaf, facing camera, gaze at the re-inflating bubbles, expression patient as its own clause, mouth closed and relaxed at frame zero, hands empty. Calm patience mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC07 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough, foam city of pale golden bubbles hel
     n3 containment: inside the doming loaf, facing camera, gaze at the re-in
     n4 states     : empty, held

---

## SC08 | pose: the Explorer braced during oven spring
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Wide shot. Macro interior inside bread dough in a hot oven, expanding golden bubbles, heat glow, crust forming at top edge, steam, warm orange light. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, braced in the foam city, facing camera three-quarter, gaze up at the expanding bubbles, expression awed as its own clause, mouth closed and relaxed at frame zero, hands empty. Dramatic heat mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC08 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough in a hot oven, expanding golden bubbl
     n3 states     : empty

---

## SC09 | pose: the Explorer standing in the setting crumb
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium close shot. Macro interior inside bread dough in a hot oven, expanding golden bubbles, heat glow, crust forming at top edge, steam, warm orange light. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, standing in the setting crumb, facing camera, gaze at the firming walls, expression satisfied as its own clause, mouth closed and relaxed at frame zero, hands empty. Satisfying set mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC09 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough in a hot oven, expanding golden bubbl
     n3 states     : empty, standing

---

## SC10 | pose: the Explorer calmly in the finished crumb
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium shot. Macro interior inside bread dough in a hot oven, expanding golden bubbles, heat glow, crust forming at top edge, steam, warm orange light. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, standing calmly in the finished crumb, facing camera three-quarter, gaze at the still bubble walls, expression thoughtful as its own clause, mouth closed and relaxed at frame zero, hands empty. Still calm mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC10 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough in a hot oven, expanding golden bubbl
     n3 states     : empty, standing

---

## SC11 | pose: the Explorer inside the cooling loaf
[[CAST-001-SHEET]]
The complete visible cast contains exactly 1 character: the Explorer. Medium shot. Macro interior inside bread dough in a hot oven, expanding golden bubbles, heat glow, crust forming at top edge, steam, warm orange light. the Explorer, a small figure in an ivory industrial helmet with an opaque reflective visor and cyan side-light rings, orange technical coveralls, a chest instrument and grey boots, inside the cooling loaf, facing camera, gaze at the cooling crumb, expression content as its own clause, mouth closed and relaxed at frame zero, hands empty. Gentle cooling mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC11 validation rules:
     n1 mouth      : mouth closed and relaxed at frame zero, hands empty
     n2 containment: inside bread dough in a hot oven, expanding golden bubbl
     n3 containment: inside the cooling loaf, facing camera, gaze at the cool
     n4 states     : empty

---

## SC12 | pose: the adult slicing the cooled loaf
[[CAST-002-SHEET]]
The complete visible cast contains exactly 1 character: the adult. Close-up shot. Close-up of a freshly sliced loaf of bread on a wooden board, soft airy crumb with visible bubbles, golden crust, warm kitchen light. one adult in plain home clothes at the board, facing camera three-quarter, gaze at the sliced crumb face, expression pleased, mouth closed and relaxed at frame zero, one hand holding the cooled loaf steady on the wooden board, one slice cut. Satisfying reveal mood, Photoreal cinematic scientific visualization, warm polished home realism, ivory-and-orange equipment palette, cyan accent light. Clean natural anatomy, hands anatomically correct.

SC12 validation rules:
     n1 contact    : hand holding the cooled loaf steady on the wooden board, one s
     n2 mouth      : mouth closed and relaxed at frame zero, one hand hol
     n3 placement  : on the wooden board
     n4 states     : holding
     n5 frame-0 fwd: these must be VISIBLE and at rest — the cooled loaf
     n6 performable: is the clip's first action performable from this frozen instant?

---
