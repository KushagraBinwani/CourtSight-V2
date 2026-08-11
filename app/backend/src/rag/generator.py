from google import genai

from src.config import (
    GEMINI_API_KEY,
    LLM_MODEL,
)


class Generator:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )

        return response.text