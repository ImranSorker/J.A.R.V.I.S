# J.A.R.V.I.S. V12.8.0 — Next Session Certification Plan

V12.8.0 remains the product version. The source-side state-of-the-art hardening pass is complete. The next session is certification on the user's real development machine, not another feature batch.

## P0 — target-machine certification

1. Install/use Flutter 3.47.x and run `flutter pub get`, `flutter analyze`, `flutter test` and Windows release build.
2. Start the real FastAPI backend and certify the Flutter Holo WebSocket end-to-end with runtime token injection.
3. Install the intended LanceDB, sentence-transformers, llama-cpp-python and Whisper profiles and rerun `python main.py --doctor`.
4. Load a real GGUF model on the RTX 4060 Ti and measure prompt throughput, generation throughput, VRAM residency, context behavior and fallback to the local llama server.
5. Install Playwright browsers and execute redirect, private-IP, metadata-IP, DNS-rebinding and hostile-subresource tests.
6. Exercise microphone, camera, TTS/STT, Android ADB and document integrations on their actual target devices.

## P1 — release certification

7. Run Black, Ruff, Pyflakes, mypy and Bandit from `requirements-dev.txt` as blocking gates.
8. Run `scripts/generate_grpc.py` and verify generated bindings remain compatible with `polyglot/schema/jarvis.proto`.
9. Build Go, TypeScript, C++ and Java interoperability clients; compile Rust and C# with their target toolchains.
10. Run the full CI matrix for Python 3.12/3.13, Windows/Linux and Flutter stable.
11. Perform a clean-machine installation from the requirement profiles and verify no undeclared runtime dependency is needed.

## P2 — operational certification

12. Run long-duration soak tests for event journaling, memory consolidation, missions/jobs, router health and Holo reconnect behavior.
13. Exercise crash/restart recovery for missions, jobs, event replay and durable memory.
14. Measure evaluation quality/safety/latency/cost metrics across the installed local models and calibrate router decisions.
15. Validate the polyglot runtime manifest and script-runtime capability availability on the target host.

## Definition of done

- Product version remains **12.8.0**.
- `python -m compileall -q .` passes.
- Full Python pytest suite passes with warnings as errors.
- Dependency graph has zero cycles and zero unreachable modules.
- Feature audit is 35/35.
- Service/protocol/authority audits pass.
- Release verifier passes.
- Flutter, native GPU, browser, voice and device certification passes on the real target environment.
- No certification result is reported as passed when the required target runtime/toolchain is absent.
