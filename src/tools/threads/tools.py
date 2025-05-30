"""OpenAI Thread API tools implementation."""
import logging
from typing import Any, Dict, List, Optional, Union, cast

from openai import OpenAI

from ..messages import MessageAttachment
from ..models import ToolResources
from .models import (
    CreateThreadRequest,
    DeleteThreadResponse,
    ModifyThreadRequest,
    ThreadMessage,
    ThreadObject,
)

logger = logging.getLogger(__name__)
client = OpenAI()


def create_thread(
    messages: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, str]] = None,
    tool_resources: Optional[Union[Dict[str, Any], ToolResources]] = None,
) -> ThreadObject:
    """
    Create a thread.

    Args:
        messages: List of messages to start the thread with
        metadata: Key-value pairs (max 16 pairs)
        tool_resources: Resources for tools

    Returns:
        ThreadObject: The created thread
    """
    logger.info("Creating thread")

    # Convert raw message dicts to ThreadMessage objects if provided
    thread_messages = None
    if messages:
        thread_messages = [
            ThreadMessage(
                content=msg["content"],
                role=msg["role"],
                file_ids=msg.get("file_ids"),
                attachments=[
                    MessageAttachment.model_validate(attachment)
                    for attachment in msg.get("attachments", [])
                ]
                if msg.get("attachments")
                else None,
                metadata=msg.get("metadata"),
            )
            for msg in messages
        ]

    # Convert tool_resources dict to ToolResources if needed
    tool_resources_obj = None
    if tool_resources:
        if isinstance(tool_resources, dict):
            tool_resources_obj = ToolResources.model_validate(tool_resources)
        else:
            tool_resources_obj = tool_resources

    request = CreateThreadRequest(
        messages=thread_messages,
        metadata=metadata,
        tool_resources=tool_resources_obj,
    )

    request_data = request.model_dump(exclude_none=True)
    logger.info(f"Creating thread with request data: {request_data}")

    response = client.beta.threads.create(**request_data)
    logger.info(f"Got response from OpenAI: {response}")

    return cast(ThreadObject, ThreadObject.model_validate(response))


def get_thread(thread_id: str) -> ThreadObject:
    """
    Get thread by ID.

    Args:
        thread_id: (REQUIRED) The ID of the thread to retrieve

    Returns:
        ThreadObject: The retrieved thread
    """
    logger.info(f"Getting thread {thread_id}")

    response = client.beta.threads.retrieve(thread_id)
    return cast(ThreadObject, ThreadObject.model_validate(response))


def modify_thread(
    thread_id: str,
    metadata: Optional[Dict[str, str]] = None,
    tool_resources: Optional[Union[Dict[str, Any], ToolResources]] = None,
) -> ThreadObject:
    """
    Modify a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread to modify
        metadata: Key-value pairs (max 16 pairs)
        tool_resources: Resources for tools

    Returns:
        ThreadObject: The modified thread
    """
    logger.info(f"Modifying thread {thread_id}")

    # Convert tool_resources dict to ToolResources if needed
    tool_resources_obj = None
    if tool_resources:
        if isinstance(tool_resources, dict):
            tool_resources_obj = ToolResources.model_validate(tool_resources)
        else:
            tool_resources_obj = tool_resources

    request = ModifyThreadRequest(
        metadata=metadata,
        tool_resources=tool_resources_obj,
    ).model_dump(exclude_none=True)

    response = client.beta.threads.update(thread_id, **request)
    return cast(ThreadObject, ThreadObject.model_validate(response))


def delete_thread(thread_id: str) -> DeleteThreadResponse:
    """
    Delete a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread to delete

    Returns:
        DeleteThreadResponse: The deletion status
    """
    logger.info(f"Deleting thread {thread_id}")

    response = client.beta.threads.delete(thread_id)
    return cast(DeleteThreadResponse, DeleteThreadResponse.model_validate(response))
