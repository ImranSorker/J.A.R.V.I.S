# J.A.R.V.I.S. V12.8.0 — Architecture Convergence

V12.8.0 remains the permanent development trunk. Progress is tracked by internal milestones and CI evidence, never feature version bumps.

## Internal milestone: Phase A Foundation
Stable Capability, Event, Resource, Lifecycle and Config contracts; bounded event fabric; structured concurrency; capability discovery; architecture boundaries; dependency-cycle detection; strict warning-free regression gate.

## Internal milestone: Phase B Intelligence
Unified cognitive runtime, bounded context assembly, model residency, hybrid semantic/lexical/graph-aware retrieval with reranking, provenance-aware memory lifecycle, and deterministic evaluation.

The next architecture work must converge existing legacy subsystems behind these contracts rather than add parallel feature managers.

# J.A.R.V.I.S. V12.8.0 Permanent Trunk — Internal Kernel Architecture

## Goal

V12.7.3 is feature-rich but the `JARVISCore` bootstrap is still a large integration composition root. V12.8.0 introduces a **Kernel boundary** without deleting the mature V12 subsystems.

### V12.8 — Runtime Hardening
- Event-sourced runtime journal (`core/v13/event_store.py`) with SQLite WAL, replay and correlation IDs.
- Default-deny capability firewall (`core/v13/capability_policy.py`).
- Deterministic DAG contract for long-running work (`core/v13/task_graph.py`).
- Kernel/facade lifecycle (`core/v13/runtime.py`) that can sit above existing V12 services.
- Backward-compatible integration in `JARVISCore`.

### Internal Kernel — Platform Architecture

```text
                    ┌──────────────────────────┐
                    │       JARVIS UI/API      │
                    └────────────┬─────────────┘
                                 │ commands/events
                    ┌────────────▼─────────────┐
                    │       Kernel Runtime        │
                    │ lifecycle + correlation  │
                    └──────┬─────────┬─────────┘
                           │         │
                ┌──────────▼───┐ ┌──▼─────────────┐
                │ Event Store  │ │ Capability     │
                │ replay/WAL   │ │ Firewall       │
                └──────────────┘ └──────┬─────────┘
                                        │ grants
                         ┌──────────────▼──────────────┐
                         │ Execution / Task Fabric     │
                         │ DAG + leases + idempotency  │
                         └──────┬───────────┬──────────┘
                                │           │
                  ┌─────────────▼──┐   ┌──▼──────────────┐
                  │ Model Gateway  │   │ Tool/Agent Gate │
                  │ route/admit    │   │ sandbox/verify  │
                  └───────┬────────┘   └──────┬──────────┘
                          │                   │
             ┌────────────▼──────┐   ┌────────▼──────────┐
             │ Local/Remote LLMs │   │ OS / Browser / IO │
             └───────────────────┘   └───────────────────┘

        Durable state: memory + world model + jobs + event journal
        Cross-cutting: audit, tracing, SLOs, recovery, supply-chain policy
```

## Design principles

1. **Kernel, not monolith:** UI, models, tools and memory become replaceable providers.
2. **Events over hidden coupling:** important state transitions emit durable events.
3. **Default deny:** capabilities are opt-in; high-impact capabilities require approval.
4. **Everything resumable:** long jobs use task IDs, dependencies, leases and idempotency.
5. **Model independence:** the runtime talks to a model gateway, never directly to one vendor/runtime.
6. **Local-first:** the default deployment remains usable with local GGUF/llama.cpp/LM Studio.
7. **Portable state:** events and state are stored in versioned, migratable stores.
8. **No unrestricted system authority:** computer-use, shell, filesystem writes and network access stay behind policy gates.

## Migration sequence

**V12.8.0:** adopt the kernel/event/policy contracts while retaining all V12 services.

**V12.8.0 internal milestones:** move job execution, model routing, memory mutations, computer-use and distributed workers behind the kernel interfaces one subsystem at a time.

**Future internal milestone:** make the kernel the only orchestration entry point; `JARVISCore` becomes a compatibility/composition layer. UI/API clients consume the same command/event contracts.

This release intentionally does **not** replace the mature V12 implementations wholesale. It establishes the stable seams needed to evolve them safely.
