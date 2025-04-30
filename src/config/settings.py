"""Application settings."""
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"

    # Project
    PROJECT_NAME: str = "openai-assistant-mcp"
    VERSION: str = "0.1.0"

    # Host to bind the server to
    # NOTE: Using 0.0.0.0 is intentional for container environments,
    # access control should be handled by container networking and firewalls
    HOST: str = "0.0.0.0"  # nosec

    # Port to bind the server to
    PORT: int = 8001

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # OpenAI Settings
    OPENAI_API_KEY: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
