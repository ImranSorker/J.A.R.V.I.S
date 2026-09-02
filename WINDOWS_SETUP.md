# JARVIS 12.0.2 — Windows 11

## Base install

Use **64-bit Python 3.12.x** for the most predictable native-model compatibility.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-windows.txt
.\.venv\Scripts\python.exe main.py --doctor
```

`requirements-windows.txt` intentionally does **not** install `llama-cpp-python` automatically. On Windows, native llama.cpp can require a matching pre-built CUDA wheel or a local CMake/MSVC build. The current llama-cpp-python project publishes pre-built CUDA wheels for Python 3.10–3.12 for supported CUDA versions, including 11.8, 12.1–12.5 and 13.0/13.2. Choose the wheel matching the CUDA runtime you intend to use.

For example, for CUDA 12.1:

```powershell
.\.venv\Scripts\python.exe -m pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

Then run:

```powershell
.\.venv\Scripts\python.exe main.py --doctor
```

## Start

CLI:

```powershell
.\.venv\Scripts\python.exe main.py
```

GUI:

```powershell
.\.venv\Scripts\python.exe main.py --gui
```

or use:

```powershell
.\run_jarvis.ps1
```

## Windows security note

Linux JARVIS can use Bubblewrap/Firejail for stronger OS-level isolation. Windows does not provide an equivalent through the Python standard library. JARVIS therefore uses a constrained child-process fallback on Windows with a cleaned environment, workspace confinement and timeouts. This is **not** a hostile-code sandbox. High-risk execution remains approval-gated.

## Model directory

Place GGUF models in:

```text
data\models\
```

JARVIS will discover `.gguf` files automatically.


## Using an already-running local llama-server

JARVIS V12.0.2 includes an optional provider-neutral OpenAI-compatible adapter. It does not import or require LM Studio. If a local llama-server is listening on `127.0.0.1:52851/v1`, run `scripts\run_with_llama_server.ps1`, enter the server API key when prompted, and JARVIS will use the server as a model backend. The key is kept only in the current process environment.

For fully independent inference, install a compatible `llama-cpp-python` CUDA build and JARVIS will use the native GGUF backend directly.
