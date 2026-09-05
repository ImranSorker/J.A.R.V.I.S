# J.A.R.V.I.S. V12.8.0 — Kernel Upgrade

JARVIS V12.8.0 is a proactive, policy-governed autonomous assistant platform integrating model routing, memory, RAG/content trust, agent swarm execution, bounded data pipelines, durable missions/jobs, browser/network policy, secure subprocess execution, and a Flet command center.

## Run

```bash
python -m pip install -e '.[dev]'
python main.py --doctor
python main.py
python main.py --gui
python main.py --api
```

The default configuration enables bounded autonomous operation. Autonomy is budgeted by mission runtime, agents, parallelism, network requests, CPU, memory, file writes, and external actions. High-impact irreversible actions remain subject to explicit authority rules.

## Verification

- `python -m compileall -q .` — PASS
- `python scripts/verify_release.py dist/JARVIS_V12.8.0_SUPREME.zip` — PASS
- `pytest -q --disable-warnings` — **279 passed, 3 skipped**
- Skipped tests require the Flet runtime, which was unavailable in the audit environment.
- Python source contains no TODO/FIXME/NotImplemented markers or bare `pass` placeholders.
- Release manifest is generated from final source contents and excludes itself.

## Platform-dependent components

Native model inference, GPU acceleration, browser automation, voice I/O, computer-use drivers, and target-platform Flet rendering require their platform-specific dependencies and hardware for final end-to-end validation.

See `V12.8.0_SUPREME_REPORT.md` for the complete hardening and integration report.


## V12.8/V13 kernel
The runtime now includes a durable event journal, default-deny capability firewall, deterministic task DAG, and a V13 kernel facade while preserving the V12 subsystem APIs. See `V12_8_V13_ARCHITECTURE.md`.
