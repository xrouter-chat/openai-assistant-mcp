"""Application context for OpenAI MCP server."""
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from ..config.settings import Settings


@dataclass
class OpenAIAppContext:
    """Application context containing all shared dependencies."""

    settings: Settings
    openai_client: Optional[OpenAI] = None  # Only for static mode
