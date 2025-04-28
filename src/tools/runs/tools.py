"""OpenAI Run API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, Union, cast

from openai import OpenAI

from ...config.settings import Settings
from ..models import CodeInterpreterTool, FileSearchTool, FunctionTool
from .models import ResponseFormat, RunObject, ToolChoice, TruncationStrategy

logger = logging.getLogger("openai-assistant-mcp")
settings = Settings()
client = OpenAI()


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

    Args:
        thread_id: The ID of the thread to run
        assistant_id: The ID of the assistant to use
        model: Optional model override for this run
        instructions: Optional instructions override for this run
        additional_instructions: Optional additional instructions for this run
        tools: Optional list of tools for this run
        metadata: Optional key-value pairs (max 16 pairs)
        stream: Optional boolean for streaming mode
        temperature: Optional sampling temperature (0-2)
        top_p: Optional nucleus sampling value (0-1)
        max_completion_tokens: Optional maximum completion tokens
        max_prompt_tokens: Optional maximum prompt tokens
        response_format: Optional response format configuration
        tool_choice: Optional tool choice configuration
        truncation_strategy: Optional truncation strategy
        parallel_tool_calls: Optional boolean for parallel tool calls

    Returns:
        Dict containing created run data
    """
    logger.info(f"Creating run for thread {thread_id} with assistant {assistant_id}")

    request_data = {
        "assistant_id": assistant_id,
        "model": model,
        "instructions": instructions,
        "additional_instructions": additional_instructions,
        "tools": tools,
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

    validated = RunObject.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump(exclude_none=True)
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)


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

    Args:
        assistant_id: The ID of the assistant to use
        thread: Optional thread configuration
        model: Optional model override for this run
        instructions: Optional instructions override for this run
        tools: Optional list of tools for this run
        metadata: Optional key-value pairs (max 16 pairs)
        stream: Optional boolean for streaming mode
        temperature: Optional sampling temperature (0-2)
        top_p: Optional nucleus sampling value (0-1)
        max_completion_tokens: Optional maximum completion tokens
        max_prompt_tokens: Optional maximum prompt tokens
        response_format: Optional response format configuration
        tool_choice: Optional tool choice configuration
        truncation_strategy: Optional truncation strategy
        parallel_tool_calls: Optional boolean for parallel tool calls

    Returns:
        Dict containing created run data
    """
    logger.info(f"Creating thread and run with assistant {assistant_id}")

    request_data = {
        "assistant_id": assistant_id,
        "thread": thread,
        "model": model,
        "instructions": instructions,
        "tools": tools,
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

    validated = RunObject.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump(exclude_none=True)
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)


def list_runs(
    thread_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List runs for a thread.

    Args:
        thread_id: The ID of the thread to list runs for
        limit: Optional limit on number of runs (1-100, default 20)
        order: Optional sort order ('asc' or 'desc', default 'desc')
        after: Optional cursor for pagination (get runs after this ID)
        before: Optional cursor for pagination (get runs before this ID)

    Returns:
        Dict containing list of runs
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
    return cast(Dict[str, Any], response.model_dump())


def get_run(thread_id: str, run_id: str) -> Dict[str, Any]:
    """
    Get run by ID.

    Args:
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run to retrieve

    Returns:
        Dict containing run data
    """
    logger.info(f"Getting run {run_id} from thread {thread_id}")

    response = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return cast(Dict[str, Any], RunObject.model_validate(response).model_dump())


def modify_run(
    thread_id: str,
    run_id: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Modify a run.

    Args:
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run to modify
        metadata: Optional key-value pairs (max 16 pairs)

    Returns:
        Dict containing modified run data
    """
    logger.info(f"Modifying run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.update(
        thread_id=thread_id, run_id=run_id, metadata=metadata
    )
    return cast(Dict[str, Any], RunObject.model_validate(response).model_dump())


def submit_tool_outputs(
    thread_id: str,
    run_id: str,
    tool_outputs: List[Dict[str, str]],
    stream: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Submit outputs for tool calls.

    Args:
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run to submit outputs for
        tool_outputs: List of tool outputs with tool_call_id and output
        stream: Optional boolean for streaming mode

    Returns:
        Dict containing updated run data
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
    return cast(Dict[str, Any], RunObject.model_validate(response).model_dump())


def cancel_run(thread_id: str, run_id: str) -> Dict[str, Any]:
    """
    Cancel a run.

    Args:
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run to cancel

    Returns:
        Dict containing cancelled run data
    """
    logger.info(f"Cancelling run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
    return cast(Dict[str, Any], RunObject.model_validate(response).model_dump())
