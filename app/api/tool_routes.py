from fastapi import APIRouter
from app.mcp.registry import registry
from pydantic import BaseModel
from app.mcp.executor import executor
from app.mcp.context import context_manager

router = APIRouter()

@router.get("/tools")
async def list_tools():
    return registry.list_tools()




class ToolExecutionRequest(BaseModel):
    tool_name: str
    params: dict
    session_id: str = "default"


@router.post("/tools/execute")
async def execute_tool(req: ToolExecutionRequest):
    return executor.execute(
        req.tool_name,
        req.params,
        req.session_id
    )

@router.get("/context/{session_id}")
async def get_context(session_id: str):
    return context_manager.get(session_id)