"""PostgreSQL connection — async engine with SQLAlchemy."""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://yael:yael123@localhost:5433/yael_englander"
)

# SQLAlchemy expects "postgresql+asyncpg://..." for async
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def get_engine():
    return engine


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
