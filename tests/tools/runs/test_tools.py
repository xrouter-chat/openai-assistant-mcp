"""Tests for OpenAI Run API tools implementation."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    from src.tools.models import CodeInterpreterTool
    from src.tools.runs.tools import (
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
    "created_at": 1699063290,
    "assistant_id": "asst_abc123",
    "thread_id": "thread_abc123",
    "status": "completed",
    "started_at": 1699063290,
    "expires_at": None,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": 1699063291,
    "last_error": None,
    "model": "gpt-4o",
    "instructions": None,
    "tools": [{"type": "code_interpreter"}],
    "metadata": {},
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579,
    },
    "temperature": 1.0,
    "top_p": 1.0,
    "max_prompt_tokens": 1000,
    "max_completion_tokens": 1000,
    "truncation_strategy": {
        "type": "auto",
        "last_messages": None,
    },
    "response_format": "auto",
    "tool_choice": "auto",
    "parallel_tool_calls": True,
}

EXAMPLE_RUN_LIST = {
    "object": "list",
    "data": [
        {
            "id": "run_abc123",
            "object": "thread.run",
            "created_at": 1699075072,
            "assistant_id": "asst_abc123",
            "thread_id": "thread_abc123",
            "status": "completed",
            "started_at": 1699075072,
            "expires_at": None,
            "cancelled_at": None,
            "failed_at": None,
            "completed_at": 1699075073,
            "last_error": None,
            "model": "gpt-4o",
            "instructions": None,
            "tools": [{"type": "code_interpreter"}],
            "metadata": {},
            "usage": {
                "prompt_tokens": 123,
                "completion_tokens": 456,
                "total_tokens": 579,
            },
            "temperature": 1.0,
            "top_p": 1.0,
            "max_prompt_tokens": 1000,
            "max_completion_tokens": 1000,
            "truncation_strategy": {
                "type": "auto",
                "last_messages": None,
            },
            "response_format": "auto",
            "tool_choice": "auto",
            "parallel_tool_calls": True,
        },
        {
            "id": "run_abc456",
            "object": "thread.run",
            "created_at": 1699063290,
            "assistant_id": "asst_abc123",
            "thread_id": "thread_abc123",
            "status": "completed",
            "started_at": 1699063290,
            "expires_at": None,
            "cancelled_at": None,
            "failed_at": None,
            "completed_at": 1699063291,
            "last_error": None,
            "model": "gpt-4o",
            "instructions": None,
            "tools": [{"type": "code_interpreter"}],
            "metadata": {},
            "usage": {
                "prompt_tokens": 123,
                "completion_tokens": 456,
                "total_tokens": 579,
            },
            "temperature": 1.0,
            "top_p": 1.0,
            "max_prompt_tokens": 1000,
            "max_completion_tokens": 1000,
            "truncation_strategy": {
                "type": "auto",
                "last_messages": None,
            },
            "response_format": "auto",
            "tool_choice": "auto",
            "parallel_tool_calls": True,
        },
    ],
    "first_id": "run_abc123",
    "last_id": "run_abc456",
    "has_more": False,
}

EXAMPLE_MODIFIED_RUN = {
    "id": "run_abc123",
    "object": "thread.run",
    "created_at": 1699075072,
    "assistant_id": "asst_abc123",
    "thread_id": "thread_abc123",
    "status": "completed",
    "started_at": 1699075072,
    "expires_at": None,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": 1699075073,
    "last_error": None,
    "model": "gpt-4o",
    "instructions": None,
    "tools": [{"type": "code_interpreter"}],
    "metadata": {
        "modified": "true",
        "user": "abc123",
    },
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579,
    },
    "temperature": 1.0,
    "top_p": 1.0,
    "max_prompt_tokens": 1000,
    "max_completion_tokens": 1000,
    "truncation_strategy": {
        "type": "auto",
        "last_messages": None,
    },
    "response_format": "auto",
    "tool_choice": "auto",
    "parallel_tool_calls": True,
}

EXAMPLE_CANCELLED_RUN = {
    "id": "run_abc123",
    "object": "thread.run",
    "created_at": 1699076126,
    "assistant_id": "asst_abc123",
    "thread_id": "thread_abc123",
    "status": "cancelling",
    "started_at": 1699076126,
    "expires_at": 1699076726,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": None,
    "last_error": None,
    "model": "gpt-4o",
    "instructions": "You summarize books.",
    "tools": [{"type": "file_search"}],
    "metadata": {},
    "temperature": 1.0,
    "top_p": 1.0,
    "response_format": "auto",
    "tool_choice": "auto",
    "parallel_tool_calls": True,
}

EXAMPLE_TOOL_OUTPUTS_RUN = {
    "id": "run_123",
    "object": "thread.run",
    "created_at": 1699075592,
    "assistant_id": "asst_123",
    "thread_id": "thread_123",
    "status": "queued",
    "started_at": 1699075592,
    "expires_at": 1699076192,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": None,
    "last_error": None,
    "model": "gpt-4o",
    "instructions": None,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ],
    "metadata": {},
    "usage": None,
    "temperature": 1.0,
    "top_p": 1.0,
    "max_prompt_tokens": 1000,
    "max_completion_tokens": 1000,
    "truncation_strategy": {
        "type": "auto",
        "last_messages": None,
    },
    "response_format": "auto",
    "tool_choice": "auto",
    "parallel_tool_calls": True,
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.runs.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_create_run(mock_openai_client):
    """Test creating a run."""
    mock_openai_client.beta.threads.runs.create.return_value = EXAMPLE_RUN

    # Create a tool instance that will be converted to dict by create_run
    tool = CodeInterpreterTool(type="code_interpreter")
    result = create_run(
        thread_id="thread_abc123",
        assistant_id="asst_abc123",
        model="gpt-4o",
        tools=[tool],
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["assistant_id"] == "asst_abc123"
    assert result["status"] == "completed"
    assert result["tools"][0]["type"] == "code_interpreter"

    # Check that the API was called with the tool converted to a dict
    mock_openai_client.beta.threads.runs.create.assert_called_once_with(
        thread_id="thread_abc123",
        assistant_id="asst_abc123",
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}],
    )


def test_create_thread_and_run(mock_openai_client):
    """Test creating a thread and run."""
    mock_openai_client.beta.threads.create_and_run.return_value = EXAMPLE_RUN

    result = create_thread_and_run(
        assistant_id="asst_abc123",
        thread={
            "messages": [
                {
                    "role": "user",
                    "content": "How does AI work? Explain it in simple terms.",
                }
            ]
        },
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["assistant_id"] == "asst_abc123"
    assert result["status"] == "completed"

    mock_openai_client.beta.threads.create_and_run.assert_called_once_with(
        assistant_id="asst_abc123",
        thread={
            "messages": [
                {
                    "role": "user",
                    "content": "How does AI work? Explain it in simple terms.",
                }
            ]
        },
    )


def test_list_runs(mock_openai_client):
    """Test listing runs."""
    mock_openai_client.beta.threads.runs.list.return_value = EXAMPLE_RUN_LIST

    result = list_runs(
        thread_id="thread_abc123",
        limit=2,
        order="desc",
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 2
    assert result["first_id"] == "run_abc123"
    assert result["last_id"] == "run_abc456"
    assert not result["has_more"]

    mock_openai_client.beta.threads.runs.list.assert_called_once_with(
        thread_id="thread_abc123",
        limit=2,
        order="desc",
    )


def test_get_run(mock_openai_client):
    """Test retrieving a run."""
    mock_openai_client.beta.threads.runs.retrieve.return_value = EXAMPLE_RUN

    result = get_run(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["assistant_id"] == "asst_abc123"
    assert result["status"] == "completed"

    mock_openai_client.beta.threads.runs.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )


def test_modify_run(mock_openai_client):
    """Test modifying a run."""
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
    """Test submitting tool outputs."""
    mock_openai_client.beta.threads.runs.submit_tool_outputs.return_value = (
        EXAMPLE_TOOL_OUTPUTS_RUN
    )

    tool_outputs = [
        {
            "tool_call_id": "call_abc123",
            "output": "70 degrees and sunny.",
        }
    ]

    result = submit_tool_outputs(
        thread_id="thread_123",
        run_id="run_123",
        tool_outputs=tool_outputs,
    )

    assert result["id"] == "run_123"
    assert result["object"] == "thread.run"
    assert result["status"] == "queued"
    assert result["tools"][0]["type"] == "function"
    assert result["tools"][0]["function"]["name"] == "get_current_weather"

    mock_openai_client.beta.threads.runs.submit_tool_outputs.assert_called_once_with(
        thread_id="thread_123",
        run_id="run_123",
        tool_outputs=tool_outputs,
    )


def test_cancel_run(mock_openai_client):
    """Test cancelling a run."""
    mock_openai_client.beta.threads.runs.cancel.return_value = EXAMPLE_CANCELLED_RUN

    result = cancel_run(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )

    assert result["id"] == "run_abc123"
    assert result["object"] == "thread.run"
    assert result["status"] == "cancelling"
    assert result["tools"][0]["type"] == "file_search"

    mock_openai_client.beta.threads.runs.cancel.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
    )
