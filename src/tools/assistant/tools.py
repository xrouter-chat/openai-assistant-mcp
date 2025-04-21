"""OpenAI Assistant API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, cast

from openai import OpenAI

from ...config.settings import Settings
from .models import (
    AssistantObject,
    CreateAssistantRequest,
    ModifyAssistantRequest,
    ResponseFormat,
    Tool,
    ToolResources,
)

logger = logging.getLogger("openai-assistant-mcp")
settings = Settings()
client = OpenAI()


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
) -> Dict[str, Any]:
    """
    Create an assistant.

    Args:
        model: ID of the model to use
        name: Optional name of the assistant (max 256 chars)
        description: Optional description of the assistant (max 512 chars)
        instructions: Optional system instructions (max 256k chars)
        tools: Optional list of tools (max 128 tools)
        tool_resources: Optional resources for tools
        metadata: Optional key-value pairs (max 16 pairs)
        temperature: Optional sampling temperature (0-2)
        top_p: Optional nucleus sampling parameter (0-1)
        response_format: Optional output format specification
        reasoning_effort: Optional reasoning effort level (low/medium/high)

    Returns:
        Dict containing created assistant data
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

    validated = AssistantObject.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump()
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)


def get_assistant(assistant_id: str) -> Dict[str, Any]:
    """
    Get assistant by ID.

    Args:
        assistant_id: The ID of the assistant to retrieve

    Returns:
        Dict containing assistant data
    """
    logger.info(f"Getting assistant {assistant_id}")

    response = client.beta.assistants.retrieve(assistant_id)
    return cast(Dict[str, Any], AssistantObject.model_validate(response).model_dump())


def list_assistants() -> Dict[str, Any]:
    """
    List assistants.

    This is an MCP resource since it takes no arguments.

    Returns:
        Dict containing list of assistants
    """
    logger.info("Listing assistants")

    response = client.beta.assistants.list()
    return cast(
        Dict[str, Any],
        {
            "data": [
                AssistantObject.model_validate(a).model_dump() for a in response.data
            ]
        },
    )


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
) -> Dict[str, Any]:
    """
    Modify an assistant.

    Args:
        assistant_id: The ID of the assistant to modify
        model: Optional ID of the model to use
        name: Optional name of the assistant (max 256 chars)
        description: Optional description of the assistant (max 512 chars)
        instructions: Optional system instructions (max 256k chars)
        tools: Optional list of tools (max 128 tools)
        tool_resources: Optional resources for tools
        metadata: Optional key-value pairs (max 16 pairs)
        temperature: Optional sampling temperature (0-2)
        top_p: Optional nucleus sampling parameter (0-1)
        response_format: Optional output format specification
        reasoning_effort: Optional reasoning effort level (low/medium/high)

    Returns:
        Dict containing modified assistant data
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
    return cast(Dict[str, Any], AssistantObject.model_validate(response).model_dump())


def delete_assistant(assistant_id: str) -> Dict[str, Any]:
    """
    Delete an assistant.

    Args:
        assistant_id: The ID of the assistant to delete

    Returns:
        Dict containing deletion status
    """
    logger.info(f"Deleting assistant {assistant_id}")

    response = client.beta.assistants.delete(assistant_id)
    return cast(Dict[str, Any], {"id": response.id, "deleted": response.deleted})
