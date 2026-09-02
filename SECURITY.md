# JARVIS Security Baseline

JARVIS is fail-closed by default.

## Required secrets

Set these as environment variables; never commit them:

- `JARVIS_API_TOKEN`: at least 32 random characters. Required for every API endpoint except health/docs.
- `JARVIS_SECURITY_SECRET`: at least 32 random characters. Used to sign short-lived approval tokens.
- `JARVIS_DISTRIBUTED_TOKEN`: strong random token if distributed mode is enabled.

Example generation:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## High-risk actions

Shell/process execution, source modification, browser control, filesystem writes, network access, camera and microphone access require an explicit capability grant and a cryptographically signed, short-lived approval token.

Legacy strings such as `APPROVE-test` are intentionally rejected.

## Deployment

- Bind the API to `127.0.0.1` unless a reverse proxy and authentication boundary are configured.
- Do not set CORS to `*`.
- Do not enable shell/network capabilities unless they are actually required.
- Run generated code only inside a real OS/container sandbox for untrusted workloads. The bundled validator is a validation aid, not a security boundary.
- Keep the workspace and audit log on a filesystem writable only by the JARVIS service account.
