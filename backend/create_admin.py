"""CLI script to create an approved member (admin or member)."""

import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.config import DATABASE_URL
from backend.auth.utils import hash_password
from database.postgres.models import ApprovedMember


async def main():
    if len(sys.argv) < 4:
        print("Usage: python -m backend.create_admin <name> <email> <password> [admin|member]")
        sys.exit(1)

    name = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    role = sys.argv[4] if len(sys.argv) > 4 else "admin"

    engine = create_async_engine(DATABASE_URL, echo=False)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        member = ApprovedMember(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=True,
        )
        session.add(member)
        await session.commit()
        print(f"[OK] Created {role}: {name} ({email})")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
