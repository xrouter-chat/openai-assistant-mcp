"""Application settings."""
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Project
    PROJECT_NAME: str = "carrot-quest-mcp"
    VERSION: str = "0.1.0"

    # Host to bind the server to
    # NOTE: Using 0.0.0.0 is intentional for container environments,
    # access control should be handled by container networking and firewalls
    HOST: str = "0.0.0.0"  # nosec

    # Port to bind the server to
    PORT: int = 8001

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    # Carrot Quest Settings
    CARROT_QUEST_API_URL: str = "https://api.carrotquest.io"
    CARROT_QUEST_API_TOKEN: str = ""

    @field_validator("CARROT_QUEST_API_URL")
    @classmethod
    def validate_api_url(cls, v: str) -> str:
        """Validate API URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("API URL must start with http:// or https://")
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Rate Limiting
    RATE_LIMIT_DEFAULT: int = 100  # requests per minute
    RATE_LIMIT_BURST: int = 200

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # Доступные форматы: json, text, structured
    LOG_EXTRA_FIELDS: list[str] = []  # Дополнительные поля для логов

    # Feature Flags
    ENABLE_AUTH: bool = True  # Feature flag for authentication

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
