# JARVIS V12.1.0 — Core Consolidation & Hardening

This release is a corrective engineering pass over V12.0.3.

## Completed
- Dual-Brain routing with fast/strong model roles and complexity classification.
- Fail-closed native inference and streaming error propagation.
- LanceDB-first unified memory; SQLite is explicit legacy compatibility only.
- Document table + deterministic chunking + real overlap + RAG retrieval integration.
- Persistent AION experiences/goals and AION planner integration for complex tasks.
- Real ToolRegistry execution from ReAct/MCP paths.
- Real bounded DuckDuckGo HTML search provider.
- Optional Playwright browser adapter with URL validation.
- Real local pyttsx3 TTS and microphone/STT conversation loop when optional packages exist.
- Real optional PEFT/Transformers LoRA training path.
- Real backend benchmark measurement; fabricated metrics removed.
- Persistent missions and Lance-backed workflow store.
- Watchdog and AION bridge lifecycle integration.
- Qwen/Ollama backend joins the unified model plane when enabled.
- Flet tab switching fixed so Code/System/Browser remain inside the dashboard shell.
- Normal Settings UI no longer exposes a permissive security toggle.
- Flet packaged writable-state paths use FLET_APP_STORAGE_DATA.
- Audit retention pruning and lifecycle cleanup improved.
- Packaging and version consistency updated to 12.1.0.

## Validation
- Python AST parse: PASS
- Production module imports: 121/121 PASS in audit environment
- compileall: PASS
- pytest: 122 PASS
- Core startup/shutdown smoke test: PASS

## Hardware-dependent validation still required
- Windows Flet rendering/pixel comparison.
- NVIDIA/CUDA inference on the target RTX 4060 Ti.
- Real microphone/speaker devices.
- Playwright Chromium installation and browser runtime.
- Multi-machine model-parallel inference.
