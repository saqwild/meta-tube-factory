# demo-video - 3-minute judge demo (Remotion)

Composes the hackathon demo from two recorded tracks:

- Track A: OBS window captures of the Muse window per stage
  (see episodes/inside-the-process/EP001/_recording/recording-log.md).
- Track B: the episode artifacts themselves (stills, storyboard, clips).

## Planned compositions (180 s total)

1. Hook (0:00-0:15): one finished EP001 Bread clip.
2. Factory (0:15-0:45): flow diagram, five Muse organs, one profile file
   adding a channel.
3. Proof (0:45-2:00): side-by-side - left, a stage executing and its
   validator verdict; right, the artifact it produced.
4. Episode (2:00-2:30): three best clips, SAM 3.1 segmentation overlay,
   Muse Voice Transcribe audit line.
5. Close (2:30-3:00): owner gate approval, $150 spend ledger, public
   repo and YouTube links.

## Build

Uses the repo's existing Remotion + ffmpeg stack (same as 06a
postproduction). Raw OBS captures are never committed; only selected
clips, this scaffold, and the final render are. Input data is the
recording log plus episode artifacts - captions, slates, and the spend
ledger are generated from those files, not typed by hand.
