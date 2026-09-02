# JARVIS v11.1.0 Bug/Incompatibility Fix Report

## Validation performed
- `python -m pytest -q`: 81 passed
- `python -m compileall -q .`: passed
- Runtime import smoke test for core/API/native/memory/voice/UI/browser modules: passed
- Dashboard rendering smoke test: passed
- Doctor check: runs; optional components are reported explicitly when not installed

## Fixed
1. **Dashboard runtime crash** — `api/server.py` shadowed the imported `html` module with a local variable, causing `UnboundLocalError` when rendering the dashboard. The module is now imported as `html_lib`.
2. **Dashboard HTML injection** — dynamic primary-model and persona values are now escaped, matching the existing model-list escaping.
3. **Streaming API incompatibility** — `/chat` with `stream=true` previously attempted to serialize a generator through the normal JSON response path. It now returns a `StreamingResponse`.
4. **Streaming fallback failure** — `ModelRouter.chat_stream()` did not use the configured fallback chain and could report no model even when a fallback was available. It now loads/tries candidates in the same fallback order as non-streaming chat and supports the mock fallback.
5. **Self-edit approval token dropped by API** — the request model accepted `approval_token`, but the API handler did not forward it. The token is now passed through.
6. **Invalid persona accepted by API** — `/persona/{name}` now rejects unknown persona names with HTTP 404 instead of silently setting an unusable persona.
7. **Fractional model parameter parsing** — model discovery now correctly parses names such as `0.5B`, `1.5B`, and `7B` instead of truncating fractional values.
8. **Native model compatibility default** — the default native discovery configuration now targets `.gguf` rather than legacy `.bin` files that may not be loadable by modern llama.cpp builds.
9. **Model metadata typing** — `ModelSpec.param_count` now accepts fractional parameter counts.
10. **Browser resource cleanup** — navigation/extraction pages are closed in `finally` blocks so timeouts/errors do not leak Playwright pages.

## Notes
The optional dependency stack is intentionally lazy: JARVIS can boot without LanceDB, llama-cpp-python, Flet, or embedding packages, using its documented fallbacks where available. Current PyPI releases for llama-cpp-python, SciPy, and Flet advertise Python 3.13 compatibility; the requirements remain open-ended so installers resolve compatible current releases.
