"""OpenAI Run API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, Union

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta.threads.run import Run

from ..models import CodeInterpreterTool, FileSearchTool, FunctionTool, ResponseFormat
from .models import ToolChoice, TruncationStrategy

logger = logging.getLogger(__name__)


def create_run(
    client: OpenAI,
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
) -> Run:
    """
    Create a run.

    Args:
        client: OpenAI client instance (injected)
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

    Returns:
        Run: The created run from OpenAI SDK
    """
    logger.info(f"Creating run for thread {thread_id} with assistant {assistant_id}")

    # Convert tool models to dictionaries if provided
    tools_data = None
    if tools:
        tools_data = [tool.model_dump() for tool in tools]

    request_data = {
        "assistant_id": assistant_id,
        "model": model,
        "instructions": instructions,
        "additional_instructions": additional_instructions,
        "tools": tools_data,
        "metadata": metadata,
        "stream": stream,
        "temperature": temperature,
        "top_p": top_p,
        "max_completion_tokens": max_completion_tokens,
        "max_prompt_tokens": max_prompt_tokens,
        "response_format": response_format,
        "tool_choice": tool_choice,
        "truncation_strategy": truncation_strategy,
        "parallel_tool_calls": parallel_tool_calls,
    }
    # Remove None values
    request_data = {k: v for k, v in request_data.items() if v is not None}

    logger.info(f"Creating run with request data: {request_data}")

    response = client.beta.threads.runs.create(thread_id=thread_id, **request_data)
    logger.info(f"Got response from OpenAI: {response}")

    return response


def create_thread_and_run(
    client: OpenAI,
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
) -> Run:
    """
    Create a thread and run it in one request.

    Args:
        client: OpenAI client instance (injected)
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

    Returns:
        Run: The created run from OpenAI SDK
    """
    logger.info(f"Creating thread and run with assistant {assistant_id}")

    # Convert tool models to dictionaries if provided
    tools_data = None
    if tools:
        tools_data = [tool.model_dump() for tool in tools]

    request_data = {
        "assistant_id": assistant_id,
        "thread": thread,
        "model": model,
        "instructions": instructions,
        "tools": tools_data,
        "metadata": metadata,
        "stream": stream,
        "temperature": temperature,
        "top_p": top_p,
        "max_completion_tokens": max_completion_tokens,
        "max_prompt_tokens": max_prompt_tokens,
        "response_format": response_format,
        "tool_choice": tool_choice,
        "truncation_strategy": truncation_strategy,
        "parallel_tool_calls": parallel_tool_calls,
    }
    # Remove None values
    request_data = {k: v for k, v in request_data.items() if v is not None}

    logger.info(f"Creating thread and run with request data: {request_data}")

    response = client.beta.threads.create_and_run(**request_data)
    logger.info(f"Got response from OpenAI: {response}")

    return response


def list_runs(
    client: OpenAI,
    thread_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> SyncCursorPage[Run]:
    """
    List runs for a thread.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread to list runs for
        limit: Limit on number of runs (1-100, default 20)
        order: Sort order ('asc' or 'desc', default 'desc')
        after: Cursor for pagination (get runs after this ID)
        before: Cursor for pagination (get runs before this ID)

    Returns:
        SyncCursorPage[Run]: The list of runs from OpenAI SDK
    """
    logger.info(f"Listing runs for thread {thread_id}")

    params = {
        "limit": limit,
        "order": order,
        "after": after,
        "before": before,
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    response = client.beta.threads.runs.list(thread_id=thread_id, **params)
    logger.info(f"Got response from OpenAI: {response}")

    return response


def get_run(client: OpenAI, thread_id: str, run_id: str) -> Run:
    """
    Get run by ID.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to retrieve

    Returns:
        Run: The retrieved run from OpenAI SDK
    """
    logger.info(f"Getting run {run_id} from thread {thread_id}")

    response = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return response


def modify_run(
    client: OpenAI,
    thread_id: str,
    run_id: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Run:
    """
    Modify a run.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to modify
        metadata: Key-value pairs (max 16 pairs)

    Returns:
        Run: The modified run from OpenAI SDK
    """
    logger.info(f"Modifying run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.update(
        thread_id=thread_id, run_id=run_id, metadata=metadata
    )
    return response


def submit_tool_outputs(
    client: OpenAI,
    thread_id: str,
    run_id: str,
    tool_outputs: List[Dict[str, str]],
    stream: Optional[bool] = None,
) -> Run:
    """
    Submit outputs for tool calls.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to submit outputs for
        tool_outputs: (REQUIRED) List of tool outputs with tool_call_id and output
        stream: Boolean for streaming mode

    Returns:
        Run: The updated run from OpenAI SDK
    """
    logger.info(f"Submitting tool outputs for run {run_id} in thread {thread_id}")

    request_data = {
        "tool_outputs": tool_outputs,
        "stream": stream,
    }
    # Remove None values
    request_data = {k: v for k, v in request_data.items() if v is not None}

    response = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id, run_id=run_id, **request_data
    )
    return response


def cancel_run(client: OpenAI, thread_id: str, run_id: str) -> Run:
    """
    Cancel a run.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to cancel

    Returns:
        Run: The cancelled run from OpenAI SDK
    """
    logger.info(f"Cancelling run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
    return response
