"""Configuration for the main bot."""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://yael:yael123@localhost:5433/yael_englander"
)
if POSTGRES_URL.startswith("postgresql://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

BOT_PORT = int(os.getenv("BOT_PORT", "5002"))
MAX_CONVERSATION_HISTORY = 20
