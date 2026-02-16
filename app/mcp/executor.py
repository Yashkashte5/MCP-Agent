import inspect
import time
from app.mcp.registry import registry
from app.mcp.context import context_manager
from app.utils.logger import logger


class ToolExecutor:

    async def execute(
        self,
        tool_name: str,
        params: dict,
        session_id: str = "default",
        trace_id: str | None = None,
    ):
        tool = registry.get(tool_name)

        if not tool:
            logger.warning(
                f"Tool lookup failed | trace={trace_id} | tool={tool_name}"
            )
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        func = tool["function"]

        start_time = time.time()

        try:
            logger.info(
                f"Executing tool | trace={trace_id} "
                f"| tool={tool_name} | params={params}"
            )

            # Async vs sync handling
            if inspect.iscoroutinefunction(func):
                result = await func(**params)
            else:
                result = func(**params)

            duration = round(time.time() - start_time, 3)

            # Save tool interaction in session memory
            context_manager.save(session_id, "tool", {
                "tool": tool_name,
                "params": params,
                "result": result,
                "trace_id": trace_id,
                "execution_time": duration,
            })

            logger.info(
                f"Tool execution success | trace={trace_id} "
                f"| tool={tool_name} | time={duration}s"
            )

            return {
                "success": True,
                "tool": tool_name,
                "result": result,
                "execution_time": duration
            }

        except Exception as e:
            duration = round(time.time() - start_time, 3)

            logger.exception(
                f"Tool execution error | trace={trace_id} "
                f"| tool={tool_name} | time={duration}s"
            )

            return {
                "success": False,
                "tool": tool_name,
                "error": str(e),
                "execution_time": duration
            }


executor = ToolExecutor()
