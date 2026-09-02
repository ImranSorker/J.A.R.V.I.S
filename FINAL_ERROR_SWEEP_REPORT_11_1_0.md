# JARVIS 11.1.0 Final Error Sweep

## Findings fixed

1. Computer-use tools existed but were not registered in JARVISCore. Added screenshot/click registration.
2. ToolRegistry did not map the `computer` tag to `computer.control`; added capability mapping and high-risk capability classification.
3. Voice conversation loop `start()` could create duplicate worker threads and `stop()` did not join them. Made lifecycle idempotent and bounded on stop.
4. Wake-word detector had the same duplicate-thread/lifecycle issue. Fixed.
5. Self-edit used the process current working directory rather than the canonical project root, causing incorrect path authorization when launched from another directory. Fixed to use PROJECT_ROOT.
6. API doctor endpoint depended on the current working directory. Fixed to resolve the repository root from the API module location.

## Validation

- Python compileall: PASS
- AST parse: PASS
- Automated tests: 108 passed, 1 skipped
- Non-test Python imports: 106/106 passed
- JARVISCore smoke initialization: PASS
- Tool registration smoke test: PASS
- Computer tools registered: screenshot + click
- Flet physical integration test: NOT RUN because Flet/Flutter is not installed in the audit environment.

## Remaining environmental validation

- Physical Windows Flet run
- Physical Linux Flet run
- Android emulator/device Flet run
- Native llama-cpp-python/GPU combinations
- Playwright browser binaries
- Microphone/TTS hardware
- Multi-machine distributed deployment
