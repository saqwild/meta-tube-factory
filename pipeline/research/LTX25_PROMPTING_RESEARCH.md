# LTX-2.5 prompting — consolidated research

**Compiled 2026-10-29** for `vidgen-ltx`: Muse Image frame-0 stills + LTX-2.5 i2v.

This file is **evidence**, not doctrine. The binding rules live in
[`../LTX_I2V_CONTRACT.md`](../LTX_I2V_CONTRACT.md) and
[`../MUSE_FRAME0_CONTRACT.md`](../MUSE_FRAME0_CONTRACT.md); this file records *where each of
those rules came from and how strong the evidence is*, so a future agent can tell a vendor
fact from a sibling pipeline's hypothesis without re-doing the research.

---

## 1. Sources, with provenance

| # | Source | Kind | Retrieved | Weight |
|---|---|---|---|---|
| S1 | `docs.ltx.io/open-source-model/usage-guides/prompting-guide` | Vendor documentation | 2026-10-29 (this session) | **Authoritative** on syntax/format |
| S2 | `huggingface.co/Lightricks/LTX-2.5` model card | Vendor spec | 2026-10-29 (this session) | **Authoritative** on geometry/limits |
| S3 | `~/.claude/skills/ltx25-prompting/` (SKILL.md + references/) | In-house vendor-syntax skill | read 2026-10-29 | Derived from S1/S2; used as the post-hoc conformance checker |
| S4 | `C:\pycode\codex-grumpy\rules\prompt\channel_prompt_constraints.md` §9, §9a–9d | Sibling-pipeline doctrine | read 2026-10-29 | **Production craft**, see §4 caveat |
| S5 | `C:\pycode\codex-grumpy\research\ltx_2_5_prompting_audit_2026-10-29.md` | Sibling-pipeline audit | dated 2026-10-29 | Same sources as S1–S2, four days older |
| S6 | `C:\pycode\vidgen-dist\app\config.py`, `app/batch.py`, `workflows/` (the app now lives at `C:\pycode\app-vidgen-dist`) | The actual render app | read 2026-10-29; `batch.py` re-read 2026-10-29 | **Ground truth** for what we can render |
| S7 | Cut Plane pilot-readiness tests (`channel_profiles/cutplane/bible/TEST_RESULTS.md`) | Real LTX-2.5 renders on `app-vidgen-dist` | run 2026-10-29 | **Render-validated**, one test profile; see §7. The cutplane profile was removed from this repo 2026-10-29 — §7 is the retained record |

**S1/S2 were fetched live in this session**, not taken from S5's summary of them. Where S5 and
S1 disagree, S1 wins and the difference is noted below.

---

## 2. Vendor facts (S1, S2) — these are not negotiable

### Architecture
LTX-2.5 uses a **custom Gemma-4-12B text encoder with projections**, explicitly designed to
"hold complex prompts together (multiple characters, camera moves, lighting, actions) instead
of dropping details" (S2). It ships a **native audio VAE + vocoder** — video and audio are
generated together and synchronised, from text, image, or video input.

Two consequences that drive this whole conversion:

1. **There is no documented LTX-2.5 PromptRelay node or vendor timing control.** LTX-2.3's
   `GLOBAL::` / `BEAT:: <frames> ::` node format (ComfyUI-PromptRelay) has *no LTX-2.5 graph
   equivalent*; the encoder reads one continuous prompt and there is **no native per-second
   timing control**. **However**, this pipeline still authors clip prompts in the
   `GLOBAL::` / `BEAT:: <frames> ::` *syntax* as an owner-locked model-facing pacing convention
   (`render.prompt_format == "prompt_relay_beats_v1"`), adopted 2026-10-29 from the
   `vidgen-codex-ltx` sibling where a 20-second LTX-2.5 render of the beat form beat the
   regular-prose alternative — **local empirical result, not vendor timing evidence.** The
   frame labels are passed through the current graph unchanged; ordering inside a beat still
   comes only from chronological connective language. See `../LTX_I2V_CONTRACT.md` §Scope.
2. **Audio is prompted, not attached.** Ambient sound, foley, music intent and spoken
   dialogue are all described in the same prompt body. Dialogue goes in quotation marks;
   specify language/accent where it matters.

### Geometry and duration (S2)
```
width  % 32 == 0
height % 32 == 0
num_frames % 8 == 1          # 1, 9, 17, … 121, … 481
fps = 24
recommended stage-1 resolution: 544x960; stage 2 runs at 2x stage 1
```
`num_frames = 1 + 8k` is the constraint that makes 20 s at 24 fps land on **481 frames**
(`1 + 8x60`, `(481-1)/24 = 20.0`). LTX-2.5 also ships an optional **duration-predictor node**
that infers length from the prompt when a frame count isn't supplied — a *generation setting*,
not a prompting technique, and not in use here (our graph sets duration explicitly).

**Never write duration, fps, aspect ratio, resolution, or the model name into the prompt
text** (S1, S3). Those live in the graph; in the prompt they are dead tokens at best and
misleading ones at worst.

### Required prompt elements (S1, verbatim structure)
1. **Establish the shot** — cinematography terms matching genre; shot scale.
2. **Set the scene** — lighting, colour palette, surface textures, atmosphere.
3. **Describe the action** — one sequence flowing naturally start to finish.
4. **Define the character(s)** — age, hair, clothing, distinguishing features; emotion
   expressed through *physical cues*, never abstract labels ("sad", "confused").
5. **Identify camera movement(s)** — how and when it moves, and **how subjects look *after*
   the move**, so the model can complete the motion accurately.
6. **Describe the audio** — ambient, music, speech; dialogue in quotation marks.

### Length (S1)
- Single continuous take: **roughly 4–8 descriptive sentences**, present tense, one flowing
  paragraph.
- Screenplay-style (dialogue-heavy or multi-beat) **may exceed that**, "provided every
  sentence adds concrete visual or audio detail."
- S1 states **no hard word ceiling.** The 200-word figure in S4/S5 was LTX-2 era guidance
  carried forward, not an LTX-2.5 vendor limit; **retired from the contract 2026-10-29** — see
  §4. The validator keeps only a 450-word runaway tripwire (`LTXV-D004`) against prompt bloat.

### Multi-shot (new in 2.5, S1)
LTX-2.5 can generate several shots joined by explicit cuts inside one prompt. Written as one
chronological paragraph — never a shot list or numbered beats. At **every** cut you must
include: the transition named in natural language; the new shot re-established (scale, angle,
who is in frame, lighting if changed); consistent identity re-stated for anything recurring;
and **explicit audio continuity** ("the synth score continues across the cut").

Prefer **2–4 shots** per generation.

> **For i2v this is off by default.** S1 is explicit: *"For image-to-video from a first frame,
> prefer a single continuous take unless you intentionally describe a cut away from that
> opening image."* Multi-shot is the option for when the clip is *meant* to leave the
> conditioning frame behind. This pipeline's default is one continuous take per clip.

### i2v specifics (S1, S3)
- The conditioning image is the **visual anchor**; the prompt describes what happens *from* it.
- **Do not describe the input image in depth** — write the new motion, performance, camera and
  audio, not an inventory of what is already visible, unless a visible detail must change.
- Author the opening clause to match **what the image actually shows**, not a planned pose.

### Stated limitations (S1, S2)
- **On-screen text:** short-text accuracy and cross-frame consistency improved in 2.5, but
  exact spelling is **still not guaranteed**. Keep in-scene text short and prominent; put
  critical titles/labels/logos in post.
- **Complex physics:** highly chaotic motion still produces artifacts. Prefer simpler,
  plausible motion — especially multi-subject or fast-twisting action.
- Negative prompting: a default negative prompt exists in the Diffusers implementation;
  `guidance_scale` and `audio_guidance_scale` are separate controls. **The negative channel is
  real on LTX-2.5** — which is why suppression belongs there and never in the positive.

---

## 3. What the render app can actually do (S6) — ground truth

Verified by reading `vidgen-dist` source, not its README (which still describes the retired
2.3 relay app and is stale).

```
workflow : workflows/LTX25_T2V_I2V_Two_Stage_Distilled.json   (2.3 relay graphs archived
                                                               under workflows/legacy_2.3/)
megapixels        0.98   -> 1344x768, 16:9, 64-clean on both axes
fps               24
duration          20     SECONDS; the graph computes 1 + floor(fps*duration/8)*8 internally
cfg (base)        1.0    LTXVDualCFGGuider.video_cfg
cfg_refine        1.0
cfg_audio         1.0
img_compression   18     LTXVPreprocess — the causal lever against invented characters
steps             inert  (distilled model uses fixed ManualSigmas schedules)
lora_strength     inert  (no LoraLoaderModelOnly node in this graph)
```

This table is `vidgen-dist`'s shipped app default (`app/config.py`), not a claim that every channel
renders at these numbers. `signed-anyway` overrode `cfg` and `img_compression` to 1.2 / 22 after
EP001 (see `channel_profiles/signed-anyway/channel.json` → `render.cfg_note` /
`img_compression_note`, and open question 4 below) — a channel's own `channel.json` is
authoritative whenever it states a render-validated value different from this baseline.

**Batch ingest contract** (`app/batch.py`) — this is exactly what stage `04g` must emit:
- a **`master-prompt.txt`** containing `@@ s{n}` section markers, one per clip. `@@ i{n}`
  markers also act as boundaries and are skipped. A leading line consisting only of
  `[[TAG]]` tokens is stripped before the prompt reaches LTX.
- a **folder of stills**, matched to `@@ s{n}` by the scene number that **prefixes** the
  filename stem (`image1`, `sc01`, `s01_v2` all resolve to n=1; a suffix never identifies the
  scene). An unrecognised name is skipped and reported; two files with the same number make
  that scene ambiguous and it is not rendered. *(Corrected 2026-10-29 by re-reading
  `C:\pycode\app-vidgen-dist\app\batch.py` `_scene_number()`; the 2026-10-29 reading described
  an earlier last-digit-run matcher with tie-breaking, which the app no longer uses.)*

Two constraints this places on the pipeline:

- **Duration is a global app setting, not per-clip.** Locked to **20 s for every clip on both
  channels** by owner decision, 2026-10-29. See the override note in each `channel.json`.
- **Aspect is fixed 16:9** by the graph's `ResolutionSelector`. 9:16 Shorts are produced as a
  post-production reframe of the same 16:9 footage, never a separate still/clip batch
  (owner decision, 2026-10-29).

---

## 4. Sibling-pipeline craft (S4, S5) — useful, but grade the evidence

`codex-grumpy`'s `channel_prompt_constraints.md` is the most developed LTX prose doctrine
available locally, and most of it is imported into `LTX_I2V_CONTRACT.md`. But it carries a
warning **in its own header** that must not be laundered away in the port:

> "This channel has NOT rendered anything yet. Every 'render-validated' claim below is
> evidence from claude-shorts' own EP001–EP009 production … not from this channel."

and

> "This file itself was already found to carry cross-pipeline contamination even in
> claude-shorts' own copy."

So findings arrive here in three grades, and `LTX_I2V_CONTRACT.md` marks each one:

**Grade A — vendor-confirmed (S1/S2).** No relay syntax; no timing markers; dialogue in
quotes; camera movement plus post-move appearance; audio described explicitly; i2v prefers a
single take; don't inventory the conditioning image; no duration/aspect/fps in text; on-screen
text unreliable; chaotic physics unreliable.

**Grade B — render-validated on a sibling under LTX-2.3, model-agnostic in nature.** These are
about *how a video model reads language*, not about 2.3's segment encoder, so they transfer:
- Positive-text negation backfires — the model renders the tokens it sees. A "no captions,
  no subtitles" clause **causes** burned-in subtitles. Suppression lives only in the negative
  node. (Corroborated by S1's own positive-framing guidance and by the Muse Image guidance
  that "empty street" beats "no cars".)
- A labelled `Spoken dialogue:` block reads as a caption track and triggers burned-in text.
  Fold dialogue into the character's action instead.
- Ending on a frozen held pose makes the model fill dead air by repeating the last line — every
  clip needs a *productive tail*.
- A clip that names no continuing ambient sound invites the model to invent dialogue to fill
  silence.
- Unaccounted-for on-screen characters get animated wrongly (the wrong mouth moves). Every
  non-speaking visible character needs an explicit closed-mouth/reaction clause.
- The first and last sentence must name the character as grammatical subject, or the clip
  spawns extra characters or drifts the camera off the subject.
- Bare species/role words for background extras ("neighbours", "kids") render as photoreal
  humans — always state "anthropomorphic animal" explicitly where that's the intent.
- Concrete photographable verbs only; LTX is a literal reader ("catches her eye" → a literal
  grab).

**Grade C — LTX-2.3-era numbers, explicitly unproven on 2.5.** Carried as the safe default,
flagged `[2.3-RETEST]`, never presented as fact:
- ~~180-word soft / 200-word hard prompt ceiling.~~ **RETIRED 2026-10-29.** S1 sets no
  ceiling and S2 says the encoder is *built* to hold long prompts; the number was LTX-2-era
  guidance from S4/S5, not a 2.5 rule. `LTX_I2V_CONTRACT.md` no longer carries a word ceiling.
  `LTXV-D004` is now a runaway tripwire at 450 words (bloat/inventory catch only), not a limit.
  Open question 1 below is rescoped from "does 200 hold" to "is a dense prompt delivered as
  cleanly as a lean one".
- "Repeating a full room inventory materialises or duplicates props."
- "At most one prop action per clip."
- The destructive/transformative-event rule (state-not-transition, split across two clips).
- `[VSTYLE] Low motion.` — a seed-pinned A/B/C test on 2.3 found this token **inert**. It is
  not an LTX-2.5 authoring requirement. Do not append it; describe the exact plausible motion
  wanted instead.

---

## 5. Where S5 (the 2026-10-29 audit) and S1 differ

| Claim in S5 | Status against S1/S2 today |
|---|---|
| "Keep the full prompt at or below 200 words" | **Not a vendor rule — retired 2026-10-29.** S1 gives 4–8 sentences for single-shot and explicitly allows longer for dialogue-heavy scenes; S2 says the encoder is built for long prompts. No word ceiling in the contract; `LTXV-D004` is a 450-word runaway tripwire only. |
| "one chronological, present-tense, 4–8-sentence prompt" | **Confirmed** by S1 for single-shot. |
| "the render graph, not the prompt text, owns duration/fps/aspect/resolution" | **Confirmed** by S1 and by S6. |
| "481 frames = 20 s at 24 fps" | **Confirmed** arithmetic against S2's `num_frames % 8 == 1`. Note `vidgen-dist` computes this internally from a seconds value — do not hand-enter frame counts. |
| Ingredients IC-LoRA reference-sheet workflow | Real, but **not the path this pipeline uses.** Our identity lock is Muse Image's `--ref-asset` at still-generation time; by the time LTX runs, identity is already baked into the approved frame-0 pixels. |
| "Prompt Enhancer is optional; A/B it as a single variable" | Sound method. Not wired into `vidgen-dist`'s current graph — treat as a future test, not a current control. |

---

## 6. Open questions — test before trusting either way

EP001 (signed-anyway) rendered a full 29-clip LTX-2.5 batch on 2026-10-29 and settled
question 4 below (struck through). The remaining questions are still open — one low-motion
dialogue episode does not answer them. These are the tests worth spending the next pilot batch
on, in priority order. Record verdicts in `LTX_I2V_CONTRACT.md`, not here.

1. **Prompt density, not length.** The word ceiling is retired (§4, §5), so the question is no
   longer "does 200 hold". Take the densest real clip (~300–330 words, every anchor load-bearing)
   and a lean rewrite of the same beat, render both at the same still and seed, and confirm the
   dense one is delivered as cleanly — same adherence, no dropped audio or camera move. If it is,
   nothing more to do here. If dense prompts degrade, the fix is tighter prose, not a word cap.
2. **20 s dialogue occupancy.** At the planning pace, a 20 s clip carries roughly 30–33 spoken
   words. Confirm the model actually delivers that in 20 s rather than rushing or padding —
   this is the number the whole scene-word-budget depends on and it has never been measured
   on 2.5.
3. **Multi-speaker mouth binding.** The single-speaker mouth-lock clause is Grade B mitigation
   for a 2.3-era failure. Verify it still earns its words on 2.5's decoder.
4. ~~**`img_compression 18`.** Validated as the anti-invented-character lever on 2.3 and
   carried into the 2.5 graph unchanged (S6). Confirm on real 2.5 output.~~ **CONFIRMED on
   real 2.5 output, 2026-10-29 (EP001).** The lever still behaves as documented — raising it
   to 22 (from the untested 18 default) measurably reduced unrequested model-added movement
   across a full 29-clip batch, with no adverse side effect observed. `channel_profiles/
   signed-anyway/channel.json` now carries 22 as its validated default. Same episode also
   found the CFG-vs-artifact tradeoff empirically: base-pass cfg 1.5 produced visible extra
   smoke off a practical lamp; 1.2 rendered clean. Both promoted to **[B]**.
5. **Frame-0 adherence.** How literally does 2.5 honour the conditioning frame? This sets how
   strict `04f2`'s still gate has to be.
6. **Destructive/transformative events** (Grade C, §4). Most expensive rule in the set — it
   spends a whole extra clip every time it fires. Worth one deliberate test.

---

## 7. Retained findings from the removed Cut Plane test profile (S7)

`channel_profiles/cutplane/` was a no-cast factual channel profile that never produced an
episode; it was removed on 2026-10-29. Its 2026-10-29 GPU tests are real LTX-2.5 evidence that
other profiles' notes cite, so the findings are kept here. Settings for every test:
`app-vidgen-dist`, `ltx-2.5-22b-distilled-transformer-bf16`, 8 steps, LoRA 0.5, two-pass,
1344x768, 24 fps, 20 s, **CFG 1.0 on both passes**.

- **Native in-clip narration works and holds voice identity.** Two seeds, identical prompt:
  the quoted line was recited word-perfect both times, including a number, and median F0 was
  124.0 vs 122.1 Hz — one speaker. Measure pitch on the isolated voice, not the mixed track: a
  first pass on the mix mistook different machine ambience for a different voice.
- **Negatives were inert at CFG 1.0 distilled.** Constraints that must hold go in the positive
  prompt. Untested at the CFG 1.2 base pass that signed-anyway, clover-and-paws and
  inside-the-process use — do not generalise past CFG 1.0 without a test.
- **The beat packet drives material motion**, and colour identity must be restated in
  `GLOBAL::` *and* every `BEAT::` or the material drifts mid-clip. Describe the physics as the
  material *becoming* the new state, not moving over an existing one.
- **`BEAT::` weights are proportional and normalised** by the app — one positive number, never
  a range (bare = frames, trailing `s` = seconds). Text after a `BEAT::` joins that beat; the
  style echo belongs in `GLOBAL::`.
- **No audio stems.** One stereo AAC stream; continuous room tone is what hides clip seams.
- **`img_compression` 20 vs 18, seed-matched:** no colour change and nothing invented at either;
  the divergence grew with time (seed-path drift), not compression.
- **A narrated clip reached 495 words**, over the 450-word `LTXV-D004` tripwire. A
  narration-heavy channel may need that tripwire raised on evidence, not by default.
