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
        self.tools[name] = {
            "description": description,
            "function": func,
            "schema": schema or {},
        }

    def list_tools(self):
        return {
            name: {
                "description": data["description"],
                "schema": data["schema"],
            }
            for name, data in self.tools.items()
        }

    def get(self, name):
        return self.tools.get(name)


registry = ToolRegistry()
