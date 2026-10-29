# Codex launch note

No Codex-specific behavior. Follow `adapters/generic/AGENT.md` exactly.

Where a skill named in the Claude adapter isn't available, perform the equivalent Muse Image
Pro or LTX-2.5 prompting manually — the writer skills under `local_skills/` are plain markdown
and are the actual method, not a wrapper around a tool call. Read
`local_skills/ltx-production-writer/SKILL.md` or
`local_skills/frame0-still-writer/SKILL.md` directly, follow it, and say in the stage's
confirmation note that you worked from the skill file manually.

The validator is a plain script and runs anywhere:

```bash
python -m unittest discover -s tests
```
