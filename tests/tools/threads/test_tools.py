"""Tests for OpenAI Thread API tools implementation."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    from src.tools.threads.tools import (
        create_thread,
        delete_thread,
        get_thread,
        modify_thread,
    )

# Example responses from OpenAI API
EXAMPLE_THREAD = {
    "id": "thread_abc123",
    "object": "thread",
    "created_at": 1699012949,
    "metadata": {},
    "tool_resources": {},
}

EXAMPLE_THREAD_WITH_MESSAGES = {
    "id": "thread_abc123",
    "object": "thread",
    "created_at": 1699012949,
    "metadata": {},
    "tool_resources": {},
}

EXAMPLE_THREAD_WITH_TOOL_RESOURCES = {
    "id": "thread_abc123",
    "object": "thread",
    "created_at": 1699014083,
    "metadata": {},
    "tool_resources": {"code_interpreter": {"file_ids": []}},
}

EXAMPLE_MODIFIED_THREAD = {
    "id": "thread_abc123",
    "object": "thread",
    "created_at": 1699014083,
    "metadata": {"modified": "true", "user": "abc123"},
    "tool_resources": {},
}

EXAMPLE_DELETED_RESPONSE = {
    "id": "thread_abc123",
    "object": "thread.deleted",
    "deleted": True,
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.threads.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_create_thread(mock_openai_client):
    """Test creating a thread."""
    mock_openai_client.beta.threads.create.return_value = EXAMPLE_THREAD

    result = create_thread()

    assert result["id"] == "thread_abc123"
    assert result["object"] == "thread"
    assert isinstance(result["created_at"], int)
    assert result["metadata"] == {}
    assert result["tool_resources"] == {}

    mock_openai_client.beta.threads.create.assert_called_once()


def test_create_thread_with_messages(mock_openai_client):
    """Test creating a thread with initial messages."""
    mock_openai_client.beta.threads.create.return_value = EXAMPLE_THREAD_WITH_MESSAGES

    messages = [
        {
            "role": "user",
            "content": "Hello, how are you?",
        }
    ]
    result = create_thread(messages=messages)

    assert result["id"] == "thread_abc123"
    assert result["object"] == "thread"

    mock_openai_client.beta.threads.create.assert_called_once()


def test_create_thread_with_tool_resources(mock_openai_client):
    """Test creating a thread with tool resources."""
    mock_openai_client.beta.threads.create.return_value = (
        EXAMPLE_THREAD_WITH_TOOL_RESOURCES
    )

    tool_resources = {"code_interpreter": {"file_ids": []}}
    result = create_thread(tool_resources=tool_resources)

    assert result["id"] == "thread_abc123"
    assert result["tool_resources"]["code_interpreter"]["file_ids"] == []

    mock_openai_client.beta.threads.create.assert_called_once()


def test_get_thread(mock_openai_client):
    """Test retrieving a thread."""
    mock_openai_client.beta.threads.retrieve.return_value = EXAMPLE_THREAD

    result = get_thread("thread_abc123")

    assert result["id"] == "thread_abc123"
    assert result["object"] == "thread"
    assert isinstance(result["created_at"], int)

    mock_openai_client.beta.threads.retrieve.assert_called_once_with("thread_abc123")


def test_modify_thread(mock_openai_client):
    """Test modifying a thread."""
    mock_openai_client.beta.threads.update.return_value = EXAMPLE_MODIFIED_THREAD

    metadata = {"modified": "true", "user": "abc123"}
    result = modify_thread(thread_id="thread_abc123", metadata=metadata)

    assert result["id"] == "thread_abc123"
    assert result["metadata"]["modified"] == "true"
    assert result["metadata"]["user"] == "abc123"

    mock_openai_client.beta.threads.update.assert_called_once_with(
        "thread_abc123", metadata=metadata
    )


def test_delete_thread(mock_openai_client):
    """Test deleting a thread."""
    mock_openai_client.beta.threads.delete.return_value = EXAMPLE_DELETED_RESPONSE

    result = delete_thread("thread_abc123")

    assert result["id"] == "thread_abc123"
    assert result["object"] == "thread.deleted"
    assert result["deleted"] is True

    mock_openai_client.beta.threads.delete.assert_called_once_with("thread_abc123")
