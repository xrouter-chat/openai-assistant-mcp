"""Middleware for handling credentials in passthrough mode."""
import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class PassthroughHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to extract credentials from headers in passthrough mode."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Extract OpenAI API key from headers if in passthrough mode."""
        # Check if we have app context from lifespan
        if hasattr(request.app.state, "app_context"):
            app_context = request.app.state.app_context

            if app_context.settings.MCP_CREDENTIAL_MODE == "passthrough":
                # Extract API key from header (case-insensitive)
                api_key = None
                for header_name, header_value in request.headers.items():
                    if header_name.lower() == "x-openai-api-key":
                        api_key = header_value
                        break

                if api_key:
                    request.state.openai_api_key = api_key
                    logger.debug(
                        "Extracted OpenAI API key from X-OpenAI-API-Key header"
                    )
                else:
                    logger.debug("No X-OpenAI-API-Key header found in request")

        response = await call_next(request)
        return response
