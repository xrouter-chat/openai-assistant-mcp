"""Pydantic models for OpenAI Run Steps API.

This module provides type-safe models for interacting with the OpenAI Run Steps API,
including models for different types of run steps and their details.
"""

from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from ..runs.models import RunUsage


# Message Creation Step Details
class MessageCreationStepDetails(BaseModel):
    """Model for message creation step details."""

    type: Literal["message_creation"] = Field(
        description="The type of step. Always message_creation for this type."
    )
    message_creation: Dict[str, str] = Field(
        description="Details about the message that was created"
    )


# Tool Call Models - Function
class ToolCallFunction(BaseModel):
    """Model for tool call function details."""

    name: str = Field(description="The name of the function")
    arguments: str = Field(
        description="The arguments that the model passed to the function"
    )
    output: Optional[str] = Field(
        default=None, description="The output of the function call"
    )


class FunctionToolCall(BaseModel):
    """Model for function tool call details."""

    id: str = Field(description="The ID of the tool call")
    type: Literal["function"] = Field(
        description="The type of tool call. Always function for this type."
    )
    function: ToolCallFunction = Field(description="The function definition")


# Tool Call Models - Code Interpreter
class CodeInterpreterLogOutput(BaseModel):
    """Model for code interpreter log output."""

    type: Literal["logs"] = Field(
        description="The type of output. Always logs for this type."
    )
    logs: str = Field(description="The text output from the Code Interpreter tool call")


class CodeInterpreterImageOutput(BaseModel):
    """Model for code interpreter image output."""

    type: Literal["image"] = Field(
        description="The type of output. Always image for this type."
    )
    image: Dict[str, str] = Field(
        description="The image output from the Code Interpreter tool call"
    )


CodeInterpreterOutput = Union[CodeInterpreterLogOutput, CodeInterpreterImageOutput]


class CodeInterpreterToolCall(BaseModel):
    """Model for code interpreter tool call details."""

    id: str = Field(description="The ID of the tool call object")
    type: Literal["code_interpreter"] = Field(
        description="The type of tool call. Always code_interpreter for this type."
    )
    code_interpreter: Dict[str, Union[str, List[CodeInterpreterOutput]]] = Field(
        description="The Code Interpreter tool call definition"
    )


# Tool Call Models - File Search
class FileSearchResult(BaseModel):
    """Model for file search result."""

    file_id: str = Field(description="The ID of the file that result was found in")
    file_name: str = Field(description="The name of the file that result was found in")
    score: float = Field(
        description="The score of the result. All values must be between 0 and 1"
    )
    content: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="The content of the result that was found. "
        "Only included if requested.",
    )


class FileSearchToolCall(BaseModel):
    """Model for file search tool call details."""

    id: str = Field(description="The ID of the tool call object")
    type: Literal["file_search"] = Field(
        description="The type of tool call. Always file_search for this type."
    )
    file_search: Dict[
        str, Union[Dict[str, Union[str, float]], List[FileSearchResult]]
    ] = Field(description="The file search details and results")


# Combined Tool Call type
ToolCall = Union[FunctionToolCall, CodeInterpreterToolCall, FileSearchToolCall]


class ToolCallsStepDetails(BaseModel):
    """Model for tool calls step details."""

    type: Literal["tool_calls"] = Field(
        description="The type of step. Always tool_calls for this type."
    )
    tool_calls: List[ToolCall] = Field(
        description="A list of tool calls the assistant made"
    )


StepDetails = Union[MessageCreationStepDetails, ToolCallsStepDetails]


class RunStepObject(BaseModel):
    """Model representing a run step in API responses."""

    id: str = Field(description="The identifier of the run step")
    object: Literal["thread.run.step"] = Field(
        description="The object type, which is always thread.run.step"
    )
    created_at: int = Field(
        description="The Unix timestamp (in seconds) for when the run step was created"
    )
    run_id: str = Field(description="The ID of the run this step is a part of")
    assistant_id: str = Field(
        description="The ID of the assistant associated with this run step"
    )
    thread_id: str = Field(
        description="The ID of the thread this run step is a part of"
    )
    type: Literal["message_creation", "tool_calls"] = Field(
        description="The type of run step"
    )
    status: Literal[
        "in_progress", "cancelled", "failed", "completed", "expired"
    ] = Field(description="The status of the run step")
    cancelled_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when "
        "the run step was cancelled",
    )
    completed_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when "
        "the run step was completed",
    )
    expired_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run step expired",
    )
    failed_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the run step failed",
    )
    last_error: Optional[Dict[Literal["code", "message"], str]] = Field(
        default=None,
        description="The last error associated with this run step. "
        "Will be null if there are no errors.",
    )
    metadata: Optional[Dict[str, str]] = Field(
        default=None,
        description="Set of 16 key-value pairs that can be attached to an object.",
    )
    step_details: StepDetails = Field(description="The details of the run step")
    usage: Optional[RunUsage] = Field(
        default=None, description="Usage statistics related to the run step"
    )


class RunStepListResponse(BaseModel):
    """Model for run step list responses."""

    object: Literal["list"] = Field(description="The object type, which is always list")
    data: List[RunStepObject] = Field(description="List of run step objects")
    first_id: str = Field(description="The ID of the first run step in the list")
    last_id: str = Field(description="The ID of the last run step in the list")
    has_more: bool = Field(description="Whether there are more run steps to fetch")
