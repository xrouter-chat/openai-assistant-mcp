"""Common models shared across OpenAI API tools.

This module provides common models used by multiple OpenAI API tools,
such as metadata, tool resources, and common tools.
"""

from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

# Metadata type
MetadataKey = str
MetadataValue = str
Metadata = Dict[MetadataKey, MetadataValue]


# Common tool models
class FileSearchTool(BaseModel):
    """Tool for searching through files."""

    type: Literal["file_search"] = Field(
        description="The type of tool being defined: file_search"
    )


class CodeInterpreterTool(BaseModel):
    """Tool for executing code in a sandboxed environment."""

    type: Literal["code_interpreter"] = Field(
        description="The type of tool being defined: code_interpreter"
    )


class CodeInterpreterResource(BaseModel):
    """Resources for code interpreter tool."""

    file_ids: List[str] = Field(
        default_factory=list,
        description="A list of file IDs made available to the code_interpreter tool.",
        max_length=20,
    )


class FileSearchResource(BaseModel):
    """Resources for file search tool."""

    vector_store_ids: List[str] = Field(
        default_factory=list,
        description="The vector store attached to this assistant.",
        max_length=1,
    )


class ToolResources(BaseModel):
    """Resources available to assistant tools."""

    code_interpreter: Optional[CodeInterpreterResource] = Field(
        default=None, description="Resources for the code interpreter tool."
    )
    file_search: Optional[FileSearchResource] = Field(
        default=None, description="Resources for the file search tool."
    )


class RankingOptions(BaseModel):
    """Options for ranking file search results."""

    score_threshold: float = Field(
        ge=0,
        le=1,
        description="The score threshold for the file search. "
        "All values must be a floating point number between 0 and 1.",
    )
    ranker: Optional[str] = Field(
        default=None,
        description="The ranker to use for the file search. "
        "If not specified will use the auto ranker.",
    )


class FileSearchConfig(BaseModel):
    """Configuration for file search tool."""

    max_num_results: Optional[int] = Field(
        default=None,
        ge=1,
        le=50,
        description="The maximum number of results the file search tool should output.",
    )
    ranking_options: Optional[RankingOptions] = Field(
        default=None, description="The ranking options for the file search."
    )


class AssistantFileSearchTool(FileSearchTool):
    """Tool for searching through files with assistant-specific configuration."""

    file_search: Optional[FileSearchConfig] = Field(
        default=None, description="Overrides for the file search tool."
    )


class FunctionParameters(BaseModel):
    """Parameters for a function tool."""

    name: str = Field(
        pattern=r"^[a-zA-Z0-9_-]+$",
        max_length=64,
        description="The name of the function to be called.",
    )
    description: Optional[str] = Field(
        default=None, description="A description of what the function does."
    )
    parameters: Optional[dict] = Field(
        default=None,
        description="The parameters the functions accepts, "
        "described as a JSON Schema object.",
    )
    strict: Optional[bool] = Field(
        default=None,
        description="Whether to enable strict schema adherence when generating "
        "the function call.",
    )


class FunctionTool(BaseModel):
    """Tool for calling functions."""

    type: Literal["function"] = Field(
        description="The type of tool being defined: function"
    )
    function: FunctionParameters = Field(description="The function definition.")


Tool = Union[CodeInterpreterTool, AssistantFileSearchTool, FunctionTool]
