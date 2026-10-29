# Story engine (every episode from the next LTX episode on, all pillars)

**Status:** ADOPTED 2026-10-29 by owner direction ("adopt the changes related to this channel; no change in video generation, it remains LTX for us, same duration etc.").
**Source:** the sibling profile's `STORY_ENGINE.md`, approved there on 2026-10-29 ("we adopt the concept / idea / logic / story telling but rest we keep same as ours"). Only the storytelling logic is taken. Every render fact below is this profile's own.
**Authority:** this file controls story structure for the next LTX episode and later. Where it conflicts with an older bible file on story shape, this file wins. `channel.json` stays authoritative for runtime numbers. LTX EP001 ("How Glass Bottles Are Made") is unaffected.

## 1. What changes and what does not

| Adopt (storytelling logic) | Unchanged (ours) |
|---|---|
| Control narrates in the second person, to "you" | LTX-2.5 **i2v**, one approved frame-0 still per clip, `GLOBAL::`/`BEAT::` packets (`pipeline/LTX_I2V_CONTRACT.md`) |
| The clock or sequence is the plot | Fixed **20 s** clips (`render.clip_duration_seconds`), about 30-32 clips, about 10-11 min |
| Arc: hook → struggle → breakthrough → climax ≈45% → objection ≈55% → practical → caveats → callback | Native audio; Control is the off-screen voice; helmet-radio Explorer lines |
| One master metaphor the **Explorer enters**; checkpoint metaphors staged **inside** | Inside-first identity: **75-80% of screen time inside** |
| Brief outside moments with the recurring **"you" figure** | Photoreal style; the locked Explorer/capsule masters; `SEO.md` rules, KPIs and baseline rule |
| A true surprise beat that leads the Shorts | `LTX_I2V_CONTRACT.md` §4 rules for cuts and camera; sourcing, claim and visualization ledgers, compliance, stage order |
| "No dead 5 seconds" | Render app, render settings, negative-prompt base, 06a post-production route |
| A Story Definition Sheet before the script | Frame-0 stills by `04f2`; the `blocking.json` geometry authority |

## 2. The "you" anchor per pillar

| | Inside Your Body | Inside Materials | Inside Manufacturing | Inside Technology |
|---|---|---|---|---|
| "You" are… | the host | the one who meets or uses the material | the one holding the finished object | the device user |
| Clock | your hours or days | the material's own timeline | the production sequence | device time |
| Protagonist | you | you, with the material as co-star | the **hero object** in your hand | you, with the device as co-star |
| Stakes | focus, health, performance | will it hold, crack or rust? | will this piece survive heat, stress, inspection? | battery, heat, speed |
| Practical section | understanding a habit, **never medical advice** | "what this explains around you", **never DIY/curing/construction advice** | "what this explains about objects you use" | "what this explains about your device" |
| Title test variant | What Happens To Your Body When You… (Hour by Hour) | What Happens Inside [Material] As It [Verb]s After You [Action] | How [Object] Is Made, Second by Second | What Happens Inside Your [Device] When You [Action] (Minute by Minute) |

Title variants must still carry the recorded primary phrase or a natural variant within the first 40 characters (`SEO.md` §4). Evidence for this engine comes from Body channels; the other pillars are an extrapolation to be measured.

## 3. Arc on the clip grid (targets, not quotas)

Percentages of runtime are the rule; the clip numbers assume a 32-clip episode (32 × 20 s) and scale with the real count.

| Share of runtime | About clips | Job |
|---|---|---|
| 0-7% | 1-2 | Hook: outside "you" trigger, viewer question, master metaphor introduced, clock starts, early disclosure |
| 8-25% | 3-8 | Ordinary world → first mechanism; each checkpoint has its own metaphor staged inside |
| 25-40% | 9-13 | Struggle zone; first breakthrough near 38% |
| 43-50% | 14-16 | **Climax:** the master metaphor pays off with the Explorer inside it |
| 53-58% | 17-18 | **Objection:** "But wait, isn't…?" with a sourced answer |
| 60-68% | 19-22 | Transformation and finished state |
| 70-85% | 22-27 | **Practical:** explanation, never instruction |
| 88-95% | 28-30 | Caveats and "what we simplified" |
| 95-100% | 31-32 | **Callback** to the opening moment, plus a comment question tied to the clock |

- **Surprise beat:** one true, sourced "what?" fact placed before 50%; it leads the Shorts.
- **Outside clips:** about 6-8 of 32 (trigger, 2-3 clock check-ins, consequence, practical anchor, callback). Every other clip is inside. An outside clip carries only the "you" figure, never the Explorer in the same frame. A locator view of the body or object (where the organ or part sits) is also an outside clip, used only when needed.

## 4. Narration (Control)

- Speak to "you" throughout, with no lecture voice. Open each checkpoint on the clock ("Hour 20.").
- The Explorer's helmet-radio lines voice the viewer's question or objection at the right arc point.
- Words per clip stay as in `channel.json` → `render.spoken_word_band`; the second person changes the voice, not the word budget.

## 5. Metaphors: the inside becomes the place

- One master metaphor per episode, set up early and paid off at the climax. The Explorer physically enters it.
- One smaller metaphor per checkpoint, also staged inside.
- **Inside means inside** (`VISUAL_STYLE_CONTRACT.md`): "inside" is the real interior of the named organ, material or device, not an outside view of a digital model. An outside locator view is allowed only when needed to show where it sits.
- Every metaphor is logged in the 02a visualization ledger **as a metaphor**, and the description's VISUALIZATION CONVENTIONS names it.
- Under the one-state-per-clip rule, a metaphor place is a frame-0 plate of its own; the Explorer arrives in it across a cut, never by one clip morphing a mechanism into a place.

## 6. Pacing: "no dead 5 seconds"

- Every 20 s clip shows a visible change about every 5 s: an action, a camera reveal, a flow or a light change.
- A still process is kept alive with camera travel, flow, the Explorer turning, or a light change. It is **not** kept alive by morphing the frame-0 object into another state inside a take; i2v keeps frame 0's shape, so a change of state belongs across a cut (a clip boundary, or a declared cut under §7).
- The closing beat of each clip carries a visible action (`LTX_I2V_CONTRACT.md` §4).
- 06a overlay rhythm: a persistent clock or progress element, plus a new overlay event (clock tick, bar fill, label, metaphor tag) at least every 5 s, as Remotion `text_box` titles, uncluttered and never covering the action or the subtitle safe zone.

## 7. Cuts and camera

LTX-2.5 supports cuts inside one prompt natively, and `pipeline/LTX_I2V_CONTRACT.md` §4 already governs them. **This engine adds no new mechanism and no new syntax**; it only sets where this channel may use what the contract allows.

- **Camera movement:** unchanged. Every clip already carries a motivated camera movement in natural language, never a number (`LTXV-D053`). The "visible change about every 5 s" of §6 is delivered first by camera and flow.
- **Single take stays the default**, as in the contract: one continuous take unless the clip genuinely needs a new framing. A cut is never used to escape a frame-0 contradiction.
- **A declared cut is allowed on process and environment clips**, under the contract: name the transition in prose (a hard cut, a match cut and so on), re-establish scale, identity and light after it, state whether dialogue, music and ambience continue across it, and record `declared_cuts` for the clip so `LTXV-D050`/`D051` can check the count. An undeclared cut still fails.
- **Not on Explorer or "you" clips.** After a cut the video model has no frame-0 anchor, and a close-up of the Explorer is where costume drift and a shoulder patch appeared in the sibling profile's tests (§8). Those clips use camera movement instead. This is a channel rule, not an engine limit.
- **Restate every state-bearing detail after the cut** (positions, contact, gap, colours, materials): the shot after it has only text.
- **Place the cut at a sentence break** if the clip has dialogue, and let the narration land on the shot that shows the result (`LTX_I2V_CONTRACT.md` §4).
- **No LTX render on this channel has used a declared cut yet** (EP001 was 32 single takes). Treat the first use as unproven: pilot it at 04h, start with at most one cut per clip, and record the result before relying on it. A cut also changes the "one state per clip" planning rule: a state change may now sit across a declared cut inside a clip, but clip-boundary changes stay the safer default.

## 8. Recurring-character protection (every shot showing the Explorer or the "you" figure)

The sibling profile found that its video model inserts unplanned cuts on its own, and that on an Explorer close-up the costume drifts and a flag patch appears (two published clips). The protections are kept here because the failure is a channel risk, not an engine one:

1. **Restate the locked look in the prompt, positively.** For the Explorer: "the orange pressure suit with dark-grey panels, plain dark-grey shoulder panels and grey harness straps, the square grey chest unit with a round lens and a glowing cyan light strip, and the smooth white dome helmet with a round cyan side light and an opaque black-mirror visor". The same applies to the "you" figure's locked wardrobe, which must be plain and unbranded. No negations in a positive prompt.
2. **Negative terms** (`channel.json` → `render.negative_prompt_additions`): shoulder patch, arm badge, chest emblem, insignia, flag, mission patch, ribbed helmet band, helmet stripes, visible face behind the visor.
3. **At 05 ingest,** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8) and compare each hit with the clip's declared cuts; any hit that is not a declared cut is reviewed. EP001 of this profile did this by hand; a reusable tool exists only in the sibling repo (`tools/cut_scan.py`, reference only).
4. **At 05a,** zoom-check every Explorer or "you" close-up against the locked reference (helmet cyan side light, chest unit, plain shoulder panels, visor opaque). Call a patch a "flag" only when it is unambiguous at full resolution.

A failing clip is re-rendered with a new seed or fixed at its frame-0 still, per `AGENTS.md` ("a failure gets fixed at the layer it lives in").

## 9. The recurring "you" figure (CAST-002)

- One everyman for every episode and pillar, **locked once**, never regenerated: the master is `locked-references/characters/EP004-CAST002-*.png` (adopted 2026-10-29).
- Always narrated as "you"; never named aloud, never speaks, generic unbranded wardrobe.
- Appears only in outside clips and never shares a frame with the Explorer (one visible character per clip).
- Never shown drinking alcohol or smoking (owner rule 2026-10-29).
- LTX rules from EP001 apply: the figure must already exist in frame 0 of any clip that uses them; an off-screen "you" is never named or entered; the same restatement and QA rules apply (§8).

## 10. Story Definition Sheet (`story/story-definition.md`)

Drafted at 01-ideation (owner gate with the premise) and confirmed after 02a claims clear, at the start of 03a.

| Field | Question |
|---|---|
| Pillar and "you" anchor | Which moment in the viewer's life opens and closes the episode? |
| Clock / sequence | The timeline, its checkpoints and real time stamps |
| Protagonist | You, you with a co-star, or the hero object |
| Want and stakes | What is at stake if the process fails? |
| Outside beats | Trigger, 2-3 clock check-ins, consequence, callback (about 6-8 clips) |
| Inside checkpoints | What the Explorer sees at each checkpoint |
| Master metaphor | The place the Explorer enters; where it is set up and where it pays off |
| Checkpoint metaphors | One per checkpoint, staged inside |
| Struggle and breakthrough | Where the viewer feels the hard part; where it turns |
| Climax (~45%) | The highest point |
| Objection (~55%) | "But wait, isn't…?" plus its sourced answer |
| Practical (~70-85%) | What it explains, and why that is not instruction |
| Surprise beat | The one true "what?" fact → lead Short |
| What we simplified | Scale, colour, timing, visibility, metaphors |
| Callback and comment question | Closing line that echoes the opening; the clock-tied question |

## 11. Compliance by pillar

- **Body:** no medical advice. Wording follows the evidence level:
  - guideline or review: "research shows";
  - human trial: "in a clinical trial";
  - observational study: "people who… tend to";
  - animal or cell study: "**in mice**, researchers found".

  Topics that invite dangerous imitation or unsupervised medical change need a safety boundary or replacement (for example, day-by-day alcohol withdrawal, breath-holding).
- **Other pillars:** the practical section is explanation, never instruction. No claims of factory access or real footage.
- **All pillars:** outside scenes show generic, unbranded people and places. No real-world insignia on any character (§8).

## 12. The next episode

No topic is chosen. Topics the channel has already produced or published, on either profile, are off the list unless the owner says otherwise: the platelet plug (Body), glass bottles (Manufacturing; the sibling's EP002 and this profile's EP001), concrete (Materials) and sleep deprivation (Body). Measure against the channel's own baseline (`SEO.md` §13).
