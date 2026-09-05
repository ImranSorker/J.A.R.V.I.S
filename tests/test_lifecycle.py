"""Tests for lifecycle module."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.lifecycle import (
    AppState,
    HealthStatus,
    LifecycleManager,
    get_lifecycle,
)


class TestAppState:
    """Test application state enum."""

    def test_states_exist(self):
        """All expected states should exist."""
        assert AppState.INITIALIZING.value == "initializing"
        assert AppState.RUNNING.value == "running"
        assert AppState.DEGRADED.value == "degraded"
        assert AppState.SHUTTING_DOWN.value == "shutting_down"
        assert AppState.STOPPED.value == "stopped"


class TestHealthStatus:
    """Test health status dataclass."""

    def test_healthy_status(self):
        """Should create healthy status."""
        status = HealthStatus(healthy=True, message="OK")
        assert status.healthy is True
        assert status.message == "OK"

    def test_unhealthy_status(self):
        """Should create unhealthy status."""
        status = HealthStatus(healthy=False, checks={"db": False})
        assert status.healthy is False
        assert status.checks == {"db": False}


class TestLifecycleManager:
    """Test lifecycle management."""

    def test_initial_state(self):
        """Should start in INITIALIZING state."""
        manager = LifecycleManager()
        assert manager.state == AppState.INITIALIZING

    def test_startup_transition(self):
        """Should transition to RUNNING on startup."""
        manager = LifecycleManager()
        manager.startup()
        assert manager.state == AppState.RUNNING

    def test_shutdown_handlers_called(self):
        """Should call registered shutdown handlers."""
        manager = LifecycleManager()
        called = []
        
        def handler():
            called.append(True)
        
        manager.register_shutdown(handler)
        manager.startup()
        manager.shutdown()
        
        assert len(called) == 1

    def test_health_checks_run(self):
        """Should run registered health checks."""
        manager = LifecycleManager()
        
        def healthy_check():
            return True
        
        def unhealthy_check():
            return False
        
        manager.register_health_check("healthy", healthy_check)
        manager.register_health_check("unhealthy", unhealthy_check)
        
        result = manager.get_health()
        assert result.checks["healthy"] is True
        assert result.checks["unhealthy"] is False
        assert result.healthy is False


class TestGetLifecycle:
    """Test global lifecycle accessor."""

    def test_returns_singleton(self):
        """Should return same instance on repeated calls."""
        lc1 = get_lifecycle()
        lc2 = get_lifecycle()
        assert lc1 is lc2
