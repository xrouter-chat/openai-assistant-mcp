"""Tests for OpenAI Run Steps API tools implementation."""
from unittest.mock import Mock, patch

import pytest

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    from src.tools.run_steps.tools import get_run_step, list_run_steps

# Example responses from OpenAI API documentation
EXAMPLE_RUN_STEP = {
    "id": "step_abc123",
    "object": "thread.run.step",
    "created_at": 1699063291,
    "run_id": "run_abc123",
    "assistant_id": "asst_abc123",
    "thread_id": "thread_abc123",
    "type": "message_creation",
    "status": "completed",
    "cancelled_at": None,
    "completed_at": 1699063291,
    "expired_at": None,
    "failed_at": None,
    "last_error": None,
    "step_details": {
        "type": "message_creation",
        "message_creation": {"message_id": "msg_abc123"},
    },
    "usage": {"prompt_tokens": 123, "completion_tokens": 456, "total_tokens": 579},
}

EXAMPLE_RUN_STEP_LIST = {
    "object": "list",
    "data": [
        {
            "id": "step_abc123",
            "object": "thread.run.step",
            "created_at": 1699063291,
            "run_id": "run_abc123",
            "assistant_id": "asst_abc123",
            "thread_id": "thread_abc123",
            "type": "message_creation",
            "status": "completed",
            "cancelled_at": None,
            "completed_at": 1699063291,
            "expired_at": None,
            "failed_at": None,
            "last_error": None,
            "step_details": {
                "type": "message_creation",
                "message_creation": {"message_id": "msg_abc123"},
            },
            "usage": {
                "prompt_tokens": 123,
                "completion_tokens": 456,
                "total_tokens": 579,
            },
        }
    ],
    "first_id": "step_abc123",
    "last_id": "step_abc456",
    "has_more": False,
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.run_steps.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_list_run_steps(mock_openai_client):
    """Test listing run steps."""
    mock_openai_client.beta.threads.runs.steps.list.return_value = EXAMPLE_RUN_STEP_LIST

    result = list_run_steps(
        thread_id="thread_abc123",
        run_id="run_abc123",
        limit=20,
        order="desc",
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == "step_abc123"
    assert result["data"][0]["type"] == "message_creation"
    assert result["data"][0]["status"] == "completed"
    assert result["first_id"] == "step_abc123"
    assert result["last_id"] == "step_abc456"
    assert not result["has_more"]

    mock_openai_client.beta.threads.runs.steps.list.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        extra_query={
            "limit": 20,
            "order": "desc",
        },
    )


def test_list_run_steps_with_include(mock_openai_client):
    """Test listing run steps with include parameter."""
    mock_openai_client.beta.threads.runs.steps.list.return_value = EXAMPLE_RUN_STEP_LIST

    result = list_run_steps(
        thread_id="thread_abc123",
        run_id="run_abc123",
        include=["step_details.tool_calls[*].file_search.results[*].content"],
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 1

    mock_openai_client.beta.threads.runs.steps.list.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        extra_query={
            "include": ["step_details.tool_calls[*].file_search.results[*].content"],
        },
    )


def test_get_run_step(mock_openai_client):
    """Test retrieving a run step."""
    mock_openai_client.beta.threads.runs.steps.retrieve.return_value = EXAMPLE_RUN_STEP

    result = get_run_step(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
    )

    assert result["id"] == "step_abc123"
    assert result["object"] == "thread.run.step"
    assert result["type"] == "message_creation"
    assert result["status"] == "completed"
    assert result["step_details"]["type"] == "message_creation"
    assert result["step_details"]["message_creation"]["message_id"] == "msg_abc123"

    mock_openai_client.beta.threads.runs.steps.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
        extra_query=None,
    )


def test_get_run_step_with_include(mock_openai_client):
    """Test retrieving a run step with include parameter."""
    mock_openai_client.beta.threads.runs.steps.retrieve.return_value = EXAMPLE_RUN_STEP

    result = get_run_step(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
        include=["step_details.tool_calls[*].file_search.results[*].content"],
    )

    assert result["id"] == "step_abc123"
    assert result["object"] == "thread.run.step"

    mock_openai_client.beta.threads.runs.steps.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
        extra_query={
            "include": ["step_details.tool_calls[*].file_search.results[*].content"],
        },
    )
