"""Pydantic models for OpenAI Assistant API.

This module provides type-safe models for interacting with the OpenAI Assistant API,
including models for assistants, tools, and response formats.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..models import Metadata, ResponseFormat, Tool, ToolResources


# Assistant models
class BaseAssistant(BaseModel):
    """Base model for OpenAI Assistant with common fields."""

    name: Optional[str] = Field(
        default=None, max_length=256, description="The name of the assistant."
    )
    description: Optional[str] = Field(
        default=None, max_length=512, description="The description of the assistant."
    )
    instructions: Optional[str] = Field(
        default=None,
        max_length=256_000,
        description="The system instructions that the assistant uses.",
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to an object.",
    )
    tools: Optional[List[Tool]] = Field(
        default=None,
        description="A list of tools enabled on the assistant.",
        max_length=128,
    )
    tool_resources: Optional[ToolResources] = Field(
        default=None,
        description="A set of resources that are used by the assistant's tools.",
    )
    temperature: Optional[float] = Field(
        default=None,
        ge=0,
        le=2,
        description="What sampling temperature to use, between 0 and 2.",
    )
    top_p: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="An alternative to sampling with temperature, "
        "called nucleus sampling.",
    )
    response_format: Optional[ResponseFormat] = Field(
        default=None, description="Specifies the format that the model must output."
    )


class AssistantObject(BaseAssistant):
    """Model representing an assistant in API responses."""

    id: Optional[str] = Field(
        default=None,
        description="The identifier, which can be referenced in API endpoints.",
    )
    object: Optional[Literal["assistant"]] = Field(
        default=None, description="The object type, which is always assistant."
    )
    created_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the assistant "
        "was created.",
    )
    model: Optional[str] = Field(default=None, description="ID of the model to use.")


class CreateAssistantRequest(BaseAssistant):
    """Model for creating a new assistant."""

    model: str = Field(description="ID of the model to use.")
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Constrains effort on reasoning for reasoning models.",
    )


class ModifyAssistantRequest(BaseAssistant):
    """Model for modifying an existing assistant."""

    model: Optional[str] = Field(
        default=None,
        description="ID of the model to use.",
    )
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Constrains effort on reasoning for reasoning models.",
    )
