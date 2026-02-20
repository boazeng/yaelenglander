"""Auth utilities — password hashing, JWT tokens & Google OAuth."""

from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from backend.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_HOURS, GOOGLE_CLIENT_ID


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(member_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": str(member_id), "role": role, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_google_token(credential: str) -> dict:
    """Verify Google ID token and return user info (email, name, picture)."""
    idinfo = id_token.verify_oauth2_token(
        credential, google_requests.Request(), GOOGLE_CLIENT_ID
    )
    return {
        "email": idinfo["email"],
        "name": idinfo.get("name", ""),
        "picture": idinfo.get("picture", ""),
    }
