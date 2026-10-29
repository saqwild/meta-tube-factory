# Agent adapters

Adapters are optional launch notes for a particular LLM platform. They never
define the process and cannot override `pipeline/`, `channel_profiles/`, or
the single-active-stage rule in `AGENTS.md`. Use `generic/AGENT.md` when a
platform has no dedicated file — in practice, every platform here just points
back to it, because nothing about this pipeline is vendor-specific.
