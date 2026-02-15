import json
import re


def extract_json(text: str):
    """
    Extract JSON object from LLM response safely.
    Handles markdown fences, extra text, etc.
    """

    # Remove markdown ```json ``` fences if present
    text = re.sub(r"```json|```", "", text).strip()

    # Try direct JSON parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Extract first JSON object using regex
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None
