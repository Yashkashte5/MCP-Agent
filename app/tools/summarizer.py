from app.llm.router import router


async def summarize_text(text: str):
    prompt = f"""
Summarize this text concisely:

{text}
"""

    summary = await router.generate(prompt)

    return {
        "summary": summary.strip()
    }
