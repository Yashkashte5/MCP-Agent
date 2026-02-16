def validate_plan(plan: dict, available_tools: list):
    """
    Strict validation for planner output.

    Prevents:
    - hallucinated tools
    - invalid action types
    - malformed steps
    - duplicate tool loops
    - bad planner JSON
    """

    if not isinstance(plan, dict):
        return False, "Plan must be a dict"

    steps = plan.get("steps")
    if steps is None:
        return False, "Missing 'steps' key"

    if not isinstance(steps, list):
        return False, "'steps' must be a list"

    # Allow empty plan (means no tool needed)
    if len(steps) == 0:
        return True, "No tools required"

    tool_names = {tool["name"] for tool in available_tools}
    seen_tools = set()

    for i, step in enumerate(steps):

        if not isinstance(step, dict):
            return False, f"Step {i} must be an object"

        # 🔹 Strict action check
        action = step.get("action")
        if action != "tool":
            return False, f"Invalid action in step {i}: {action}"

        # 🔹 Tool validation
        tool_name = step.get("tool_name")
        if not tool_name:
            return False, f"Missing tool_name in step {i}"

        if tool_name not in tool_names:
            return False, f"Unknown tool: {tool_name}"

        # 🔹 Prevent repeated tool loops
        if tool_name in seen_tools:
            return False, f"Repeated tool detected: {tool_name}"

        seen_tools.add(tool_name)

    return True, "Valid plan"
