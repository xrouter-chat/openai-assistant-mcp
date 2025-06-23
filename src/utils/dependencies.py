"""FastMCP dependencies for dependency injection."""
import logging
from typing import Optional

from fastmcp.server.dependencies import get_http_request
from openai import OpenAI
from starlette.requests import Request

from ..config.settings import Settings

logger = logging.getLogger(__name__)


def get_openai_client() -> OpenAI:
    """Get OpenAI client for current request.

    For STDIO transport: Creates client from environment settings.
    For HTTP transport in STATIC mode: Creates client from environment settings.
    For HTTP transport in PASSTHROUGH mode: Creates client from request headers.

    Returns:
        OpenAI client instance

    Raises:
        RuntimeError: If no client is available
        ValueError: If required credentials are missing
    """
    settings = Settings()

    try:
        # Try to get HTTP request - if this fails, we're in STDIO mode
        request: Optional[Request] = None
        try:
            request = get_http_request()
        except Exception:
            # We're in STDIO mode, use settings
            logger.debug("No HTTP request context - using STDIO mode")
            pass

        if request is None:
            # STDIO mode - always use settings
            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required for STDIO mode"
                )

            logger.debug("Creating OpenAI client from environment (STDIO mode)")
            return OpenAI(api_key=settings.OPENAI_API_KEY)

        # HTTP mode
        if settings.MCP_CREDENTIAL_MODE == "STATIC":
            # Use settings even in HTTP mode
            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required in STATIC mode"
                )

            logger.debug("Creating OpenAI client from environment (HTTP STATIC mode)")
            return OpenAI(api_key=settings.OPENAI_API_KEY)

        elif settings.MCP_CREDENTIAL_MODE == "PASSTHROUGH":
            # Get API key from request state (set by middleware)
            api_key = getattr(request.state, "openai_api_key", None)
            if not api_key:
                raise ValueError(
                    "X-OpenAI-API-Key header is required in PASSTHROUGH mode"
                )

            # Create client on the fly
            logger.debug(
                "Creating OpenAI client from request headers (PASSTHROUGH mode)"
            )
            return OpenAI(api_key=api_key)

        else:
            raise ValueError(f"Unknown credential mode: {settings.MCP_CREDENTIAL_MODE}")

    except Exception as e:
        logger.error(f"Failed to get OpenAI client: {e}")
        raise
