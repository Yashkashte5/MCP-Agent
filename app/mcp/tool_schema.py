from app.mcp.registry import registry


def get_tool_descriptions():
    tools = []

    for name, data in registry.tools.items():
        tools.append({
            "name": name,
            "description": data.get("description", ""),
            "params": data.get("schema", {}),
        })

    return tools
