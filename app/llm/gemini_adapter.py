import os
import httpx
from app.llm.base import BaseLLM


class GeminiAdapter(BaseLLM):

    async def generate(self, prompt: str):
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload)

        data = response.json()

        # Raise error so router fallback triggers
        if "candidates" not in data:
            raise Exception(f"Gemini API error: {data}")

        return data["candidates"][0]["content"]["parts"][0]["text"]
