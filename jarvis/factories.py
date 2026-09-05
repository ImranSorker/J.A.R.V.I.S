"""Factories module - Model, tool, and backend creation.

Provides factory functions for creating:
- Model backends (native, OpenAI-compatible, distributed)
- Tool instances with proper configuration
- Service components with dependency injection
"""

from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class FactoryRegistry:
    """Registry for factory functions."""

    def __init__(self) -> None:
        self._factories: dict[str, Callable[..., Any]] = {}

    def register(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to register a factory function."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._factories[name] = func
            logger.debug("Registered factory: %s", name)
            return func

        return decorator

    def get(self, name: str) -> Callable[..., Any]:
        """Get a factory by name."""
        if name not in self._factories:
            raise KeyError(f"Factory not found: {name}")
        return self._factories[name]

    def create(self, name: str, **kwargs: Any) -> Any:
        """Create an instance using a registered factory."""
        factory = self.get(name)
        logger.info("Creating instance via factory: %s", name)
        return factory(**kwargs)


# Global registry instance
_registry = FactoryRegistry()


def get_registry() -> FactoryRegistry:
    """Get the global factory registry."""
    return _registry


@_registry.register("model_backend")
def create_model_backend(backend_type: str, config: dict[str, Any]) -> Any:
    """Factory for creating model backends.

    Args:
        backend_type: Type of backend ('native', 'openai', 'distributed')
        config: Backend configuration

    Returns:
        Configured model backend instance
    """
    from core.native_backend import NativeInferenceBackend
    from core.openai_compatible_backend import OpenAICompatibleBackend

    if backend_type == "native":
        logger.info("Creating native model backend")
        return NativeInferenceBackend(
            n_ctx=config.get("n_ctx", 8192),
            n_batch=config.get("n_batch", 512),
            n_gpu_layers=config.get("n_gpu_layers", -1),
            timeout=config.get("timeout", 120),
        )
    elif backend_type == "openai":
        logger.info("Creating OpenAI-compatible backend")
        return OpenAICompatibleBackend(
            base_url=config.get("base_url"),
            api_key=config.get("api_key"),
            model=config.get("model"),
            timeout=config.get("timeout", 120),
        )
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")


@_registry.register("tool")
def create_tool(tool_name: str, config: dict[str, Any]) -> Any:
    """Factory for creating tools.

    Args:
        tool_name: Name of the tool to create
        config: Tool configuration

    Returns:
        Configured tool instance
    """
    # Import tools lazily to avoid circular dependencies
    from tools import (
        calculator_tool,
        file_tools,
        shell_tool,
        web_search_tool,
        code_executor_tool,
    )

    tool_map = {
        "calculator": calculator_tool,
        "file": file_tools,
        "shell": shell_tool,
        "web_search": web_search_tool,
        "code_executor": code_executor_tool,
    }

    if tool_name not in tool_map:
        raise ValueError(f"Unknown tool: {tool_name}")

    logger.info("Creating tool: %s", tool_name)
    return tool_map[tool_name]


@_registry.register("security_executor")
def create_security_executor(config: dict[str, Any]) -> Any:
    """Factory for creating security executor.

    Args:
        config: Security configuration

    Returns:
        Configured security executor
    """
    from core.security_executor import SecurityExecutor

    logger.info("Creating security executor")
    return SecurityExecutor(
        allow_shell=config.get("allow_shell", False),
        allow_network=config.get("allow_network", False),
        allow_code_execution=config.get("allow_code_execution", False),
        allowed_capabilities=config.get("allowed_capabilities", []),
        workspace_root=config.get("workspace_root", "data/workspace"),
    )
