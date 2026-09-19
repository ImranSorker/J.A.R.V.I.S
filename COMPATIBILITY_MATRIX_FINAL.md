# J.A.R.V.I.S. V12.8.0 — Compatibility Matrix

| Layer | Preferred target | Purpose | Certification status |
|---|---|---|---|
| Python | 3.13.x | Cognitive/backend runtime | Headless PASS |
| Flutter/Dart | Flutter 3.47.x generation | First-party GUI | Source updated; target build required |
| Windows | Windows 11 x64 | Primary desktop target | Target-machine certification required |
| Linux | Current mainstream desktop/server Linux | Server/headless runtime | Headless source/runtime PASS; platform certification recommended |
| Android | Flutter + Kotlin platform layer | Mobile/device UI | Target-device certification required |
| Rust | Current stable toolchain | Trusted native runtime | Source contract present; native build required |
| C++ | Current compiler + CUDA where applicable | Inference/GPU runtime | Source contract present; native hardware build required |
| Go | Current stable Go | Distributed services | Source checks PASS |
| TypeScript | Current Node/browser toolchain | Web/browser integration | Source checks PASS |
| Java | Current LTS JDK | JVM integrations | Source checks PASS |
| C# | Current .NET SDK | Windows/.NET integrations | Target build required when SDK is available |
| MCP | 2026-07-28 | Tool/agent protocol | Contract adapter implemented |
| SPIFFE/SPIRE | Current stable | Workload identity | Integration planned |
| WebAuthn | Level 3-capable platform | Operator authentication | Integration planned |
| WASI/WASM | Current runtime | Untrusted plugins | Integration planned |
| OpenTelemetry | Current SDKs | Observability | Core instrumentation present; Profiles integration planned |

## Hardware baseline excluding LLM weights

Recommended workstation: 6–8 CPU cores, 16 GB RAM, 25 GB free SSD. GPU is optional for the core application but recommended for vision/media acceleration and required by some local model runtimes.

## Important

The compatibility matrix distinguishes source compatibility from actual target certification. A language/runtime being represented in the repository does not imply that every compiler or platform was available in the validation container.
