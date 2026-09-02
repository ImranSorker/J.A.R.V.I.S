# J.A.R.V.I.S. 12.1.1 — Command Center Release

JARVIS 12.1.1 is the current Windows-focused integration build. It retains the model-independent cognitive core, LanceDB-first memory, capability-based security, local/remote inference adapters, AION/RAG/workflow foundations, and adds a complete Flet Command Center UI based on the supplied JARVIS dashboard reference.

## Current desktop UI

The Flet desktop surface now mirrors the reference composition:

- top JARVIS status/header with Model Router, Agent Manager, Toolbox and Settings
- left navigation for Dashboard, Chat, Voice, Agents, Tools, Workflows, Projects, Memory, Documents, RAG Library, System Monitor, Resources and Terminal
- central reactor/dashboard hero
- real chat input and streamed JARVIS responses
- model selection wired to `JARVISCore.router`
- file picker constrained to the configured workspace
- live CPU/RAM/GPU/VRAM telemetry when the local sensor APIs are available
- active-model, agent, memory and status cards
- guarded settings, voice controls, RAG workspace and diagnostics views

Flet 0.86.x is the targeted desktop runtime. Flet's documented `ft.run()` entrypoint, `page.run_task()` background-task model, `ProgressRing`, `FilePicker`, and window APIs are used for the current UI architecture.

## Install on Windows

Use a clean Python 3.12/3.13 virtual environment and the Windows dependency profile:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-windows.txt
```

Do **not** install `llama-cpp-python` as part of the basic Windows setup unless you intentionally have the compiler/CUDA toolchain for that native backend. JARVIS can use an OpenAI-compatible local llama-server such as the one provided by LM Studio.

## Run

```powershell
python main.py --doctor
python main.py --gui
```

The preferred full desktop launch is `python main.py --gui` because it constructs and wires the complete `JARVISCore` before starting Flet. `python -m gui.flet_app` is retained as a UI-only/degraded diagnostic entry point.

## Local llama-server

Keep your existing local llama-server running and use the supplied helper when credentials are configured through the process environment:

```powershell
.\scripts\run_with_llama_server.ps1
```

The core treats this as an inference adapter, not as JARVIS's permanent intelligence owner.

## Verification

From the project directory:

```powershell
python -m compileall -q .
python -m pytest -q
```

The repaired source tree currently passes **112 automated tests** in the dependency-rich audit environment used during this build pass.

Live Windows Flet rendering, NVIDIA/CUDA native inference, Playwright browser binaries, microphone/speaker hardware, and multi-machine distributed execution still require validation on the target machine.

## Security

The default security mode remains guarded. Filesystem access is workspace-contained, high-risk capabilities require explicit approval by default, and the UI does not expose an unrestricted terminal. Windows process isolation remains a containment mechanism, not a hostile-code security boundary.

Read `SECURITY.md` before enabling high-risk capabilities.

## Historical audit records

The repository retains the earlier V10/V11 audit and upgrade documents for provenance. They are historical records, not the current release specification. The current release status is captured in `RELEASE_NOTES_V12_0_3.md` and `CURRENT_STATUS_V12_0_3.md`.
