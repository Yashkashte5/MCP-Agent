import os

from app.llm.groq_adapter import GroqAdapter
from app.llm.gemini_adapter import GeminiAdapter
from app.utils.logger import logger


class LLMRouter:

    def __init__(self):
        self.primary = os.getenv("LLM_PROVIDER", "groq")

    def get_primary(self):
        if self.primary == "gemini":
            return GeminiAdapter()
        return GroqAdapter()

    def get_fallback(self):
        if self.primary == "gemini":
            return GroqAdapter()
        return GeminiAdapter()

    async def generate(self, prompt: str):

        primary_model = self.get_primary()

        try:
            return await primary_model.generate(prompt)

        except Exception as primary_error:
            print("Primary LLM failed:", primary_error)

            fallback_model = self.get_fallback()

            try:
                return await fallback_model.generate(prompt)

            except Exception as fallback_error:
                print("Fallback also failed:", fallback_error)
                return "LLM services temporarily unavailable."
    async def generate(self, prompt: str):

        primary_model = self.get_primary()

        logger.info(f"LLM request | provider={self.primary}")

        try:
            response = await primary_model.generate(prompt)
            logger.info("Primary LLM success")
            return response

        except Exception as primary_error:
            logger.error(f"Primary LLM failed: {primary_error}")

            fallback_model = self.get_fallback()

            try:
                response = await fallback_model.generate(prompt)
                logger.info("Fallback LLM success")
                return response

            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                return "LLM services temporarily unavailable."


router = LLMRouter()
