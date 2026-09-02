# JARVIS 10.7.1 → 10.8.0

## 10.7.1 Stability
- Fixed hardware profiler syntax error.
- Fixed vector-memory missing `time`.
- Hardened subprocess/error handling.
- Fixed orchestrator regex control characters.

## 10.7.2–10.7.5 Data Fabric
- Unified runtime persistence behind Lance.
- Added Lance-backed messages, experiences, model benchmarks and learning data.
- SQLite retained only as an explicit one-time migration reader.
- Removed sqlite-utils runtime dependency.

## 10.7.6 AION
- Added cognitive engine for goals, experiences, strategy evaluation and curiosity proposals.

## 10.7.7 Model intelligence
- Added persistent model registry and benchmark history.

## 10.7.8–10.7.9
- Added strategy memory and verification primitives.
- Preserved sandbox validation and self-edit dry-run semantics.

## 10.7.10
- Consolidated the stability/data/learning architecture as the release baseline.

## 10.8.0
- Integrated AION, model registry, strategy engine and verification into JARVIS Core.
- Added AION status, memory statistics and best-model API endpoints.
- Preserved native inference independence from Ollama/LM Studio.
- Added explicit migration script for legacy SQLite databases.

## Verification policy
A model, policy or self-edit is never promoted merely because it was generated. Candidate changes must pass compilation/tests and explicit promotion/verification gates.
