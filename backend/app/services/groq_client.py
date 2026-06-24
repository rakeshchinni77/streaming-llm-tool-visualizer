import os
import logging
from typing import Any

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self) -> None:
        self.api_key = os.getenv("LLM_API_KEY") or os.getenv("GROQ_API_KEY")
        self.model = (
            os.getenv("LLM_MODEL")
            or os.getenv("MODEL_NAME")
            or "llama-3.3-70b-versatile"
        )

        if not self.api_key:
            raise ValueError("LLM_API_KEY is required to initialize GroqService")

        try:
            from groq import Groq
        except ImportError as exc:
            logger.exception("Groq SDK is not installed")
            raise RuntimeError("Groq SDK is required but missing") from exc

        self.client = Groq(api_key=self.api_key)

    def generate_response(self, user_message: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
            )

            if not getattr(chat_completion, "choices", None):
                return ""

            first_choice = chat_completion.choices[0]
            assistant_text = ""

            if hasattr(first_choice, "message"):
                assistant_text = getattr(first_choice.message, "content", "") or ""
            elif hasattr(first_choice, "content"):
                assistant_text = getattr(first_choice, "content", "") or ""

            return assistant_text.strip()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Groq generation failed")
            raise RuntimeError("Failed to generate response from Groq") from exc
