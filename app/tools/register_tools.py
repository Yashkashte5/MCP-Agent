from app.mcp.registry import registry
from app.tools.analytics import basic_stats
from app.tools.summarizer import summarize_text


def register_all_tools():
    registry.register(
        name="basic_stats",
        description="Counts words and characters",
        func=basic_stats,
        schema={"text": "string"},
    )

    registry.register(
        name="summarize_text",
        description="Summarizes long text",
        func=summarize_text,
        schema={"text": "string"},
    )
