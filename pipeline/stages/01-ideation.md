# 01 — ideation

## Inputs

`channel_profiles/<slug>/channel.json` (`positioning`, `format`, `tone`/`spine`
fields), the channel's read-only reference bible for voice/lore, prior
episodes in `episodes/<slug>/` (avoid repeating a premise or subject).

## Task

Lock a single episode premise: logline, target runtime bucket (from
`channel.json` → `format`), and — for a channel whose `pipeline_stages`
includes `02a-sourcing`/`02b-compliance` — an explicit note on what real-world
mechanism (if any) the fiction is *inspired by* without depicting a real
person, company, or event.

### `inside-the-process` — frame the question the viewer actually has

The premise must also contain:

- **The general viewer question**, in the words a curious viewer would type — "how is a glass
  bottle made?", "what is a battery made of and how does it work?" — not a question that
  already starts partway through the process. EP001's premise asked "how does *molten glass*
  become this shape?", which silently skipped everything before melting; that is the framing
  failure this rule exists for.
- **The full process chain**, one line per state, from the *true* raw/original starting
  substance (or, for a biological process, the anatomy involved and its resting state) to the
  finished result in use.
- **A proposed scope** — where the episode starts and ends on that chain, and why. Anything on
  the chain outside the scope is named, because `01b-coverage-scan` must either bring it in or
  give it an on-screen disclosure.

`01b-coverage-scan` turns this into the owner-approved coverage map; see
`pipeline/process_coverage.md`.

### `inside-the-process` — story definition (`bible/STORY_ENGINE.md`)

From the next LTX episode on, also write `story/story-definition.md`, the Story Definition Sheet (`STORY_ENGINE.md` §10), and give it
to the owner with the premise. It is a draft: every fact in it is a research target until `02a` clears it, and `03a` confirms or
revises it. Choose topics as "you + an everyday action + time". Name the pillar's "you" anchor (§2) and a master metaphor that can be
staged as an inside place the Explorer enters. The sheet's clock must be real: do not promise an hour-by-hour structure for a topic
whose sources do not support one. This sheet is a document, not a machine gate.

## Output

`episodes/<slug>/EPxxx/story/premise.md` — logline, runtime target, cast
count, one-paragraph owner rationale for why this episode and not another
(plus, for `inside-the-process`, the viewer question, process chain and proposed scope above).

## Forbidden

Do not write dialogue or scenes here. Do not select cast members yet — that's
`03a-writer`.

## Stop condition

Owner reads and either accepts the premise (advance) or asks for another pass
at the same stage.
