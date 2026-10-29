"""Adopt the channel-level changes of sibling-repo's inside-the-process profile (owner, 2026-10-29).

Scope (owner): channel setup only. Nothing about video generation changes -- LTX-2.5 i2v, fixed 20 s clips, frame-0 stills,
GLOBAL::/BEAT:: packets, render settings and the stage list stay ours. LTX-2.5 doctrine (I2V, 15 s shots, <d> tags,
intra-clip cuts, the 960x544 upscale profile) is NOT adopted. The Story Definition Sheet / skill / stage-contract edits are
outside this pass (owner: "profile only").

Every edit asserts its anchor, so a re-run on an already-edited file fails loudly instead of duplicating text.
Reads sibling-repo read-only. A backup of the pre-edit profile is in the session scratchpad.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIBLE = HERE / "bible"
MM = Path(r"C:\pycode\sibling-repo\channel_profiles\inside-the-process")


def rd(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def wr(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8", newline="\n")


def sub(p: Path, old: str, new: str) -> None:
    s = rd(p)
    assert s.count(old) == 1, f"{p.name}: anchor not found exactly once: {old[:70]!r} (count {s.count(old)})"
    wr(p, s.replace(old, new))


def sub_line(p: Path, startswith: str, new_line: str) -> None:
    lines = rd(p).split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    assert len(hits) == 1, f"{p.name}: line starting {startswith[:60]!r} matched {len(hits)} times"
    lines[hits[0]] = new_line
    wr(p, "\n".join(lines))


def append(p: Path, text: str) -> None:
    s = rd(p)
    wr(p, s.rstrip("\n") + "\n\n" + text.strip("\n") + "\n")


def between(s: str, start: str, end: str) -> str:
    a = s.index(start)
    b = s.index(end, a)
    return s[a:b]


# ---------------------------------------------------------------------------------------------------------------------
# 1. locked references (the images were copied byte-for-byte by the owner-approved step; hashes recorded here)
# ---------------------------------------------------------------------------------------------------------------------
wr(HERE / "locked-references" / "README.md", """# inside-the-process — channel-level locked reference images

**Adopted from the sibling repo `sibling-repo` on 2026-10-29 (owner decision).** The files in `characters/` are the
channel masters for the Explorer, the capsule and the recurring "you" figure. They are still images and engine-agnostic;
they were copied byte-for-byte and the SHA-256 values below match the source files. Do not regenerate them.

| File | Role | SHA-256 |
|---|---|---|
| `EP001-CAST001-sheet.png` | Explorer master sheet (never a conditioning input) | `61a11b4eb79e73c88ba606f72fdef0d24b5ffe93363e1cc96561ad3decbf7728` |
| `EP001-CAST001-full-body.png` | Explorer, full body | `b7f47933ea090195c85b87d19a0fd674c217d949ef434d27c896e2d37dd02a02` |
| `EP001-CAST001-portrait.png` | Explorer, portrait | `0024b9fe9ba8551c47bf3ce00d3ce740967599ef262b27642962f35835080446` |
| `EP001-CAST001-seated-in-capsule.png` | Explorer seated in the capsule | `5b4dc965b1d6ae5c6c84c8cb4765664cf8b3fdcd306ece01d2106fb415394ca5` |
| `EP001-PROP001-capsule-sheet.png` | Capsule master sheet | `41770ae9d00b5222bbccd07971bfa09005ca7792516fd7db3e6a26d67742d612` |
| `EP004-CAST002-sheet.png` | "You" figure master sheet (never a conditioning input) | `e313375153c3815bf20bf1005d67fd2923f5c5333ea7c9a5d7cd0b688949485e` |
| `EP004-CAST002-full-body.png` | "You" figure, full body | `476dc92e799c2c4945b4c1c30f22ce9b0d352a8b13cf20bb6b945287285822c8` |
| `EP004-CAST002-portrait.png` | "You" figure, portrait | `1890a0ae89f76c134cd41b8ed4a40710f2176a212f8bad3b346b58cfe8e1e202` |
| `EP004-CAST002-seated-desk.png` | "You" figure, seated at a desk | `7ea66109ae0cd1efc5d69eb3216389e6109eca2217cf98d1308920ae58191579` |

The `EP001-`/`EP004-` prefixes are the **sibling profile's** episode numbers (where each master was made and locked: Explorer and
capsule by the owner on 2026-10-29; CAST-002 owner-selected from three candidates at that profile's EP004 04b on 2026-10-29,
generated with muse-image-1.0 via muse-image as an owner-directed exception to Muse Image). Keep the names unchanged so the
hashes and the sibling's manifests stay traceable. This profile's own episode numbering is separate.

**Use.** Condition frame-0 stills on the bare `full-body`, `portrait`, `seated-in-capsule` or `seated-desk` file, never on a
whole `sheet` (a still-image model fed a composed sheet inherits the whole page). Episodes snapshot the files they use
byte-for-byte into `visual/references/characters/` and record their SHA-256 hashes in `visual/references/manifest.md`.

**Not masters.** The Explorer/capsule references that inside-the-process LTX EP001 generated for itself are episode-local;
they stay in that episode and are not channel masters. The Explorer in later episodes is conditioned on the masters above.
No voice asset is locked.

The authoritative designs are `../bible/CAST.md`, `../bible/CHARACTER_BIBLE.md` and `../bible/VISUAL_STYLE_CONTRACT.md`.
""")

# ---------------------------------------------------------------------------------------------------------------------
# 2. STORY_ENGINE.md (new) -- the storytelling logic, rewritten for this profile's LTX numbers
# ---------------------------------------------------------------------------------------------------------------------
wr(BIBLE / "STORY_ENGINE.md", """# Story engine (every episode from the next LTX episode on, all pillars)

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
| A true surprise beat that leads the Shorts | One state per clip, state changes across cuts; sourcing, claim and visualization ledgers, compliance, stage order |
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
- **Outside clips:** about 6-8 of 32 (trigger, 2-3 clock check-ins, consequence, practical anchor, callback). Every other clip is inside. An outside clip carries only the "you" figure, never the Explorer in the same frame.

## 4. Narration (Control)

- Speak to "you" throughout, with no lecture voice. Open each checkpoint on the clock ("Hour 20.").
- The Explorer's helmet-radio lines voice the viewer's question or objection at the right arc point.
- Words per clip stay as in `channel.json` → `render.spoken_word_band`; the second person changes the voice, not the word budget.

## 5. Metaphors: the inside becomes the place

- One master metaphor per episode, set up early and paid off at the climax. The Explorer physically enters it.
- One smaller metaphor per checkpoint, also staged inside.
- Every metaphor is logged in the 02a visualization ledger **as a metaphor**, and the description's VISUALIZATION CONVENTIONS names it.
- Under the one-state-per-clip rule, a metaphor place is a frame-0 plate of its own; the Explorer arrives in it across a cut, never by one clip morphing a mechanism into a place.

## 6. Pacing: "no dead 5 seconds"

- Every 20 s clip shows a visible change about every 5 s: an action, a camera reveal, a flow or a light change.
- A still process is kept alive with camera travel, flow, the Explorer turning, or a light change. It is **not** kept alive by morphing the frame-0 object into another state inside the clip; i2v keeps frame 0's shape, and state changes belong across cuts.
- The closing beat of each clip carries a visible action (`LTX_I2V_CONTRACT.md` §4).
- 06a overlay rhythm: a persistent clock or progress element, plus a new overlay event (clock tick, bar fill, label, metaphor tag) at least every 5 s, as Remotion `text_box` titles, uncluttered and never covering the action or the subtitle safe zone.

## 7. Cuts (not adopted)

The sibling profile allows one planned cut inside a 15 s clip. That is a LTX-2.5 capability and is **not** adopted. Here a clip is one continuous take; changes of state happen across clips. Any hard cut inside a rendered clip is therefore unplanned and is reviewed at 05 (§8).

## 8. Recurring-character protection (every shot showing the Explorer or the "you" figure)

The sibling profile found that its video model inserts unplanned cuts on its own, and that on an Explorer close-up the costume drifts and a flag patch appears (two published clips). The protections are kept here because the failure is a channel risk, not an engine one:

1. **Restate the locked look in the prompt, positively.** For the Explorer: "the orange pressure suit with dark-grey panels, plain dark-grey shoulder panels and grey harness straps, the square grey chest unit with a round lens and a glowing cyan light strip, and the smooth white dome helmet with a round cyan side light and an opaque black-mirror visor". The same applies to the "you" figure's locked wardrobe, which must be plain and unbranded. No negations in a positive prompt.
2. **Negative terms** (`channel.json` → `render.negative_prompt_additions`): shoulder patch, arm badge, chest emblem, insignia, flag, mission patch, ribbed helmet band, helmet stripes, visible face behind the visor.
3. **At 05 ingest,** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8). With no planned cuts, every hit is reviewed. EP001 of this profile did this by hand; a reusable tool exists only in the sibling repo (`tools/cut_scan.py`, reference only).
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
""")

# ---------------------------------------------------------------------------------------------------------------------
# 3. CAST, CHARACTER_BIBLE, VISUAL_STYLE_CONTRACT: voice rule, costume lock, CAST-002
# ---------------------------------------------------------------------------------------------------------------------
sub_line(BIBLE / "CAST.md", "Voice: adult English, curious and concise.",
         "Voice: adult English, curious and concise, heard only over the helmet radio. There is never lip-synced on-screen speech. "
         "While the line plays, the visible Explorer holds still, watching, with the visor unchanged; gestures come before or after "
         "the line. The face is never revealed (`VISUAL_STYLE_CONTRACT.md` voice rule). LTX-2.5 generates authorized dialogue natively "
         "from exact quoted prompt lines (see `channel.json` → `render.narration_mode` and `cast.explorer_voice_mode`). Record the actual "
         "accepted clip provenance; a written voice adjective is not an identity lock. No tested voice descriptor exists yet under this "
         "profile (see `channel.json` → `render.voice_lock_note`). Post-production may balance or repair reviewed audio but is not the "
         "default dialogue source.")
sub(BIBLE / "CAST.md", "Promotion to channel locked references follows the existing second-use rule.",
    "Promotion to channel locked references follows the existing second-use rule; the Explorer, capsule and \"you\" masters are "
    "already locked (see the section below).")
s = rd(BIBLE / "CAST.md")
i = s.index("## Production-profile note (LTX)")
wr(BIBLE / "CAST.md", s[:i] + """## Story-engine additions (`STORY_ENGINE.md`, adopted 2026-10-29)

- **The Explorer (CAST-001) costume is locked.** It is restated positively in every prompt showing the Explorer, and close-ups are zoom-checked at 05a (`VISUAL_STYLE_CONTRACT.md` → "Explorer costume lock"; `STORY_ENGINE.md` §8).
- **CAST-002 — recurring outside "you" figure** (registered in `channel.json` → `cast.core_cast`):
  - silent; never shares a frame with the Explorer (`max_characters_in_frame: 1`);
  - never shown drinking alcohol or smoking (owner on-screen rule, 2026-10-29);
  - one everyman for every episode and pillar, **locked once**: the master is in `locked-references/characters/` and is never regenerated;
  - always narrated as "you", never named aloud, never speaks;
  - generic unbranded wardrobe, restated in every prompt;
  - appears only in outside rows, and only when already present in frame 0.

  See `STORY_ENGINE.md` §9.

## Production-profile note (LTX)

The Explorer (CAST-001), capsule (PROP-001) and "you" (CAST-002) masters in `locked-references/characters/` were adopted from the sibling profile on 2026-10-29 (owner decision) and are the channel masters on both engines. The Explorer/capsule references that LTX EP001 generated for itself are episode-local and are not masters. Later episodes' stills are made at `04f2` under `local_skills/frame0-still-writer/SKILL.md`, conditioned on the masters, never on a text description.
""")

sub_line(BIBLE / "CHARACTER_BIBLE.md", "Allowed: observe, point without touching",
         "Allowed: observe, point without touching, brace during movement, turn toward a process, react with contained surprise and speak "
         "concise questions. Speech is always a voice heard over the helmet radio. While the line plays, the Explorer holds still, "
         "watching, with the visor unchanged. Gestures (lean, helmet turn, pointing, open-palm question) come in the speech-free moments "
         "before or after the line. There is never lip-synced speech, and the face is never shown (`VISUAL_STYLE_CONTRACT.md` voice rule). "
         "Avoid exaggerated comedy, panic, triumph, dancing and direct manipulation of the process.")
sub_line(BIBLE / "CHARACTER_BIBLE.md", "Do not re-anchor from a late generated frame when the master exists.",
         "Do not re-anchor from a late generated frame when the master exists. The channel masters in `../locked-references/characters/` "
         "are the image locks (adopted from the sibling profile 2026-10-29, owner decision); the text specification alone is not an "
         "image lock. LTX EP001's own Explorer/capsule references are episode-local, not masters.")

vsc = rd(MM / "bible" / "VISUAL_STYLE_CONTRACT.md")
costume_why = ("*Why:* a video model can insert an unplanned cut to an Explorer close-up, and without the restatement it redraws a generic "
               "astronaut. The sibling profile saw a stars-and-stripes shoulder patch, a chest emblem and a ribbed helmet band that way "
               "(two published clips). The render negative list carries the drift terms (`channel.json` → `render.negative_prompt_additions`). "
               "Close-ups are zoom-checked at 05a. Full rules: `STORY_ENGINE.md` §8.")
voice_block = """## Explorer identity and voice lock

When the Explorer is visible, the orange pressure suit and white helmet use a continuous uniform black-mirror visor panel of opaque black ceramic glass. Its exterior stays smooth, unbroken, reflective, and visually featureless for the full clip. The capsule canopy may be clear; it remains visually distinct from the Explorer helmet visor.

**Voice rule (owner decision 2026-10-29, after the LTX EP001 pilot; confirmed channel-wide 2026-10-29).** The Explorer's face is never revealed. The visor is never raised, turned transparent, opened or removed. No face, eyes, lips or mouth are ever visible.

The Explorer **does speak**, but only as a **background voice-over**, never as lip-synced on-screen speech:
- The Explorer may be visible while their line plays. The on-screen body performs the line through **body gestures only**: a lean, a head or helmet turn, pointing toward the process without touching it, an open-palm questioning hand, a small brace.
- Give the Explorer lines only in clips where the Explorer is visible, placed before Control's line, with a non-overlapping handoff.
- Control remains an off-screen radio voice.

**Prompt wording.** Whenever a prompt says the Explorer speaks, says or talks, the video model tries to reveal the face or soften the visor to show lips. Write every Explorer line with the proven helmet-radio pattern:

> The Explorer, seated in the capsule behind the canopy, holds still, watching the bottle, the dark visor unchanged, as the Explorer's voice comes over the helmet radio, in a curious, concise adult voice: "…"

- **The body holds still and keeps watching while the line plays.** Gestures belong in the speech-free moments before or after the line, never during it.
- **The voice arrives through a device, the helmet radio.** Always add the same voice description ("a curious, concise adult voice") so the voice stays consistent across clips.
- **Never write that the Explorer speaks, says, talks, asks, replies, answers or narrates, and never mention the Explorer's mouth, lips, face or "closed-mouthed".** When the Explorer is silent, write it as the visor ("the dark visor unchanged" or "sealed").
- **Never copy the script's labels into prompt prose.** The script's "Explorer (background voice-over)" label and its visible-action notes are authoring notes only.
- `pipeline/LTX_I2V_CONTRACT.md` §4 holds the LTX rules for dialogue clips.

*Why:* in LTX EP001, every clip that asked the Explorer to speak turned the visor transparent and rendered a face, a different face each time, while the helmet-radio pattern held. Keep an Explorer-voice clip in each episode's 04h pilot as a regression check.

## Explorer costume lock (from the next LTX episode, adopted 2026-10-29)

These details are locked from `locked-references/characters/` (CAST-001), and **every prompt showing the Explorer restates them positively**:
- the orange pressure suit with dark-grey panels, **plain dark-grey shoulder panels** and grey harness straps;
- the square grey chest unit with a round lens and a glowing cyan light strip;
- the smooth white dome helmet with a **round cyan side light** and an opaque black-mirror visor.

""" + costume_why + """

The recurring outside **"you" figure** (CAST-002, locked in `locked-references/characters/`) gets the same treatment (`STORY_ENGINE.md` §9): plain, unbranded wardrobe, restated in every prompt.
"""
sub(BIBLE / "VISUAL_STYLE_CONTRACT.md",
    "Keep the two in agreement if either changes.\n\n## Scientific visualization is an illustration",
    "Keep the two in agreement if either changes.\n\n" + voice_block + "\n## Scientific visualization is an illustration")

# ---------------------------------------------------------------------------------------------------------------------
# 4. CINEMATOGRAPHY, COMPLIANCE, SCRIPT docs, SCIENCE
# ---------------------------------------------------------------------------------------------------------------------
s = rd(BIBLE / "CINEMATOGRAPHY_CONTRACT.md")
i = s.index("## Production-profile note (LTX)")
wr(BIBLE / "CINEMATOGRAPHY_CONTRACT.md", s[:i] + """## Pacing (from the next LTX episode, `STORY_ENGINE.md` §6-7)

- **A visible change about every 5 s of a 20 s clip**, with no static or unchanged stretch longer than about 5 s. A still process is kept alive with camera travel, flow, the Explorer turning, or a light change, never by morphing the frame-0 object into another state inside the clip.
- **A clip is one continuous take.** The sibling profile's planned cut inside a clip is not adopted; a change of state happens across clips. Any hard cut in a rendered clip is unplanned and is reviewed at 05.
- Describe framing as a still composition, not as "from X up to Y", which a video model can read as a pedestal move.

## Production-profile note (LTX)

This is the same visual grammar as the sibling LTX profile, with the clip unit changed from a fixed 15 seconds to this repo's universal fixed 20 seconds (`channel.json` → `render.clip_duration_seconds`). A whole causal sequence spans more or fewer clips than it would have under the LTX profile; replan clip counts from the 20-second unit, not by porting a LTX shot list.
""")

append(BIBLE / "COMPLIANCE_GATE.md", """## Story-engine additions (`STORY_ENGINE.md` §11, adopted 2026-10-29)

- **Practical sections are explanation, never instruction**, in every pillar (Body: no medical advice; other pillars: no DIY, curing or construction advice).
- Body topics that invite dangerous imitation or unsupervised medical change (for example, day-by-day alcohol withdrawal, breath-holding) need a safety boundary or must be replaced.
- **No real-world insignia on any character.** That includes national flags and mission patches on the Explorer or the "you" figure (two clips of the sibling profile's EP003 shipped one).
- **No on-screen alcohol or smoking** (owner rule, 2026-10-29): never show drinking, smoking, bottles of alcohol or cigarettes. Research and narration about them are fine. When a gate is in doubt, ask "topic or depiction?" first.""")

sb = BIBLE / "SCRIPT_BRIEF.md"
sub(sb, "- Claim and visualization ledgers with direct sources.\n",
    "- Owner-approved `story/coverage-map.json` for coverage-enabled episodes; every in-scope MUST item must be explained, and each deliberate MUST omission needs its exact on-screen disclosure.\n- Claim and visualization ledgers with direct sources.\n")
sub_line(sb, "Explorer asks concise questions or names what is visible.",
         "Explorer asks concise questions or names what is visible, always as a voice over the helmet radio while the visible Explorer holds "
         "still with the visor unchanged (gestures only before or after the line), and only when visible (`VISUAL_STYLE_CONTRACT.md` voice "
         "rule). Control explains one causal step at a time and states important limits. No line may claim an event the shot does not show. "
         "Native LTX-2.5 dialogue must use the approved exact wording within the channel's spoken-word band per clip "
         "(`channel.json` → `render.spoken_word_band`).")
sub(sb, "with time, visible action, claim/visualization IDs, exact dialogue",
    "with time, visible action, coverage IDs, claim/visualization IDs, exact dialogue")
append(sb, """## Story-engine inputs (from the next LTX episode)

The writer receives the confirmed `story/story-definition.md` (`STORY_ENGINE.md` §10) alongside the ledgers. The script must realise its "you" anchor, clock, master metaphor, struggle and breakthrough, objection, practical section and callback on the arc in `STORY_ENGINE.md` §3. Explanation only, never instruction (§11). Metaphors are staged as inside places the Explorer enters, never as outside scenes.""")

sc = BIBLE / "SCRIPT_CRAFT.md"
sub_line(sc, "- Explorer: observation, question, surprise or concise synthesis.",
         "- Explorer: observation, question, surprise or concise synthesis. The Explorer's lines are a voice over the helmet radio, only in "
         "rows where the Explorer is visible, and ahead of Control within a clip. The Explorer holds still, watching, while the line plays. "
         "Mark any body gesture for the speech-free moment before or after the line. The face is never revealed.")
sub(sc, "6. Confirm the hook, title and description can be paid off honestly.",
    "6. Confirm the hook, title and description can be paid off honestly.\n7. For coverage-enabled episodes, confirm each in-scope MUST item has a supported beat and each scoped-out MUST item is disclosed on screen.")
append(sc, """## Story engine (from the next LTX episode)

The story structure follows `STORY_ENGINE.md`: second-person Control narration, the clock as the plot, the arc placed on the clip grid (climax ≈45%, objection ≈55%, practical 70-85%, callback), a master metaphor the Explorer enters, and checkpoint metaphors staged inside. Everything above still applies. Where it conflicts on story shape, `STORY_ENGINE.md` wins.""")

sub(BIBLE / "EPISODE_SPEC.md", "- Mark exact native LTX-2.5 dialogue windows separately",
    "- For coverage-enabled episodes, an owner-approved `story/coverage-map.json`; its in-scope MUST items must map to beat-table rows and supported claims, while out-of-scope MUST items use their verbatim disclosure.\n- Mark exact native LTX-2.5 dialogue windows separately")

sa = BIBLE / "SCIENCE_AND_SOURCING.md"
append(sa, """## Wording follows the evidence level (from the next LTX episode)

| Evidence | Wording |
|---|---|
| Guideline or systematic review | "research shows" |
| Human randomised trial | "in a clinical trial" |
| Observational study | "people who… tend to" |
| Animal or cell study | "**in mice**, researchers found" (name the organism) |
| Contested finding | "scientists still debate…", with both sides sourced |

Every story metaphor (`STORY_ENGINE.md` §5) is logged in the visualization ledger as a metaphor.""")

# ---------------------------------------------------------------------------------------------------------------------
# 5. SEO: timeline test variants, the four-panel thumbnail system
# ---------------------------------------------------------------------------------------------------------------------
seo = BIBLE / "SEO.md"
mm_seo = rd(MM / "bible" / "SEO.md")
sub(seo, "10. A browse variant may emphasize curiosity, but it must retain the primary mechanism or an unambiguous natural variant.\n",
    "10. A browse variant may emphasize curiosity, but it must retain the primary mechanism or an unambiguous natural variant.\n"
    + re.search(r"(?m)^11\. EP004\+ \*\*timeline test variants\*\*.*$", mm_seo).group(0).replace("EP004+", "From the next LTX episode,") + "\n")
new_thumb = between(mm_seo, "The title carries the **mechanism and familiar trigger**. The primary thumbnail",
                    "### Required production-ready thumbnail brief")
old_thumb = between(rd(seo), "The title carries the **mechanism and familiar trigger**. The thumbnail carries the",
                    "### Required production-ready thumbnail brief")
sub(seo, old_thumb, new_thumb)
sub(seo, "Create two materially different concepts before upload.",
    "Create the four-panel causal-ladder primary and one materially different alternate before upload.")
sub(seo, "- [ ] Final thumbnail matches the brief, remains readable at 10% scale and uses no more than three words.\n",
    "- [ ] Primary thumbnail follows the four-panel causal ladder, uses only accepted process states, and shows input → process → outcome.\n"
    "- [ ] Primary transformation phrase uses six or fewer content words; optional context and fixed brand footer follow the documented limits.\n"
    "- [ ] Any primary-layout exception is documented in `metadata/package.md` and owner-approved before upload.\n"
    "- [ ] Final thumbnail matches the brief and remains readable at 10% scale.\n")
sub(BIBLE / "BRAND_ASSET_PROMPTS.md", "- Titles carry the mechanism; thumbnail copy adds at most three words.",
    "- Titles carry the mechanism. Primary thumbnails use the four-panel causal ladder: a six-word-or-fewer transformation phrase, input/trigger, in-process state, and outcome. A three-word context line and the fixed three-word footer are allowed when legible.")

# ---------------------------------------------------------------------------------------------------------------------
# 6. QA_CHECKLIST
# ---------------------------------------------------------------------------------------------------------------------
append(BIBLE / "QA_CHECKLIST.md", """## Story-engine checks (from the next LTX episode, `STORY_ENGINE.md`)

- **05 ingest:** scan every clip for hard cuts (ffmpeg `scdet`, score ≥ 8). Clips here have no planned cuts, so every hit is listed for review.
- **05a:** zoom-check every Explorer or "you" close-up against the locked reference: helmet cyan side light, grey chest unit with cyan strip, plain dark-grey shoulder panels, opaque visor. Call a patch a flag only when it is unambiguous at full resolution.
- **05a / 04h:** check for dead stretches (a visible change about every 5 s) and confirm each clip's beats happen.
- **03b:** the arc lands (hook, struggle, climax ≈45%, objection ≈55%, practical, callback), narration is second person, and the master metaphor is set up and paid off.""")

# ---------------------------------------------------------------------------------------------------------------------
# 7. CHANNEL_SETUP, PILOT_AND_EPISODE_FORMATS, README, LAUNCH_PLAN, 30_DAY_LAUNCH_PLAN
# ---------------------------------------------------------------------------------------------------------------------
cs = BIBLE / "CHANNEL_SETUP.md"
sub(cs, "2. **Inside Your Body** — pillar playlist (created under the LTX profile; shared channel-level asset)\n3. **Inside Materials**\n4. **Inside Manufacturing**\n",
    "2. **[Inside Your Body](https://www.youtube.com/playlist?list=PLBiZcVdqb2Ao)** — live playlist\n"
    "3. **[Inside Materials](https://www.youtube.com/playlist?list=PLf5DDYun02wc)** — live playlist (`PLf5DDYun02wc`, created 2026-10-29)\n"
    "4. **[Inside Manufacturing](https://www.youtube.com/playlist?list=PLT2dw2WV-HmU)** — live playlist (`PLT2dw2WV-HmU`)\n")
sub(cs, "None recorded under this production profile yet. This profile has published nothing; do not carry over the LTX profile's video IDs, schedule dates or playlist-content facts as if they belonged to an episode produced here.",
    """| Destination | URL | Status |
|---|---|---|
| Channel | [@explainedfromwithin](https://www.youtube.com/@explainedfromwithin) | Handle claimed |
| Inside Your Body playlist | [Open playlist](https://www.youtube.com/playlist?list=PLBiZcVdqb2Ao) | Live; holds the sibling profile's EP001 ([How a Platelet Plug Forms Inside a Tiny Cut](https://youtu.be/CSJrzlJenYY)) |
| Inside Manufacturing playlist | [Open playlist](https://www.youtube.com/playlist?list=PLT2dw2WV-HmU) | Live; the sibling profile's EP002 ([How Glass Bottles Are Made: Molten Glass to Bottle](https://youtu.be/85UYUmkiJCU)) is scheduled as its first video. This profile's EP001 ("How Glass Bottles Are Made: Sand to Bottle, From the Inside") is also intended for this playlist; it is not uploaded yet |
| Inside Materials playlist | [Open playlist](https://www.youtube.com/playlist?list=PLf5DDYun02wc) | Live; the sibling profile's EP003 ([How Concrete Hardens](https://youtu.be/hTQf3x9ISRs)) is scheduled as its first video |

Video IDs and schedule dates above belong to the sibling profile's episodes and are recorded as channel facts only. Before each scheduled release YouTube withholds the video metadata from unauthenticated requests, so the owner-confirmed Studio state is the authority. This profile has published nothing.""")
sub(cs, "- [ ] Create the remaining three pillar playlists.\n",
    "- [x] Pillar playlists created: Inside Your Body, Inside Manufacturing, Inside Materials.\n- [ ] Create the remaining pillar playlist: **Inside Technology**.\n")

pf = BIBLE / "PILOT_AND_EPISODE_FORMATS.md"
s = rd(pf)
print("PILOT tail:", s[s.index("This profile's own EP001 topic"):][:200].replace("\n", " "))

rm = BIBLE / "README.md"
sub(rm, "- No Explorer/capsule reference images exist under this profile yet; nothing is promoted to `../locked-references`.",
    "- **Channel masters locked (adopted 2026-10-29):** the Explorer, capsule and recurring \"you\" figure masters are in `../locked-references/characters/` (copied from the sibling profile; hashes in that folder's README).\n"
    "- **Story engine adopted 2026-10-29:** `STORY_ENGINE.md` controls story structure from the next LTX episode on. Only its storytelling logic is taken; the render path (LTX-2.5 i2v, 20 s clips) is unchanged.")
sub(rm, "| Story | `EPISODE_SPEC.md`,", "| Story | **`STORY_ENGINE.md` (controls story structure from the next LTX episode)**, `EPISODE_SPEC.md`,")
sub(rm, "| 00–01 | `NICHE_DECISION.md`,", "| 00–01 | `STORY_ENGINE.md` (§2 anchors, §10 Story Definition Sheet), `NICHE_DECISION.md`,")
sub(rm, "| 02–02b | `SCIENCE_AND_SOURCING.md`, `COMPLIANCE_GATE.md`,", "| 02–02b | `SCIENCE_AND_SOURCING.md`, `COMPLIANCE_GATE.md`, `STORY_ENGINE.md` §5 and §11,")
sub(rm, "| 03a–03b | `SCRIPT_BRIEF.md`,", "| 03a–03b | `STORY_ENGINE.md` (§3-5, §10), `SCRIPT_BRIEF.md`,")
sub(rm, "| 04a–04c | `VISUAL_STYLE_CONTRACT.md`, `CINEMATOGRAPHY_CONTRACT.md`, `AMBIENT_LIFE_CONTRACT.md`, `KEY_CHARACTER_PROMPTS.md` |",
    "| 04a–04c | `VISUAL_STYLE_CONTRACT.md`, `CINEMATOGRAPHY_CONTRACT.md`, `AMBIENT_LIFE_CONTRACT.md`, `KEY_CHARACTER_PROMPTS.md`, `STORY_ENGINE.md` §9 (\"you\" figure) |")
sub(rm, "| 04d–04h | `PRODUCTION.md`,", "| 04d–04h | `STORY_ENGINE.md` (§6, §8), `PRODUCTION.md`,")
sub(rm, "| 05–05a | `QA_CHECKLIST.md`,", "| 05–05a | `STORY_ENGINE.md` §8, `QA_CHECKLIST.md`,")
sub(pf, "Materials, in whatever order `01-ideation` selects. Do not scale a batch from\none episode alone.",
    "Materials, in whatever order `01-ideation` selects. Do not scale a batch from\none episode alone.\n\n"
    "**Status (2026-10-29).** This profile's EP001 (Inside Manufacturing, glass bottles) is closed and awaits owner upload. The channel's other\n"
    "produced topics, on the sibling profile, are the platelet plug (Body), glass bottles (Manufacturing), concrete (Materials) and sleep\n"
    "deprivation (Body). The next LTX episode follows `STORY_ENGINE.md` and picks a topic none of them covers, unless the owner says otherwise.")
sub(BIBLE / "LAUNCH_PLAN.md", "## First episode seed\n",
    "**Status (2026-10-29).** This profile's EP001 (\"How Glass Bottles Are Made: Sand to Bottle, From the Inside\", Inside Manufacturing) is closed and\n"
    "awaits owner upload. The channel now has live pillar playlists for Inside Your Body, Inside Manufacturing and Inside Materials and a story engine\n"
    "(`STORY_ENGINE.md`) that governs the next LTX episode. The text below is the original plan for EP001 and is kept as the record.\n\n## First episode seed\n")
sub(BIBLE / "30_DAY_LAUNCH_PLAN.md", "## Week 1 — topic and pre-production\n",
    "**Status (2026-10-29).** EP001 of this profile has cleared final-package QA and is closed, awaiting the owner's upload and the 48 h / 7 d / 28 d reviews.\n"
    "The weekly list below is the original EP001 plan and is reused for the next episode, which follows `STORY_ENGINE.md`.\n\n## Week 1 — topic and pre-production\n")

# ---------------------------------------------------------------------------------------------------------------------
# 8. channel.json (hand-formatted JSON, so text-level edits; the result is parsed to prove it is still valid)
# ---------------------------------------------------------------------------------------------------------------------
import json

CJ = HERE / "channel.json"
sub(CJ, '"core_cast": ["CAST-001", "VOICE-001"],', '"core_cast": ["CAST-001", "VOICE-001", "CAST-002"],')
sub_line(CJ, '    "reference_status":',
         '    "reference_status": "Channel masters locked (adopted from the sibling profile 2026-10-29, owner decision): Explorer CAST-001, capsule PROP-001 and the recurring outside \\"you\\" figure CAST-002, in locked-references/characters/ (hashes in that README). LTX EP001\'s own Explorer/capsule references are episode-local, not masters. No voice asset is locked.",')
sub(CJ, '    "thumbnail_text_max_words": 3,',
    '    "thumbnail_text_max_words": 6,\n'
    '    "thumbnail_system": {\n'
    '      "default_primary": "four_panel_causal_ladder",\n'
    '      "layout": ["text promise", "input or trigger", "in-process state", "visible outcome"],\n'
    '      "primary_phrase_max_words": 6,\n'
    '      "optional_context_line_max_words": 3,\n'
    '      "fixed_brand_footer_max_words": 3,\n'
    '      "total_visible_text_max_words": 12,\n'
    '      "source_policy": "Use accepted episode scenes or approved stills only. Do not invent a process state in the thumbnail.",\n'
    '      "typography_policy": "Composite text deterministically after image generation whenever possible.",\n'
    '      "exception_policy": "A deviation requires a documented episode-specific reason in metadata/package.md and an owner decision before upload.",\n'
    '      "adopted": "2026-10-29, from the sibling profile (owner: channel-setup changes only)"\n'
    '    },')
sub(CJ, '    "thumbnail_overlay_words_max": 3,',
    '    "thumbnail_overlay_words_max": 12,\n'
    '    "thumbnail_primary_phrase_max_words": 6,\n'
    '    "thumbnail_context_line_max_words": 3,\n'
    '    "thumbnail_brand_footer_max_words": 3,\n'
    '    "thumbnail_default_layout": "four_panel_causal_ladder",\n'
    '    "thumbnail_exception_documentation_required": true,')
sub(CJ, '    "Every central explanatory claim traced to a direct source; an unresolved central claim blocks release."\n  ],',
    '    "Every central explanatory claim traced to a direct source; an unresolved central claim blocks release.",\n'
    '    "No real-world insignia on any character: no national flag, mission patch, shoulder patch, arm badge or chest emblem on the Explorer or the \\"you\\" figure.",\n'
    '    "Never show drinking alcohol or smoking on screen; research and narration about them are allowed."\n  ],')
sub(CJ, '      "bending or drooping machine blades"\n    ],',
    '      "bending or drooping machine blades",\n'
    '      "shoulder patch",\n      "arm badge",\n      "chest emblem",\n      "insignia",\n      "flag",\n      "mission patch",\n'
    '      "ribbed helmet band",\n      "helmet stripes",\n      "visible face behind the visor"\n    ],')
s = rd(CJ)
i = s.index('  "launch": {')
j = s.index('  "bible_documents": [')
wr(CJ, s[:i] + '''  "launch": {
    "status": "ep001_closed_awaiting_upload",
    "note": "This LTX profile's EP001 (\\"How Glass Bottles Are Made: Sand to Bottle, From the Inside\\", Inside Manufacturing) cleared final-package QA on 2026-10-29 and is closed; the owner uploads it. The channel itself is live under the sibling-repo LTX profile, which has produced EP001 platelet plug (Body), EP002 glass bottles (Manufacturing), EP003 concrete (Materials) and EP004 sleep deprivation (Body). The next LTX episode follows bible/STORY_ENGINE.md (adopted 2026-10-29) and picks a topic none of those covers.",
    "candidate_pillars_untested": [
      "Inside Your Body",
      "Inside Materials",
      "Inside Manufacturing",
      "Inside Technology"
    ]
  },
  "visual_identity": {
    "deep_expedition_navy": "#071821",
    "explorer_orange": "#E46F2A",
    "instrument_cyan": "#52D6E8",
    "warm_ivory": "#F2EEE5",
    "signal_amber": "#F0B44D",
    "display_typeface": "Bahnschrift",
    "body_typeface": "Segoe UI"
  },
  "playlists": {
    "pillars": ["Inside Your Body", "Inside Materials", "Inside Manufacturing", "Inside Technology"],
    "shorts": "Process Clips",
    "master_long_form_after_two_episodes": "All Micro-Journeys",
    "live": {
      "inside_your_body": {
        "title": "Inside Your Body",
        "playlist_id": "PLBiZcVdqb2Ao",
        "playlist_url": "https://www.youtube.com/playlist?list=PLBiZcVdqb2Ao"
      },
      "inside_manufacturing": {
        "title": "Inside Manufacturing",
        "playlist_id": "PLT2dw2WV-HmU",
        "playlist_url": "https://www.youtube.com/playlist?list=PLT2dw2WV-HmU"
      },
      "inside_materials": {
        "title": "Inside Materials",
        "playlist_id": "PLf5DDYun02wc",
        "playlist_url": "https://www.youtube.com/playlist?list=PLf5DDYun02wc"
      }
    },
    "pending": ["Inside Technology"],
    "note": "Channel-level destinations, shared by both production profiles. The sibling profile's videos in them (EP001 CSJrzlJenYY, EP002 85UYUmkiJCU, EP003 hTQf3x9ISRs) are channel facts, not this profile's episodes; this profile has published nothing. Source: sibling-repo channel.json, read 2026-10-29."
  },
  "postproduction": {
    "tool": "askyt_editor/run_episode.py",
    "engine": "Remotion + ffmpeg",
    "config_contract": "pipeline/stages/06a-postproduction-assembly.md",
    "episode_local_working_required": true,
    "preserve_native_audio": true,
    "burn_subtitles": true,
    "burn_watermark": true,
    "youtube_studio_watermark_is_canonical": false,
    "watermark_position": "top-left",
    "watermark_size_percent": 8,
    "watermark_opacity": 0.85,
    "youtube_studio_watermark_policy": "disable_when_using_baked_watermark_to_avoid_duplicate_marks",
    "note": "Values match what LTX EP001's 06a already used and the sibling profile's channel.json. First-appearance callouts are per-episode (Remotion text_box labels), not channel-level."
  },
''' + s[j:])
sub(CJ, '    "SCIENCE_AND_SOURCING.md",\n', '    "SCIENCE_AND_SOURCING.md",\n    "STORY_ENGINE.md",\n')
d = json.loads(rd(CJ))
assert d["cast"]["core_cast"] == ["CAST-001", "VOICE-001", "CAST-002"] and "STORY_ENGINE.md" in d["bible_documents"]
sub(CJ, '"reference_bible_note": "Self-contained',
    '"reference_bible_note": "ADOPTION 2026-10-29 (owner): the sibling profile\'s channel-level changes since 2026-10-29 were adopted here -- story engine, CAST-002 and the locked masters, costume/insignia/alcohol rules, four-panel thumbnail system, live playlists, evidence-level wording. Video generation is unchanged (LTX-2.5 i2v, 20 s clips). See CHANGELOG.md. Original note: Self-contained')
json.loads(rd(CJ))
print("adopt: bible + channel.json edits done")
