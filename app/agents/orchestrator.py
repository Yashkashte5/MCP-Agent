from app.llm.router import router
from app.mcp.executor import executor
from app.mcp.context import context_manager
from app.utils.logger import logger


class AgentOrchestrator:

    async def run(self, prompt: str, session_id: str = "default"):
        logger.info(f"Agent request | session={session_id}")

        # Save user input
        context_manager.save(session_id, "user", prompt)

        # Simple decision logic (expand later)
        if "count" in prompt.lower():
            logger.info("Agent decision | tool=basic_stats")

            result = executor.execute(
                "basic_stats",
                {"text": prompt},
                session_id
            )

            return {
                "type": "tool_result",
                "data": result
            }

        # Otherwise use LLM
        logger.info("Agent decision | llm_response")

        response = await router.generate(prompt)

        context_manager.save(session_id, "assistant", response)

        logger.info(f"Agent response generated | session={session_id}")

        return {
            "type": "llm_response",
            "data": response
        }


agent = AgentOrchestrator()
