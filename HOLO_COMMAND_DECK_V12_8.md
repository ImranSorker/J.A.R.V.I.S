# J.A.R.V.I.S. V12.8.0 — Holo Command Deck

The Flutter Holo Command Deck is an internal frontend implementation within the permanent V12.8.0 trunk. It does not constitute a release/version increment.

## Authority model

Flutter owns presentation, user interaction, visualization, local navigation state, and intent submission only. JARVIS Core remains authoritative for missions, memory, policy, model routing, tools, execution, security, and system state.

## Transport

`api/server.py` exposes an authenticated `/holo` WebSocket. The first message must negotiate Holo Protocol v1. Loopback clients may operate without a token when no Holo token is configured. Non-loopback access requires `JARVIS_HOLO_TOKEN` (or the API token fallback). Remote deployments should use TLS and `wss`.

## Implemented frontend capabilities

- Live telemetry and model inventory.
- Typed connection states, heartbeat, bounded exponential reconnect, stale-socket protection, and pending-request cleanup.
- Mission submission, mission status/cancellation, and mission DAG visualization.
- Streaming-ready chat event handling and a communications drawer.
- Agent, model-router, memory, diagnostics, and security observability panels.
- Responsive desktop/compact layouts.
- Explicit backend-authoritative action results.
- Holographic Canvas rendering with repaint isolation.

## Security boundary

The Holo client cannot directly execute host commands. High-impact actions remain controlled by the existing JARVIS policy/execution architecture. The shell tool no longer treats a caller-supplied authorization flag as sufficient authorization; a valid permission grant is required.

## Validation boundary

Python validation is executed in the repository environment. Flutter validation requires a machine with the Flutter SDK and target platform tooling; this environment does not provide the Flutter SDK, so Flutter build/test execution is not claimed here.
