# JARVIS v11.1.0 — Additional Hardening Audit

## Scope
A fourth-pass review of the fully hardened build, including execution-policy calls, sandbox construction, tool input validation, API input limits, model discovery, plugin promotion, distributed discovery, memory/document ingestion, and self-awareness indexing.

## Findings fixed

1. **ExecutionPolicy argument-order bug**
   - Shell, Python executor, and SecurityExecutor passed arguments to `check()` in the wrong positional order.
   - Fixed with explicit keyword arguments.

2. **Weak bwrap filesystem isolation**
   - The previous bwrap invocation did not hide the host root filesystem.
   - The sandbox now creates an isolated root, exposes only required runtime directories read-only, mounts `/work` read-only, provides a temporary `/tmp`, disables networking, and clears the environment.

3. **Tool schema resource-exhaustion gaps**
   - Added enforcement for string lengths, numeric ranges, and array sizes in ToolRegistry.
   - Tightened shell, browser, web-search, and Python-executor schemas.

4. **Generated-plugin metadata substitution**
   - Promotion now reparses the validated artifact and requires the supplied metadata to exactly match the artifact's embedded `__meta__`.

5. **Distributed discovery did not actually broadcast**
   - Startup now launches a bounded presence-broadcast loop.
   - Broadcast sockets are closed after each send.
   - Empty-auth configurations no longer create a busy loop.

6. **Native model loader symlink/oversize exposure**
   - Symlinked model files are ignored and model files above the size ceiling are skipped.

7. **Self-awareness resource exhaustion**
   - Symlinked and oversized Python files are ignored during indexing.

8. **Document ingestion limits**
   - Chunk size is bounded and extracted text has an additional expansion limit.

9. **Session export filename collisions**
   - Exports now include a random suffix instead of relying only on second-resolution timestamps.

10. **API payload exhaustion**
    - Chat, task, session, self-edit, and tool-generation request fields now have explicit Pydantic size limits.

## Validation
- Python compilation: passed
- Existing + new regression suite: **93/93 passed**
- New regression tests cover execution-policy authorization, plugin metadata binding, generic schema limits, symlinked model rejection, and sandbox root isolation.

## Remaining architectural risks
A real network egress proxy is still preferable to browser-side DNS checks for strongest SSRF guarantees. Same-host filesystem races are also not fully eliminated without OS primitives such as Linux `openat2()`/file-descriptor-relative operations or container isolation.
