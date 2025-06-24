"""OpenAI Run Steps API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, cast

from openai import NOT_GIVEN, OpenAI
from openai.types.beta.threads.runs import RunStepInclude

logger = logging.getLogger(__name__)


def list_run_steps(
    client: OpenAI,
    thread_id: str,
    run_id: str,
    limit: Optional[int] = None,
    order: Optional[Literal["asc", "desc"]] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    include: Optional[List[RunStepInclude]] = None,
) -> Dict[str, Any]:
    """
    List run steps for a run.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run to list steps for
        limit: Limit on number of steps (1-100, default 20)
        order: Sort order ('asc' or 'desc', default 'desc')
        after: Cursor for pagination (get steps after this ID)
        before: Cursor for pagination (get steps before this ID)
        include: List of additional fields to include in the response
                Currently only supports
                'step_details.tool_calls[*].file_search.results[*].content'

    Returns:
        SyncCursorPage[RunStep]: The list of run steps from OpenAI SDK
    """
    logger.info(f"Listing run steps for run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id,
        limit=limit if limit is not None else NOT_GIVEN,
        order=order if order is not None else NOT_GIVEN,
        after=after if after is not None else NOT_GIVEN,
        before=before if before is not None else NOT_GIVEN,
        include=include if include is not None else NOT_GIVEN,
    )
    logger.info(f"Got response from OpenAI: {response}")

    return cast(Dict[str, Any], response.model_dump())


def get_run_step(
    client: OpenAI,
    thread_id: str,
    run_id: str,
    step_id: str,
    include: Optional[List[RunStepInclude]] = None,
) -> Dict[str, Any]:
    """
    Get run step by ID.

    Args:
        client: OpenAI client instance (injected)
        thread_id: (REQUIRED) The ID of the thread the run belongs to
        run_id: (REQUIRED) The ID of the run the step belongs to
        step_id: (REQUIRED) The ID of the run step to retrieve
        include: List of additional fields to include in the response
                Currently only supports
                'step_details.tool_calls[*].file_search.results[*].content'

    Returns:
        RunStep: The retrieved run step from OpenAI SDK
    """
    logger.info(f"Getting run step {step_id} from run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=step_id,
        include=include if include is not None else NOT_GIVEN,
    )
    logger.info(f"Got response from OpenAI: {response}")

    return cast(Dict[str, Any], response.model_dump())
