import json
from typing import Any, Tuple

import openai
from functions import function_schemas, get_driver_standings


class FormulaOneAI:
    def __init__(self, api_key, gpt_model="gpt-4"):
        self.api_key = api_key
        openai.api_key = self.api_key

        self.gpt_model = gpt_model
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        self.function_schema = function_schemas
        self.function_mapping = {"get_driver_standings": get_driver_standings}

    def ask(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self._chat_completion()
        if response.get("function_call"):
            function_name, kwargs = self.parse_response(response)
            func = self.function_mapping[function_name]
            function_response = func(**kwargs)

            self.messages.append(response)  # extend conversation with assistant's reply
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

            second_response = self._chat_completion()
            return second_response["content"]
        else:
            return response["content"]

    def _chat_completion(self) -> dict[str, Any]:
        response = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=self.messages,
            functions=self.function_schema,
            max_tokens=100,
        )
        message = response["choices"][0]["message"]

        self.messages.append(message)
        return message

    def parse_response(self, message: dict[str, Any]) -> Tuple[str, Any]:
        return message["function_call"]["name"], json.loads(
            message["function_call"]["arguments"]
        )
