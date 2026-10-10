"""
Centralized configuration for Agent Incident Analyzer.

Loads environment variables and provides validated configuration for the application.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    # NVIDIA NIM Configuration
    nvidia_api_key: str = Field(default="", description="NVIDIA API key for LLM access")
    nvidia_model: str = Field(
        default="meta/llama-3.1-405b-instruct",
        description="NVIDIA model name to use"
    )
    nvidia_base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        description="NVIDIA API base URL"
    )

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./data/incident_analyzer.db",
        description="Database connection URL"
    )

    # Application Settings
    app_name: str = Field(default="Agent Incident Analyzer", description="Application name")
    app_env: str = Field(default="development", description="Environment (development/production)")
    log_level: str = Field(default="INFO", description="Logging level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_config(env_file: Optional[str] = None) -> Config:
    """
    Load configuration from environment variables.

    Args:
        env_file: Optional path to .env file. If not provided, will search in current directory.

    Returns:
        Config object with validated settings.

    Raises:
        ValidationError: If required environment variables are invalid.
    """
    # Load .env file if provided
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to load .env from the project root
        project_root = Path(__file__).parent.parent
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)

    return Config()


def validate_llm_config(config: Config) -> None:
    """
    Validate that LLM configuration is complete.

    Raises:
        ValueError: If NVIDIA API key is missing or empty.
    """
    if not config.nvidia_api_key or config.nvidia_api_key == "your_nvidia_api_key_here":
        raise ValueError(
            "NVIDIA_API_KEY is not configured. "
            "Please set it in your .env file or environment variables."
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config object.

    Raises:
        ValidationError: If configuration is invalid.
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
