# J.A.R.V.I.S. V12.8.0 internal foundation milestone — Foundation Stabilization

## Purpose
V12.8.0 internal foundation milestone is a stabilization release focused on lifecycle correctness, permanent kernel integration, runtime capability discovery, configuration validation, and release reproducibility.

## Changes
- Secure-by-default runtime configuration: guarded mode, no shell/code/network by default, explicit high-risk approval, strict isolation.
- Added `core.capability_registry` for deterministic optional-capability discovery.
- JARVISCore now starts and closes the kernel runtime and bridges core events into the kernel event journal without a strong-reference cycle.
- kernel event handlers now log failures instead of silently swallowing exceptions.
- Added idempotent lifecycle cleanup to persistent SQLite stores and a final core-owned resource sweep.
- Added kernel runtime/event-store lifecycle APIs and idempotency regression coverage.
- Fixed test file-handle ownership in token accounting tests.
- Version metadata is aligned at 12.8.0 internal milestone.

## Verification
- `python -m compileall -q .` — PASS
- `python -m pytest -q` — 286 passed, 3 skipped in the available environment
- `scripts/service_contract_check.py` — PASS
- `scripts/smoke_test.py` — PASS

The three skips are environment-dependent Flet runtime tests because the audit environment does not have the Flet runtime installed.
