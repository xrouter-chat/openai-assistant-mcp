"""OpenAI Message API module.

This module provides models and utilities for interacting with the OpenAI Message API.
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
from .tools import (
    create_message,
    delete_message,
    get_message,
    list_messages,
    modify_message,
)

__all__ = [
    # Tools
    "create_message",
    "delete_message",
    "get_message",
    "list_messages",
    "modify_message",
    # Models
    "ImageFileContent",
    "MessageImageFile",
    "ImageUrlContent",
    "MessageImageUrl",
    "FileCitationDetail",
    "FileCitationAnnotation",
    "FilePathDetail",
    "FilePathAnnotation",
    "TextContent",
    "MessageText",
    "RefusalContent",
    "MessageRefusal",
    "MessageContent",
    "AttachmentTool",
    "MessageAttachment",
    "CreateMessageRequest",
    "ModifyMessageRequest",
    "MessageIncompleteDetails",
    "MessageObject",
    "MessageListResponse",
    "DeleteMessageResponse",
]
