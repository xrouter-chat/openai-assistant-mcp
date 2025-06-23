"""Application settings."""
from typing import List, Literal, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Project
    PROJECT_NAME: str = "openai-assistant-mcp"
    VERSION: str = "0.1.0"
    REGISTRY_ID: str = ""

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

    # MCP Credential Mode Settings
    MCP_CREDENTIAL_MODE: Literal["STATIC", "PASSTHROUGH"] = "STATIC"

    @field_validator("MCP_CREDENTIAL_MODE")
    @classmethod
    def validate_credential_mode(cls, v: str) -> str:
        """Validate credential mode."""
        allowed_modes = {"STATIC", "PASSTHROUGH"}
        v_upper = v.upper()
        if v_upper not in allowed_modes:
            raise ValueError(
                f"MCP_CREDENTIAL_MODE must be one of: {', '.join(allowed_modes)}"
            )
        return v_upper

    # MCP Transport Settings
    TRANSPORT: str = "stdio"  # stdio, http, streamable-http, or sse

    @field_validator("TRANSPORT")
    @classmethod
    def validate_transport(cls, v: str) -> str:
        """Validate transport type."""
        allowed_transports = {"stdio", "http", "streamable-http", "sse"}
        if v.lower() not in allowed_transports:
            raise ValueError(
                f"Transport must be one of: {', '.join(allowed_transports)}"
            )
        return v.lower()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
