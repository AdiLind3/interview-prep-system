"""Configuration management for interview prep system."""
import os
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for the interview prep system."""

    def __init__(self):
        """Initialize configuration with defaults."""
        self.root_dir = Path(__file__).parent.parent
        self.config_file = self.root_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create defaults.

        Returns:
            Configuration dictionary
        """
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "sql": {
                "exercises_dir": str(self.root_dir / "sql" / "exercises"),
                "solutions_dir": str(self.root_dir / "sql" / "solutions"),
                "tests_dir": str(self.root_dir / "sql" / "tests"),
                "time_limits": {
                    "easy": 15,
                    "medium": 25,
                    "hard": 40
                }
            },
            "python": {
                "exercises_dir": str(self.root_dir / "python" / "exercises"),
                "solutions_dir": str(self.root_dir / "python" / "solutions"),
                "tests_dir": str(self.root_dir / "python" / "tests"),
                "time_limits": {
                    "easy": 15,
                    "medium": 30,
                    "hard": 45
                }
            },
            "flashcards": {
                "data_file": str(self.root_dir / "concepts" / "flashcards" / "cards.json"),
                "study_session_duration": 15,
                "spaced_repetition": {
                    "initial_interval": 1,
                    "easy_multiplier": 2.5,
                    "good_multiplier": 1.3,
                    "hard_multiplier": 1.0
                }
            },
            "progress": {
                "tracker_file": str(self.root_dir / "progress" / "tracker.json"),
                "daily_goals": {
                    "sql_exercises": 5,
                    "python_exercises": 4,
                    "flashcards": 20,
                    "study_time_minutes": 180
                }
            },
            "interview": {
                "date": "2026-02-17",
                "company": "tasq.ai",
                "position": "Junior Data Engineer"
            }
        }

    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Dot-separated key path (e.g., "sql.time_limits.easy")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value


# Global config instance
config = Config()
