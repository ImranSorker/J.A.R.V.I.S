# JARVIS v11.1.0 — Adversarial Fix Report

## Fixed in this pass

- Eliminated double-consumption of one-time approval tokens across ToolRegistry and high-risk handlers.
- Added approval-token schema support for self-edit and passed a single authorization decision inward.
- Fixed Qwen streaming `json` import, response cleanup, HTTP status handling, and parser error handling.
- Constrained SecurityExecutor working directories to the configured JARVIS workspace and hardened its environment.
- Hardened workspace file reads/writes against final-component symlinks and made writes atomic/fsynced.
- Constrained session export IDs and imports to the data directory with size and format validation.
- Constrained document ingestion to the workspace with a 20MB input limit.
- Restricted legacy model discovery to GGUF, matching the native loader's compatibility contract.
- Bound AutoProgrammer promotion to the validated content hash and protected the promotion destination.
- Reworked distributed RPC signing to one canonical authenticated payload and added receiver-side timestamp/nonce verification helper.
- Authenticated UDP worker discovery and added replay protection; unsigned discovery is rejected.
- Python code execution now requires an OS-level sandbox (bubblewrap/firejail); it refuses to execute when no real sandbox is available.

## Verification

- Python compilation: passed
- Existing test suite: 81/81 passed
- New adversarial regression tests: 7/7 passed
- Total: 88/88 passed

## Remaining architectural limitation

The browser still needs a dedicated network egress proxy for a hard DNS-rebinding boundary. Filesystem TOCTOU protection is improved with final-component no-follow checks and atomic replacement, but a hostile same-host process with arbitrary directory mutation privileges should ultimately be isolated with OS-level namespaces/containers.
