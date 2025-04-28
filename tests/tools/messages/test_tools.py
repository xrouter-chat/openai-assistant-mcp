"""Tests for OpenAI Message API tools implementation."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    from src.tools.messages.tools import (
        create_message,
        delete_message,
        get_message,
        list_messages,
        modify_message,
    )

# Example responses from OpenAI API
EXAMPLE_MESSAGE = {
    "id": "msg_abc123",
    "object": "thread.message",
    "created_at": 1713226573,
    "assistant_id": None,
    "thread_id": "thread_abc123",
    "run_id": None,
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "How does AI work? Explain it in simple terms.",
                "annotations": [],
            },
        }
    ],
    "attachments": [],
    "metadata": {},
}

EXAMPLE_MESSAGE_LIST = {
    "object": "list",
    "data": [
        {
            "id": "msg_abc123",
            "object": "thread.message",
            "created_at": 1699016383,
            "assistant_id": None,
            "thread_id": "thread_abc123",
            "run_id": None,
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "value": "How does AI work? Explain it in simple terms.",
                        "annotations": [],
                    },
                }
            ],
            "attachments": [],
            "metadata": {},
        },
        {
            "id": "msg_abc456",
            "object": "thread.message",
            "created_at": 1699016383,
            "assistant_id": None,
            "thread_id": "thread_abc123",
            "run_id": None,
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "value": "Hello, what is AI?",
                        "annotations": [],
                    },
                }
            ],
            "attachments": [],
            "metadata": {},
        },
    ],
    "first_id": "msg_abc123",
    "last_id": "msg_abc456",
    "has_more": False,
}

EXAMPLE_MODIFIED_MESSAGE = {
    "id": "msg_abc123",
    "object": "thread.message",
    "created_at": 1699017614,
    "assistant_id": None,
    "thread_id": "thread_abc123",
    "run_id": None,
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": {
                "value": "How does AI work? Explain it in simple terms.",
                "annotations": [],
            },
        }
    ],
    "file_ids": [],
    "metadata": {
        "modified": "true",
        "user": "abc123",
    },
}

EXAMPLE_DELETED_RESPONSE = {
    "id": "msg_abc123",
    "object": "thread.message.deleted",
    "deleted": True,
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.messages.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_create_message(mock_openai_client):
    """Test creating a message."""
    mock_openai_client.beta.threads.messages.create.return_value = EXAMPLE_MESSAGE

    result = create_message(
        thread_id="thread_abc123",
        role="user",
        content="How does AI work? Explain it in simple terms.",
    )

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message"
    assert result["role"] == "user"
    assert result["content"][0]["type"] == "text"
    assert (
        result["content"][0]["text"]["value"]
        == "How does AI work? Explain it in simple terms."
    )

    mock_openai_client.beta.threads.messages.create.assert_called_once_with(
        thread_id="thread_abc123",
        role="user",
        content="How does AI work? Explain it in simple terms.",
    )


def test_list_messages(mock_openai_client):
    """Test listing messages."""
    mock_openai_client.beta.threads.messages.list.return_value = EXAMPLE_MESSAGE_LIST

    result = list_messages(
        thread_id="thread_abc123",
        limit=2,
        order="desc",
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 2
    assert result["first_id"] == "msg_abc123"
    assert result["last_id"] == "msg_abc456"
    assert not result["has_more"]

    mock_openai_client.beta.threads.messages.list.assert_called_once_with(
        thread_id="thread_abc123",
        limit=2,
        order="desc",
    )


def test_get_message(mock_openai_client):
    """Test retrieving a message."""
    mock_openai_client.beta.threads.messages.retrieve.return_value = EXAMPLE_MESSAGE

    result = get_message(
        thread_id="thread_abc123",
        message_id="msg_abc123",
    )

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message"
    assert result["role"] == "user"
    assert result["content"][0]["type"] == "text"

    mock_openai_client.beta.threads.messages.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        message_id="msg_abc123",
    )


def test_modify_message(mock_openai_client):
    """Test modifying a message."""
    mock_openai_client.beta.threads.messages.update.return_value = (
        EXAMPLE_MODIFIED_MESSAGE
    )

    metadata = {"modified": "true", "user": "abc123"}
    result = modify_message(
        thread_id="thread_abc123",
        message_id="msg_abc123",
        metadata=metadata,
    )

    assert result["id"] == "msg_abc123"
    assert result["metadata"]["modified"] == "true"
    assert result["metadata"]["user"] == "abc123"

    mock_openai_client.beta.threads.messages.update.assert_called_once_with(
        thread_id="thread_abc123",
        message_id="msg_abc123",
        metadata=metadata,
    )


def test_delete_message(mock_openai_client):
    """Test deleting a message."""
    mock_openai_client.beta.threads.messages.delete.return_value = (
        EXAMPLE_DELETED_RESPONSE
    )

    result = delete_message(
        thread_id="thread_abc123",
        message_id="msg_abc123",
    )

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message.deleted"
    assert result["deleted"] is True

    mock_openai_client.beta.threads.messages.delete.assert_called_once_with(
        thread_id="thread_abc123",
        message_id="msg_abc123",
    )
