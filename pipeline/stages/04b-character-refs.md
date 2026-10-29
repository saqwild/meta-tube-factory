# 04b — episode character sheets (Muse Image)

## Three tiers, and the base tier is a bare figure

**Owner decision, 2026-10-29, after a failed first approach.** Character references live at three
levels. Getting the base tier wrong was the single most expensive mistake made in this pipeline
so far, and the fix is recorded here so it is not repeated.

| | **Tier 0 — identity** | **Tier 1 — episode sheet** | **Tier 2 — frame-0 stills** |
|---|---|---|---|
| where | `bible/characters/identity/` | `episodes/<EPID>/visual/references/characters/` | `episodes/<EPID>/renders/stills/` |
| what it is | **one bare figure.** No wardrobe, neutral pose, plain backdrop, no panels, no labels | this episode's look and wardrobe on that identity | one still per clip |
| locks | **who the character is** | **what they wear and how the episode looks** | **what is happening at that instant** |
| conditioned on | nothing — it is the root | Tier 0 | Tier 1 |
| lifespan | the channel | one episode | one clip |
| scope | the full cast | **only the characters this episode uses** | every clip |

Each tier adds exactly one thing: identity → wardrobe → moment.

> **This tiering is channel-declared, not universal.** It is the model for a channel that keeps
> persistent bare-figure identity masters (clover-and-paws: `channel.json → cast.reference_tiers`).
> A channel may instead declare a **per-episode** workflow — no persistent masters, each episode
> generates its character sheets from text cards (signed-anyway: `channel.json →
> cast.reference_workflow`, owner decision 2026-10-29). Read the channel's own `cast` block
> first; if it declares a per-episode workflow, "Tier 0" below means that episode's approved
> portrait, not a channel-level master, and the "never condition on a sheet" rule still applies
> at the sheet-building step (portrait → full-body → six-panel), not to the episode's own sheet.

## Never condition on a character *sheet*

A sheet is a **composed page** — panel layout, backdrop, detail insets, captions, and a rendering
style. Conditioning on it delivers the page, not just the character.

This was proven the hard way. Conditioning an episode sheet on a channel *sheet* produced output
that reproduced the source's **text labels** — "GINGER FUR", "CREAM PATCHES" — despite the prompt
explicitly saying "no text". That was never identity leaking. It was page design leaking, and the
rendering style rode along with it, defeating every attempt to restyle the character.

A **bare figure** carries almost none of that, which leaves the prompt's own style language room
to act. Full evidence is the six-run test in the source repo (`C:\pycode\clover_and_paws`) that
this doctrine was imported from.

**Corollary:** if a Tier-1 sheet comes out wrong, do not patch the sheet. **Fix Tier 0 and
regenerate.** A derivative cannot be argued out of a fault it inherited.

## Inputs

- `visual/scene-list.md` — which characters this episode needs, and in what wardrobe
- the **Tier-0 identity masters** for exactly those characters
- `channel.json` → `cast`, `render.look_and_feel`; the bible's visual-style contract and the
  character cards for permanent anchors
- the episode's declared look and feel

## Before anything else

```bash
python tools/check_reference_assets.py --channel <slug>
```

Then **open the identity masters and look at them.** A hash proves a file is unchanged; it says
nothing about whether the pixels are usable. This project reached a wrong conclusion twice by
reading a card's text instead of viewing the image it describes.

### Upload ceiling — real, and it fails unhelpfully

Flow's uploader silently rejects large references: *"Reference image upload did not finish (Add to
Prompt never became enabled)"*. A 12 MB / 3840×2160 PNG and a 22 MB / 5504×3072 PNG both failed;
~2 MB JPEGs at ≈2752×1536 work.

Tier-0 masters should be kept inside that budget. If one is not, generate a downscaled JPEG proxy
for upload — **never modify the master.**

## Task

### 1. Confirm the episode's look and feel

Stated explicitly before any generation and recorded in the manifest. If it is not stated, stop
and ask. Do not infer it from the masters, whose register may differ deliberately — that
difference is the entire point of separating the tiers.

### 2. Generate one sheet per required character

Condition on that character's **Tier-0 identity master**, and state in prose:

- the episode's look and feel
- **the wardrobe** — Tier 0 is undressed, so every garment must be described here
- every **permanent identity anchor** the character's card declares. These survive undressing and
  must survive dressing: a signature accessory, a marking, a motif.

> ⚠ **A wardrobe layer can hide a body marking.** Where a character's signature is on the body
> rather than on clothing, say so explicitly in every prompt that dresses them, or the garment
> will cover it and the channel's cheapest binary QA check disappears.

**Generation path: Muse Image via Meta Model API** -- python tools/meta_models.py image --prompt PROMPT. One character per run, into its own folder. Record still_generator=muse-image-1.0 for every sheet. Reference masters are inputs, never regenerated here.

### A stale still can land in the wrong slot

A repeated or misfiled image looks plausible and renders in the wrong clip. At 04f2 a stale still lands in the wrong clip slot, looks plausible, and renders.

**Two defences, both required:**

1. **Hash every download against everything previously downloaded.** Anything already seen is
   stale by definition:
   ```bash
   python -c "
   import hashlib,pathlib,sys
   base=pathlib.Path(sys.argv[1]); new=pathlib.Path(sys.argv[2])
   prev={hashlib.sha256(p.read_bytes()).hexdigest() for d in base.iterdir() if d!=new for p in d.glob('*.jpg')}
   for p in sorted(new.glob('*.jpg')):
       h=hashlib.sha256(p.read_bytes()).hexdigest()
       print(p.name, 'STALE' if h in prev else 'fresh')" <gen-root> <new-folder>
   ```
2. **Look at the image before promoting it.** The hash check catches repeats; only your eyes catch
   a fresh image of the wrong subject.

Generate **one character per run** into its **own folder**. Batching several into one folder makes
this impossible to untangle after the fact.

### 3. Generate the hardest character first, alone, and check

Not the lead — the one whose design most resists the episode's look. Confirm identity survived
before spending the rest of the cast on an approach that may not work.

### 4. Where two characters share frames, prove they sit together

Especially if their Tier-0 masters came from different sources. One two-shot, both masters
attached, before any frame-0 work. Two lineages that have never shared a frame may not agree on
scale, register or light.

## Output

- `episodes/<slug>/EPxxx/visual/references/characters/EP<id>-CAST0XX-sheet.<ext>` — one per
  character the episode uses.
- `_gen/` and `_variants/` — every unselected generation, retained until the episode closes. They
  are the cheap fallback; deleting them turns a subtly-wrong keep into a full re-roll.
- `visual/references/manifest.md` — per sheet: the Tier-0 master and its SHA-256, the look-and-feel
  string, the wardrobe described, the prompt, the result's SHA-256, and the `[[TAG]]` it resolves
  to at `04f2`.

## Promotion

Episode sheets are **never** promoted to Tier 0 — they carry one episode's wardrobe and look.

Promotion applies only to a genuinely **new recurring character**: introduced episode-local, used
again later. At that point build it a proper **bare identity master** and a card. Never promote a
dressed or styled sheet into the identity tier; that is precisely the failure this structure
exists to prevent.

## Forbidden

Do not edit a Tier-0 master. Do not condition a sheet on another sheet. Do not generate frame-0
stills here — that is `04f2`. Do not generate a sheet for a character the episode does not use.
Do not let the episode's look override a permanent identity anchor. Do not delete unselected
variants before the keep is confirmed.

## Stop condition

Every character the episode uses has one episode sheet, conditioned on its bare identity master,
in the declared look and wardrobe, recorded in the manifest with both hashes — identity confirmed
**by eye against the master**, and any characters sharing a frame confirmed to sit together.
