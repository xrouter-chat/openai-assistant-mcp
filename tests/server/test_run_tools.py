"""Tests for OpenAI Run API MCP server tools."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    with patch("src.tools.runs.tools.client", mock_openai):
        from src.server import (
            cancel_run,
            create_run,
            create_thread_and_run,
            get_run,
            list_runs,
            modify_run,
            submit_tool_outputs,
        )

# Example responses from OpenAI API
EXAMPLE_RUN = {
    "id": "run_abc123",
    "object": "thread.run",
    "created_at": 1699012949,
    "thread_id": "thread_abc123",
    "assistant_id": "asst_abc123",
    "status": "completed",
    "required_action": None,
    "last_error": None,
    "expires_at": None,
    "started_at": 1699012950,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": 1699012951,
    "model": "gpt-4",
    "instructions": None,
    "tools": [],
    "file_ids": [],
    "metadata": {},
}

EXAMPLE_RUN_LIST = {
    "object": "list",
    "data": [EXAMPLE_RUN],
    "first_id": "run_abc123",
    "last_id": "run_abc123",
    "has_more": False,
}

EXAMPLE_MODIFIED_RUN = {
    **EXAMPLE_RUN,
    "metadata": {"modified": "true", "user": "abc123"},
}

EXAMPLE_CANCELLED_RUN = {
    **EXAMPLE_RUN,
    "status": "cancelled",
    "cancelled_at": 1699012952,
}

EXAMPLE_THREAD_AND_RUN = {
    "thread_id": "thread_abc123",
    "run_id": "run_abc123",
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.runs.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_create_run(mock_openai_client):
    """Test creating a run through MCP server."""
    mock_openai_client.beta.threads.runs.create.return_value = EXAMPLE_RUN

    result = create_run(
        thread_id="thread_abc123",
        assistant_id="asst_abc123",
        model="gpt-4",
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["thread_id"] == "thread_abc123"
    assert result["assistant_id"] == "asst_abc123"
    assert result["status"] == "completed"
    assert result["model"] == "gpt-4"
    assert isinstance(result["created_at"], int)

    mock_openai_client.beta.threads.runs.create.assert_called_once_with(
        thread_id="thread_abc123",
        assistant_id="asst_abc123",
        model="gpt-4",
    )


def test_create_thread_and_run(mock_openai_client):
    """Test creating a thread and run through MCP server."""
    mock_openai_client.beta.threads.create_and_run.return_value = EXAMPLE_THREAD_AND_RUN

    result = create_thread_and_run(
        assistant_id="asst_abc123",
        thread={"messages": [{"role": "user", "content": "Hello"}]},
        model="gpt-4",
    )

    assert result["thread_id"] == "thread_abc123"
    assert result["run_id"] == "run_abc123"

    mock_openai_client.beta.threads.create_and_run.assert_called_once_with(
        assistant_id="asst_abc123",
        thread={"messages": [{"role": "user", "content": "Hello"}]},
        model="gpt-4",
    )


def test_list_runs(mock_openai_client):
    """Test listing runs through MCP server."""
    mock_openai_client.beta.threads.runs.list.return_value = EXAMPLE_RUN_LIST

    result = list_runs(
        thread_id="thread_abc123",
        limit=10,
        order="desc",
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 1
    assert result["first_id"] == "run_abc123"
    assert result["last_id"] == "run_abc123"
    assert result["has_more"] is False
    assert result["data"][0]["id"] == "run_abc123"
    assert result["data"][0]["thread_id"] == "thread_abc123"

    mock_openai_client.beta.threads.runs.list.assert_called_once_with(
        thread_id="thread_abc123",
        limit=10,
        order="desc",
    )


def test_get_run(mock_openai_client):
    """Test retrieving a run through MCP server."""
    mock_openai_client.beta.threads.runs.retrieve.return_value = EXAMPLE_RUN

    result = get_run(thread_id="thread_abc123", run_id="run_abc123")

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["thread_id"] == "thread_abc123"
    assert result["assistant_id"] == "asst_abc123"
    assert result["status"] == "completed"
    assert isinstance(result["created_at"], int)

    mock_openai_client.beta.threads.runs.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )


def test_modify_run(mock_openai_client):
    """Test modifying a run through MCP server."""
    mock_openai_client.beta.threads.runs.update.return_value = EXAMPLE_MODIFIED_RUN

    metadata = {"modified": "true", "user": "abc123"}
    result = modify_run(
        thread_id="thread_abc123",
        run_id="run_abc123",
        metadata=metadata,
    )

    assert result["id"] == "run_abc123"
    assert result["metadata"]["modified"] == "true"
    assert result["metadata"]["user"] == "abc123"

    mock_openai_client.beta.threads.runs.update.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        metadata=metadata,
    )


def test_submit_tool_outputs(mock_openai_client):
    """Test submitting tool outputs through MCP server."""
    mock_openai_client.beta.threads.runs.submit_tool_outputs.return_value = EXAMPLE_RUN

    tool_outputs = [{"tool_call_id": "call_abc123", "output": "Hello"}]
    result = submit_tool_outputs(
        thread_id="thread_abc123",
        run_id="run_abc123",
        tool_outputs=tool_outputs,
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["thread_id"] == "thread_abc123"
    assert result["status"] == "completed"

    mock_openai_client.beta.threads.runs.submit_tool_outputs.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        tool_outputs=tool_outputs,
    )


def test_cancel_run(mock_openai_client):
    """Test cancelling a run through MCP server."""
    mock_openai_client.beta.threads.runs.cancel.return_value = EXAMPLE_CANCELLED_RUN

    result = cancel_run(thread_id="thread_abc123", run_id="run_abc123")

    assert result["id"] == "run_abc123"
    assert result["status"] == "cancelled"
    assert isinstance(result["cancelled_at"], int)

    mock_openai_client.beta.threads.runs.cancel.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )
