import os
import httpx
from app.llm.base import BaseLLM


class GroqAdapter(BaseLLM):

    async def generate(self, prompt: str):
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=payload)

        # IMPORTANT DEBUG STEP
        print("Groq RAW RESPONSE:", response.text)

        data = response.json()

        if "choices" not in data:
            raise Exception(f"Groq API error: {data}")

        return data["choices"][0]["message"]["content"]
