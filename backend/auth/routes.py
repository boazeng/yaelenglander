"""Auth routes — login & user info."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.models import ApprovedMember
from backend.dependencies import get_db, get_current_user
from .utils import verify_password, create_access_token, verify_google_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    name: str
    role: str


class MeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ApprovedMember).where(ApprovedMember.email == req.email)
    )
    member = result.scalar_one_or_none()
    if not member or not member.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="אימייל או סיסמה שגויים")
    if not verify_password(req.password, member.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="אימייל או סיסמה שגויים")
    token = create_access_token(member.id, member.role)
    return LoginResponse(token=token, name=member.name, role=member.role)


class GoogleLoginRequest(BaseModel):
    credential: str


@router.post("/google", response_model=LoginResponse)
async def google_login(req: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with Google ID token. User must be a pre-approved family member."""
    try:
        google_user = verify_google_token(req.credential)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="טוקן Google לא תקין")

    result = await db.execute(
        select(ApprovedMember).where(ApprovedMember.email == google_user["email"])
    )
    member = result.scalar_one_or_none()

    if not member:
        # Auto-create member if not exists (role=member, no password)
        member = ApprovedMember(
            name=google_user["name"],
            email=google_user["email"],
            role="member",
            is_active=True,
        )
        db.add(member)
        await db.commit()
        await db.refresh(member)

    if not member.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="החשבון לא פעיל")

    token = create_access_token(member.id, member.role)
    return LoginResponse(token=token, name=member.name, role=member.role)


@router.get("/me", response_model=MeResponse)
async def me(user: ApprovedMember = Depends(get_current_user)):
    return MeResponse(id=user.id, name=user.name, email=user.email, role=user.role)
