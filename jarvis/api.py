"""API module - HTTP server with health endpoints.

Provides:
- FastAPI application
- Health check endpoints (/health/live, /health/ready)
- API routes for JARVIS operations
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    checks: dict[str, bool] | None = None
    message: str | None = None


class ReadinessResponse(BaseModel):
    """Readiness check response model."""

    ready: bool
    dependencies: dict[str, str] = {}


# Create FastAPI app
app = FastAPI(
    title="JARVIS API",
    description="JARVIS AI Assistant HTTP API",
    version="13.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health/live", response_model=HealthResponse, tags=["health"])
async def liveness_probe() -> HealthResponse:
    """Liveness probe - is the application running?
    
    Returns 200 if the application process is alive.
    Kubernetes uses this to determine if a pod should be restarted.
    """
    return HealthResponse(
        status="alive",
        message="Application is running"
    )


@app.get("/health/ready", response_model=HealthResponse, tags=["health"])
async def readiness_probe() -> HealthResponse:
    """Readiness probe - is the application ready to serve traffic?
    
    Returns 200 if all dependencies are available and the application
    can serve requests. Kubernetes uses this to determine if traffic
    should be routed to the pod.
    """
    from jarvis.lifecycle import get_lifecycle
    
    lifecycle = get_lifecycle()
    health = lifecycle.get_health()
    
    status_code = 200 if health.healthy else 503
    
    return HealthResponse(
        status="ready" if health.healthy else "not_ready",
        checks=health.checks,
        message=health.message
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    """Combined health check endpoint."""
    from jarvis.lifecycle import get_lifecycle
    
    lifecycle = get_lifecycle()
    health = lifecycle.get_health()
    
    return HealthResponse(
        status="healthy" if health.healthy else "unhealthy",
        checks=health.checks,
        message=health.message
    )


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": "JARVIS API",
        "version": "13.0.0",
        "docs": "/docs",
        "health": "/health",
        "liveness": "/health/live",
        "readiness": "/health/ready"
    }


def create_app() -> FastAPI:
    """Factory function to create the FastAPI application.
    
    This allows for easier testing and configuration.
    """
    return app
