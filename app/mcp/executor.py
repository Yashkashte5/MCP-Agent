from app.mcp.registry import registry
from app.mcp.context import context_manager
from app.utils.logger import logger


class ToolExecutor:

    @staticmethod
    def execute(tool_name: str, params: dict, session_id: str = "default"):
        logger.info(f"Tool execution requested | tool={tool_name} | session={session_id}")

        tool = registry.get(tool_name)

        if not tool:
            logger.warning(f"Tool not found | tool={tool_name}")
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        try:
            func = tool["function"]

            logger.info(f"Executing tool | tool={tool_name} | params={params}")
            result = func(**params)

            # Save interaction to context
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
            logger.error(f"Tool execution failed | tool={tool_name} | error={str(e)}")

            return {
                "success": False,
                "tool": tool_name,
                "error": str(e)
            }


executor = ToolExecutor()
