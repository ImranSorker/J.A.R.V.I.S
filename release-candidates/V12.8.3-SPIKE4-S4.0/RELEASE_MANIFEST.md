# JARVIS + AURELIS V12.8.3 — Spike 4 / S4.0 Release Candidate

**Status: RELEASE CANDIDATE — NOT A PRODUCTION-CERTIFIED RELEASE**

This record identifies the candidate build prepared for publication. It does **not** contain the source archive itself. The archive asset still needs to be uploaded through a GitHub release/upload-capable surface.

## Build artifact identity

- **Artifact filename:** `JARVIS_AURELIS_MASTER_BUILD_V12.8.3_SPIKE4_S4.0.zip`
- **Reported archive size:** 22,553,213 bytes
- **Reported archive entries:** 4,098
- **Reported archive SHA-256:** `40fa945b13e886b84ca2571eea3e216b611fd491b598efef00807974edc3902b`
- **Baseline date recorded in the accompanying engineering evidence:** 18 October 2026
- **Target release line:** JARVIS V12.8.3 / AURELIS / Spike 4 S4.0

The digest above is copied from the available verification record; consumers should independently recompute SHA-256 after downloading the actual asset.

## Verification evidence recorded for this candidate

The prior engineering report records the following results:

- ZIP integrity and archive-path checks: PASS.
- Python syntax compilation with `python -m compileall -q -f .`: PASS in the reported environment.
- Agent Forge manifest-bridge tests: 10 passed.
- Spike 1 proof-of-concept tests: 48 passed, 4 skipped; native integration and real disposable-VM Bubblewrap acceptance remain unproven.
- Spike 2 proof-of-concept tests: 37 passed, 1 skipped.
- Spike 3 proof-of-concept tests: 37 passed, 2 skipped.
- Gate 2 idempotency overlay integration rerun: 1 passed, 40 failed in the reported disposable integrated copy, with `EventValidationError: event type/name is not registered: Tool.IdempotencyProofRegistered`.

These are scoped engineering results, not proof of full production readiness.

## Release blockers / limitations

1. **Gate 1 — secure execution:** remains open pending real Linux VM acceptance evidence for the required sandbox controls. Keep the shell-enabling feature flag disabled.
2. **Gate 2 — durable side effects/idempotency:** remains open. Do not enable exactly-once writes or blind retries of uncertain effects. The recorded integration failure must be resolved and retested in the canonical worktree.
3. **Donor provenance:** the five donor portfolios in staging are not cleared for production inclusion merely because candidate files are present in the archive. Preserve attribution, license and NOTICE obligations for any retained or adapted source.
4. **Full artifact upload:** the connected GitHub operations available to this publication workflow can create text files and Git objects, but do not provide a binary release-asset upload operation. **The ZIP has not been uploaded to GitHub by this change.**
5. **Agent Forge:** the recorded bundle includes a manifest-bridge prototype; it does not establish that the complete separate Agent Forge runtime is implemented or production-wired.

## Before tagging a public release

- Upload the exact ZIP as a GitHub release asset using an upload-capable client or GitHub web interface.
- Recompute and compare its SHA-256 against the value above.
- Run the final canonical-tree regression suite and document all skipped tests and known failures.
- Close Gate 1 and Gate 2 with acceptance evidence and explicit approvals.
- Complete provenance/license/NOTICE review for every donor-derived file intended for distribution.
- Publish a final release page only after the package asset, checksum, installation instructions, known limitations and required third-party notices are present.

## Scope of this commit

This file is a transparent candidate manifest only. It does not replace the source tree, upload the archive, certify the build, close security gates, or claim that donor provenance is resolved.
