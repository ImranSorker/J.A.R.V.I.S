# Additional Issues Review — JARVIS 11.1.0

## Fixed
- `/dashboard` now returns HTMLResponse rather than a JSON/string response, including the booting state.
- Distributed mode now passes configured coordinator port and authentication token consistently and refuses to start without a >=32-character token.
- Computer screenshot tool is workspace-contained and classified high-risk because it captures the host screen.
- STT failures/unavailable backend now return an empty transcript instead of an error string that could be interpreted as user speech.
- Flet dependency narrowed to the current 0.86 minor line and project metadata pins supported Python 3.12/3.13 for reproducible builds; Flet 0.86 currently supports bundled Python 3.12/3.13/3.14, while JARVIS native ML dependencies are not guaranteed to have wheels on every 3.14 target.
- Added pyproject metadata and pytest configuration.

## Validation
- Python compileall: PASS
- Existing test suite: 98/98 PASS
- 120 non-test modules imported successfully in the audit environment
- Static integration assertions: PASS
- Flet graphical runtime could not be launched because Flet is not installed in the audit container.

## Remaining issues
1. Real GUI tap/typing/device tests require an environment with Flet installed; Flet 0.86 provides `flet test` for real UI integration testing.
2. Native inference remains platform/dependency sensitive (`llama-cpp-python`, CUDA/Metal/CPU builds, model availability).
3. Browser SSRF protection is still defense-in-depth; a dedicated egress proxy/network namespace is stronger against DNS rebinding.
4. Filesystem TOCTOU races against a hostile same-host process cannot be fully solved with path resolution alone; descriptor-relative/openat-style operations or an OS sandbox are needed.
5. Python/shell execution isolation depends on OS sandbox availability and is not a universal security boundary on every OS.
6. Voice/STT/TTS remain hardware/provider dependent and are intentionally optional.
7. Distributed mode requires a secure shared token and should be deployed on a trusted network or behind authenticated transport.
