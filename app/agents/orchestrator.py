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
import uuid
from app.memory.vector_store import retrieve_memory, store_memory


class AgentOrchestrator:

    async def run(self, prompt: str, session_id: str = "default"):
        import uuid

        trace_id = str(uuid.uuid4())
        logger.info(f"Agent trace started | trace_id={trace_id}")

        # ---- Save user input ----
        context_manager.save(session_id, "user", prompt)

        history = context_manager.get(session_id)
        recent_history = history[-6:] if history else []

        tools = get_tool_descriptions()

        # ---- Retrieve vector memory only for meaningful prompts ----
        memory_context = ""
        if len(prompt.split()) > 6:
            try:
                memory_chunks = retrieve_memory(prompt, k=3)
                memory_context = "\n".join(memory_chunks) if memory_chunks else ""
            except Exception as e:
                logger.error(f"Memory retrieval failed: {e}")

        # ---- Conversation summarization (periodic) ----
        if len(history) % 10 == 0 and history:
            summary_prompt = f"Summarize conversation:\n{history}"
            new_summary = await router.generate(summary_prompt)
            save_summary(session_id, new_summary)

        summary = get_summary(session_id)

        # =====================================================
        # 🔹 PLANNER LAYER (only when needed)
        # =====================================================
        plan = None
        if tools and any(
            word in prompt.lower()
            for word in ["summarize", "calculate", "search", "tool"]
        ):
            plan = await planner.create_plan(prompt, tools)

        if plan:
            is_valid, reason = validate_plan(plan, tools)
            if not is_valid:
                logger.warning(f"Invalid plan: {reason}")
                plan = None

        # =====================================================
        # 🔹 EXECUTE PLAN
        # =====================================================
        if plan and "steps" in plan:

            if len(plan["steps"]) > 5:
                logger.warning("Plan too long, truncating")
                plan["steps"] = plan["steps"][:5]

            logger.info(f"Execution plan: {plan}")

            aggregated_results = []

            for step in plan["steps"]:
                action = step.get("action", "")
                tool_name = step.get("tool_name")

                if action == "tool" and tool_name:
                    params = step.get("params") or {"text": prompt}

                    logger.info(f"Executing planned tool: {tool_name}")

                    result = await executor.execute(
                        tool_name,
                        params,
                        session_id,
                        trace_id=trace_id
                    )

                    aggregated_results.append({
                        "tool": tool_name,
                        "result": result
                    })

            if aggregated_results:
                final_prompt = f"""
    You are an AI assistant.

    Relevant past context:
    {memory_context}

    Conversation summary:
    {summary}

    Recent conversation:
    {json.dumps(recent_history, indent=2)}

    User request:
    {prompt}

    Tool results:
    {json.dumps(aggregated_results, indent=2)}

    Provide the final helpful answer.
    """

                final_response = await router.generate(final_prompt)
                context_manager.save(session_id, "assistant", final_response)

                # Store meaningful conversations only
                if len(prompt.split()) > 6 and "?" not in prompt:
                    try:
                        store_memory(
                            f"User: {prompt}\nAssistant: {final_response}",
                            {
                                "session": session_id,
                                "timestamp": now,
                                "topic": "project"
                                }

                        )
                    except Exception as e:
                        logger.error(f"Memory store failed: {e}")

                return {
                    "type": "llm_response",
                    "data": final_response
                }

        # =====================================================
        # 🔹 REACTIVE AGENT LOOP (fallback)
        # =====================================================
        system_prompt = f"""
    You are an AI agent with access to tools.

    Relevant past context:
    {memory_context}

    Conversation summary:
    {summary}

    Recent conversation:
    {json.dumps(recent_history, indent=2)}

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

    IMPORTANT:
    - Do not repeat tool calls.
    - Use tool results before calling another tool.
    """

        current_prompt = system_prompt + "\nUser: " + prompt
        max_steps = 3
        executed_tools = set()
        response = ""

        for step in range(max_steps):
            logger.info(f"Agent step {step+1}")

            response = await router.generate(current_prompt)
            decision = extract_json(response)

            if not decision:
                logger.warning("Failed JSON extraction — fallback")
                break

            if decision.get("action") == "tool":
                tool_name = decision.get("tool_name")
                params = decision.get("params", {})

                if not tool_name or tool_name in executed_tools:
                    logger.warning("Tool call blocked")
                    break

                executed_tools.add(tool_name)

                result = await executor.execute(
                    tool_name,
                    params,
                    session_id
                )

                current_prompt += f"""

    Tool execution completed.

    Tool: {tool_name}
    Result:
    {json.dumps(result, indent=2)}

    Use this result to answer the user.
    """
                continue

            if decision.get("action") == "chat":
                final_response = decision.get("response", response)
                context_manager.save(session_id, "assistant", final_response)

                if len(prompt.split()) > 6 and "?" not in prompt:
                    try:
                        store_memory(
                            f"User: {prompt}\nAssistant: {final_response}",
                            {"session": session_id}
                        )
                    except Exception as e:
                        logger.error(f"Memory store failed: {e}")

                return {
                    "type": "llm_response",
                    "data": final_response
                }

        # ---- Final fallback ----
        context_manager.save(session_id, "assistant", response)

        return {
            "type": "llm_response",
            "data": response
        }



agent = AgentOrchestrator()
