# JARVIS v11.1.0 Audit

## Scope
This release addresses the major V10.8.0/v11.1.0 audit gap: compilation is not the same thing as hardware/runtime verification, and blacklist-based shell filtering is not a security boundary.

## Security changes
1. Capability authorization is centralized.
2. High-risk tools can require an explicit approval token.
3. Shell filtering no longer depends on a short dangerous-command blacklist.
4. Every permission decision and shell invocation can be recorded in an append-only audit log.
5. Self-edit remains dry-run by default and now adds a compile gate, workspace boundary, backup and rollback check.

## Independence
No provider lock-in was introduced. JARVIS can continue to own native inference and model discovery directly. Ollama/LM Studio remain optional model acquisition paths.

## Verification levels
- L0 syntax/compile: automated.
- L1 unit/regression: automated.
- L2 import/API smoke: automated where dependencies exist.
- L3 live dependency integration: executed by `Doctor` when the dependency is installed.
- L4 hardware integration: must be run on the target machine.
- L5 endurance/failure injection: next validation stage.

## Known environment limitations
The build environment may not contain CUDA, llama-cpp-python, LanceDB, Flet, sounddevice or sentence-transformers. v11.1.0 does not silently label those features as passed. Use `/doctor` after installing requirements on the target machine.
