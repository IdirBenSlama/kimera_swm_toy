"""
Translation Configuration Management
===================================

Handles loading and validation of translation service configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TranslationConfig:
    """Manages translation service configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        if config_path is None:
            # Look for config in multiple locations
            possible_paths = [
                Path("config/translation_config.yaml"),
                Path(__file__).parent.parent.parent.parent / "config" / "translation_config.yaml",
                Path.home() / ".kimera" / "translation_config.yaml",
            ]
            
            for path in possible_paths:
                if path.exists():
                    config_path = str(path)
                    break
            else:
                # Use default configuration
                config_path = None
        
        self.config_path = config_path
        self._config = self._load_config()
        self._resolve_environment_variables()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if self.config_path and Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info(f"Loaded translation config from {self.config_path}")
                return config
            except Exception as e:
                logger.error(f"Failed to load config from {self.config_path}: {e}")
        
        # Return default configuration
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "default_service": "mock",
            "services": {
                "mock": {},
                "google": {
                    "credentials_path": None,
                    "project_id": None,
                    "rate_limit": 10,
                    "batch_size": 100
                },
                "deepl": {
                    "api_key": None,
                    "api_endpoint": "https://api-free.deepl.com/v2",
                    "rate_limit": 5
                },
                "huggingface": {
                    "model_name": "Helsinki-NLP/opus-mt-en-es",
                    "device": "cpu",
                    "cache_dir": "~/.cache/huggingface"
                }
            },
            "cache": {
                "enabled": True,
                "backend": "memory",
                "ttl": 86400,
                "sqlite_path": "cache/translation_cache.db",
                "redis": {
                    "host": "localhost",
                    "port": 6379,
                    "db": 0,
                    "password": None
                }
            },
            "languages": {
                "supported": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "ar"],
                "default_source": None,
                "default_target": "en"
            },
            "performance": {
                "max_concurrent_requests": 10,
                "timeout": 30,
                "retry": {
                    "max_attempts": 3,
                    "backoff_factor": 2,
                    "max_backoff": 60
                }
            },
            "logging": {
                "level": "INFO",
                "log_requests": True,
                "log_cache": True,
                "log_file": "logs/translation.log"
            }
        }
    
    def _resolve_environment_variables(self):
        """Resolve environment variables in configuration."""
        def resolve_value(value):
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                return os.getenv(env_var, value)
            elif isinstance(value, dict):
                return {k: resolve_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_value(v) for v in value]
            return value
        
        self._config = resolve_value(self._config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Dot-separated key path (e.g., "services.google.api_key")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_service_config(self, service: str) -> Dict[str, Any]:
        """Get configuration for a specific service."""
        return self.get(f"services.{service}", {})
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return self.get("cache", {})
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        return self.get("languages.supported", ["en"])
    
    def get_default_service(self) -> str:
        """Get default translation service."""
        return self.get("default_service", "mock")
    
    def is_service_configured(self, service: str) -> bool:
        """Check if a service is properly configured."""
        config = self.get_service_config(service)
        
        if service == "google":
            return bool(config.get("credentials_path") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        elif service == "deepl":
            return bool(config.get("api_key") or os.getenv("DEEPL_API_KEY"))
        elif service == "huggingface":
            return True  # Always available if transformers is installed
        elif service == "mock":
            return True
        
        return False
    
    def get_available_services(self) -> list:
        """Get list of configured and available services."""
        available = []
        
        for service in ["mock", "google", "deepl", "huggingface"]:
            if self.is_service_configured(service):
                # Also check if required libraries are installed
                if service == "google":
                    try:
                        import google.cloud.translate_v2
                        available.append(service)
                    except ImportError:
                        pass
                elif service == "deepl":
                    try:
                        import deepl
                        available.append(service)
                    except ImportError:
                        pass
                elif service == "huggingface":
                    try:
                        import transformers
                        available.append(service)
                    except ImportError:
                        pass
                else:
                    available.append(service)
        
        return available
    
    def validate(self) -> Dict[str, Any]:
        """Validate configuration and return status."""
        status = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "available_services": self.get_available_services()
        }
        
        # Check if any service is configured
        if not status["available_services"]:
            status["errors"].append("No translation services are properly configured")
            status["valid"] = False
        
        # Check default service
        default_service = self.get_default_service()
        if default_service not in status["available_services"]:
            if "mock" in status["available_services"]:
                status["warnings"].append(
                    f"Default service '{default_service}' not available, will use 'mock'"
                )
            else:
                status["errors"].append(f"Default service '{default_service}' not available")
                status["valid"] = False
        
        # Check cache configuration
        cache_config = self.get_cache_config()
        if cache_config.get("enabled") and cache_config.get("backend") == "redis":
            try:
                import redis
            except ImportError:
                status["warnings"].append("Redis caching enabled but redis-py not installed")
        
        return status


# Global configuration instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> TranslationConfig:
    """Get or create global configuration instance."""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = TranslationConfig(config_path)
    
    return _config_instance


def reload_config(config_path: Optional[str] = None):
    """Reload configuration from file."""
    global _config_instance
    _config_instance = TranslationConfig(config_path)