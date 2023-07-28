from typing import Any, TypedDict


class Parameters(TypedDict):
    type: str
    properties: dict[str, dict[str, Any]]
    required: list[str]


class FunctionSchema(TypedDict):
    name: str
    description: str
    parameters: Parameters
