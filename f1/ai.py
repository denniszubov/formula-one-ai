import json
from typing import Any, Callable, Optional

import openai
import pandas as pd
import tiktoken
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

        # Add PandasAI function to input F1 data functions
        funcs.append(self.ask_pandasai)

        # Generate schemas for GPT and function mappings
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
        self.messages.append(response)  # extend conversation with assistant's reply

        while response.get("function_call"):
            function_name, kwargs = self._parse_response(response)
            func = self.function_mapping[function_name]
            function_response = func(**kwargs)

            if isinstance(function_response, pd.DataFrame):
                self.last_returned_df = function_response

            # extend conversation with function response
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": self._serialize_response(function_response),
                }
            )

            response = self._chat_completion()
            self.messages.append(response)  # extend conversation with assistant's reply

        self.messages.append(response)  # Add latest GPT assistant response
        return response["content"]

    def ask_pandasai(self, prompt: str) -> Any:
        """Function that makes use of PandasAI to run data analysis on a pd.DataFrame
        or create plots of graphs using the pd.DataFrame. This function has access
        to the most recently returned pd.DataFrame.

        Args:
            prompt (str): The prompt to give to the AI to run the data analysis or to
                create plots or graphs. The prompt will take the form of natural language
                (e.g. "Find the French driver with the most amount of wins between 2000
                and 2022 in the dataframe")
        Return:
            Any: The response to the prompt.
        """
        if self.last_returned_df.empty:
            raise RuntimeError("Empty pd.DataFrame being given to PandasAI")

        return self.pandas_ai(self.last_returned_df, prompt)

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

    def _get_token_length(self, prompt: str) -> int:
        """Get the token length of the given prompt

        This is useful for checking the tokens before sending a
        response back to GPT in the case that the response is
        too long"""
        encoder = tiktoken.encoding_for_model(self.gpt_model)
        encoding = encoder.encode(prompt)
        return len(encoding)

    def _response_is_too_long(self, prompt: str) -> bool:
        """Check if the response is too long to give to GPT.

        Currently our token limit is set at 1000 tokens"""
        return self._get_token_length(prompt) > 1000
