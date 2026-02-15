import inspect
from app.mcp.registry import registry
from app.mcp.context import context_manager
from app.utils.logger import logger


class ToolExecutor:

    async def execute(self, tool_name: str, params: dict, session_id: str = "default"):
        tool = registry.get(tool_name)

        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        try:
            func = tool["function"]

            logger.info(f"Executing tool | tool={tool_name} | params={params}")

            if inspect.iscoroutinefunction(func):
                result = await func(**params)
            else:
                result = func(**params)

            context_manager.save(session_id, "tool", {
                "tool": tool_name,
                "params": params,
                "result": result
            })

            logger.info(f"Tool execution success | tool={tool_name}")

            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }

        except Exception as e:
            logger.error(f"Tool execution error | {e}")
            return {
                "success": False,
                "tool": tool_name,
                "error": str(e)
            }


executor = ToolExecutor()
