import inspect
from typing import Any, Callable, get_args, get_origin

import requests

from f1.typing import FunctionSchema

SIMPLE_MAPPING = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}


def get_schema_type(type_hint: Any) -> dict[str, Any]:
    """
    This function accepts a type hint and returns the corresponding JSON schema type.
    It maps basic types to their corresponding JSON schema types, and also processes list types.
    """
    schema_type = SIMPLE_MAPPING.get(type_hint)
    if schema_type:
        return {"type": schema_type}

    if get_origin(type_hint) is list:
        list_type_hint = get_args(type_hint)[0]
        list_type = SIMPLE_MAPPING.get(list_type_hint)
        if list_type is None:
            raise RuntimeError(f"Encountered unsupported type in list: {type_hint}")
        return {"type": "array", "items": {"type": list_type}}

    raise RuntimeError(f"Encountered unsupported type in list: {type_hint}")


def create_function_schema(func: Callable[..., Any]) -> FunctionSchema:
    """
    This function creates a JSON schema for a given Python function.
    It extracts the function name, description (or uses the name if not present),
    and parameters with their type and required attributes.
    """
    schema: FunctionSchema = {
        "name": func.__name__,
        "description": func.__doc__ or func.__name__,
        "parameters": {"type": "object", "properties": {}, "required": []},
    }

    func_parameters = inspect.signature(func).parameters
    for parameter_name, parameter in func_parameters.items():
        type_hint = parameter.annotation

        # Get schema type for parameter
        schema_type = get_schema_type(type_hint)
        schema["parameters"]["properties"][parameter_name] = schema_type

        # Check if parameter is required
        if parameter.default is inspect.Parameter.empty:
            schema["parameters"]["required"].append(parameter_name)

    return schema


def generate_schemas(funcs: list[Callable[..., Any]]) -> list[FunctionSchema]:
    """
    Generates JSON schemas for a list of Python functions.
    Used to generate schemas for GPT to use function calling
    """
    return [create_function_schema(func) for func in funcs]


def get_most_recent_race() -> dict[str, str]:
    """Get most recent race information. This will be given to GPT in the
    system prompt to give it more context."""
    url = "http://ergast.com/api/f1/current/last.json"

    response = requests.get(url)
    data = response.json()["MRData"]["RaceTable"]["Races"][0]

    most_recent_race = {
        "season": data["season"],
        "round": data["round"],
        "race_name": data["raceName"],
        "circuit_name": data["Circuit"]["circuitName"],
        "country": data["Circuit"]["Location"]["country"],
    }
    return most_recent_race
