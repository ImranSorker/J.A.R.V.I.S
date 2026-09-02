# JARVIS 10.9.0 — Cognitive Platform Upgrade

## Completed
- Visual desktop chat now calls the JARVIS core instead of returning a placeholder.
- Persistent workflow graph engine with validation and cycle detection.
- Persistent mission engine with checkpoints.
- Local model discovery for GGUF/Safetensors/BIN/ONNX.
- Resource manager and GPU-aware placement scheduler.
- Learned router history and benchmark feedback path.
- Failure memory and strategy memory.
- Hybrid retrieval foundation.
- Hierarchical AION planning, goals, experience and curiosity.
- Cognitive state machine: perceive → understand → plan → execute → verify → learn → idle.
- Plugin capability policy foundation.
- Continual-learning candidate/promote gate.
- Lance remains the authoritative persistent application store; JSON remains configuration/interchange.

## Security boundary
The self-edit and command execution components remain policy-controlled. A subprocess is not treated as a hardened security boundary. Production deployments should use an OS/container/VM isolation boundary for untrusted generated code.

## Validation
The release includes regression tests for the new deterministic engines. Hardware, native inference, Flet, LanceDB, browser and GPU paths remain environment-dependent and should be integration-tested on the target machine.
