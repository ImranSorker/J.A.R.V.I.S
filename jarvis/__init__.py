"""JARVIS v13 - Modular Package Structure.

This package reorganizes the monolithic main.py into focused modules:
- bootstrap: Startup, config validation, secret checks
- lifecycle: Application lifecycle management
- factories: Model, tool, and backend factories
- api: HTTP API server and health endpoints
- cli: Command-line interface
- gui: Graphical user interface (Flet-based)
"""

__version__ = "13.0.0"
