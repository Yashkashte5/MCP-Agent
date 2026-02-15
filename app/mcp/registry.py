from typing import Dict, Callable, Any


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        schema: dict = None,
    ):
        """Register a tool with metadata for agent usage."""
        self.tools[name] = {
            "description": description,
            "function": func,
            "schema": schema or {},
        }

    def list_tools(self):
        """Basic listing (used for API/debug)."""
        return {
            name: {
                "description": data["description"],
                "schema": data["schema"],
            }
            for name, data in self.tools.items()
        }

    def get(self, name):
        """Get full tool entry."""
        return self.tools.get(name)

    def get_tool_descriptions(self):
        """
        LLM-friendly tool descriptions.
        Used by agent orchestrator for tool reasoning.
        """
        return [
            {
                "name": name,
                "description": data["description"],
                "params": data["schema"],
            }
            for name, data in self.tools.items()
        ]


registry = ToolRegistry()
