# JARVIS 11.1.0 — Engineering & Security Review

## Validation

- Python compilation: PASS
- Regression tests before changes: 79 passed
- Regression tests after hardening: 81 passed

## Findings

### High priority

1. **Approval-token replay cache could reset live nonces**
   - `core/security_tokens.py` previously cleared the entire `_USED` set after 100,000 entries.
   - That could make still-valid approval tokens reusable after cache saturation.
   - Fixed by storing nonce expiry times, pruning only expired entries, and refusing new consumptions when the bounded cache is saturated.

2. **Browser screenshot path lacked request-level SSRF filtering**
   - `navigate()` and `extract()` installed a Playwright route guard, but `screenshot()` did not.
   - A redirect or subresource could therefore bypass the initial `safe_url()` check.
   - Fixed by applying the same request guard to screenshots and guaranteeing page cleanup with `finally`.

### Medium priority

3. **API self-edit could not supply an approval token**
   - `/self-edit` exposed `dry_run=False`, but the request schema had no `approval_token` field.
   - This made configured apply-mode unusable through the API while remaining fail-closed.
   - Fixed by adding an optional approval token to `EditReq` and forwarding it to the existing signed-token gate.

4. **Dashboard output was not HTML-escaped**
   - Model names and persona values were interpolated directly into HTML.
   - The endpoint is authenticated, but escaping is still appropriate defense-in-depth.
   - Fixed with `html.escape()` for displayed dynamic values.

## Architecture assessment

### Strengths

- Clear separation between orchestration, tools, policy, memory, model backends, and API.
- Capability-based authorization is substantially better than command-string blacklists.
- High-risk actions use signed, short-lived, scoped approvals.
- Workspace path validation consistently uses resolved paths and containment checks.
- Shell execution uses argv lists with `shell=False`.
- Self-editing has syntax validation, backups, atomic replacement, approval, and rollback.
- Auto-generated plugins are statically validated and not directly imported.
- The test suite covers many security invariants and the build compiles cleanly.

### Remaining architectural risks

- `tools/code_executor.py` is **not a real sandbox**. Python started with `-I` still has access to OS resources available to the service account. The project's own SECURITY.md correctly says it is not a security boundary. For untrusted generated code, use a container/VM/sandbox with filesystem, network, CPU, memory, and syscall restrictions.
- SSRF protection remains inherently sensitive to DNS/network races. The browser request guard is improved, but a production-grade deployment should enforce egress policy outside the application as well (firewall/container network policy).
- The API uses one bearer token for all authenticated operations rather than per-capability authorization at the HTTP boundary. For multi-user or remotely exposed deployments, add route-level capability scopes and stronger identity/audit attribution.
- The in-memory rate limiter can grow with distinct client IPs. A bounded cache or external rate limiter is preferable for long-running exposed deployments.
- Dependency requirements are mostly lower-bounded rather than pinned/locked. Production deployments should use a lockfile, hashes, and automated dependency/security scanning.
- There are several broad `except Exception` handlers. These are acceptable for optional integrations, but security-sensitive paths should prefer typed exceptions and structured logging so failures cannot silently degrade into unsafe behavior.

## Recommended next hardening phase

1. Put code execution and untrusted plugin execution behind a real OS/container sandbox.
2. Add API integration tests for authentication, rate limiting, CORS, self-edit approval, and every high-risk endpoint.
3. Add route-level capability scopes to the API.
4. Add egress firewall/network policy in addition to application SSRF checks.
5. Introduce a locked dependency set and CI security scanning.
6. Add fuzz/property tests for path handling, URL parsing, token decoding, and tool argument validation.
7. Add structured security events for denied actions, approval issuance, approval consumption, and rollback.
