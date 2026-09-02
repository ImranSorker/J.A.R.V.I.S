# JARVIS 12.0.1 — Final Source Audit

## Scope

Audited the uploaded JARVIS 12.0.0 IRONCLAD source archive on Windows-oriented compatibility grounds, then applied a second-pass fix set. The source tree was checked with compilation, AST parsing, import smoke tests, core startup/shutdown smoke tests, regression tests, and targeted security/RAG/persistence tests.

## Fixed in 12.0.1

1. Unified release version metadata: main runtime, API, GUI, pyproject, config and VERSION now agree on 12.0.1.
2. Fixed high-risk approval semantics: a valid, one-use approval can temporarily authorize the exact requested capability instead of being blocked by the default capability allow-list.
3. Added a Windows execution path. Linux keeps Bubblewrap/Firejail isolation; Windows uses a constrained child process with cleaned environment, workspace confinement and timeout. It is explicitly not treated as a hostile-code sandbox.
4. Fixed Windows disk monitoring so it uses the active system volume rather than assuming `/`.
5. Fixed RAG wiring: the main runtime now gives HybridRetriever the Lance store and injects retrieved context into normal chat when available.
6. Fixed the retriever/Lance API mismatch that previously caused silent RAG retrieval failures.
7. Added bounded lexical text search to the Lance store for operation when embeddings are unavailable.
8. Added Lance-backed AION experience persistence instead of silently calling a nonexistent store method.
9. Made Lance normalization serialize nested dictionaries/lists-of-dictionaries safely for Lance schemas.
10. Removed SQLite from the default runtime configuration; the legacy SQLite migration adapter remains available for old databases.
11. Fixed AION learning records so reward/success are based on the verification result instead of always being recorded as perfect success.
12. Made ReAct max steps honor configuration.
13. Registered discovered local models in the model registry during startup.
14. Improved Doctor path reporting and added platform/architecture/NVIDIA diagnostics.
15. Added Windows-specific dependency and launcher files so the default Windows install does not accidentally trigger a llama.cpp source build.
16. Added regression coverage for approval semantics, Lance text search, AION persistence and RAG retrieval.
17. Removed runtime databases, caches and generated artifacts from the release archive.

## Validation

- Python compilation: PASS
- AST parse: PASS (151 Python files)
- Non-test imports: PASS (105 modules)
- Regression tests: PASS (109 passed)
- JARVISCore startup/shutdown smoke: PASS
- Tool registration smoke: PASS
- RAG/Lance targeted tests: PASS
- Approval token targeted tests: PASS
- Stale 11.1.0/12.0.0 runtime-version scan: PASS
- `shell=True`, `os.system`, `eval`, `exec` runtime scan: PASS (none found outside tests)

## Environment-dependent validation still required

1. Windows 11 Flet desktop execution on the target machine.
2. NVIDIA CUDA + llama-cpp-python native inference on the target RTX GPU.
3. LanceDB native engine execution with the installed version.
4. Sentence-transformers model download/load and embedding performance.
5. Playwright browser installation and actual browser automation.
6. Microphone, speaker, STT/TTS and wake-word hardware.
7. Real LAN distributed deployment across multiple Windows/Linux machines.
8. Long-duration VRAM, thermal, memory-leak and model-swap endurance tests.
9. Strong OS-level sandboxing for hostile code on Windows; the current Windows child-process path is an approval-gated containment fallback, not a security boundary.
10. True tensor/pipeline model parallelism across multiple physical GPUs/machines remains an architectural feature, not a completed capability.

## Release classification

JARVIS 12.0.1 is source/integration hardened and Windows-oriented, but it is not hardware-certified until the environment-dependent tests above are executed on the user's actual Windows 11 machine.
