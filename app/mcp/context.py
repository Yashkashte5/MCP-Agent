from app.mcp.memory_db import save_memory, get_memory


class ContextManager:

    def save(self, session_id, role, content):
        save_memory(session_id, role, content)

    def get(self, session_id):
        return get_memory(session_id)


context_manager = ContextManager()
