"""Tests for bootstrap module."""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.bootstrap import (
    ConfigValidationError,
    SecretMissingError,
    load_config,
    setup_logging,
    validate_secrets,
    validate_security_config,
)


class TestValidateSecrets:
    """Test secret validation."""

    def test_missing_secrets_development_mode(self, monkeypatch):
        """Should warn but not raise in development mode."""
        monkeypatch.delenv("JARVIS_API_TOKEN", raising=False)
        monkeypatch.delenv("JARVIS_SECURITY_SECRET", raising=False)
        
        # Should not raise in development mode
        validate_secrets(mode="development")

    def test_missing_secrets_production_mode(self, monkeypatch):
        """Should raise in production mode."""
        monkeypatch.delenv("JARVIS_API_TOKEN", raising=False)
        monkeypatch.delenv("JARVIS_SECURITY_SECRET", raising=False)
        
        with pytest.raises(SecretMissingError):
            validate_secrets(mode="production")

    def test_present_secrets(self, monkeypatch):
        """Should pass when secrets are present."""
        monkeypatch.setenv("JARVIS_API_TOKEN", "test-token")
        monkeypatch.setenv("JARVIS_SECURITY_SECRET", "test-secret")
        
        # Should not raise
        validate_secrets(mode="production")


class TestLoadConfig:
    """Test configuration loading."""

    def test_load_valid_config(self):
        """Should load valid config file."""
        config = load_config("/workspace/config.json")
        assert "security" in config
        assert "api" in config

    def test_load_nonexistent_file(self):
        """Should raise for nonexistent file."""
        with pytest.raises(ConfigValidationError):
            load_config("/nonexistent/config.json")


class TestValidateSecurityConfig:
    """Test security configuration validation."""

    def test_wildcard_rejected(self):
        """Should reject wildcard permissions."""
        config = {"security": {"allowed_capabilities": ["*"]}}
        
        with pytest.raises(ConfigValidationError):
            validate_security_config(config)

    def test_explicit_caps_accepted(self):
        """Should accept explicit capabilities."""
        config = {"security": {"allowed_capabilities": ["calculator", "filesystem.read"]}}
        
        # Should not raise
        validate_security_config(config)
