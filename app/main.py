from fastapi import FastAPI
from app.config import settings
from app.mcp.registry import registry
from app.tools.analytics import basic_stats
from app.api.tool_routes import router as tool_router
from app.api.agent_routes import router_api

app = FastAPI(title=settings.APP_NAME)
app.include_router(tool_router)
app.include_router(router_api)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}

@app.on_event("startup")
async def register_tools():
    registry.register(
        name="basic_stats",
        description="Returns word and character count",
        func=basic_stats,
        schema={
            "text": "string"
        },
    )
