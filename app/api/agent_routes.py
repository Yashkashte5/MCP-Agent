from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.router import router
from app.agents.orchestrator import agent

router_api = APIRouter()


class PromptRequest(BaseModel):
    prompt: str

class AgentRequest(BaseModel):
    prompt: str
    session_id: str = "default"


@router_api.post("/agent/run")
async def run_agent(req: AgentRequest):
    return await agent.run(req.prompt, req.session_id)
