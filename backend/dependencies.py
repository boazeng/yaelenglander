"""Shared dependencies — DB session & auth middleware."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from .config import DATABASE_URL, JWT_SECRET, JWT_ALGORITHM
from database.postgres.models import ApprovedMember

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db():
    async with SessionLocal() as session:
        yield session


def _decode_token(token: str) -> dict:
    from jose import jwt, JWTError
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="טוקן לא תקין")


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> ApprovedMember:
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="נדרשת כניסה")
    payload = _decode_token(creds.credentials)
    member_id = payload.get("sub")
    if not member_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="טוקן לא תקין")
    result = await db.execute(select(ApprovedMember).where(ApprovedMember.id == int(member_id)))
    member = result.scalar_one_or_none()
    if not member or not member.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="משתמש לא פעיל")
    return member


async def get_admin_user(
    user: ApprovedMember = Depends(get_current_user),
) -> ApprovedMember:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="הרשאת מנהל נדרשת")
    return user
