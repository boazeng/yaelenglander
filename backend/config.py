"""Backend configuration — loads from .env"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PHOTOS_DIR = PROJECT_ROOT / "files" / "photos"
ORIGINALS_DIR = PHOTOS_DIR / "originals"
THUMBS_DIR = PHOTOS_DIR / "thumbs"

# Ensure dirs exist
ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)

# Server
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "5003"))

# Database
DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://yael:yael123@localhost:5433/yael_englander"
)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "yael-memorial-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 72

# Claude Vision
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_VISION_MODEL = "claude-sonnet-4-5-20250929"

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

# Allowed image types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
THUMBNAIL_SIZE = (300, 300)
