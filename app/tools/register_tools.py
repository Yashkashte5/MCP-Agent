from app.mcp.registry import registry
from app.tools.summarizer import summarize_text


def register_all_tools():

    registry.register(
        name="summarize_text",
        description="Summarizes long text",
        func=summarize_text,
        schema={"text": "string"},
    )
