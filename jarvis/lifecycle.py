"""Lifecycle module - Application lifecycle management.

Handles:
- Startup sequence
- Graceful shutdown
- Health monitoring
- Signal handling
"""

from __future__ import annotations

import asyncio
import logging
import signal
import sys
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)


class AppState(Enum):
    """Application state machine."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    DEGRADED = "degraded"
    SHUTTING_DOWN = "shutting_down"
    STOPPED = "stopped"


@dataclass
class HealthStatus:
    """Health check result."""

    healthy: bool
    checks: dict[str, bool] = field(default_factory=dict)
    message: str = ""


class LifecycleManager:
    """Manages application lifecycle with graceful shutdown support."""

    def __init__(self) -> None:
        self.state = AppState.INITIALIZING
        self._shutdown_handlers: list[Callable[[], Any]] = []
        self._health_checks: dict[str, Callable[[], bool]] = {}
        self._lock = threading.Lock()
        self._start_time: float | None = None

    def register_shutdown(self, handler: Callable[[], Any]) -> None:
        """Register a shutdown handler to be called on exit.
        
        Handlers are called in reverse order of registration.
        """
        self._shutdown_handlers.append(handler)
        logger.debug("Registered shutdown handler: %s", handler.__name__)

    def register_health_check(
        self, name: str, check: Callable[[], bool]
    ) -> None:
        """Register a health check function."""
        self._health_checks[name] = check
        logger.debug("Registered health check: %s", name)

    def get_health(self) -> HealthStatus:
        """Run all health checks and return status."""
        checks = {}
        all_healthy = True
        
        for name, check_fn in self._health_checks.items():
            try:
                result = check_fn()
                checks[name] = result
                if not result:
                    all_healthy = False
            except Exception as exc:
                logger.error("Health check %s failed: %s", name, exc)
                checks[name] = False
                all_healthy = False
        
        return HealthStatus(
            healthy=all_healthy,
            checks=checks,
            message="All checks passed" if all_healthy else "Some checks failed"
        )

    def startup(self) -> None:
        """Mark application as started."""
        with self._lock:
            self.state = AppState.RUNNING
            self._start_time = time.time()
            logger.info("Application started successfully")

    def mark_degraded(self) -> None:
        """Mark application as running in degraded mode."""
        with self._lock:
            if self.state == AppState.RUNNING:
                self.state = AppState.DEGRADED
                logger.warning("Application running in degraded mode")

    def shutdown(self) -> None:
        """Perform graceful shutdown."""
        with self._lock:
            if self.state in (AppState.SHUTTING_DOWN, AppState.STOPPED):
                return
            self.state = AppState.SHUTTING_DOWN
        
        logger.info("Initiating graceful shutdown...")
        
        # Call shutdown handlers in reverse order
        for handler in reversed(self._shutdown_handlers):
            try:
                logger.debug("Calling shutdown handler: %s", handler.__name__)
                handler()
            except Exception as exc:
                logger.error("Shutdown handler %s failed: %s", handler.__name__, exc)
        
        with self._lock:
            self.state = AppState.STOPPED
        
        uptime = time.time() - self._start_time if self._start_time else 0
        logger.info("Shutdown complete. Uptime: %.2f seconds", uptime)

    def setup_signal_handlers(self) -> None:
        """Setup Unix signal handlers for graceful shutdown."""
        
        def signal_handler(signum: int, frame: Any) -> None:
            sig_name = signal.Signals(signum).name
            logger.info("Received signal %s, initiating shutdown", sig_name)
            self.shutdown()
            sys.exit(0)
        
        # Register for SIGINT and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.debug("Signal handlers registered")


# Global lifecycle instance
_lifecycle: LifecycleManager | None = None


def get_lifecycle() -> LifecycleManager:
    """Get or create the global lifecycle manager."""
    global _lifecycle
    if _lifecycle is None:
        _lifecycle = LifecycleManager()
    return _lifecycle
