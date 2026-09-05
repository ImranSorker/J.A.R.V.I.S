"""Type definitions for JARVIS.

Replaces Any types with proper TypedDict and Protocol definitions
for better type safety and IDE support.
"""

from __future__ import annotations

from typing import Any, Literal, Protocol, TypedDict


class ModelConfig(TypedDict, total=False):
    """Configuration for a model backend."""

    n_ctx: int
    n_batch: int
    n_gpu_layers: int
    timeout: int
    flash_attn: bool


class SecurityConfig(TypedDict, total=False):
    """Security configuration settings."""

    allow_code_execution: bool
    allow_network: bool
    allow_shell: bool
    allowed_capabilities: list[str]
    allowed_executables: list[str]
    audit_log: str
    fail_closed: bool
    high_risk_capabilities: list[str]
    mode: Literal["restricted", "autonomous", "development"]
    require_approval_for_high_risk: bool
    sandbox_strict_isolation: bool
    workspace_root: str


class APIConfig(TypedDict, total=False):
    """API server configuration."""

    host: str
    port: int
    cors_origins: list[str]
    rate_limit: str


class MemoryConfig(TypedDict, total=False):
    """Memory subsystem configuration."""

    db_path: str | None
    embedding_model: str
    lance_path: str
    max_history: int
    max_sessions: int


class BudgetConfig(TypedDict, total=False):
    """Autonomy budget limits."""

    max_agents: int
    max_cpu_seconds: int
    max_external_actions: int
    max_files_written: int
    max_memory_mb: int
    max_network_requests: int
    max_parallel_tasks: int
    max_runtime_seconds: int


class TokenPrice(TypedDict):
    """Token pricing information."""

    prompt_per_1k: float
    completion_per_1k: float


class ObservabilityConfig(TypedDict, total=False):
    """Observability and monitoring configuration."""

    audit_max_mb: int
    audit_retain_days: int
    log_path: str
    max_log_mb: int
    retain_days: int
    token_accounting: dict[str, Any]


class FullConfig(TypedDict, total=False):
    """Complete JARVIS configuration."""

    version: str
    mode: str
    security: SecurityConfig
    api: APIConfig
    memory: MemoryConfig
    autonomy: dict[str, Any]
    brain: dict[str, Any]
    observability: ObservabilityConfig


class Message(Protocol):
    """Protocol for message objects."""

    role: str
    content: str


class ToolResult(Protocol):
    """Protocol for tool execution results."""

    success: bool
    data: Any
    error: str | None


class ModelBackend(Protocol):
    """Protocol for model inference backends."""

    def infer(self, prompt: str, **kwargs: Any) -> str:
        """Run inference on the given prompt."""
        ...

    def stream(self, prompt: str, **kwargs: Any) -> Any:
        """Stream inference results."""
        ...


class HealthCheckable(Protocol):
    """Protocol for components that can be health-checked."""

    def is_healthy(self) -> bool:
        """Return True if the component is healthy."""
        ...
