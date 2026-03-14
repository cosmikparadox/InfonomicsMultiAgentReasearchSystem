"""Configuration for the research system."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """System configuration loaded from environment variables."""

    model_config = {"env_prefix": "RESEARCH_", "env_file": ".env"}

    anthropic_api_key: str = Field(default="", description="Anthropic API key")

    # Model selection per agent role
    default_model: str = "claude-sonnet-4-6"
    orchestrator_model: str = "claude-sonnet-4-6"
    critic_model: str = "claude-sonnet-4-6"

    # Research parameters
    max_refinement_rounds: int = 3
    max_tokens_per_request: int = 8192
    critique_threshold: float = 0.7  # findings below this confidence get re-examined

    # Output
    output_dir: str = "data/outputs"
    log_level: str = "INFO"
