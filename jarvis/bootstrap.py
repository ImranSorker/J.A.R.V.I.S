"""Bootstrap module - Startup validation and configuration.

Handles:
- Configuration loading and validation
- Secret validation (JARVIS_API_TOKEN, JARVIS_SECURITY_SECRET)
- Fail-closed security defaults
- Import error handling
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""

    pass


class SecretMissingError(Exception):
    """Raised when required secrets are missing in production mode."""

    pass


def validate_secrets(mode: str = "development") -> None:
    """Validate required secrets based on mode.
    
    In production mode, fails fast if required secrets are missing.
    In development mode, logs warnings but continues.
    
    Required secrets:
    - JARVIS_API_TOKEN: API authentication
    - JARVIS_SECURITY_SECRET: Security operations
    
    Args:
        mode: Operating mode ('development' or 'production')
        
    Raises:
        SecretMissingError: In production mode if secrets are missing
    """
    required_secrets = [
        "JARVIS_API_TOKEN",
        "JARVIS_SECURITY_SECRET",
    ]
    
    missing = []
    for secret in required_secrets:
        if not os.environ.get(secret):
            missing.append(secret)
    
    if missing:
        msg = f"Required secrets missing: {', '.join(missing)}"
        if mode == "production":
            logger.critical(msg)
            raise SecretMissingError(msg)
        else:
            logger.warning(
                "%s - Running in development mode without required secrets",
                msg
            )


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate configuration from JSON file.
    
    Args:
        config_path: Path to config file. Defaults to ./config.json
        
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigValidationError: If config is invalid or missing required fields
    """
    if config_path is None:
        config_path = Path("config.json")
    elif isinstance(config_path, str):
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise ConfigValidationError(f"Config file not found: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as exc:
        raise ConfigValidationError(f"Invalid JSON in config file: {exc}") from exc
    
    # Validate required top-level keys
    required_keys = ["security", "api", "memory"]
    for key in required_keys:
        if key not in config:
            logger.warning(f"Missing optional config section: {key}")
    
    # Enforce fail-closed security defaults
    security = config.get("security", {})
    if security.get("fail_closed", False):
        # Ensure dangerous capabilities are disabled
        if security.get("allow_shell"):
            logger.warning("Overriding: allow_shell forced to false (fail-closed)")
            security["allow_shell"] = False
        if security.get("allow_code_execution"):
            logger.warning("Overriding: allow_code_execution forced to false (fail-closed)")
            security["allow_code_execution"] = False
        if security.get("allow_network"):
            logger.warning("Overriding: allow_network forced to false (fail-closed)")
            security["allow_network"] = False
    
    return config


def validate_security_config(config: dict[str, Any]) -> bool:
    """Validate security configuration meets fail-closed requirements.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        True if security config is valid
        
    Raises:
        ConfigValidationError: If security config violates policies
    """
    security = config.get("security", {})
    
    # Check for wildcard permissions (security risk)
    allowed_caps = security.get("allowed_capabilities", [])
    if "*" in allowed_caps:
        raise ConfigValidationError(
            "Wildcard '*' in allowed_capabilities is a security risk. "
            "Use explicit capability names."
        )
    
    # Verify high-risk capabilities require approval
    if security.get("require_approval_for_high_risk") is False:
        logger.warning(
            "Security warning: require_approval_for_high_risk is disabled"
        )
    
    return True


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application logging.
    
    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
