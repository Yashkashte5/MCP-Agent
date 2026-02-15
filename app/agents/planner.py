from app.llm.router import router
from app.utils.json_guard import extract_json
from app.utils.logger import logger


class AgentPlanner:

    async def create_plan(self, prompt: str, tools: list):
        planner_prompt = f"""
You are an AI planning agent.

User request:
{prompt}

Available tools:
{tools}

Create a short execution plan.

Respond ONLY JSON:

{{
"steps": [
  {{
    "action": "tool/chat",
    "tool_name": "...",
    "purpose": "why needed"
  }}
]
}}
"""

        response = await router.generate(planner_prompt)

        plan = extract_json(response)

        if not plan:
            logger.warning("Planner failed — fallback simple chat")
            return None

        return plan


planner = AgentPlanner()
