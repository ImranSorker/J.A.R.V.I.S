# Recommended Next Upgrade Batch — V12.7

## 1. Production-grade distributed worker fabric
Add authenticated, mutually authenticated worker registration, heartbeats, remote execution leases, queue partitioning, worker capabilities and secure cross-machine cancellation. Make local-first scheduling the default with remote spillover only when policy permits.

## 2. World-model expansion
Add temporal entity history, causal edges, confidence decay, contradiction resolution and event replay. Persist why a world-state fact changed, not merely its latest value.

## 3. True sandbox tiering
Introduce explicit OS-isolation classes: local trusted, restricted workspace, namespace/bubblewrap, and hardened external sandbox/container. Fail closed for untrusted code when the required isolation tier is unavailable.

## 4. Autonomous evaluation lab
Give JARVIS an automated benchmark harness for tool success, hallucination, latency, resource use, prompt-injection resistance and regression detection. Feed results into ModelIntelligence without permitting unsafe self-promotion.

## 5. Memory lifecycle governance
Add per-namespace retention, encryption-key rotation generations, cryptographic deletion verification, index-version migrations, memory compaction and recovery snapshots.

## 6. Multimodal perception loop
Unify screenshots, vision, speech, documents and UI state into a time-bounded perception graph that agents can query without bypassing content-trust boundaries.

## 7. Computer-use verification loop
Require observe → act → verify for desktop actions, with duplicate-action protection, UI-state hashes, action idempotency and rollback/undo strategies where available.

## 8. Self-improvement canary system
Run generated changes through isolated build/test/security environments, then canary only the changed subsystem before promotion. Automatically revert on health, performance or security regression.

## 9. Full supply-chain security
Add pinned/hash-verified dependency lock files, SBOM generation, vulnerability scanning in CI, signed release manifests and reproducible build metadata.

## 10. Formal policy testing
Generate adversarial policy cases automatically: confused deputy, cross-session access, capability escalation, malformed mission grants, SSRF redirect chains, plugin traversal, output-schema attacks and cancellation races.
