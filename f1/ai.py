import json
import os
import shutil
from typing import Any, Callable, Optional

import openai
import pandas as pd
import tiktoken
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

from f1.helpers import generate_schemas
from f1.prompts import SYSTEM_CONTENT, response_too_long_prompt


class FormulaOneAI:
    def __init__(
        self,
        api_key: Optional[str],
        funcs: list[Callable[..., Any]],
        gpt_model: str = "gpt-3.5-turbo-0613",
    ):
        if api_key is None:
            raise RuntimeError("API Key given is null")
        self.api_key = api_key
        openai.api_key = self.api_key

        self.gpt_model = gpt_model
        self.messages: list[dict[str, Any]] = []

        # Add PandasAI function to input F1 data functions
        functions = funcs.copy()
        functions.append(self.data_analysis)
        functions.append(self.create_chart)

        # Generate schemas for GPT and function mappings
        self.function_schema = generate_schemas(functions)
        self.function_mapping = {func.__name__: func for func in functions}

        # Keep track of last called function, last returned dataframe, and last returned function response
        self.last_called_function: str = ""
        self.last_returned_df: pd.DataFrame = pd.DataFrame({})
        self.last_returned_function_response: Any = None

        # Create PandasAI object
        llm = OpenAI(api_token=self.api_key)
        self.pandas_ai = PandasAI(llm, save_charts=True, save_charts_path="f1")

        # Delete any graphs if there are any
        self._delete_all_graphs("f1/exports/charts")

    def ask(self, prompt):
        # Delete old graphs
        self._delete_all_graphs("f1/exports/charts")

        # Add initial conversation messages
        self.messages = [{"role": "system", "content": SYSTEM_CONTENT}]
        self.messages.append({"role": "user", "content": prompt})

        response = self._chat_completion()
        self.messages.append(response)  # extend conversation with assistant's reply

        while response.get("function_call"):
            function_name, kwargs = self._parse_response(response)
            func = self.function_mapping[function_name]
            function_response = func(**kwargs)

            self.last_called_function = function_name
            self.last_returned_function_response = function_response

            if isinstance(function_response, pd.DataFrame):
                self.last_returned_df = function_response

            serialized_response = self._serialize_response(function_response)

            self._add_function_response(serialized_response)

            response = self._chat_completion()
            self.messages.append(response)  # extend conversation with assistant's reply

        return response["content"]

    def data_analysis(self, prompt: str) -> Any:
        """Function that can run data analysis on a pd.DataFrame.

        This function cannot fetch any data. It can only be called after getting
        data from another function first.

        This function has access to the most recently returned pd.DataFrame.

        Args:
            prompt (str): The prompt to run the data analysis. The prompt will take the
            form of natural language (e.g. if you want to find a driver_id from driver info,
            then you can have the prompt as, "Get me the driver_id of driver x from the dataframe")
        Return:
            Any: The response to the prompt.
        """
        if self.last_returned_df.empty:
            raise RuntimeError("Empty pd.DataFrame being given to PandasAI")

        return self.pandas_ai(self.last_returned_df, prompt)

    def create_chart(self, prompt: str) -> Any:
        """Function that can create plots or graphs.

        This function cannot fetch any data. It can only be called after getting
        data from another function first.

        This function has access to the most recently returned pd.DataFrame.

        The chart(s) will be saved and displayed to the user in the application. Your
        response after this function should mention that the graph has been created and
        is ready to view

        Args:
            prompt (str): The prompt to create the plots or graphs. The prompt will take
            the form of natural language (e.g. if you want to graph driver finishing position,
            then you can have the prompt as, "Plot the driver finishing position.")
        Return:
            Any: The response to the prompt.
        """
        if self.last_returned_df.empty:
            raise RuntimeError("Empty pd.DataFrame being given to PandasAI")

        return self.pandas_ai(self.last_returned_df, prompt)

    def _delete_all_graphs(self, dir_name) -> None:
        """Delete all the previously created graphs"""
        if not os.path.isdir(dir_name):
            return

        # Get subdirectories
        subdirectories = [f.path for f in os.scandir(dir_name) if f.is_dir()]
        for subdir in subdirectories:
            # Delete each subdirectory
            shutil.rmtree(subdir)

    def _add_function_response(self, serialized_response: str) -> None:
        """Create a response for GPT after receiving the function response.

        Add the response to the conversation."""
        function_response = self.last_returned_function_response
        function_name = self.last_called_function

        if self._response_is_too_long(serialized_response):
            # We will not send back to the whole response to GPT
            # We will send back info about the response and tell it
            # to use PandasAI to access the data

            # Check that response is a dataframe
            if not isinstance(function_response, pd.DataFrame):
                response_type = type(function_response)
                raise RuntimeError(
                    f"Function was too long to return. Type: {response_type}"
                )

            content = response_too_long_prompt(function_name, function_response)
            # extend conversation with custom user response
            self.messages.append(
                {
                    "role": "user",
                    "content": content,
                }
            )
        else:
            # extend conversation with function response
            self.messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": serialized_response,
                }
            )

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
