"""OpenAI Assistant API tools implementation."""
import logging
from typing import Dict, List, Literal, Optional

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_deleted import AssistantDeleted

from src.config.settings import Settings

from ..models import ResponseFormat, Tool, ToolResources
from .models import CreateAssistantRequest, ModifyAssistantRequest

logger = logging.getLogger(__name__)
settings = Settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_assistant(
    model: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Tool]] = None,
    tool_resources: Optional[ToolResources] = None,
    metadata: Optional[Dict[str, str]] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    response_format: Optional[ResponseFormat] = None,
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None,
) -> Assistant:
    """
    Create an assistant.

    Args:
        model: (REQUIRED) ID of the model to use
        name: Name of the assistant (max 256 chars)
        description: Description of the assistant (max 512 chars)
        instructions: System instructions (max 256k chars)
        tools: List of tools (max 128 tools)
        tool_resources: Resources for tools
        metadata: Key-value pairs (max 16 pairs)
        temperature: Sampling temperature (0-2)
        top_p: Nucleus sampling parameter (0-1)
        response_format: Output format specification
        reasoning_effort: Reasoning effort level (low/medium/high)

    Returns:
        Assistant object from OpenAI SDK
    """
    logger.info("Creating assistant")

    request = CreateAssistantRequest(
        model=model,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        response_format=response_format,
        reasoning_effort=reasoning_effort,
    )

    request_data = request.model_dump()
    logger.info(f"Creating assistant with request data: {request_data}")

    response = client.beta.assistants.create(**request_data)
    logger.info(f"Got response from OpenAI: {response}")
    logger.info(f"Response type: {type(response)}")

    return response


def get_assistant(assistant_id: str) -> Assistant:
    """
    Get assistant by ID.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to retrieve

    Returns:
        Assistant object from OpenAI SDK
    """
    logger.info(f"Getting assistant {assistant_id}")

    response = client.beta.assistants.retrieve(assistant_id)
    return response


def list_assistants() -> SyncCursorPage[Assistant]:
    """
    List assistants.

    This is an MCP resource since it takes no arguments.

    Returns:
        SyncCursorPage[Assistant] from OpenAI SDK
    """
    logger.info("Listing assistants")

    response = client.beta.assistants.list()
    return response


def modify_assistant(
    assistant_id: str,
    model: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Tool]] = None,
    tool_resources: Optional[ToolResources] = None,
    metadata: Optional[Dict[str, str]] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    response_format: Optional[ResponseFormat] = None,
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None,
) -> Assistant:
    """
    Modify an assistant.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to modify
        model: ID of the model to use
        name: Name of the assistant (max 256 chars)
        description: Description of the assistant (max 512 chars)
        instructions: System instructions (max 256k chars)
        tools: List of tools (max 128 tools)
        tool_resources: Resources for tools
        metadata: Key-value pairs (max 16 pairs)
        temperature: Sampling temperature (0-2)
        top_p: Nucleus sampling parameter (0-1)
        response_format: Output format specification
        reasoning_effort: Reasoning effort level (low/medium/high)

    Returns:
        Assistant object from OpenAI SDK
    """
    logger.info(f"Modifying assistant {assistant_id}")

    request = ModifyAssistantRequest(
        model=model,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        tool_resources=tool_resources,
        metadata=metadata,
        temperature=temperature,
        top_p=top_p,
        response_format=response_format,
        reasoning_effort=reasoning_effort,
    ).model_dump(exclude_none=True)

    response = client.beta.assistants.update(assistant_id, **request)
    return response


def delete_assistant(assistant_id: str) -> AssistantDeleted:
    """
    Delete an assistant.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to delete

    Returns:
        AssistantDeleted object from OpenAI SDK
    """
    logger.info(f"Deleting assistant {assistant_id}")

    response = client.beta.assistants.delete(assistant_id)
    return response
