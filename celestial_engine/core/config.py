"""
Configuration management for the Celestial Engine.
Loads and validates configuration from YAML files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMModelConfig:
    """Configuration for a single LLM model."""
    name: str
    use_cases: list[str]
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SectionConfig:
    """Configuration for an entry section."""
    name: str
    slug: str
    min_words: int
    target_words: int
    max_words: int
    model: str
    requirements: list[str] = field(default_factory=list)


class EngineConfig:
    """Main configuration class for the Celestial Engine."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "engine_config.yaml"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}

        self.load()

    def load(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def reload(self):
        """Reload configuration from file."""
        self.load()

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path to config value (e.g., "llm.models.primary.name")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    # Convenience properties
    @property
    def engine_name(self) -> str:
        return self.get("engine.name", "Celestial Engine")

    @property
    def engine_version(self) -> str:
        return self.get("engine.version", "2.0.0")

    @property
    def llm_base_url(self) -> str:
        return self.get("llm.base_url", "http://127.0.0.1:11434")

    @property
    def llm_timeout(self) -> int:
        return self.get("llm.timeout", 600)

    @property
    def llm_retry_attempts(self) -> int:
        return self.get("llm.retry_attempts", 3)

    def get_model_config(self, model_type: str) -> Optional[LLMModelConfig]:
        """Get configuration for a specific model type."""
        models = self.get("llm.models", {})
        if model_type not in models:
            return None

        model_data = models[model_type]
        return LLMModelConfig(
            name=model_data.get("name", ""),
            use_cases=model_data.get("use_cases", []),
            params=model_data.get("params", {})
        )

    def get_section_configs(self) -> list[SectionConfig]:
        """Get configurations for all entry sections."""
        sections = self.get("entry.sections", [])
        return [
            SectionConfig(
                name=s["name"],
                slug=s["slug"],
                min_words=s["min_words"],
                target_words=s["target_words"],
                max_words=s["max_words"],
                model=s["model"],
                requirements=s.get("requirements", [])
            )
            for s in sections
        ]

    @property
    def target_tier(self) -> str:
        return self.get("entry.target_tier", "CELESTIAL")

    @property
    def min_score(self) -> int:
        return self.get("entry.min_score", 95)

    @property
    def validation_weights(self) -> Dict[str, float]:
        return self.get("validation.criteria", {})

    @property
    def refinement_max_iterations(self) -> int:
        return self.get("refinement.max_iterations", 5)

    @property
    def refinement_strategies(self) -> list[Dict[str, Any]]:
        return self.get("refinement.strategies", [])

    @property
    def batch_parallel_workers(self) -> int:
        return self.get("batch.parallel_workers", 3)

    @property
    def preprocessing_enabled(self) -> bool:
        return self.get("preprocessing.enabled", True)

    @property
    def monitoring_enabled(self) -> bool:
        return self.get("monitoring.enabled", True)

    @property
    def log_level(self) -> str:
        return self.get("monitoring.log_level", "INFO")

    @property
    def entries_dir(self) -> Path:
        return Path(self.get("storage.entries_dir", "data/entries"))

    @property
    def logs_dir(self) -> Path:
        return Path(self.get("storage.logs_dir", "data/logs"))

    @property
    def cache_dir(self) -> Path:
        return Path(self.get("storage.cache_dir", "data/cache"))

    @property
    def checkpoints_dir(self) -> Path:
        return Path(self.get("storage.checkpoints_dir", "data/checkpoints"))

    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.entries_dir,
            self.logs_dir,
            self.cache_dir,
            self.checkpoints_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ready: {directory}")

    def to_dict(self) -> Dict[str, Any]:
        """Get full configuration as dictionary."""
        return self._config.copy()


# Global configuration instance
_global_config: Optional[EngineConfig] = None


def get_config(config_path: Optional[Path] = None) -> EngineConfig:
    """Get global configuration instance."""
    global _global_config

    if _global_config is None:
        _global_config = EngineConfig(config_path)

    return _global_config


def reload_config():
    """Reload global configuration."""
    global _global_config

    if _global_config is not None:
        _global_config.reload()
