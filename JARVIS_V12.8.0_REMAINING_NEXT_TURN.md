# J.A.R.V.I.S. V12.8.0 — Remaining Next-Turn Work

Product version remains `12.8.0`. The source-level feature roadmap has been implemented; the remaining items are deployment certification, empirical measurement, and longer-horizon research rather than placeholder modules.

## Target-environment certification

- Flutter desktop/mobile/web analyze, test, build and UI soak on real target machines.
- Real Flutter ↔ FastAPI/Holo authenticated session and reconnect testing.
- Native GGUF/llama.cpp + CUDA benchmark on the RTX 4060 Ti, including VRAM admission, hot swap, tokens/sec and thermal behavior.
- Real LanceDB + embedding stack certification.
- Real Whisper/STT/TTS/audio-device certification.
- Real camera/screen/OCR/computer-use adversarial testing.
- Rust trusted-runtime build and OS-level sandbox validation.
- C#/.NET build and Windows integration certification.
- Full generated gRPC build for every supported language target.
- mTLS certificate rotation/revocation and multi-node chaos/soak tests.
- Crash/restart/recovery testing across long-running missions.

## Empirical optimization

- Populate model benchmark/evaluation datasets from real local workloads.
- Calibrate adaptive routing with measured quality/latency/power/VRAM data.
- Establish service SLO baselines and burn-rate alert thresholds.
- Profile memory consolidation and retrieval latency at production-sized stores.
- Tune agent reputation and swarm scheduling from real task outcomes.

## Long-horizon research intentionally retained

These are deliberately kept for a future engineering turn because they require substantially broader system design or external validation:

- trusted execution environments / hardware-backed key isolation;
- full distributed memory consistency and conflict-free synchronization;
- production-grade multi-node scheduler with topology-aware placement;
- complete semantic computer-use benchmark suite across changing applications;
- multimodal long-term memory for image/audio/video artifacts;
- formal model-policy verification and machine-checkable capability proofs;
- a full JARVIS system digital twin with predictive dependency simulation;
- secure plugin signing/publisher infrastructure suitable for public distribution;
- the eventual JARVIS native runtime/AI-native operating-system layer.
