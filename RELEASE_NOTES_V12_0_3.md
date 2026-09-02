# JARVIS 12.1.0 — Integration & Command Center Release

## Fixed
- Replaced the placeholder Flet UI with a functional command-center interface modeled on the supplied JARVIS dashboard reference.
- Added navigation, chat composition, streaming chat integration, model selection, system telemetry, memory status, agent/tool/workflow views, voice status, RAG workspace, file picking and guarded settings.
- Changed GUI startup to a stable `ft.run()` closure that keeps the UI application object alive for the session.
- Added `gui/__init__.py` for explicit package discovery.
- Removed implicit production mock inference fallback. A mock backend is only eligible when explicitly present in a router fallback chain or explicitly enabled.
- Native inference no longer fabricates a mock answer when the native model is not loaded.
- Streaming fallback now returns an explicit backend-unavailable status instead of silently pretending a model answered.
- Centralized workspace-path validation through the hardened Fortress path primitive.
- Anchored project-relative runtime paths so source and packaged launches do not depend on the process working directory.
- Fixed API/runtime release version metadata to 12.1.0.
- Added cross-platform path regression assertions.
- Added a fail-closed router regression test.
- Made the proactive monitor report failures instead of silently swallowing them.
- Corrected README run commands and current-release documentation.

## Verification
- `python -m compileall -q .`: PASS
- AST parse of Python sources: PASS
- Automated test suite: **112 passed** in the dependency-rich audit environment.
- Full real Windows Flet rendering: not executable in the Linux audit environment and must be verified on the target Windows machine.
- Native CUDA/llama.cpp inference: requires target hardware/toolchain validation.
