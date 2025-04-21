"""Tests for OpenAI Assistant API tools implementation."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    from src.tools.assistant.models import CodeInterpreterTool
    from src.tools.assistant.tools import (
        create_assistant,
        delete_assistant,
        get_assistant,
        list_assistants,
        modify_assistant,
    )

# Example responses from OpenAI API
EXAMPLE_ASSISTANT = {
    "id": "asst_abc123",
    "object": "assistant",
    "created_at": 1698984975,
    "name": "Math Tutor",
    "description": None,
    "model": "gpt-4o",
    "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    "tools": [{"type": "code_interpreter"}],
    "metadata": {},
    "top_p": 1.0,
    "temperature": 1.0,
    "response_format": "auto",
}

EXAMPLE_ASSISTANTS_LIST = {
    "object": "list",
    "data": [
        {
            "id": "asst_abc123",
            "object": "assistant",
            "created_at": 1698982736,
            "name": "Coding Tutor",
            "description": None,
            "model": "gpt-4o",
            "instructions": "You are a helpful assistant designed to make me better at coding!",
            "tools": [],
            "tool_resources": {},
            "metadata": {},
            "top_p": 1.0,
            "temperature": 1.0,
            "response_format": "auto",
        },
        {
            "id": "asst_abc456",
            "object": "assistant",
            "created_at": 1698982718,
            "name": "My Assistant",
            "description": None,
            "model": "gpt-4o",
            "instructions": "You are a helpful assistant designed to make me better at coding!",
            "tools": [],
            "tool_resources": {},
            "metadata": {},
            "top_p": 1.0,
            "temperature": 1.0,
            "response_format": "auto",
        },
    ],
    "first_id": "asst_abc123",
    "last_id": "asst_abc456",
    "has_more": False,
}

EXAMPLE_DELETED_RESPONSE = {
    "id": "asst_abc123",
    "object": "assistant.deleted",
    "deleted": True,
}


@pytest.fixture
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.assistant.tools.client", mock_openai) as mock_client:
        yield mock_client


def test_create_assistant(mock_openai_client):
    """Test creating an assistant."""
    mock_openai_client.beta.assistants.create.return_value = EXAMPLE_ASSISTANT

    result = create_assistant(
        model="gpt-4o",
        name="Math Tutor",
        instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        tools=[CodeInterpreterTool(type="code_interpreter")],
    )

    assert result["id"] == "asst_abc123"
    assert result["name"] == "Math Tutor"
    assert result["model"] == "gpt-4o"
    assert len(result["tools"]) == 1
    assert result["tools"][0]["type"] == "code_interpreter"

    mock_openai_client.beta.assistants.create.assert_called_once()


def test_get_assistant(mock_openai_client):
    """Test retrieving an assistant."""
    mock_openai_client.beta.assistants.retrieve.return_value = EXAMPLE_ASSISTANT

    result = get_assistant("asst_abc123")

    assert result["id"] == "asst_abc123"
    assert result["name"] == "Math Tutor"
    assert result["model"] == "gpt-4o"

    mock_openai_client.beta.assistants.retrieve.assert_called_once_with("asst_abc123")


def test_list_assistants(mock_openai_client):
    """Test listing assistants."""
    mock_openai_client.beta.assistants.list.return_value = Mock(
        data=EXAMPLE_ASSISTANTS_LIST["data"]
    )

    result = list_assistants()

    assert len(result["data"]) == 2
    assert result["data"][0]["id"] == "asst_abc123"
    assert result["data"][0]["name"] == "Coding Tutor"
    assert result["data"][1]["id"] == "asst_abc456"
    assert result["data"][1]["name"] == "My Assistant"

    mock_openai_client.beta.assistants.list.assert_called_once()


def test_modify_assistant(mock_openai_client):
    """Test modifying an assistant."""
    modified_assistant = dict(EXAMPLE_ASSISTANT)
    modified_assistant["instructions"] = "New instructions"
    mock_openai_client.beta.assistants.update.return_value = modified_assistant

    result = modify_assistant(
        assistant_id="asst_abc123", instructions="New instructions"
    )

    assert result["id"] == "asst_abc123"
    assert result["instructions"] == "New instructions"

    mock_openai_client.beta.assistants.update.assert_called_once_with(
        "asst_abc123", instructions="New instructions"
    )


def test_delete_assistant(mock_openai_client):
    """Test deleting an assistant."""
    mock_openai_client.beta.assistants.delete.return_value = Mock(
        **EXAMPLE_DELETED_RESPONSE
    )

    result = delete_assistant("asst_abc123")

    assert result["id"] == "asst_abc123"
    assert result["deleted"] is True

    mock_openai_client.beta.assistants.delete.assert_called_once_with("asst_abc123")
