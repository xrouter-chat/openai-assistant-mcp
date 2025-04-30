"""OpenAI Message API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, Union, cast

from openai import OpenAI

from src.config.settings import Settings

from .models import (
    CreateMessageRequest,
    DeleteMessageResponse,
    MessageAttachment,
    MessageContent,
    MessageListResponse,
    MessageObject,
    ModifyMessageRequest,
)

logger = logging.getLogger(__name__)
settings = Settings()
client = OpenAI()


def create_message(
    thread_id: str,
    role: Literal["user", "assistant"],
    content: Union[str, List[MessageContent]],
    attachments: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Create a message.

    Args:
        thread_id: (REQUIRED) The ID of the thread to create a message for
        role: (REQUIRED) The role of the entity creating the message
            ('user' or 'assistant')
        content: (REQUIRED) The content of the message (string or list of content parts)
        attachments: List of file attachments
        metadata: Key-value pairs (max 16 pairs)

    Returns:
        Dict containing created message data
    """
    logger.info(f"Creating message in thread {thread_id}")

    # Convert raw attachment dicts to MessageAttachment objects if provided
    message_attachments = None
    if attachments:
        message_attachments = [
            MessageAttachment.model_validate(attachment) for attachment in attachments
        ]

    # Convert content to proper format if it's a list
    if isinstance(content, list):
        # Assuming content is already a list of MessageContent objects
        # since we updated the type hint
        pass

    request = CreateMessageRequest(
        role=role,
        content=content,
        attachments=message_attachments,
        metadata=metadata,
    )

    request_data = request.model_dump(exclude_none=True)
    logger.info(f"Creating message with request data: {request_data}")

    response = client.beta.threads.messages.create(thread_id=thread_id, **request_data)
    logger.info(f"Got response from OpenAI: {response}")

    validated = MessageObject.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump(exclude_none=True)
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)


def list_messages(
    thread_id: str,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List messages for a thread.

    Args:
        thread_id: (REQUIRED) The ID of the thread to list messages for
        limit: Limit on number of messages (1-100, default 20)
        order: Sort order ('asc' or 'desc', default 'desc')
        after: Cursor for pagination (get messages after this ID)
        before: Cursor for pagination (get messages before this ID)
        run_id: Filter for messages from a specific run

    Returns:
        Dict containing list of messages
    """
    logger.info(f"Listing messages for thread {thread_id}")

    params = {
        "limit": limit,
        "order": order,
        "after": after,
        "before": before,
        "run_id": run_id,
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    response = client.beta.threads.messages.list(thread_id=thread_id, **params)
    return cast(
        Dict[str, Any], MessageListResponse.model_validate(response).model_dump()
    )


def get_message(thread_id: str, message_id: str) -> Dict[str, Any]:
    """
    Get message by ID.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to retrieve

    Returns:
        Dict containing message data
    """
    logger.info(f"Getting message {message_id} from thread {thread_id}")

    response = client.beta.threads.messages.retrieve(
        thread_id=thread_id, message_id=message_id
    )
    return cast(Dict[str, Any], MessageObject.model_validate(response).model_dump())


def modify_message(
    thread_id: str,
    message_id: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Modify a message.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to modify
        metadata: Key-value pairs (max 16 pairs)

    Returns:
        Dict containing modified message data
    """
    logger.info(f"Modifying message {message_id} in thread {thread_id}")

    request = ModifyMessageRequest(metadata=metadata).model_dump(exclude_none=True)

    response = client.beta.threads.messages.update(
        thread_id=thread_id, message_id=message_id, **request
    )
    return cast(Dict[str, Any], MessageObject.model_validate(response).model_dump())


def delete_message(thread_id: str, message_id: str) -> Dict[str, Any]:
    """
    Delete a message.

    Args:
        thread_id: (REQUIRED) The ID of the thread the message belongs to
        message_id: (REQUIRED) The ID of the message to delete

    Returns:
        Dict containing deletion status
    """
    logger.info(f"Deleting message {message_id} from thread {thread_id}")

    response = client.beta.threads.messages.delete(
        thread_id=thread_id, message_id=message_id
    )
    return cast(
        Dict[str, Any], DeleteMessageResponse.model_validate(response).model_dump()
    )
