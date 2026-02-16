from app.llm.router import router
from app.utils.json_guard import extract_json
from app.utils.logger import logger


class AgentPlanner:

    async def create_plan(self, prompt: str, tools: list):
        planner_prompt = f"""
You are a planning agent for an AI system.

Available tools:
{tools}

STRICT RULES:

- Only use tools from the provided list.
- NEVER invent tool names.
- If the user request can be answered directly,
  return:

{{
  "steps": []
}}

- Only call tools when absolutely necessary.
- Each step MUST follow:

{{
  "action": "tool",
  "tool_name": "...",
  "purpose": "why tool is needed"
}}

Output ONLY valid JSON.
No explanations.
No extra text.

"""

        response = await router.generate(planner_prompt)

        plan = extract_json(response)

        if not plan:
            logger.warning("Planner failed — fallback simple chat")
            return None

        return plan


planner = AgentPlanner()
