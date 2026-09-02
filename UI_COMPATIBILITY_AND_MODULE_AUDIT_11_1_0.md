# UI, Compatibility & Module Audit — JARVIS 11.1.0

## Scope
- Full Python compilation and regression suite
- JARVISCore startup/shutdown smoke test
- FastAPI health/auth/model-load smoke tests
- CLI helper import-safety checks
- Flet UI API compatibility review against modern Flet 0.83+ APIs
- Workflow UI execution path review
- Optional-module/fallback behavior review
- Native runtime and document-ingestion compatibility checks

## Findings fixed
1. Migrated the Flet UI from the legacy `Tabs(tabs=[...])` shape to the current `Tabs` + `TabBar` + `TabBarView` API.
2. Switched the Flet entrypoint to `ft.run()` with a compatibility fallback to `ft.app()`.
3. Moved long-running chat work through Flet's `page.run_thread()` when available.
4. Added interactive model selection/loading, persona selection, refresh, and visible UI error reporting.
5. Added workflow input validation and error feedback in the UI.
6. Removed import-time execution from `scripts/doctor.py`, `scripts/generate_secrets.py`, and `scripts/issue_approval.py`.
7. Moved API rate limiting after authentication so unauthenticated traffic cannot evict authenticated rate-limit buckets.
8. `/models/{name}/load` now returns 404 for unknown models rather than an internal error.
9. Bubblewrap sandbox now exposes `/usr/local`, which is required on common Python installations where `sys.executable` lives there.
10. Document ingestion now rejects unsupported extensions and reports PDF extraction failures instead of silently reporting success.
11. Legacy native runtime now enforces regular `.gguf` files, configured model roots, and a maximum model size.

## Validation
- Python compilation: PASS
- Test suite: **98/98 PASS**
- JARVISCore startup/shutdown: PASS
- FastAPI health: PASS
- Unauthenticated protected API: 401 PASS
- Authenticated `/models`: 200 PASS
- Unknown model load: 404 PASS
- CLI script import safety: PASS

## UI environment note
The audit environment did not have Flet installed and had no network access to install it. The UI was therefore validated statically against the current Flet documentation and with syntax/compatibility regression tests. The packaged dependency is now constrained to `flet>=0.83,<0.87` to avoid silently crossing known API generations.
