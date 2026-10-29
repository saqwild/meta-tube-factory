# 02 — research

## Inputs

`story/premise.md`.

## Task

Gather whatever supporting material the premise needs to be specific instead
of generic — for Signed Anyway that's plausibility research on the financial
mechanism named in the premise; for Clover & Bruno Stories that's the concrete
chore, errand or wish the episode turns on, and the specific street detail that
makes it theirs — a plotless "cute animals doing things" compilation is a
research failure, not a style choice. Public web reading is allowed here (and in
`02a-sourcing`, and in `inside-the-process`'s `01b-coverage-scan`) and nowhere else in the
pipeline.

For `inside-the-process`, research is driven by the owner-approved `story/coverage-map.json`,
not by what is most interesting: research **every in-scope MUST item**, and cite each item's id
(`COV03`, …) beside the findings that answer it in `research-notes.md`. An item the research
cannot answer is recorded as such — it goes back to the owner (reopen `01b` to rescope it with a
disclosure), never silently dropped. Then run:

```bash
python tools/coverage_validator.py --channel inside-the-process --episode EPxxx --stage 02-research --emit-review
```

## Output

`episodes/<slug>/EPxxx/story/research-notes.md` — findings, source URLs where
used, and which findings will actually inform the script vs. which were
explored and set aside.

## Forbidden

Do not write dialogue. Do not let research material become copyable source
text for the script (paraphrase and cite, never transcribe a real transcript).
