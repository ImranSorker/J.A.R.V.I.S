# JARVIS V12.0.2 — Runtime & GUI Stability Update

- Self-awareness scanning moved off the startup critical path and made bounded/incremental with cache.
- GUI module now has a direct entry point (`python -m gui.flet_app`).
- Native model router lazily loads backends for non-streaming chat as well as streaming.
- Added provider-neutral OpenAI-compatible local-server adapter for llama.cpp `llama-server`; LM Studio remains an optional launcher/acquisition layer.
- Added Windows helper scripts that keep the local server API key in process environment only.
- Fixed duplicate verification and undefined verification in streaming chat.
- Fixed `/lora load` command ordering.
- Shutdown now closes memory and joins managed threads.
- JARVIS scans common local model directories including `~/.lmstudio/models`.
- Version metadata updated to 12.0.2.

## Validation
`python -m compileall -q .` passed.
`python -m pytest -q` passed: 111 tests.
