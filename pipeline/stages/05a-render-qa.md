# 05a — render QA

## Inputs

`renders/render-manifest.json`, the actual render files it points to, `visual/shot-plan.md` and
`_context/blocking.json` (what each clip was supposed to show), and the approved stills at
`renders/stills/`.

## Task

Run the mechanical pre-check before the human review below:

```
python tools/render_audio_audit.py --channel <slug> --episode EPxxx --emit-review
```

`render-manifest.json`'s own checks (`05-render-ingest`) verify duration, resolution, hash and
whether audio is present/silent — never that the clip's actual spoken audio matches the dialogue
it was rendered from. This transcribes every clip and diffs it against its approved quoted line
in `7-video-prompts.md`. It exists because that exact gap let a real defect through on EP001: two
clips passed every structural check clean while carrying a *different episode's* dialogue,
undetected until someone happened to listen. A `FAIL` here is a wrong-content clip, not a
beat-adherence judgment call — resolve it before spending time on the qualitative review below.

Beyond the word-similarity score (which screens for a wholesale wrong-clip swap) each dialogue
clip also gets a structural check: the negation multiset and any spoken digit figures must match
the approved line. A one-word polarity flip ("did not authorize" → "did authorize") scores ~0.9
on similarity but FAILs here — the `reasons` field on a failing clip names which structural check
tripped.

Human QA of the full batch, against **beat adherence** — not a vague "does it look right".

For each clip: **did the named action actually happen?** Name the action from the clip's
`anchors` and say whether it occurred. Aggregate motion, general liveliness and file size are
not evidence in either direction. This is the single check that has historically been fudged
into meaninglessness, and it is the reason this stage exists.

Then, per clip:

- **Frame-0 fidelity** — the clip starts from its approved still without drifting or re-staging.
- **Cast and environment drift** against the locked references from `04b`/`04c`.
- **Speaker binding** — the right mouth moves; non-speakers stay closed.
- **Audio** — dialogue audible and authorised, the named ambient bed present throughout, no
  invented speech in the tail. `render_audio_audit.py` above catches wrong-content dialogue
  mechanically; this bullet is the qualitative listen it doesn't replace (authorisation, ambient
  bed, tail content).
- **Artifacts** — no burned-in captions or model-rendered text, no anatomy failures, no
  duplicated props or characters.
- **Continuity across the cut points** — a continuing character is where the previous clip's
  `end_state` left them.

For `inside-the-process`, also judge every inside clip against "inside means inside" (`bible/VISUAL_STYLE_CONTRACT.md`): the camera is in the named interior, not looking at a digital or see-through model of it from outside, unless the clip is a declared locator.

## Output

`episodes/<slug>/EPxxx/qa/render-qa.md` — per clip, `PASS`/`FAIL` with the **specific** beat or
drift that failed. "Feels off" is not a finding; name the action or the anchor. Plus
`renders/audio-content-audit.json` from `render_audio_audit.py --emit-review`.

The file ends with one stage verdict line, exactly `**STAGE VERDICT: PASS**` or
`**STAGE VERDICT: FAIL**` — PASS only when every clip passes. The completion gate
(`pipeline/stage-gates.json`) reads the **last** such line, so a re-render round is recorded by
appending a new round and a new verdict line, never by editing the old one.

## Stop condition

A `FAIL` clip returns to whichever stage owns the fix — `04f3`/`04f` for a prompt problem,
`04f2` for a still problem, `04d` if the geometry was wrong, or a straight re-render at `04g`
where the prompt and still were both right and the render simply lost the roll.

A failure that recurs across clips is a **rule**, not a one-off patch: write it into
`pipeline/LTX_I2V_CONTRACT.md` with its evidence grade, add a validator rule and a test if it
is mechanically checkable, and say so here.
