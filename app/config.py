from dataclasses import dataclass
import os


@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: str = ""
    base_url: str = ""
    stream: bool = False


@dataclass
class DBConfig:
    connection: str


@dataclass
class Config:
    llm: LLMConfig
    db: DBConfig


# In-memory config storage (overrides environment defaults)
_config_override: Config | None = None


def _get_env_defaults() -> Config:
    """Load default configuration from environment variables."""
    return Config(
        llm=LLMConfig(
            provider=os.environ.get("LYST_LLM_PROVIDER", "anthropic"),
            model=os.environ.get("LYST_LLM_MODEL", "anthropic/claude-sonnet-4-20250514"),
            api_key=os.environ.get("LYST_LLM_API_KEY", ""),
            base_url=os.environ.get("LYST_LLM_BASE_URL", "https://api.anthropic.com"),
            stream=os.environ.get("LYST_STREAM", "true").lower() == "true",
        ),
        db=DBConfig(
            connection=os.environ.get("LYST_DB_CONNECTION", ""),
        ),
    )


def load_config() -> Config:
    """Load config: returns in-memory override if set, otherwise env defaults."""
    if _config_override is not None:
        return _config_override
    return _get_env_defaults()


def save_config(config: Config) -> None:
    """Save config to in-memory storage (session only, not persisted)."""
    global _config_override
    _config_override = config


def reset_config() -> None:
    global _config_override
    _config_override = None

