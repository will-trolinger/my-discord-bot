"""Bot configuration settings."""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    """Bot configuration settings loaded from environment variables."""

    # Required settings
    discord_token: str

    # Optional settings with defaults
    command_prefix: str = "!"
    log_level: str = "INFO"
    client_id: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables.

        Returns:
            Settings instance with values from environment.

        Raises:
            ValueError: If required environment variables are missing.
        """
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN environment variable is required")

        return cls(
            discord_token=token,
            command_prefix=os.getenv("COMMAND_PREFIX", "!"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            client_id=os.getenv("CLIENT_ID"),
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Cached Settings instance.
    """
    return Settings.from_env()
