from collections import defaultdict
from datetime import datetime


class ContextManager:
    def __init__(self):
        self.sessions = defaultdict(list)

    def save(self, session_id: str, role: str, content: dict):
        self.sessions[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get(self, session_id: str):
        return self.sessions.get(session_id, [])


context_manager = ContextManager()
