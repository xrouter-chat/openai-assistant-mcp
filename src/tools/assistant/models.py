from typing import Dict, List, Literal, Optional, Union, Annotated
from pydantic import BaseModel, Field

# Metadata type
MetadataKey = Annotated[str, Field(max_length=64, description="Metadata key with maximum length of 64 characters")]
MetadataValue = Annotated[str, Field(max_length=512, description="Metadata value with maximum length of 512 characters")]
Metadata = Dict[MetadataKey, MetadataValue]

# Response format models
class TextResponseFormat(BaseModel):
    type: Literal["text"] = Field(description="The type of response format being defined. Always text.")

class JsonObjectResponseFormat(BaseModel):
    type: Literal["json_object"] = Field(description="The type of response format being defined. Always json_object.")

class JsonSchemaConfig(BaseModel):
    name: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        max_length=64,
        description="The name of the response format. Must be a-z, A-Z, 0-9, or contain underscores and dashes."
    )
    description: Optional[str] = Field(default=None, description="A description of what the response format is for.")
    schema: dict = Field(description="The schema for the response format, described as a JSON Schema object.")
    strict: Optional[bool] = Field(default=None, description="Whether to enable strict schema adherence.")

class JsonSchemaResponseFormat(BaseModel):
    type: Literal["json_schema"] = Field(description="The type of response format being defined. Always json_schema.")
    json_schema: JsonSchemaConfig = Field(description="Structured Outputs configuration options.")

ResponseFormat = Union[Literal["auto"], TextResponseFormat, JsonObjectResponseFormat, JsonSchemaResponseFormat]

# Tool models
class CodeInterpreterTool(BaseModel):
    type: Literal["code_interpreter"] = Field(description="The type of tool being defined: code_interpreter")

class RankingOptions(BaseModel):
    score_threshold: float = Field(
        ge=0,
        le=1,
        description="The score threshold for the file search. All values must be a floating point number between 0 and 1."
    )
    ranker: Optional[str] = Field(
        default=None,
        description="The ranker to use for the file search. If not specified will use the auto ranker."
    )

class FileSearchConfig(BaseModel):
    max_num_results: Optional[int] = Field(
        default=None,
        ge=1,
        le=50,
        description="The maximum number of results the file search tool should output."
    )
    ranking_options: Optional[RankingOptions] = Field(
        default=None,
        description="The ranking options for the file search."
    )

class FileSearchTool(BaseModel):
    type: Literal["file_search"] = Field(description="The type of tool being defined: file_search")
    file_search: Optional[FileSearchConfig] = Field(
        default=None,
        description="Overrides for the file search tool."
    )

class FunctionParameters(BaseModel):
    name: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        max_length=64,
        description="The name of the function to be called."
    )
    description: Optional[str] = Field(
        default=None,
        description="A description of what the function does."
    )
    parameters: Optional[dict] = Field(
        default=None,
        description="The parameters the functions accepts, described as a JSON Schema object."
    )
    strict: Optional[bool] = Field(
        default=None,
        description="Whether to enable strict schema adherence when generating the function call."
    )

class FunctionTool(BaseModel):
    type: Literal["function"] = Field(description="The type of tool being defined: function")
    function: FunctionParameters = Field(description="The function definition.")

Tool = Union[CodeInterpreterTool, FileSearchTool, FunctionTool]

# Tool resources models
class CodeInterpreterResource(BaseModel):
    file_ids: List[str] = Field(
        default_factory=list,
        max_items=20,
        description="A list of file IDs made available to the code_interpreter tool."
    )

class FileSearchResource(BaseModel):
    vector_store_ids: List[str] = Field(
        default_factory=list,
        max_items=1,
        description="The vector store attached to this assistant."
    )

class ToolResources(BaseModel):
    code_interpreter: Optional[CodeInterpreterResource] = Field(
        default=None,
        description="Resources for the code interpreter tool."
    )
    file_search: Optional[FileSearchResource] = Field(
        default=None,
        description="Resources for the file search tool."
    )

# Assistant models
class BaseAssistant(BaseModel):
    name: Optional[str] = Field(
        default=None,
        max_length=256,
        description="The name of the assistant."
    )
    description: Optional[str] = Field(
        default=None,
        max_length=512,
        description="The description of the assistant."
    )
    instructions: Optional[str] = Field(
        default=None,
        max_length=256_000,
        description="The system instructions that the assistant uses."
    )
    metadata: Optional[Metadata] = Field(
        default=None,
        description="Set of key-value pairs that can be attached to an object."
    )
    tools: Optional[List[Tool]] = Field(
        default=None,
        max_items=128,
        description="A list of tools enabled on the assistant."
    )
    tool_resources: Optional[ToolResources] = Field(
        default=None,
        description="A set of resources that are used by the assistant's tools."
    )
    temperature: Optional[float] = Field(
        default=None,
        ge=0,
        le=2,
        description="What sampling temperature to use, between 0 and 2."
    )
    top_p: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="An alternative to sampling with temperature, called nucleus sampling."
    )
    response_format: Optional[ResponseFormat] = Field(
        default=None,
        description="Specifies the format that the model must output."
    )

class AssistantObject(BaseAssistant):
    id: Optional[str] = Field(
        default=None,
        description="The identifier, which can be referenced in API endpoints."
    )
    object: Optional[Literal["assistant"]] = Field(
        default=None,
        description="The object type, which is always assistant."
    )
    created_at: Optional[int] = Field(
        default=None,
        description="The Unix timestamp (in seconds) for when the assistant was created."
    )
    model: Optional[str] = Field(
        default=None,
        description="ID of the model to use."
    )

class CreateAssistantRequest(BaseAssistant):
    model: str = Field(description="ID of the model to use.")
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high."
    )
