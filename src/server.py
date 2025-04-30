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
from tools.runs import cancel_run as tools_cancel_run
from tools.runs import create_run as tools_create_run
from tools.runs import create_thread_and_run as tools_create_thread_and_run
from tools.runs import get_run as tools_get_run
from tools.runs import list_runs as tools_list_runs
from tools.runs import modify_run as tools_modify_run
from tools.runs import submit_tool_outputs as tools_submit_tool_outputs
from tools.runs.models import (
    CodeInterpreterTool,
    FileSearchTool,
    FunctionTool,
    ToolChoice,
    TruncationStrategy,
)
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

    This is typically the first step in the workflow before creating threads
    and messages.

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

    Use this to retrieve an assistant's configuration after creation.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to retrieve
    """
    return cast(Dict[str, Any], tools_get_assistant(assistant_id))


@mcp.tool()
def list_assistants() -> Dict[str, Any]:
    """List assistants. Use this to view all available assistants."""
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

    Use this to update an assistant's configuration after creation.

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

    Permanently removes an assistant and its configuration.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to delete
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

    This is done after creating an assistant and before adding messages.
    A thread maintains the conversation state between the assistant and user.

    Args:
        messages: List of messages to start the thread with
        metadata: Key-value pairs (max 16 pairs)
        tool_resources: Resources for tools
    """
    return cast(Dict[str, Any], tools_create_thread(messages, metadata, tool_resources))


@mcp.tool()
def get_thread(thread_id: str) -> Dict[str, Any]:
    """
    Get thread by ID.

    Use this to retrieve a thread's details after creation.

    Args:
        thread_id: (REQUIRED) The ID of the thread to retrieve
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

    Use this to update a thread's metadata or tool resources.

    Args:
        thread_id: (REQUIRED) The ID of the thread to modify
        metadata: Key-value pairs (max 16 pairs)
        tool_resources: Resources for tools
    """
    return cast(
        Dict[str, Any], tools_modify_thread(thread_id, metadata, tool_resources)
    )


@mcp.tool()
def delete_thread(thread_id: str) -> Dict[str, Any]:
    """
    Delete a thread.

    Permanently removes a thread and all its messages.

    Args:
        thread_id: (REQUIRED) The ID of the thread to delete
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
    Create a message in a thread.

    Messages are added to threads to build conversations.
    User messages are added when the user sends input, assistant messages
    when the assistant responds.

    Args:
        thread_id: (REQUIRED) The ID of the thread to create a message for
        role: (REQUIRED) The role of the entity creating the message
            ('user' or 'assistant')
        content: (REQUIRED) The content of the message (string or list of content parts)
        attachments: List of file attachments
        metadata: Key-value pairs (max 16 pairs)
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

    Use this to retrieve a specific message's details from a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to retrieve
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

    Use this to retrieve the conversation history in a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread to list messages for
        limit: Limit on number of messages (1-100, default 20)
        order: Sort order ('asc' or 'desc', default 'desc')
        after: Cursor for pagination (get messages after this ID)
        before: Cursor for pagination (get messages before this ID)
        run_id: Filter for messages from a specific run
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

    Use this to update message metadata after creation.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to modify
        metadata: Key-value pairs (max 16 pairs)
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

    Permanently removes a message from a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to delete
    """
    return cast(Dict[str, Any], tools_delete_message(thread_id, message_id))


# Run Tools
@mcp.tool()
def create_run(
    thread_id: str,
    assistant_id: str,
    model: Optional[str] = None,
    instructions: Optional[str] = None,
    additional_instructions: Optional[str] = None,
    tools: Optional[
        List[Union[CodeInterpreterTool, FileSearchTool, FunctionTool]]
    ] = None,
    metadata: Optional[Dict[str, str]] = None,
    stream: Optional[bool] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    max_completion_tokens: Optional[int] = None,
    max_prompt_tokens: Optional[int] = None,
    response_format: Optional[Union[Literal["auto"], ResponseFormat]] = None,
    tool_choice: Optional[
        Union[Literal["none", "auto", "required"], ToolChoice]
    ] = None,
    truncation_strategy: Optional[TruncationStrategy] = None,
    parallel_tool_calls: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create a run.

    This starts a new run with the specified assistant in a thread.
    A run represents the assistant processing messages and performing actions.

    Args:
        thread_id: (REQUIRED) The ID of the thread to run
        assistant_id: (REQUIRED) The ID of the assistant to use
        model: Model override for this run
        instructions: Instructions override for this run
        additional_instructions: Additional instructions for this run
        tools: List of tools for this run
        metadata: Key-value pairs (max 16 pairs)
        stream: Boolean for streaming mode
        temperature: Sampling temperature (0-2)
        top_p: Nucleus sampling value (0-1)
        max_completion_tokens: Maximum completion tokens
        max_prompt_tokens: Maximum prompt tokens
        response_format: Response format configuration
        tool_choice: Tool choice configuration
        truncation_strategy: Truncation strategy
        parallel_tool_calls: Boolean for parallel tool calls
    """
    return cast(
        Dict[str, Any],
        tools_create_run(
            thread_id=thread_id,
            assistant_id=assistant_id,
            model=model,
            instructions=instructions,
            additional_instructions=additional_instructions,
            tools=tools,
            metadata=metadata,
            stream=stream,
            temperature=temperature,
            top_p=top_p,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            response_format=response_format,
            tool_choice=tool_choice,
            truncation_strategy=truncation_strategy,
            parallel_tool_calls=parallel_tool_calls,
        ),
    )


@mcp.tool()
def create_thread_and_run(
    assistant_id: str,
    thread: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[
        List[Union[CodeInterpreterTool, FileSearchTool, FunctionTool]]
    ] = None,
    metadata: Optional[Dict[str, str]] = None,
    stream: Optional[bool] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    max_completion_tokens: Optional[int] = None,
    max_prompt_tokens: Optional[int] = None,
    response_format: Optional[Union[Literal["auto"], ResponseFormat]] = None,
    tool_choice: Optional[
        Union[Literal["none", "auto", "required"], ToolChoice]
    ] = None,
    truncation_strategy: Optional[TruncationStrategy] = None,
    parallel_tool_calls: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create a thread and run it in one request.

    This combines creating a new thread and starting a run into a single operation.
    Useful when you want to start a fresh conversation with an assistant.

    Args:
        assistant_id: (REQUIRED) The ID of the assistant to use
        thread: Thread configuration
        model: Model override for this run
        instructions: Instructions override for this run
        tools: List of tools for this run
        metadata: Key-value pairs (max 16 pairs)
        stream: Boolean for streaming mode
        temperature: Sampling temperature (0-2)
        top_p: Nucleus sampling value (0-1)
        max_completion_tokens: Maximum completion tokens
        max_prompt_tokens: Maximum prompt tokens
        response_format: Response format configuration
        tool_choice: Tool choice configuration
        truncation_strategy: Truncation strategy
        parallel_tool_calls: Boolean for parallel tool calls
    """
    return cast(
        Dict[str, Any],
        tools_create_thread_and_run(
            assistant_id=assistant_id,
            thread=thread,
            model=model,
            instructions=instructions,
            tools=tools,
            metadata=metadata,
            stream=stream,
            temperature=temperature,
            top_p=top_p,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            response_format=response_format,
            tool_choice=tool_choice,
            truncation_strategy=truncation_strategy,
            parallel_tool_calls=parallel_tool_calls,
        ),
    )


@mcp.tool()
def list_runs(
    thread_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List runs for a thread.

    Use this to view the history of runs in a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread to list runs for
        limit: Limit on number of runs (1-100, default 20)
        order: Sort order ('asc' or 'desc', default 'desc')
        after: Cursor for pagination (get runs after this ID)
        before: Cursor for pagination (get runs before this ID)
    """
    return cast(
        Dict[str, Any],
        tools_list_runs(
            thread_id=thread_id,
            limit=limit,
            order=order,
            after=after,
            before=before,
        ),
    )


@mcp.tool()
def get_run(thread_id: str, run_id: str) -> Dict[str, Any]:
    """
    Get run by ID.

    Use this to retrieve details about a specific run.

    Args:
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to retrieve
    """
    return cast(Dict[str, Any], tools_get_run(thread_id=thread_id, run_id=run_id))


@mcp.tool()
def modify_run(
    thread_id: str,
    run_id: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Modify a run.

    Use this to update a run's metadata.

    Args:
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to modify
        metadata: Key-value pairs (max 16 pairs)
    """
    return cast(
        Dict[str, Any],
        tools_modify_run(thread_id=thread_id, run_id=run_id, metadata=metadata),
    )


@mcp.tool()
def submit_tool_outputs(
    thread_id: str,
    run_id: str,
    tool_outputs: List[Dict[str, str]],
    stream: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Submit outputs for tool calls.

    Use this to provide the results of tool calls back to the assistant.

    Args:
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to submit outputs for
        tool_outputs: (REQUIRED) List of tool outputs with tool_call_id and output
        stream: Boolean for streaming mode
    """
    return cast(
        Dict[str, Any],
        tools_submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs,
            stream=stream,
        ),
    )


@mcp.tool()
def cancel_run(thread_id: str, run_id: str) -> Dict[str, Any]:
    """
    Cancel a run.

    Use this to stop a run that is in progress.

    Args:
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to cancel
    """
    return cast(Dict[str, Any], tools_cancel_run(thread_id=thread_id, run_id=run_id))


# Run Step Tools
# TODO: Implement run step tools
# - get_run_step
# - list_run_steps


if __name__ == "__main__":
    mcp.run()
