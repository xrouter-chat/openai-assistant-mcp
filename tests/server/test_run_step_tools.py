"""Tests for OpenAI Run Steps API MCP server tools."""
from unittest.mock import Mock, patch

import pytest
from openai import NOT_GIVEN

# Mock OpenAI before importing any modules that use it
mock_openai = Mock()
with patch("openai.OpenAI", return_value=mock_openai):
    with patch("src.tools.run_steps.tools.client", mock_openai):
        from src.server import get_run_step, list_run_steps

# Example responses from OpenAI API
EXAMPLE_RUN_STEP = {
    "id": "step_abc123",
    "object": "thread.run.step",
    "created_at": 1699012949,
    "run_id": "run_abc123",
    "assistant_id": "asst_abc123",
    "thread_id": "thread_abc123",
    "type": "message_creation",
    "status": "completed",
    "step_details": {
        "type": "message_creation",
        "message_creation": {"message_id": "msg_abc123"},
    },
    "last_error": None,
    "expired_at": None,
    "cancelled_at": None,
    "failed_at": None,
    "completed_at": 1699012950,
    "metadata": {},
}

EXAMPLE_RUN_STEP_LIST = {
    "object": "list",
    "data": [EXAMPLE_RUN_STEP],
    "first_id": "step_abc123",
    "last_id": "step_abc123",
    "has_more": False,
}


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Fixture to mock OpenAI client."""
    with patch("src.tools.run_steps.tools.client", mock_openai) as mock_client:
        mock_client.reset_mock()
        yield mock_client


def test_list_run_steps(mock_openai_client):
    """Test listing run steps through MCP server."""
    mock_openai_client.beta.threads.runs.steps.list.return_value = EXAMPLE_RUN_STEP_LIST

    result = list_run_steps(
        thread_id="thread_abc123",
        run_id="run_abc123",
        limit=10,
        order="desc",
    )

    assert result["object"] == "list"
    assert len(result["data"]) == 1
    assert result["first_id"] == "step_abc123"
    assert result["last_id"] == "step_abc123"
    assert result["has_more"] is False
    assert result["data"][0]["id"] == "step_abc123"
    assert result["data"][0]["object"] == "thread.run.step"
    assert result["data"][0]["run_id"] == "run_abc123"
    assert result["data"][0]["thread_id"] == "thread_abc123"
    assert result["data"][0]["type"] == "message_creation"
    assert result["data"][0]["status"] == "completed"

    mock_openai_client.beta.threads.runs.steps.list.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        limit=10,
        order="desc",
        after=NOT_GIVEN,
        before=NOT_GIVEN,
        include=NOT_GIVEN,
    )


def test_get_run_step(mock_openai_client):
    """Test retrieving a run step through MCP server."""
    mock_openai_client.beta.threads.runs.steps.retrieve.return_value = EXAMPLE_RUN_STEP

    result = get_run_step(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
    )

    assert result["id"] == "step_abc123"
    assert result["object"] == "thread.run.step"
    assert result["run_id"] == "run_abc123"
    assert result["thread_id"] == "thread_abc123"
    assert result["type"] == "message_creation"
    assert result["status"] == "completed"
    assert isinstance(result["created_at"], int)
    assert isinstance(result["completed_at"], int)
    assert result["step_details"]["type"] == "message_creation"
    assert result["step_details"]["message_creation"]["message_id"] == "msg_abc123"

    mock_openai_client.beta.threads.runs.steps.retrieve.assert_called_once_with(
        thread_id="thread_abc123",
        run_id="run_abc123",
        step_id="step_abc123",
        include=NOT_GIVEN,
    )
