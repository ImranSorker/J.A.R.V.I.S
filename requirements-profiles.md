# J.A.R.V.I.S. V12.8.0 Python Requirement Profiles

The Flutter/Dart Command Deck is the only first-party UI. Flet is retired and is not required.

| Profile | Install | Purpose |
|---|---|---|
| Core | `requirements.txt` | Mandatory backend, API, orchestration, policy, events and lightweight telemetry |
| Memory | `requirements-memory.txt` | LanceDB and embedding-backed persistent retrieval |
| Hardware | `requirements-hardware.txt` | NVIDIA/NVML host telemetry |
| AI | `requirements-ai.txt` | Local GGUF inference, Transformers, memory/embedding and hardware support |
| Voice | `requirements-voice.txt` | STT, TTS, microphone and audio processing |
| Browser | `requirements-browser.txt` | Playwright browser automation |
| Desktop | `requirements-desktop.txt` | Screen capture, desktop control and document formats |
| gRPC | `requirements-grpc.txt` | Protobuf/gRPC interoperability and binding generation |
| Windows | `requirements-windows.txt` | Core + NVIDIA + desktop + browser capabilities |
| Linux | `requirements-linux.txt` | Core + NVIDIA + desktop + browser capabilities |
| Development | `requirements-dev.txt` | Core + tests, linting, typing, security and protocol tooling |
| Full | `requirements-full.txt` | All Python capability groups |

Flutter dependencies are managed only by `flutter/pubspec.yaml`.

The product deliberately keeps optional heavyweight runtimes out of the mandatory core profile so a clean backend install remains small and deterministic. Runtime capability discovery reports which optional integrations are actually available.
