# JARVIS v11.1.0 — Flet UI & Platform Compatibility Audit

## Scope

Focused review of the Flet UI, packaging configuration, Windows/Linux desktop runtime assumptions, and Android packaging/runtime compatibility.

## Fixed

1. Flet build entrypoint now explicitly targets `gui/flet_app.py`; previously Flet could resolve the project's `main.py` instead of the GUI entrypoint.
2. Desktop and Android dependency sets are separated in `pyproject.toml`. Android no longer bundles JARVIS server/native/voice/browser dependencies.
3. Android/mobile UI is now an API-client mode and does not import `main.py`/`JARVISCore`.
4. Mobile API connection is configurable from the UI (URL + token) rather than assuming `127.0.0.1`, which points to the phone itself on Android.
5. API credentials entered in mobile mode remain in process memory; they are not persisted by the UI.
6. Flet integration tests were added using the official `flet.testing`/`flet test` model and stable control keys.
7. `asyncio_mode = "auto"` and `flet[test]` development dependency were added for Flet integration tests.
8. Linux desktop flavor is configured globally as `full` so the desktop build includes Flet audio/video support required by voice/media features.
9. Packaged desktop config loading now reads the bundled `config.json` via `__file__` rather than assuming the current working directory is the source directory.
10. JARVIS project-root-dependent self-awareness/self-edit setup now uses the source/project root rather than the Flet writable data directory.
11. Existing chat, model, persona, refresh, and workflow controls retain explicit keys for automated UI testing.

## Validation performed in this environment

- Python compilation: PASS
- Full JARVIS tests: **102 passed, 1 skipped**
- Platform/static compatibility tests: PASS
- UI compatibility tests: PASS
- Flet integration test definitions: collected as optional; skipped here because Flet/Flutter test host is not installed in the audit container.
- TOML parsing: PASS

## Required real-device commands

Flet 0.86+ supports real integration tests that build the app and drive it on the target platform.

### Linux

`flet test linux`

### Windows

`flet test windows`

### Android emulator/device

`flet devices`

`flet test android --device-id <DEVICE_ID>`

Golden screenshots can be recorded with `--update-goldens` and are platform/device specific.

## Platform design

### Windows

Full local JARVIS runtime is intended. Flet's Windows packaging/build is performed on Windows. Native Python packages such as `llama-cpp-python`, audio drivers, and browser dependencies must be validated on the target machine.

### Linux

Full local JARVIS runtime is intended. Flet's Linux full desktop flavor is selected because voice/media features need audio/video support. Supported Flet desktop distributions should be used.

### Android

Android is intentionally a **remote-control/API client**, not a local full JARVIS runtime. This avoids bundling server-only/native desktop dependencies that are not appropriate for Android. The Android app requires a reachable JARVIS API endpoint and a valid API token.

The Android build targets `arm64-v8a`, `x86_64`, and `armeabi-v7a`. It does not target 32-bit x86.

## Remaining limitations

1. A real Flet Flutter integration run could not be executed in this audit container because Flet/Flutter/Android SDK/device infrastructure is unavailable and package installation has no network access.
2. Windows and Linux native dependency builds are platform-specific and require validation on their respective hosts.
3. Android local model inference, shell execution, browser automation, and voice capture are not exposed as local features; they remain server-side capabilities through the API architecture.
4. Mobile API deployment should use HTTPS in production. Plain HTTP may require explicit Android cleartext configuration and is not recommended for internet-facing deployments.
5. The mobile API token is intentionally not persisted. Users must enter it again after app restart unless an external secure credential-storage layer is added.
6. Browser automation requires Playwright browser binaries to be installed/packaged separately on desktop deployments.
