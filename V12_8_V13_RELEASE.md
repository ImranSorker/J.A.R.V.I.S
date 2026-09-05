# J.A.R.V.I.S. V12.8.0 — Kernel Upgrade Release

V12.8.0 is the first step toward the JARVIS V13 platform architecture. It preserves the mature V12 autonomous stack while introducing stable kernel seams for future extraction.

## Added
- `core/v13/contracts.py` — versioned event, capability and task contracts.
- `core/v13/event_store.py` — durable SQLite/WAL append-only event journal with replay.
- `core/v13/capability_policy.py` — default-deny capability firewall with approval gates.
- `core/v13/task_graph.py` — deterministic dependency DAG with cycle detection/readiness.
- `core/v13/runtime.py` — lifecycle, event dispatch, authorization and health facade.
- V12 `JARVISCore` now boots and stops the V13 runtime facade and emits runtime/chat/system events.

## Compatibility
The existing V12 router, memory, RAG, agents, tools, distributed fabric, computer-use and self-improvement systems remain intact. V12.8 is intentionally an additive architecture migration rather than a risky rewrite.

## Next
V12.8.x should progressively move execution, model serving, memory mutation, computer use and distributed workers behind the kernel contracts. V13.0 should make those contracts the primary orchestration API.
