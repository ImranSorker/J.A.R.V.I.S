# Changelog

All notable changes to JARVIS are documented in this file.

## [13.0.0] - 2024

### Security Hardening (BREAKING)
- **Changed default security mode to fail-closed**
  - `allow_shell`: false (was: true)
  - `allow_code_execution`: false (was: true)
  - `allow_network`: false (was: true)
  - `require_approval_for_high_risk`: true (was: false)
  - `sandbox_strict_isolation`: true (was: false)
- Added startup validation for required secrets:
  - `JARVIS_API_TOKEN`
  - `JARVIS_SECURITY_SECRET`
- Removed wildcard (`*`) from allowed_capabilities
- Added explicit capability allowlist

### Architecture Improvements
- **Modular package structure**: Split monolithic main.py into focused modules:
  - `jarvis.bootstrap`: Configuration loading, secret validation, fail-closed enforcement
  - `jarvis.lifecycle`: Application lifecycle, graceful shutdown, health monitoring
  - `jarvis.api`: FastAPI application with health endpoints
  - `jarvis.types`: TypedDict and Protocol definitions replacing Any types
- Organized imports by layer with lazy loading for optional dependencies

### Observability & Reliability
- **Added health check endpoints**:
  - `/health/live` - Liveness probe (Kubernetes-compatible)
  - `/health/ready` - Readiness probe with dependency checks
  - `/health` - Combined health status
- HealthStatus dataclass for structured health reporting
- LifecycleManager for graceful shutdown handling

### Developer Experience
- **Quickstart guide**: 5-minute setup instructions (QUICKSTART.md)
- **Docker support**: 
  - Dockerfile with non-root user and health checks
  - docker-compose.yml with environment variable configuration
- Consolidated documentation into single CHANGELOG.md

### Type Safety
- Replaced Any types with proper type definitions:
  - `SecurityConfig` TypedDict
  - `ModelConfig` TypedDict
  - `APIConfig` TypedDict
  - `FullConfig` TypedDict
  - `ModelBackend` Protocol
  - `HealthCheckable` Protocol

---

## [12.8.0] - Previous Release

See previous release notes for v12.8.0 and earlier versions.
