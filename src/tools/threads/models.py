"""Pydantic models for OpenAI Thread API.

This module provides type-safe models for interacting with the OpenAI Thread API,
including models for threads and thread-specific tool resources.
"""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from ..messages import MessageAttachment, MessageContent
from ..models import Metadata, ToolResources


class ThreadMessage(BaseModel):
    """Model for messages in thread creation."""

    content: Union[str, List[MessageContent]] = Field(
        description="The content of the message. Can be a string for simple text "
        "or an array of content parts for mixed content"
    )
    role: Literal["user", "assistant"] = Field(
        description="The role of the entity creating the message"
    )
    file_ids: Optional[List[str]] = Field(
        default=None,
        description="List of File IDs to attach to the message",
    )
    attachments: Optional[List[MessageAttachment]] = Field(
        default=None,
        description="A list of files attached to the message, "
        "and the tools they should be added to",
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to the message",
    )


class CreateThreadRequest(BaseModel):
    """Model for creating a new thread."""

    messages: Optional[List[ThreadMessage]] = Field(
        default=None,
        description="A list of messages to start the thread with",
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to the thread",
    )
    tool_resources: Optional[ToolResources] = Field(
        default=None,
        description="Resources made available to assistant's tools in this thread",
    )


class ModifyThreadRequest(BaseModel):
    """Model for modifying an existing thread."""

    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to the thread",
    )
    tool_resources: Optional[ToolResources] = Field(
        default=None,
        description="Resources made available to assistant's tools in this thread",
    )


class ThreadObject(BaseModel):
    """Model representing a thread in API responses."""

    id: str = Field(
        description="The identifier, which can be referenced in API endpoints"
    )
    object: Literal["thread"] = Field(
        description="The object type, which is always thread"
    )
    created_at: int = Field(
        description="The Unix timestamp (in seconds) for when the thread was created"
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs attached to the thread",
    )
    tool_resources: Optional[ToolResources] = Field(
        default=None,
        description="Resources made available to assistant's tools in this thread",
    )


class DeleteThreadResponse(BaseModel):
    """Model for thread deletion response."""

    id: str = Field(description="The ID of the deleted thread")
    object: Literal["thread.deleted"] = Field(
        description="The object type, which is always thread.deleted"
    )
    deleted: bool = Field(description="Whether the thread was deleted")
