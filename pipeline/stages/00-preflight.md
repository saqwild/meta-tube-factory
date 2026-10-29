# 00 — preflight

**Run by:** `tools/preflight.py`, not a stage contract read by an LLM. Listed
here for completeness of the stage catalog.

## Task

1. Verify every `channel_profiles/<slug>/channel.json` parses as valid JSON and that each
   stage it declares has a matching contract file. Channels are DISCOVERED, never hardcoded —
   adding one is a data change, not a code change.
2. Ask which channel this run is for.
3. List that channel's open episodes (state files under
   `episodes/<slug>/`) and offer to resume the most recently touched one, or
   start a new episode at the next free `EPxxx` number.
4. Create `episodes/<slug>/EPxxx/episode-state.json` for a new episode with
   `next_stage` set to the first entry of that channel's `pipeline_stages`.
5. Print the contract path for `next_stage` and stop.

## Output

`episode-state.json`, `episode-state-log.md` (first line: episode created,
timestamp, channel slug).

## Forbidden

Do not write any creative content here. Do not skip the channel-selection
prompt even if only one channel has open episodes.
