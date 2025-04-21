"""OpenAI Message API models.

This package provides Pydantic models for the OpenAI Message API.
"""

from .models import (
    AttachmentTool,
    CreateMessageRequest,
    DeleteMessageResponse,
    FileCitationAnnotation,
    FileCitationDetail,
    FilePathAnnotation,
    FilePathDetail,
    ImageFileContent,
    ImageUrlContent,
    MessageAttachment,
    MessageContent,
    MessageImageFile,
    MessageImageUrl,
    MessageIncompleteDetails,
    MessageListResponse,
    MessageObject,
    MessageRefusal,
    MessageText,
    ModifyMessageRequest,
    RefusalContent,
    TextContent,
)

__all__ = [
    "AttachmentTool",
    "CreateMessageRequest",
    "DeleteMessageResponse",
    "FileCitationAnnotation",
    "FileCitationDetail",
    "FilePathAnnotation",
    "FilePathDetail",
    "ImageFileContent",
    "ImageUrlContent",
    "MessageAttachment",
    "MessageContent",
    "MessageImageFile",
    "MessageImageUrl",
    "MessageIncompleteDetails",
    "MessageListResponse",
    "MessageObject",
    "MessageRefusal",
    "MessageText",
    "ModifyMessageRequest",
    "RefusalContent",
    "TextContent",
]
