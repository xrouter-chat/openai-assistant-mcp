"""OpenAI Run Steps API tools implementation."""
import logging
from typing import Any, Dict, List, Literal, Optional, cast

from openai import OpenAI
from openai.types.beta.threads.runs import RunStepInclude

from ...config.settings import Settings
from .models import RunStepListResponse, RunStepObject

logger = logging.getLogger("openai-assistant-mcp")
settings = Settings()
client = OpenAI()


def list_run_steps(
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
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run to list steps for
        limit: Optional limit on number of steps (1-100, default 20)
        order: Optional sort order ('asc' or 'desc', default 'desc')
        after: Optional cursor for pagination (get steps after this ID)
        before: Optional cursor for pagination (get steps before this ID)
        include: Optional list of additional fields to include in the response
                Currently only supports
                'step_details.tool_calls[*].file_search.results[*].content'

    Returns:
        Dict containing list of run steps
    """
    logger.info(f"Listing run steps for run {run_id} in thread {thread_id}")

    # Build query parameters
    query_params = {
        "limit": limit,
        "order": order,
        "after": after,
        "before": before,
    }
    # Remove None values
    query_params = {k: v for k, v in query_params.items() if v is not None}

    # Add include parameter separately
    if include:
        query_params["include"] = ",".join(str(i) for i in include)

    response = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id,
        extra_query=query_params if query_params else None,
    )
    logger.info(f"Got response from OpenAI: {response}")

    validated = RunStepListResponse.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump(exclude_none=True)
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)


def get_run_step(
    thread_id: str,
    run_id: str,
    step_id: str,
    include: Optional[List[RunStepInclude]] = None,
) -> Dict[str, Any]:
    """
    Get run step by ID.

    Args:
        thread_id: The ID of the thread the run belongs to
        run_id: The ID of the run the step belongs to
        step_id: The ID of the run step to retrieve
        include: Optional list of additional fields to include in the response
                Currently only supports
                'step_details.tool_calls[*].file_search.results[*].content'

    Returns:
        Dict containing run step data
    """
    logger.info(f"Getting run step {step_id} from run {run_id} in thread {thread_id}")

    response = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=step_id,
        extra_query={"include": include} if include else None,
    )
    logger.info(f"Got response from OpenAI: {response}")

    validated = RunStepObject.model_validate(response)
    logger.info(f"Validated response: {validated}")

    result = validated.model_dump(exclude_none=True)
    logger.info(f"Final result: {result}")

    return cast(Dict[str, Any], result)
