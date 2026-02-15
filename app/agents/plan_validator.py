def validate_plan(plan: dict, available_tools: list):
    """
    Validates planner output before execution.
    Prevents hallucinated tools and bad steps.
    """

    if not plan:
        return False, "Empty plan"

    if "steps" not in plan:
        return False, "Missing steps"

    tool_names = {tool["name"] for tool in available_tools}

    for step in plan["steps"]:
        tool = step.get("tool_name")

        if not tool:
            return False, "Missing tool name"

        if tool not in tool_names:
            return False, f"Unknown tool: {tool}"

    return True, "Valid"
