# Import note — Clover & Bruno Stories profile

**Imported 2026-10-29** from `C:\pycode\clover_and_paws\channel_profile`, on the owner's
instruction that this profile and `signed-anyway` are the two that belong together in this repo.

**42 files, byte-identical at import**, verified with `diff -r`. Nothing was reorganised,
renamed, summarised or dropped.

Then two **standing repo-wide corrections** were applied — the same two already applied to
`signed-anyway`'s bible — because leaving them would have put this profile in direct conflict
with `channel.json` and with the render stack. Everything else is untouched.

## What changed, and why

**1. Retired render engine → LTX-2.5.** The profile named a previous engine in nine places. Most
were historical "the old split is abandoned" notes, which would have been harmless. One was not:

> `CHARACTER_BIBLE.md` locked that engine as **"the single unified engine for all 7 performers"**
> — a live instruction, not a historical note, directly contradicting this repo's stack.

`KEY_CHARACTER_PROMPTS.md` §5 also specified a **six-section prompt format** with `<Subject N>`
labels, `<Picture N>` anchors and `(S1)`/`(S2)` speaker IDs. That format has no equivalent here:
LTX-2.5 reads one continuous prose prompt with no sections, no labels and **no timing syntax at
all**. It was rewritten as a clip-prompt contract pointing at `pipeline/LTX_I2V_CONTRACT.md`,
**keeping every channel-specific rule it carried** — the chore/prop business, Clover's polite
register, Bruno's No-before-yes, the named sound bed (tap drip, porch creak, bag rustle,
birdsong), and the music policy. The old §6 subject-definition compiler became a short character
anchor compiler, because under image-to-video identity is carried by the approved frame-0 still
rather than by a re-description in the prompt.

**2. Clip duration → fixed 20 seconds; render aspect → 16:9.** The profile specified an 8–15
second performance unit and 9:16 Shorts. Both are owner decisions of 2026-10-29 that apply to
every channel in this repo: `vidgen-dist` takes duration as one global app setting, and the
proven LTX-2.5 graph is fixed-aspect 16:9.

The **Short survives as editorial intent** — 160–180s remains the target and it is still a growth
driver. It is now produced as a **post-production reframe of the same 16:9 footage**, never a
separate still batch, clip batch or render aspect. `VISUAL_STYLE_CONTRACT.md`'s 9:16-safe
composition note became a instruction to keep the subject clear of the left and right thirds
wherever a Short will be cut from that clip.

## 3. Rigid character rules loosened into defaults (owner decision, 2026-10-29)

Surfaced by an early clover-and-paws script's independent review (in the source repo), which
correctly failed the script for breaching two rules — and in the process exposed that the rules
themselves were the problem.

**The owner's ruling:** a supporting rule that fires identically in every episode makes the
channel predictable, which is exactly the failure the five-arc rotation exists to prevent. Let
the story drive staging.

Changed from laws to **defaults** across 16 files:

| Was | Now |
|---|---|
| "Clover NEVER appears without at least one parent. No solo Clover episodes." | Usually appears with a parent, often both — depart when the story is better for it |
| "Bruno MOSTLY appears with Pip. 80% of appearances." | Usually with Pip; solo Bruno is legitimate when the story wants him unwitnessed |
| "Pip never sides against Bruno in first beat, always supports Bruno's grumble, then nudges" | Loyal to Bruno, and that is his most natural move — but a tendency, not a script |
| "Clover never raises voice, never insults Bruno" | Politeness is her register, not an absence of range: she may be disappointed, frustrated or wrong |

**What is still forbidden is deviation by accident.** A departure from a default must be stated
and reasoned in the episode's cast snapshot at `03a-writer`. An unremarked departure is a defect.

Two things were deliberately **not** loosened, both clarified by the owner on the same day:

- **Bruno's Never-Yes-First is retained — and it is *character*, not a gag.** The owner's
  framing: he is seventy, retired, experienced, and arrogant enough to want to seem apart from
  all this, so agreeing straight away would cost him the version of himself he presents. That
  reframing matters more than it looks. A rule justified as "the channel's promise" invites
  literal repetition; a rule that falls out of who someone *is* leaves room inside it. The
  refusal is inevitable; **the excuse should change every episode** — the retirement line, the
  back, the not-my-business, the counter-complaint. A Bruno reaching for the identical excuse
  every time is written as a mechanism, not as a seventy-year-old with opinions.

- **Rosa and Mimi are not peers.** **Rosa (CAST-002) is a main character** — Clover's mother,
  core household, in most episodes. **Mimi (CAST-006) is supporting** — Street Recurring, appears
  only when a story needs her. Keeping them behaviourally distinct (Rosa steady, Mimi spirals) is
  a differentiation rule rather than a predictability trap, and Mimi must never quietly absorb
  Rosa's role in a scene.

### ⚠ Public-facing copy deliberately left alone

`bible/channel.json` → `channel.description` is the **live YouTube About text**, and it still
reads *"always comes with Mama Rosa and Papa Fin."* That is now inaccurate against the doctrine.
It was not edited here because changing published channel copy is a publishing decision, not a
doctrine one. The same phrasing appears in `SEO.md` and `README.md`'s audience-promise rows.
Raise it with the owner before touching any of them.

## 4. Environment library gained the Finn front porch (owner-approved, 2026-10-29)

Surfaced by an early clover-and-paws `04a-visual-brief` (in the source repo): the library
covered the Finn **kitchen** and **living room**, Bruno's porch, Paw Street, the shop and the
park — but not the Finn family's outdoor **front**, where much of that episode happened.

That was not cosmetic. Every clip prompt must name an `Acoustic environment:`, so four clips had
no canon sound source and would each have invented their own, drifting apart across the episode.

Added to `AMBIENT_LIFE_CONTRACT.md`, between the living room and Bruno's porch:

> **Finn Front Porch / Path** — background life: laundry line stirring, a watering can by the
> step, the bike's usual spot under the steps, curtains at the front window. Diegetic sound:
> birdsong, light breeze, leaves rustling on the path, a screen door on a spring. Avoid: traffic,
> voices from off screen, anything implying a neighbour who is not on camera.

The "avoid" column carries the channel's safety floor into sound: an off-screen voice or a
passing car implies a character nobody drew, and on this channel an unqualified figure renders as
a photoreal human.

## 5. Designated pilot changed (owner decision, 2026-10-29)

`PILOT_AND_EPISODE_FORMATS.md` names *"Polite Clover Asks Grumpy Bruno to Fix Her Bike - He Says
No At First"* as the pilot, in Example A and in the "Pilot role and validation" section;
`ADVENTURE_ARCS_LOCKED.md` Arc A and `SEO.md` candidate #1 carry the same premise.

**That premise is retired as the pilot.** It was built to ~`04f` twice — once in an earlier
`clover-and-paws` attempt, once as the source repo's `EP001` line — and nothing shipped from
either. The channel's first episode produced in this repo is instead:

> **EP001 — "Mama Cat's Birthday Swing"** (`episodes/clover-and-paws/EP001/story/premise.md`).
> Arc A (Cozy Home), Duo / Clover-led, Long ~9:30. Clover wants Mama Rosa's long-broken porch
> swing mended and repainted as a birthday surprise; one seized eye-bolt is beyond the home
> tools; Bruno's No is *"that's a husband's job — on my knees in the dirt at seventy"*; Fin
> strips the bolt trying alone; Bruno comes over with his old coffee-can of bolts and a
> stripped-bolt trick the young ones don't know.

The locked-doc bodies are **not** edited (the bible is immutable and the import is verbatim);
this note is the supersession of record. Every job the pilot exists to test — polite-vs-grumpy
read by 0:45, Never-Yes-First with a *fresh* excuse, full 5-core Duo, warm shared payoff — is
carried by the new premise, and its gate self-score is 15/16.

## 6. Safety floor reconciled with the action arcs (owner decision, 2026-10-29)

`channel.json → hard_safety_floor` read *"No peril, danger or scares — the worst outcome is a
setback, a mess, or a plan going wrong."* `ADVENTURE_ARCS_LOCKED.md` (LOCKED 2026-10-29) defines
Arc B (Stand Tall — bad guys, Papa Fin pushed down, Bruno stands shoulder-to-shoulder) and Arc C
(Rescue Dash — a tree starting to fall, a cart rolling, a kitten stuck) with their own
"Compliance for Action" limits. The two were in direct conflict.

**The owner's ruling: the action arcs win, within their own stated limits.**
`channel.json → hard_safety_floor` item 3 was rewritten to:

- **Arc A, Arc D, Arc E and all Clover-only / Bruno-only content:** no peril at all — the worst
  outcome is a setback, a mess, or a plan going wrong. (Unchanged intent.)
- **Arc B and Arc C only:** bounded, non-graphic jeopardy, strictly under
  `ADVENTURE_ARCS_LOCKED.md` "Compliance for Action" — no graphic violence (push, block, stand
  tall; never a punch or blood), no weapons, antagonists faceless / non-speaking / two-to-three
  / they leave rather than are beaten, every rescue resolves safely (the tree falls away, the
  cart is stopped, no character is actually hurt), Clover is never in danger alone, spy arcs stay
  comedic and daytime.

`02b-compliance` reads the reconciled `channel.json` line; the arc doc is the detail it points
at. EP001 is Arc A, so this does not touch it.

## 8. Mimi Tier-0 identity figure added (owner-placed, 2026-10-29)

`CAST-006` Mimi had no **Tier-0 bare identity figure** — only her composed
`reference_sheets/mimi_sheet.jpg`, which the tier rules forbid conditioning on. EP001 is the
first episode to use her, so one was built (via `muse-image CLI`, conditioned on nothing, gated by
eye against `CAST-006_MIMI.md` — grey tabby / hazel eyes / worried-kind brow / grounded adult
build / clearly not Rosa) and the owner placed it:

> `bible/characters/identity/mimi_identity.jpeg` — SHA-256
> `620e5d60fdb51106a3c9a10fb34719cedb6a430b7c8975940dc0215bbaf2b1cd`, 2752×1536. A single bare
> undressed figure; the round tortoiseshell glasses pushed up on her head are kept as her
> permanent identity anchor.

This fills a gap in the channel masters, consistent with the other six identity figures already
in `bible/characters/identity/`. `CAST-006_MIMI.md` §5's asset table still lists only the
composed sheet + voice — the same shape as every other card's §5, which predates the
`identity/` folder; a `mimi_identity.jpeg` row can be added there when the cards are next
revised. Generation detail: `episodes/clover-and-paws/EP001/visual/references/manifest.md`.

## 7. Source repo is superseded — this repo is the sole production flow (owner decision, 2026-10-29)

Section 9 below ("Relationship to the source repo") left open whether
`C:\pycode\clover_and_paws` was superseded. **The owner has now decided it is.** Clover & Bruno
Stories is produced here, in `vidgen-ltx`, on the same pipeline that shipped
`signed-anyway` EP002. The source repo's own episodes (`EP001` "Paw-Man Kite Rescue", `EP002`)
are not migrated and are not resumed. Its `channel_profile/` remains the deeper verbatim
identity record (imported here 2026-10-29); nothing in it is read by this pipeline.

## Files that differ from the verbatim source

```
CHARACTER_BIBLE.md          engine lock
CINEMATOGRAPHY_CONTRACT.md  performance unit, shot-unit template
COMPLIANCE_GATE.md          performance unit
EPISODE_SPEC.md             performance unit, Shorts aspect, audio note
KEY_CHARACTER_PROMPTS.md    prompt format (§5, §6)
NICHE_DECISION.md           engine reference
README.md                   production core row
SCRIPT_CRAFT.md             clip word budget
VISUAL_STYLE_CONTRACT.md    9:16-safe composition note
channel.json                engine note, aspect, clip duration
channel_profile.md          engine reference
```

The other **31 files are exactly as imported**, including all seven `characters/CAST-00*.md`
master cards, all seven locked reference sheets, and every brand asset.

## What is NOT read by this pipeline

`bible/channel.json` is the **source repo's own** profile schema (`schema_version: 2.0`, with
`positioning` / `brand_assets` / `cast_system` / `playlists` / `visual_identity` blocks). It is
retained as part of the faithful import and as the deeper identity record, but
`tools/preflight.py` and every stage contract read
**`channel_profiles/clover-and-paws/channel.json`** instead — this repo's own schema. Where the
two disagree on a render number, the outer one wins; that is the rule in `AGENTS.md`.

## Relationship to the source repo

`C:\pycode\clover_and_paws` still exists and has its own episodes (EP001 "Paw-Man Kite Rescue",
EP002). The import itself copied the channel's identity only. **The owner has since made the
call: that pipeline is superseded and this repo is the sole production flow — see §7 above.**
Those episodes are not migrated and not resumed.
