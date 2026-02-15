from app.llm.router import router
from app.mcp.executor import executor
from app.mcp.context import context_manager
from app.utils.logger import logger
import json
from app.mcp.tool_schema import get_tool_descriptions
from app.utils.json_guard import extract_json
from app.mcp.memory_db import save_summary, get_summary

class AgentOrchestrator:

    async def run(self, prompt: str, session_id: str = "default"):
        logger.info(f"Agent request | session={session_id}")

        # Save user input to memory
        context_manager.save(session_id, "user", prompt)
        history = context_manager.get(session_id)
        if len(history) > 8:
            summary_prompt = f"Summarize conversation:\n{history}"
            new_summary = await router.generate(summary_prompt)
            save_summary(session_id, new_summary)

        tools = get_tool_descriptions()
        
        

        summary = get_summary(session_id)


        system_prompt = f"""
            You are an AI agent with access to tools.

            Conversation history:
            {json.dumps(history, indent=2)}

            Available tools:
            {json.dumps(tools, indent=2)}

            Conversation summary:
            {summary}

            Recent conversation:
            {json.dumps(history, indent=2)}

            If a tool is useful, respond ONLY in JSON:

            {{
            "action": "tool",
            "tool_name": "...",
            "params": {{}}
            }}

            Otherwise respond:

            {{
            "action": "chat",
            "response": "your answer"
            }}
            """


        full_prompt = system_prompt + "\nUser: " + prompt

        response = await router.generate(full_prompt)

        logger.info("LLM decision received")

        # 🔹 JSON Guardrail
        decision = extract_json(response)

        if not decision:
            logger.warning("Failed to extract JSON decision — fallback to chat")
            return {
                "type": "llm_response",
                "data": response
            }

        # 🔹 Tool execution path
        if decision.get("action") == "tool":
            logger.info(f"Tool chosen by LLM: {decision.get('tool_name')}")

            result = await executor.execute(
                decision.get("tool_name"),
                decision.get("params", {}),
                session_id
            )

            return {
                "type": "tool_result",
                "data": result
            }

        # 🔹 Normal LLM response path
        return {
            "type": "llm_response",
            "data": decision.get("response", response)
        }



agent = AgentOrchestrator()
