"""
Settings module for the project.

This module provides a centralized configuration object for the project.
It loads environment variables from the .env file and makes them available as attributes.

Example:
    from service.config import settings
    print(settings.environment)
"""
import logging

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServiceSettings(BaseSettings):
    """
    Master settings class that combines all configuration sub-settings.

    This class loads environment variables from:
    1. System environment variables (highest priority)
    2. .env file in the project root
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = Field(
        default="not defined in the .env file",
        description="Current environment (local, dev, stage, prd)",
    )

    logging_level: int = Field(
        default=logging.INFO,
        alias="LOGGING_LEVEL",
        description="Root logger level",
    )
    third_party_loggers_level: int = Field(
        default=logging.INFO,
        alias="THIRD_PARTY_LOGGERS_LEVEL",
        description="Third-party loggers level",
    )
    service_name: str = Field(
        default="service_name is not defined in the .env file",
        alias="SERVICE_NAME",
        description="Service name for logging",
    )

    @field_validator("logging_level", "third_party_loggers_level")
    @classmethod
    def validate_log_level(cls, v: int) -> int:
        """Validate logging level is valid."""
        valid_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
        if v not in valid_levels:
            raise ValueError(
                f"Logging level must be one of {valid_levels}, got {v}",
            )
        return v