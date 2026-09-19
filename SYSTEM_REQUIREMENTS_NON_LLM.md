# J.A.R.V.I.S. V12.8.0 — System Requirements Without Local LLM Model Weights

## Measurement basis

- Source tree size after the current V12.8.0 frontier batch: measured with `du` at approximately **11 MiB** excluding transient build caches.
- Headless full-runtime certification measured a **maximum resident set size of 184,860 KiB (~180.5 MiB)** in this container. This is a certification-process measurement, not a full production workload ceiling.
- The estimates below deliberately exclude local LLM/GGUF model weights and their VRAM requirements.

## Recommended hardware profiles

| Profile | CPU | RAM | Storage | GPU | Intended use |
|---|---:|---:|---:|---:|---|
| Core minimum | 2 cores | 4 GB | 5 GB free | none | API, orchestration, policy, memory-lite, telemetry |
| Core recommended | 4 cores | 8 GB | 10 GB free | none | Daily backend + Flutter client + light automation |
| Full non-LLM minimum | 4 cores | 8 GB | 15 GB free | optional 2 GB | Voice/browser/desktop/document capabilities without model weights |
| Full non-LLM recommended | 6–8 cores | 16 GB | 25 GB free | optional 4–8 GB | Persistent memory, embeddings, voice, browser, desktop, profiling and parallel missions |
| Developer/AI engineering | 8+ cores | 32 GB | 50+ GB free | 8–16 GB preferred | Embeddings/rerankers, vision processing, benchmarks, builds and multiple workers |

## Software baseline

- Python **3.12–3.13** for the authoritative backend.
- Flutter/Dart for the first-party GUI.
- Windows 11 or modern Linux recommended.
- Optional capability runtimes are isolated in requirement profiles; the core backend does not require local LLM runtimes.

## Storage planning

The source tree itself is small, but persistent operation can consume substantially more storage through:

- SQLite/LanceDB memory stores
- document indexes and embeddings
- browser caches
- screenshots and media
- telemetry/trace retention
- model metadata and experiment history
- recovery snapshots

For a long-lived personal installation, **25 GB free** is a sensible baseline even without storing local LLM weights. For development and extensive RAG/media/benchmark workloads, **50 GB+ free** is preferable.

## GPU planning without LLM inference

GPU hardware is **not mandatory** for the core J.A.R.V.I.S. backend. A discrete GPU becomes useful for optional workloads such as:

- computer vision
- OpenCV processing
- embedding/reranking acceleration where supported
- media processing
- GPU telemetry and hardware-aware scheduling

These are separate from local LLM inference and do not imply that an LLM model must be loaded.

## Practical target for the current PC class

A system around a modern 8-core CPU, **16 GB RAM**, SSD storage, and an NVIDIA GPU in the 8–16 GB VRAM range is comfortably above the recommended non-LLM baseline. The main constraint on such a machine becomes workload concurrency and optional model/embedding/media assets, not the J.A.R.V.I.S. core runtime itself.

## Important limitation

The measured ~180.5 MiB RSS is from the automated headless certification workload and should not be interpreted as a hard maximum. Flutter rendering, Playwright, embeddings, Whisper, OpenCV, document processing, large RAG indexes and concurrent missions can materially raise RAM and storage usage.
