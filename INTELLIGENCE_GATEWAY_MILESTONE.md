# V12.8.0 Internal Milestone — Cognitive Control Plane

## Objective
Move inference from a thin router call into a bounded control plane without coupling cognition to a model vendor, UI, tool, or operating system.

## Guarantees
- Explicit concurrency admission.
- Prompt-size boundary.
- Optional deterministic response cache with TTL and LRU eviction.
- Adaptive model selection through the existing `ModelIntelligence` contract.
- Model residency telemetry.
- Latency and failure counters.
- Runtime enable/disable.
- Explicit-backend requests do not silently downgrade.
- Unbound requests may retry through the router fallback policy.
- No raw prompt is stored as a cache key; SHA-256 is used for the derived key.
- UI, tool execution, filesystem, and authorization remain outside this component.

## Integration
`JARVISCore` creates the gateway after the canonical router and model-intelligence services, then injects it into `UnifiedCognitiveRuntime`. The old router remains available as the replaceable provider boundary.

## Validation
The milestone has dedicated unit and integration regression coverage and is included in the complete pytest suite.
