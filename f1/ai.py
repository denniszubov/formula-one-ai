import json
from typing import Any, Callable, Optional

import openai
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

from f1.helpers import generate_schemas
from f1.prompts import SYSTEM_CONTENT


class FormulaOneAI:
    def __init__(
        self,
        api_key: Optional[str],
        funcs: list[Callable[..., Any]],
        gpt_model: str = "gpt-3.5-turbo",
    ):
        if api_key is None:
            raise RuntimeError("API Key given is null")
        self.api_key = api_key
        openai.api_key = self.api_key

        self.gpt_model = gpt_model
        self.messages: list[dict[str, Any]] = []
        self.function_schema = generate_schemas(funcs)
        self.function_mapping = {func.__name__: func for func in funcs}

        # Keep track of last returned dataframe for PandasAI
        self.last_returned_df: pd.DataFrame = pd.DataFrame({})

        # Create PandasAI object
        llm = OpenAI(api_token=self.api_key)
        self.pandas_ai = PandasAI(llm)

    def ask(self, prompt):
        self.messages = [{"role": "system", "content": SYSTEM_CONTENT}]
        self.messages.append({"role": "user", "content": prompt})
        response = self._chat_completion()
        while response.get("function_call"):
            function_name, kwargs = self._parse_response(response)
            func = self.function_mapping[function_name]
            function_response = func(**kwargs)

            if isinstance(function_response, pd.DataFrame):
                self.last_returned_df = function_response

            self.messages.append(response)  # extend conversation with assistant's reply
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": self._serialize_response(function_response),
                }
            )

            response = self._chat_completion()

        self.messages.append(response)  # Add latest GPT assistant response
        return response["content"]

    def _chat_completion(self) -> dict[str, Any]:
        response = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=self.messages,
            functions=self.function_schema,
            max_tokens=200,
        )
        message = response["choices"][0]["message"]

        return message

    def _parse_response(self, message: dict[str, Any]) -> tuple[str, Any]:
        return message["function_call"]["name"], json.loads(
            message["function_call"]["arguments"]
        )

    def _serialize_response(self, response: Any) -> str:
        if isinstance(response, pd.DataFrame):
            if response.empty:
                return "{}"
            return response.to_json()
        return json.dumps(response)
