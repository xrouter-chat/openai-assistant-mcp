"""Pydantic models for OpenAI Thread API.

This module provides type-safe models for interacting with the OpenAI Thread API,
including models for threads, messages, and thread-specific tool resources.
"""

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from ..models import CodeInterpreterTool, Metadata, ToolResources


class ImageFileDetail(BaseModel):
    """Model for image file details."""

    file_id: str = Field(description="The File ID of the image in the message content")
    detail: Optional[Literal["auto", "low", "high"]] = Field(
        default="auto", description="Specifies the detail level of the image"
    )


class ImageFile(BaseModel):
    """Model for image file content."""

    type: Literal["image_file"] = Field(
        description="The type of content part. Always image_file"
    )
    image_file: ImageFileDetail


class ImageUrlDetail(BaseModel):
    """Model for image URL details."""

    url: str = Field(description="The external URL of the image")
    detail: Optional[Literal["auto", "low", "high"]] = Field(
        default="auto", description="Specifies the detail level of the image"
    )


class ImageUrl(BaseModel):
    """Model for image URL content."""

    type: Literal["image_url"] = Field(
        description="The type of content part. Always image_url"
    )
    image_url: ImageUrlDetail


class TextContent(BaseModel):
    """Model for text content."""

    type: Literal["text"] = Field(description="The type of content part. Always text")
    text: str = Field(description="Text content to be sent to the model")


ContentPart = Union[TextContent, ImageFile, ImageUrl]


class FileSearchTool(BaseModel):
    """Tool for searching through files."""

    type: Literal["file_search"] = Field(
        description="The type of tool being defined: file_search"
    )


AttachmentTool = Union[CodeInterpreterTool, FileSearchTool]


class MessageAttachment(BaseModel):
    """Model for file attachments in messages."""

    file_id: str = Field(description="The ID of the file to attach to the message")
    tools: Optional[List[AttachmentTool]] = Field(
        default=None, description="The tools to add this file to"
    )


class ThreadMessage(BaseModel):
    """Model for messages in thread creation."""

    content: Union[str, List[ContentPart]] = Field(
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
