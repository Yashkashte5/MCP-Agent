from fastapi import FastAPI
from app.config import settings
from app.mcp.registry import registry
from app.api.tool_routes import router as tool_router
from app.api.agent_routes import router_api
from app.tools.register_tools import register_all_tools
from app.mcp.memory_db import init_db

app = FastAPI(title=settings.APP_NAME)
init_db()
register_all_tools()
app.include_router(tool_router)
app.include_router(router_api)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}


