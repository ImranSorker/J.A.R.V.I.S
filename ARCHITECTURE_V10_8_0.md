# JARVIS v11.1.0 Architecture

## Runtime
Native model discovery/loading remains independent of Ollama and LM Studio.
Those applications can be used for model acquisition, but are not runtime dependencies.

## Data
Lance is the authoritative persistent application store.
- messages
- experiences
- goals
- curiosity
- strategies
- model registry
- benchmarks
- future workflows/missions/evaluations

JSON is configuration/interchange only.
SQLite exists only as `SQLiteMigrationReader` for one-time legacy migration.

## Cognitive layer
AION provides:
- goal proposals
- experience recording
- strategy evaluation
- curiosity proposals

## Intelligence
The native model router and model swarm remain the execution layer.
Model registry records discovered models and benchmark history.

## Autonomy loop
Perceive → understand → plan → execute → verify → learn.

Sensitive actions remain behind existing security/tool risk controls.
Self-edit remains dry-run by default.
