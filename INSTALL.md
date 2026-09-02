# JARVIS 10.9.0 installation

## Linux / Kubuntu

```bash
cd JARVIS_V10_8_4_COMPLETE
chmod +x scripts/install_jarvis.sh
./scripts/install_jarvis.sh
source .venv/bin/activate
python scripts/doctor.py
python main.py
```

For NVIDIA/CUDA llama.cpp builds:

```bash
JARVIS_CUDA=1 ./scripts/install_jarvis.sh
```

If you want to skip native llama.cpp during bootstrap:

```bash
JARVIS_INSTALL_NATIVE=0 ./scripts/install_jarvis.sh
```

For browser automation, the installer attempts to install Chromium through Playwright.

## Model installation

Place `.gguf`, `.safetensors`, `.bin` or `.onnx` files under `~/models`, `./models`, or another configured model directory. JARVIS discovers them itself and can route to native backends without requiring Ollama or LM Studio.

## Permission behavior

JARVIS uses a fail-closed capability profile by default. High-risk actions require cryptographically signed, short-lived approval tokens; legacy `APPROVE-...` strings are rejected. See `SECURITY.md`.
