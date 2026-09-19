# Native no-version-hike upgrade backlog

These are capability upgrades to the permanent 12.8.0 trunk; they do not change the product version.

## P0 — Hardening
- Certified Windows plugin sandbox using restricted process identity, filesystem ACL isolation, Job Objects, and explicit network policy.
- Full strict typing campaign across legacy `Any` usage with adapter-specific protocols.
- Deterministic startup dependency graph with fail-fast critical services and graceful optional-service degradation.
- End-to-end policy recheck before every autonomous mission node.
- Transactional mission checkpoints with resume/rollback after crash or process restart.
- Secrets minimization and memory redaction across logs, telemetry, clipboard, and generated artifacts.

## P1 — Native Intelligence
- Native multimodal model adapter supporting image+text GGUF/llama.cpp deployments.
- Model benchmark lab with real measurements for prompt throughput, generation throughput, context capacity, VRAM, RAM, and latency.
- Learned local router trained from JARVIS's own verified task outcomes.
- Model lifecycle manager for discover → verify checksum → register → preload → load → unload → rollback.
- Local embedding/reranking model registry with compatibility metadata and deterministic migrations.

## P1 — Perception and interaction
- Low-latency local VAD + wake word + streaming STT + local TTS pipeline.
- Voice interruption/barge-in and cancellation integrated with Mission Authority.
- Continuous but opt-in screen/camera perception with privacy zones and frame-rate budgets.
- Clipboard Intelligence floating panel with translate/summarize/explain/fix actions performed locally.
- Native Windows desktop control adapter with verified window/application identity.

## P1 — Autonomous creation
- Artifact Factory 2.0: requirement extraction → architecture → multi-file generation → tests → sandbox build → evaluation → repair → signed package.
- Generated-project SBOM/provenance and reproducible-build metadata.
- Automatic regression-test generation for every self-modification proposal.
- Quarantine installation with atomic replacement and rollback.

## P2 — AIOS convergence
- Unified durable world-state projection for cognition, missions, devices, models, and events.
- Self-knowledge graph projections for capability health, dependencies, models, workers, and learned policies.
- Cognitive replay diffing across models/planners/tools with latency and outcome comparisons.
- Distributed worker attestation, leases, failover, and result provenance.
- Secure LAN Android dashboard pairing with capability-scoped control.

## P3 — Product polish
- Contextual proactive assistant scheduler with quiet hours and interruption scoring.
- Adaptive UI that exposes only currently available capabilities.
- One-click diagnostics and guided repair workflows.
- Native backup/restore/export of cognitive state with encrypted snapshots.
- Local observability dashboard for latency, token use, model residency, memory growth, jobs, errors, and security events.
