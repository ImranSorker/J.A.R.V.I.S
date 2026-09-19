# J.A.R.V.I.S. V12.8.0 — Remaining Next Improvements

This document is deliberately a backlog, not a placeholder list for incomplete source modules. The current source tree has passed its source-level gates; the items below are the next engineering frontier or require target-machine certification.

## Target-machine certification

1. Flutter Windows/Linux/Android build, analyze, test and UI soak.
2. RTX 4060 Ti GGUF/llama.cpp real-model benchmark and VRAM certification.
3. Real Whisper/STT, TTS, camera and microphone certification.
4. Rust native runtime and OS-level sandbox compilation/testing.
5. C#/.NET Windows integration build.
6. Multi-node gRPC interoperability and chaos/soak tests.
7. Production mTLS rotation/revocation with a real CA.
8. Long-duration mission recovery and crash/restart drills.

## Research frontier

1. Hardware-backed/TEE identity and confidential execution.
2. Distributed memory conflict-free replication and encrypted offline sync.
3. Advanced multimodal long-term memory with temporal media retrieval.
4. Formal verification/model checking for critical capability policies.
5. Engine-specific KV-cache sharing and speculative decoding benchmarks.
6. Real disaggregated prefill/decode execution once multiple inference nodes are available.
7. WebAssembly/WASI production runtime integration after choosing and certifying a runtime.
8. J.A.R.V.I.S. native-runtime/AI-native-OS layer design and hardware abstraction validation.

## Verification policy

No target-specific item is reported as passed merely because a source contract exists.
