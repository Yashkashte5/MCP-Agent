from app.llm.router import router
from app.mcp.executor import executor
from app.mcp.context import context_manager
from app.utils.logger import logger
import json
from app.mcp.tool_schema import get_tool_descriptions
from app.utils.json_guard import extract_json
from app.mcp.memory_db import save_summary, get_summary
from app.agents.planner import planner
from app.agents.plan_validator import validate_plan


class AgentOrchestrator:

    async def run(self, prompt: str, session_id: str = "default"):
        logger.info(f"Agent request | session={session_id}")

        # Save user input
        context_manager.save(session_id, "user", prompt)

        history = context_manager.get(session_id)
        tools = get_tool_descriptions()

        # ---- Memory summarization ----
        if len(history) > 8:
            summary_prompt = f"Summarize conversation:\n{history}"
            new_summary = await router.generate(summary_prompt)
            save_summary(session_id, new_summary)

        summary = get_summary(session_id)


        plan = await planner.create_plan(prompt, tools)

        if plan:
            is_valid, reason = validate_plan(plan, tools)
            if not is_valid:
                logger.warning(f"Invalid plan: {reason}")
                plan = None

        if plan and "steps" in plan:
            if len(plan["steps"]) > 5:
                logger.warning("Plan too long, truncating")
                plan["steps"] = plan["steps"][:5]

            logger.info(f"Execution plan: {plan}")

            aggregated_results = []

            for step in plan["steps"]:
                action = step.get("action", "")
                tool_name = step.get("tool_name")

                if "tool" in action and tool_name:
                    params = step.get("params") or {"text": prompt}

                    logger.info(f"Executing planned tool: {tool_name}")

                    result = await executor.execute(
                        tool_name,
                        params,
                        session_id
                    )

                    aggregated_results.append({
                        "tool": tool_name,
                        "result": result
                    })

            if aggregated_results:
                final_prompt = f"""
You are an AI assistant.

Conversation summary:
{summary}

Conversation history:
{json.dumps(history, indent=2)}

User request:
{prompt}

Tool results:
{json.dumps(aggregated_results, indent=2)}

Provide the final helpful answer.
"""

                final_response = await router.generate(final_prompt)
                context_manager.save(session_id, "assistant", final_response)

                return {
                    "type": "llm_response",
                    "data": final_response
                }



        system_prompt = f"""
You are an AI agent with access to tools.

Conversation summary:
{summary}

Conversation history:
{json.dumps(history, indent=2)}

Available tools:
{json.dumps(tools, indent=2)}

If a tool is useful respond ONLY in JSON:

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

IMPORTANT RULES:

- If a tool result is already provided, DO NOT call the same tool again.
- Use the provided tool result to generate the final answer.
- Only call another tool if absolutely necessary.
"""

        current_prompt = system_prompt + "\nUser: " + prompt
        max_steps = 3
        response = ""

        for step in range(max_steps):
            logger.info(f"Agent step {step+1}")

            response = await router.generate(current_prompt)
            decision = extract_json(response)

            if not decision:
                logger.warning("Failed JSON extraction — fallback")
                break

            # TOOL EXECUTION
            if decision.get("action") == "tool":
                tool_name = decision.get("tool_name")
                params = decision.get("params", {})

                logger.info(f"Tool chosen: {tool_name}")

                result = await executor.execute(
                    tool_name,
                    params,
                    session_id
                )

                current_prompt += f"""

Tool execution completed.

Tool: {tool_name}
Result: {result}

Use this result to answer the user.
Do NOT call the same tool again.
"""
                continue

            # FINAL CHAT RESPONSE
            if decision.get("action") == "chat":
                final_response = decision.get("response", response)
                context_manager.save(session_id, "assistant", final_response)

                return {
                    "type": "llm_response",
                    "data": final_response
                }

        # fallback
        context_manager.save(session_id, "assistant", response)

        return {
            "type": "llm_response",
            "data": response
        }


agent = AgentOrchestrator()
