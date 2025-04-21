"""Common models shared across OpenAI API tools.

This module provides common models used by multiple OpenAI API tools,
such as metadata, tool resources, and common tools.
"""

from typing import Dict, List, Literal, Optional

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
