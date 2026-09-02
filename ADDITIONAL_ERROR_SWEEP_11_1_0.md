# Additional Error Sweep — JARVIS 11.1.0

Date: 2026-08-27

## Findings fixed

### 1. Flet CI was not exercising packaged/device mode
The Flet CI matrix did not set `FLET_TEST_DEVICE_MODE=1`, so the suite could run in host mode instead of testing the application as a packaged app with embedded Python. CI now sets this globally. Flet documents device mode as the path that runs the app on-device with embedded Python, matching the build/deployment model.

### 2. Android golden test could fail on a clean checkout
The test always compared against `home.png`, but no committed golden existed in the archive. The test now explicitly skips with an actionable message until the canonical Android golden is recorded, while still validating that the captured screenshot is a PNG. Once the golden is committed, comparison becomes enforced.

### 3. UI error assertions were ineffective
The previous tests only asserted that the hidden `error` control existed. They now assert its actual visibility state for success/failure paths.

### 4. API config drift
`config.json` defined `api.cors_origins` and `api.rate_limit`, but `api/server.py` ignored them and used hard-coded/env-only defaults. The server now reads project configuration and allows environment variables to override it.

## Verification

- Python compilation: PASS
- Pytest: **110 passed, 2 skipped**
- 2 skips are expected for unavailable/record-once UI golden/device paths.
- 120 non-test Python files parsed successfully.
- Package cleanup performed before release.

## Remaining environmental validation

Actual Flet desktop/device execution still requires the Flet/Flutter/Android environments. The CI workflow is prepared to execute Linux, Windows, and Android device-mode tests. Android golden comparison requires one canonical emulator/device baseline to be recorded and committed.
