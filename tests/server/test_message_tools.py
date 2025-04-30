"""Tests for OpenAI Message API MCP server tools."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    with patch("src.tools.messages.tools.client", mock_openai):
        from src.server import (
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
    "created_at": 1699012949,
    "thread_id": "thread_abc123",
    "role": "user",
    "content": [
        {"type": "text", "text": {"value": "Hello, how are you?", "annotations": []}}
    ],
    "file_ids": [],
    "assistant_id": None,
    "run_id": None,
    "metadata": {},
}

EXAMPLE_MESSAGE_LIST = {
    "object": "list",
    "data": [EXAMPLE_MESSAGE],
    "first_id": "msg_abc123",
    "last_id": "msg_abc123",
    "has_more": False,
}

EXAMPLE_MODIFIED_MESSAGE = {
    "id": "msg_abc123",
    "object": "thread.message",
    "created_at": 1699012949,
    "thread_id": "thread_abc123",
    "role": "user",
    "content": [
        {"type": "text", "text": {"value": "Hello, how are you?", "annotations": []}}
    ],
    "file_ids": [],
    "assistant_id": None,
    "run_id": None,
    "metadata": {"modified": "true", "user": "abc123"},
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
    """Test creating a message through MCP server."""
    mock_openai_client.beta.threads.messages.create.return_value = EXAMPLE_MESSAGE

    result = create_message(
        thread_id="thread_abc123", role="user", content="Hello, how are you?"
    )

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message"
    assert result["thread_id"] == "thread_abc123"
    assert result["role"] == "user"
    assert result["content"][0]["type"] == "text"
    assert result["content"][0]["text"]["value"] == "Hello, how are you?"
    assert isinstance(result["created_at"], int)
    assert result["metadata"] == {}

    mock_openai_client.beta.threads.messages.create.assert_called_once_with(
        thread_id="thread_abc123", role="user", content="Hello, how are you?"
    )


def test_get_message(mock_openai_client):
    """Test retrieving a message through MCP server."""
    mock_openai_client.beta.threads.messages.retrieve.return_value = EXAMPLE_MESSAGE

    result = get_message(thread_id="thread_abc123", message_id="msg_abc123")

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message"
    assert result["thread_id"] == "thread_abc123"
    assert isinstance(result["created_at"], int)

    mock_openai_client.beta.threads.messages.retrieve.assert_called_once_with(
        thread_id="thread_abc123", message_id="msg_abc123"
    )


def test_list_messages(mock_openai_client):
    """Test listing messages through MCP server."""
    mock_openai_client.beta.threads.messages.list.return_value = EXAMPLE_MESSAGE_LIST

    result = list_messages(thread_id="thread_abc123", limit=10, order="desc")

    assert result["object"] == "list"
    assert len(result["data"]) == 1
    assert result["first_id"] == "msg_abc123"
    assert result["last_id"] == "msg_abc123"
    assert result["has_more"] is False

    mock_openai_client.beta.threads.messages.list.assert_called_once_with(
        thread_id="thread_abc123", limit=10, order="desc"
    )


def test_modify_message(mock_openai_client):
    """Test modifying a message through MCP server."""
    mock_openai_client.beta.threads.messages.update.return_value = (
        EXAMPLE_MODIFIED_MESSAGE
    )

    metadata = {"modified": "true", "user": "abc123"}
    result = modify_message(
        thread_id="thread_abc123", message_id="msg_abc123", metadata=metadata
    )

    assert result["id"] == "msg_abc123"
    assert result["metadata"]["modified"] == "true"
    assert result["metadata"]["user"] == "abc123"

    mock_openai_client.beta.threads.messages.update.assert_called_once_with(
        thread_id="thread_abc123", message_id="msg_abc123", metadata=metadata
    )


def test_delete_message(mock_openai_client):
    """Test deleting a message through MCP server."""
    mock_openai_client.beta.threads.messages.delete.return_value = (
        EXAMPLE_DELETED_RESPONSE
    )

    result = delete_message(thread_id="thread_abc123", message_id="msg_abc123")

    assert result["id"] == "msg_abc123"
    assert result["object"] == "thread.message.deleted"
    assert result["deleted"] is True

    mock_openai_client.beta.threads.messages.delete.assert_called_once_with(
        thread_id="thread_abc123", message_id="msg_abc123"
    )
