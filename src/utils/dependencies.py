"""MCP dependencies for dependency injection."""
import logging
from typing import Optional

from mcp.server.fastmcp import Context
from openai import OpenAI

from ..config.settings import Settings

logger = logging.getLogger(__name__)


def get_authentication_headers(context: Context) -> dict[str, str]:
    """Get authentication headers from the request context.

    Args:
        context: MCP server context containing request information

    Returns:
        Dictionary of headers with lowercase keys

    Raises:
        RuntimeError: If request context is not available
    """
    request_object = context.request_context.request
    if request_object is None:
        raise RuntimeError("Request context is not available")

    if not hasattr(request_object, "headers"):
        raise RuntimeError("Request object does not have headers")

    headers: dict[str, str] = request_object.headers
    # Convert to lowercase for case-insensitive lookup
    return {k.lower(): v for k, v in headers.items()}


def get_openai_client(context: Optional[Context] = None) -> OpenAI:
    """Get OpenAI client for current request.

    For STDIO transport: Creates client from environment settings.
    For HTTP transport in static mode: Creates client from environment settings.
    For HTTP transport in passthrough mode: Creates client from request headers.

    Args:
        context: MCP server context (required for passthrough mode)

    Returns:
        OpenAI client instance

    Raises:
        RuntimeError: If no client is available
        ValueError: If required credentials are missing
    """
    settings = Settings()

    try:
        if context is None:
            # STDIO mode - always use settings
            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required for STDIO mode"
                )

            logger.debug("Creating OpenAI client from environment (STDIO mode)")
            return OpenAI(api_key=settings.OPENAI_API_KEY)

        # HTTP mode with context available
        if settings.MCP_CREDENTIAL_MODE == "static":
            # Use settings even in HTTP mode
            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required in static mode"
                )

            logger.debug("Creating OpenAI client from environment (HTTP static mode)")
            return OpenAI(api_key=settings.OPENAI_API_KEY)

        elif settings.MCP_CREDENTIAL_MODE == "passthrough":
            # Get API key from request headers
            headers = get_authentication_headers(context)
            api_key = headers.get("x-openai-api-key")

            if not api_key:
                raise ValueError(
                    "X-OpenAI-API-Key header is required in passthrough mode"
                )

            logger.debug(
                "Creating OpenAI client from request headers (passthrough mode)"
            )
            return OpenAI(api_key=api_key)

        else:
            raise ValueError(f"Unknown credential mode: {settings.MCP_CREDENTIAL_MODE}")

    except Exception as e:
        logger.error(f"Failed to get OpenAI client: {e}")
        raise
