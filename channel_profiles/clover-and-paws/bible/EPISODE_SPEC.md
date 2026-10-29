# Episode Specification and QC — Clover & Bruno Stories
**Status**: LOCKED FINAL 2026-10-29
**Channel**: Clover & Bruno Stories @cloverandbruno
**Replaces**: previous prototype 8-11 min tribunal spec — ABANDONED

## Master specification — cat & dog family

| Dimension | Target |
|---|---|
| Shorts Runtime | 160-180s target (proven growth driver), 15-180s allowed, 24 fps. RENDERED 16:9 and reframed to 9:16 in post — never a separate render aspect |
| Longs Runtime | 8:00-15:00; target 9:30; minimum 9:00 per channel profile; 16:9, 24 fps |
| Speaking characters Shorts | Max 3 on screen even if Duo type; preferred 2 (Clover + Bruno) |
| Speaking characters Longs | Max 6; preferred 3-4 (Clover+Rosa+Fin+Bruno+Pip) |
| Performance unit | 20 seconds per clip, fixed |
| Dialogue pace | Approximately 135-145 spoken words per minute, warm gentle pace, adjusted for Bruno grumpy slow |
| Chore / prop inserts | 20-30% of runtime Shorts, 25-35% Longs (bike, dishes, bag, lawnmower) |
| Bruno gag timing | Bruno first answer = No with attitude within first 45s; soft reluctant yes + helps by 2:00 in Shorts, by 6:00 in Longs |
| Story out | Final runtime minus 15 seconds Shorts, minus 20 seconds Longs for payoff |
| Payoff / end screen | Final 15s Shorts: thank you / shared snack / hug; Final 20s Longs: emotional turn + Best for viewer + Subscribe |
| Distribution | 70% Duo both families, 15% Clover family only, 15% Bruno & Co only — locked |
| Master loudness | Target -14 LUFS-I ±1 LU; maximum -1 dBTP true peak (same as before, cozy not loud) |
| Audio delivery | 48 kHz stereo; dialogue passes phone, headphones and mono fold-down — Clover soft polite + Bruno raspy old must be clear |
| Captions | Human-reviewed UTF-8 SRT matched to picture lock |

## Required episode package

- Approved story brief with Type (A Duo 70% / B Clover 15% / C Bruno 15%) + lead declaration (Clover or Bruno) + co-appearance check
- Character reference manifest with hash-bound assets: Clover orange onesie, Bruno 70y gray + burnt-orange cardigan and glasses-on-a-chain, Rosa apron, Fin blue shirt, Pip bandana
- Shot list with timing, speaker IDs, eyelines (Clover left polite up, Bruno right grumpy down), continuity states (tire flat -> inflated)
- Prompt file using unified photoreal engine (old split abandoned) — Muse Image / photoreal prompt set
- Chore prop source file if any text (shopping list)
- Draft renders and rejection log showing human selection, especially rejecting if Bruno says yes first or Clover rude
- YPP Authorship Evidence Pack required by COMPLIANCE_GATE.md
- Final masters: Shorts 1080x1920 9:16 + Longs 1920x1080 16:9 or 4K
- Human-reviewed UTF-8 SRT captions, thumbnail (both cat and dog for Duo), metadata with disclosure copy
- Compliance sign-off: synthetic disclosure = Yes, Not made for kids, Bruno never-yes-first, Clover always polite

## Editorial QC — LOCKED for polite vs grumpy

- [ ] Cute chore / wish appears within 10 seconds Shorts, 20 seconds Longs
- [ ] Viewer understands polite request (Clover) and grumpy No (Bruno) by 0:45
- [ ] Bruno first line is No with attitude / scoff / complaint — never yes first attempt — locked gag checked
- [ ] Clover stays polite even after No: "Okay, thank you Bruno..." — never rude
- [ ] No more than 15 seconds Shorts / 25 seconds Longs passes without meaningful change in composition, prop state, or grumpy-to-soft shift
- [ ] Clover always appears with at least one parent (Rosa or Fin), ideally both — co-appearance checked
- [ ] Bruno's companion choice is deliberate — with Pip, or solo because the story wants him unwitnessed
- [ ] Max characters on screen respected: 3 Shorts, 6 Longs
- [ ] Story resolves central tension (chore done, help given) before final payoff period
- [ ] Final payoff is warm thank you / shared snack / hug, not tribunal verdict

## Visual/audio QC

- [ ] Character identity, fur, wardrobe, age, eyelines remain consistent: Clover orange onesie, Bruno burnt-orange cardigan and glasses-on-a-chain + gray fur 70y old
- [ ] Speaking mouths match assigned dialogue; silent characters do not lip-move (especially Pip, Mimi background)
- [ ] Paws and hero props pass close-up inspection (bike pump, bag)
- [ ] All readable text built in post, not trusted to generation
- [ ] Final program measures -14 LUFS-I ±1 LU with true peak no higher than -1 dBTP
- [ ] Dialogue intelligible on phone speakers: Clover soft polite + Bruno raspy grumpy clear at low volume
- [ ] Room tone continuous across clips: warm home tone, not cold office; native audio conformed in post
- [ ] UTF-8 SRT captions match final dialogue and speaker intent exactly, including Bruno sigh "[sighs] Fine..."
- [ ] Speaker labels use NAME: only when speaker changes off-screen or visually ambiguous; meaningful non-speech cues use brackets [porch creaks] [bag rustles]

## Packaging QC — cat & dog SEO

- [ ] Title leads with both names for Duo and is 90 chars or fewer: Polite Clover Asks Grumpy Bruno... / Grumpy 70-Year-Old Bruno Has to Deal...
- [ ] For Duo 70%, thumbnail shows BOTH cat and dog faces: Clover left polite 40% + Bruno right grumpy 40% + small object center
- [ ] Overlay 2-4 words exact line from episode, e.g., BRUNO SAYS NO / PLEASE BRUNO?
- [ ] Title/thumbnail do not imply real animal rescue distress footage
- [ ] Description opens with hook with both names when Duo + includes disclosure: AI-generated original stories. Not real footage. Photoreal anthropomorphic cat and dog family stories — Kitten Clover and Grumpy Dog Bruno.
- [ ] Pinned comment: Bruno said no first, then helped anyway. What would you do if you were Clover?
- [ ] Each Short with published Long uses YouTube Related Video field; description links are supporting only
- [ ] Hashtags: #catanddog #cloverandbruno present

## Post-publish review

Record at 48 hours, 7 days and 28 days:

- impressions, click-through rate, traffic source
- retention at 0:10 chore, 0:45 Bruno No, 2:00 Bruno soft yes, final payoff
- average view duration and percentage viewed
- comments: polite vs grumpy debate, subscribers gained per 1k views
- approved production minutes per GPU hour, rerender rate by failure category (e.g., Bruno says yes first = fail)

Do not establish fixed good thresholds before channel has at least 4 comparable uploads. Use first month to create channel baseline for Clover & Bruno Duo vs Clover Only vs Bruno Only.
