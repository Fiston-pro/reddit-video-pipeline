"""Configuration loader for YAML config files."""

import yaml
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """Load and access configuration from YAML file."""

    def __init__(self, config_path: str = None):
        """Initialize config loader.

        Args:
            config_path: Path to config.yaml file. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key.

        Args:
            key: Dot-separated key (e.g., 'reddit.subreddit')
            default: Default value if key not found

        Returns:
            Configuration value

        Example:
            >>> config = ConfigLoader()
            >>> config.get('reddit.subreddit')
            'cheating_stories'
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section.

        Args:
            section: Section name (e.g., 'reddit', 'video')

        Returns:
            Dictionary with section configuration
        """
        return self.config.get(section, {})

# Global config instance
config = ConfigLoader()

__all__ = ["ConfigLoader", "config"]
