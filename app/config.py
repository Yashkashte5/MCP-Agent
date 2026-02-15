import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "MCP Agent Platform"

    # LLM config (future ready)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
    LLM_MODEL = os.getenv("LLM_MODEL", "default")

settings = Settings()
