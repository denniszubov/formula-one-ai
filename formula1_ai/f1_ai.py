import openai


class FormulaOneAI:
    def __init__(self, api_key, gpt_model="gpt-4"):
        self.api_key = api_key
        openai.api_key = self.api_key

        self.gpt_model = gpt_model
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def ask(self, prompt, max_tokens=100):
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=self.messages,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"]
