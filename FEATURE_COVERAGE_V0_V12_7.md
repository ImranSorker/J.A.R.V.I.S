# J.A.R.V.I.S. Feature Coverage — V0 through V12.7

## Verification rule

Coverage is based on source actually available in the project archive and the project conversation context available to this engineering session. Exact V0–V8 source archives are not present, so those releases cannot be certified by file-level comparison.

## Capability continuity matrix

| Capability family | Early project lineage | V12.7 status |
|---|---|---|
| Core assistant/chat | foundational | Integrated |
| Persona / identity | early releases | Integrated |
| Local model inference | V9+ | Integrated |
| Model discovery | V9+ | Integrated |
| Model router | V9+ | Integrated |
| Dual-brain / specialized routing concepts | project roadmap | Integrated through model intelligence/router/swarm |
| Agent orchestration | V9+ | Integrated |
| Agent swarm | later V12 roadmap + DeepSeek workspace | Integrated |
| RAG | V9+ | Integrated |
| Unified memory | V9+ | Integrated |
| Cryptographic memory namespaces | V12.6.5 | Integrated |
| Memory governance / retention | V12.7 | Integrated |
| Knowledge graph | V12.x | Integrated |
| Temporal world model | V12.7 | Integrated |
| Voice input/STT | V9+ | Integrated when optional backend installed |
| TTS | V9+ | Integrated when optional backend installed |
| Wake-word / conversation loop | V9+ | Integrated |
| Vision/multimodal contracts | V12.x | Integrated |
| Computer use | V12.x/V12.7 | Integrated through optional adapter |
| Proactive cognition | V12.6.5 | Integrated |
| Autonomous missions | V12.6.5 | Integrated |
| Mission budgets | V12.6.5 | Integrated |
| Recovery swarm | V12.6.5 | Integrated |
| Self-healing | V10+ | Integrated |
| Self-improvement | V10+ | Integrated |
| Self-edit guard | V12.x | Integrated |
| Canary self-improvement | V12.7 | Integrated |
| Deep learning | project roadmap/V12 | Integrated |
| Continual learning | V12.x | Integrated |
| LoRA/training | V12.x | Integrated when optional ML stack installed |
| Model benchmarking | V12.x | Integrated |
| Adaptive model intelligence | V12.6.5/V12.7 | Integrated |
| GPU scheduling | V12.x | Integrated |
| Multi-GPU runtime | V12.x | Integrated |
| Hardware profiling | V12.x | Integrated |
| Device gateway | V12.6.5 | Integrated |
| Distributed worker leases | V12.7 | Integrated |
| Signed remote task dispatch | V12.7 | Integrated |
| Unified execution broker | V12.6.x | Integrated |
| Hardened OS sandbox | V12.7 | Integrated |
| Plugin isolation | V12.x | Integrated |
| Network/SSRF controls | V12.x | Integrated |
| Prompt injection/content trust | V12.x | Integrated |
| Adversarial security laboratory | V12.7 | Integrated |
| Supply-chain/SBOM audit | V12.7 | Integrated |
| Structured telemetry | V12.x | Integrated |
| Health/readiness/metrics | V12.x | Integrated |
| Flet desktop UI | V9+ | Integrated; target-environment validation required |
| API/MCP | V12.x | Integrated |
| Workspace-safe file handling | V12.x | Integrated |
| Data pipeline | V12.x + DeepSeek workspace | Integrated |

## Historical source result

Exact Python path preservation in the accessible archives:

- V12.1.2: 136/136
- V12.3.0: 156/156
- V12.4.1: 159/159
- V12.6.0: 169/169
- V12.6.1: 183/183

Older V9–V11 releases contain many renamed/replaced modules. Functional continuity is therefore evaluated by successor architecture rather than pretending exact filenames are unchanged.

V0–V8 remain unverified because their source archives are not accessible in this project workspace.
