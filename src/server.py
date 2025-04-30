"""OpenAI Assistant MCP Server.

This module implements an MCP server for interacting with OpenAI Assistant API.
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union, cast

from mcp.server.fastmcp import FastMCP

from tools import Metadata, ResponseFormat, Tool, ToolResources
from tools import create_assistant as tools_create_assistant  # Tools; Models
from tools import delete_assistant as tools_delete_assistant
from tools import get_assistant as tools_get_assistant
from tools import list_assistants as tools_list_assistants
from tools import modify_assistant as tools_modify_assistant
from tools.messages import create_message as tools_create_message
from tools.messages import delete_message as tools_delete_message
from tools.messages import get_message as tools_get_message
from tools.messages import list_messages as tools_list_messages
from tools.messages import modify_message as tools_modify_message
from tools.messages.models import MessageContent
from tools.threads import create_thread as tools_create_thread
from tools.threads import delete_thread as tools_delete_thread
from tools.threads import get_thread as tools_get_thread
from tools.threads import modify_thread as tools_modify_thread

# Get logger
logger = logging.getLogger("openai-assistant-mcp")

# Initialize FastMCP server
logger.info("Creating FastMCP server")
mcp = FastMCP("openai-assistant")
logger.info("FastMCP server created: %s", mcp)


# Assistant Tools
@mcp.tool()
def create_assistant(
    model: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Tool]] = None,
    tool_resources: Optional[ToolResources] = None,
    metadata: Optional[Metadata] = None,
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
    """
    return cast(
        Dict[str, Any],
        tools_create_assistant(
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
        ),
    )


@mcp.tool()
def get_assistant(assistant_id: str) -> Dict[str, Any]:
    """
    Get assistant by ID.

    Args:
        assistant_id: The ID of the assistant to retrieve
    """
    return cast(Dict[str, Any], tools_get_assistant(assistant_id))


@mcp.tool()
def list_assistants() -> Dict[str, Any]:
    """List assistants."""
    return cast(Dict[str, Any], tools_list_assistants())


@mcp.tool()
def modify_assistant(
    assistant_id: str,
    model: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Tool]] = None,
    tool_resources: Optional[ToolResources] = None,
    metadata: Optional[Metadata] = None,
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
    """
    return cast(
        Dict[str, Any],
        tools_modify_assistant(
            assistant_id=assistant_id,
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
        ),
    )


@mcp.tool()
def delete_assistant(assistant_id: str) -> Dict[str, Any]:
    """
    Delete an assistant.

    Args:
        assistant_id: The ID of the assistant to delete
    """
    return cast(Dict[str, Any], tools_delete_assistant(assistant_id))


# Thread Tools
@mcp.tool()
def create_thread(
    messages: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, str]] = None,
    tool_resources: Optional[Union[Dict[str, Any], ToolResources]] = None,
) -> Dict[str, Any]:
    """
    Create a thread.

    Args:
        messages: Optional list of messages to start the thread with
        metadata: Optional key-value pairs (max 16 pairs)
        tool_resources: Optional resources for tools
    """
    return cast(Dict[str, Any], tools_create_thread(messages, metadata, tool_resources))


@mcp.tool()
def get_thread(thread_id: str) -> Dict[str, Any]:
    """
    Get thread by ID.

    Args:
        thread_id: The ID of the thread to retrieve
    """
    return cast(Dict[str, Any], tools_get_thread(thread_id))


@mcp.tool()
def modify_thread(
    thread_id: str,
    metadata: Optional[Dict[str, str]] = None,
    tool_resources: Optional[Union[Dict[str, Any], ToolResources]] = None,
) -> Dict[str, Any]:
    """
    Modify a thread.

    Args:
        thread_id: The ID of the thread to modify
        metadata: Optional key-value pairs (max 16 pairs)
        tool_resources: Optional resources for tools
    """
    return cast(
        Dict[str, Any], tools_modify_thread(thread_id, metadata, tool_resources)
    )


@mcp.tool()
def delete_thread(thread_id: str) -> Dict[str, Any]:
    """
    Delete a thread.

    Args:
        thread_id: The ID of the thread to delete
    """
    return cast(Dict[str, Any], tools_delete_thread(thread_id))


# Message Tools
@mcp.tool()
def create_message(
    thread_id: str,
    role: Literal["user", "assistant"],
    content: Union[str, List[MessageContent]],
    attachments: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Create a message.

    Args:
        thread_id: The ID of the thread to create a message for
        role: The role of the entity creating the message ('user' or 'assistant')
        content: The content of the message (string or list of content parts)
        attachments: Optional list of file attachments
        metadata: Optional key-value pairs (max 16 pairs)
    """
    return cast(
        Dict[str, Any],
        tools_create_message(
            thread_id=thread_id,
            role=role,
            content=content,
            attachments=attachments,
            metadata=metadata,
        ),
    )


@mcp.tool()
def get_message(thread_id: str, message_id: str) -> Dict[str, Any]:
    """
    Get message by ID.

    Args:
        thread_id: The ID of the thread the message belongs to
        message_id: The ID of the message to retrieve
    """
    return cast(Dict[str, Any], tools_get_message(thread_id, message_id))


@mcp.tool()
def list_messages(
    thread_id: str,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List messages for a thread.

    Args:
        thread_id: The ID of the thread to list messages for
        limit: Optional limit on number of messages (1-100, default 20)
        order: Optional sort order ('asc' or 'desc', default 'desc')
        after: Optional cursor for pagination (get messages after this ID)
        before: Optional cursor for pagination (get messages before this ID)
        run_id: Optional filter for messages from a specific run
    """
    return cast(
        Dict[str, Any],
        tools_list_messages(
            thread_id=thread_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
            run_id=run_id,
        ),
    )


@mcp.tool()
def modify_message(
    thread_id: str,
    message_id: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Modify a message.

    Args:
        thread_id: The ID of the thread the message belongs to
        message_id: The ID of the message to modify
        metadata: Optional key-value pairs (max 16 pairs)
    """
    return cast(
        Dict[str, Any],
        tools_modify_message(
            thread_id=thread_id,
            message_id=message_id,
            metadata=metadata,
        ),
    )


@mcp.tool()
def delete_message(thread_id: str, message_id: str) -> Dict[str, Any]:
    """
    Delete a message.

    Args:
        thread_id: The ID of the thread the message belongs to
        message_id: The ID of the message to delete
    """
    return cast(Dict[str, Any], tools_delete_message(thread_id, message_id))


# Run Tools
# TODO: Implement run tools
# - create_run
# - get_run
# - modify_run
# - list_runs
# - cancel_run
# - submit_tool_outputs


# Run Step Tools
# TODO: Implement run step tools
# - get_run_step
# - list_run_steps


if __name__ == "__main__":
    mcp.run()
