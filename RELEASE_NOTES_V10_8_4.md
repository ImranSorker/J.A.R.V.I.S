# JARVIS 10.9.0 — Verification, Independence & Cognitive Platform Foundation

## Completed in this release

- Capability-based authorization replaces brittle shell-string blacklists.
- Full-capability independent mode remains available; high-risk capabilities require explicit approval tokens.
- Durable LanceDB data fabric with an offline JSONL bootstrap fallback when LanceDB is not installed.
- Deterministic embedding fallback so first boot does not crash when sentence-transformers is absent.
- Model Intelligence 2.0: hardware-fit scoring and benchmark recording.
- GPU scheduler: reservations, residency, eviction and placement.
- RAG 2.0 foundation: hybrid retrieval + provenance + knowledge graph.
- AION 2.0 foundation: hierarchical goals, budgets, confidence and opportunity detection.
- Continual Learning 2.0: curation, challenger/champion promotion and rollback.
- Self-edit validation/apply path with compile and diff checks, backups and rollback.
- Native inference remains JARVIS-owned; Ollama/LM Studio are optional model-acquisition helpers.
- Local voice capture/STT and TTS now use real optional providers when installed.
- JARVIS Doctor autodetects the project root and reports actual dependency/integration state.
- Installation/bootstrap scripts and dependency profiles added.
- Native model loading is lazy so missing optional native dependencies do not prevent JARVIS from booting.
- Regression and architecture tests expanded.

## Independence policy

JARVIS is not intentionally sandboxed into a toy assistant. Its capability set can be broad. The default policy is `guarded`: high-risk actions such as shell execution, system modification and browser control require an explicit approval token. This is a permission boundary, not a model/provider restriction.

## Verification

The build environment validates Python compilation, package imports, core initialization, fallback persistence, capability authorization, workflow/mission behavior and the regression suite. Hardware-specific CUDA/native inference, microphone devices, browser binaries and real LanceDB must still be exercised on the target machine after dependency installation.
