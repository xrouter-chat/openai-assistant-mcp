"""Pydantic models for OpenAI Run API.

This module provides type-safe models for interacting with the OpenAI Run API,
including models for run status, errors, and run-specific operations.
"""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from ..models import CodeInterpreterTool, FileSearchTool, FunctionTool, Metadata


class RunIncompleteDetails(BaseModel):
    """Model for incomplete run details."""

    reason: str = Field(
        description="The reason why the run is incomplete. Points to which specific "
        "token limit was reached"
    )


class RunLastError(BaseModel):
    """Model for the last error associated with a run."""

    code: Literal["server_error", "rate_limit_exceeded", "invalid_prompt"] = Field(
        description="The error code"
    )
    message: str = Field(description="A human-readable description of the error")


class ToolCallFunction(BaseModel):
    """Model for tool call function details."""

    name: str = Field(description="The name of the function")
    arguments: str = Field(
        description="The arguments that the model expects to pass to the function"
    )


class ToolCall(BaseModel):
    """Model for tool call details."""

    id: str = Field(
        description="The ID of the tool call. Must be referenced when submitting "
        "tool outputs"
    )
    type: Literal["function"] = Field(
        description="The type of tool call. Currently always function"
    )
    function: ToolCallFunction = Field(description="The function definition")


class SubmitToolOutputs(BaseModel):
    """Model for submit tool outputs action."""

    tool_calls: List[ToolCall] = Field(description="A list of the relevant tool calls")


class RequiredAction(BaseModel):
    """Model for required action details."""

    type: Literal["submit_tool_outputs"] = Field(
        description="The type of required action. Currently always submit_tool_outputs"
    )
    submit_tool_outputs: SubmitToolOutputs = Field(
        description="Details on the tool outputs needed for this run to continue"
    )


class ResponseFormatJsonSchema(BaseModel):
    """Model for JSON schema response format."""

    name: Optional[str] = Field(
        default=None,
        description="The name of the response format. "
        "Must be a-z, A-Z, 0-9, or contain "
        "underscores and dashes, with a maximum length of 64",
    )
    description: Optional[str] = Field(
        default=None,
        description="A description of what the response format is for, "
        "used by the model "
        "to determine how to respond in the format",
    )
    schema: dict = Field(
        description="The schema for the response format, described as "
        "a JSON Schema object"
    )
    strict: Optional[bool] = Field(
        default=None,
        description="Whether to enable strict schema adherence "
        "when generating the output",
    )


class ResponseFormat(BaseModel):
    """Model for response format configuration."""

    type: Literal["text", "json_object", "json_schema"] = Field(
        description="The type of response format being defined"
    )
    json_schema: Optional[ResponseFormatJsonSchema] = Field(
        default=None, description="Structured Outputs configuration options"
    )


class ToolChoice(BaseModel):
    """Model for tool choice configuration."""

    type: Literal["none", "auto", "function"] = Field(
        description="The type of the tool"
    )
    function: Optional[dict] = Field(
        default=None,
        description="The function configuration when type is function",
    )


class TruncationStrategy(BaseModel):
    """Model for truncation strategy configuration."""

    type: Literal["auto", "last_messages"] = Field(
        description="The truncation strategy to use for the thread"
    )
    last_messages: Optional[int] = Field(
        default=None,
        description="The number of most recent messages from the thread when "
        "constructing the context for the run",
    )


class RunUsage(BaseModel):
    """Model for run usage statistics."""

    completion_tokens: int = Field(
        description="Number of completion tokens used over the course of the run"
    )
    prompt_tokens: int = Field(
        description="Number of prompt tokens used over the course of the run"
    )
    total_tokens: int = Field(
        description="Total number of tokens used (prompt + completion)"
    )


class RunObject(BaseModel):
    """Model representing a run in API responses."""

    id: str = Field(description="The identifier of the run")
    object: Literal["thread.run"] = Field(
        description="The object type, which is always thread.run"
    )
    created_at: int = Field(
        description="The Unix timestamp (in seconds) for when the run was created"
    )
    thread_id: str = Field(description="The ID of the thread being executed on")
    assistant_id: str = Field(
        description="The ID of the assistant used for execution of this run"
    )
    status: Literal[
        "queued",
        "in_progress",
        "requires_action",
        "cancelling",
        "cancelled",
        "failed",
        "completed",
        "incomplete",
        "expired",
    ] = Field(description="The status of the run")
    required_action: Optional[RequiredAction] = Field(
        default=None,
        description="Details on the action required to continue the run",
    )
    last_error: Optional[RunLastError] = Field(
        default=None,
        description="The last error associated with this run",
    )
    expires_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run will expire",
    )
    started_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run was started",
    )
    cancelled_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run was cancelled",
    )
    failed_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run failed",
    )
    completed_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run was completed",
    )
    model: str = Field(description="The model that the assistant used for this run")
    instructions: str = Field(
        description="The instructions that the assistant used for this run"
    )
    tools: List[Union[CodeInterpreterTool, FileSearchTool, FunctionTool]] = Field(
        description="The list of tools that the assistant used for this run"
    )
    file_ids: List[str] = Field(
        default_factory=list,
        description="List of File IDs the assistant used for this run",
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to the run",
    )
    usage: Optional[RunUsage] = Field(
        default=None,
        description="Usage statistics related to the run",
    )
    parallel_tool_calls: bool = Field(
        default=False,
        description="Whether to enable parallel function calling during tool use",
    )
    max_completion_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of completion tokens specified "
        "to have been used",
    )
    max_prompt_tokens: Optional[int] = Field(
        default=None,
        description="The maximum number of prompt tokens specified to have been used",
    )
    temperature: Optional[float] = Field(
        default=None,
        description="The sampling temperature used for this run. "
        "Defaults to 1 if not set",
    )
    top_p: Optional[float] = Field(
        default=None,
        description="The nucleus sampling value used for this run. "
        "Defaults to 1 if not set",
    )
    response_format: Optional[Union[Literal["auto"], ResponseFormat]] = Field(
        default="auto",
        description="Specifies the format that the model must output",
    )
    tool_choice: Optional[
        Union[Literal["none", "auto", "required"], ToolChoice]
    ] = Field(
        default="auto",
        description="Controls which (if any) tool is called by the model",
    )
    truncation_strategy: Optional[TruncationStrategy] = Field(
        default=None,
        description="Controls for how a thread will be truncated prior to the run",
    )
    incomplete_details: Optional[RunIncompleteDetails] = Field(
        default=None,
        description="Details on why the run is incomplete",
    )
