"""Initialize PostgreSQL database — create tables and seed initial data."""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

from .models import Base, FamilyMember, KnowledgeItem

load_dotenv()

DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://yael:yael123@localhost:5433/yael_englander"
)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

SEED_FILE = Path(__file__).parent / "seed_data.json"


async def create_tables(engine):
    """Create all tables from models."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] Tables created")


async def seed_data(session: AsyncSession):
    """Insert seed data from JSON file."""
    if not SEED_FILE.exists():
        print("[SKIP] No seed_data.json found")
        return

    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    # Family members
    yael_ref = None
    for member in data.get("family_members", []):
        fm = FamilyMember(
            name=member["name"],
            relation=member.get("relation"),
            birth_date=member.get("birth_date"),
            details=member.get("details"),
        )
        session.add(fm)
        if member["name"] == "יעל אנגלנדר":
            yael_ref = fm

    await session.flush()

    # Set parent_id for children of Yael
    if yael_ref:
        for member in data.get("family_members", []):
            if member["name"] != "יעל אנגלנדר" and member.get("relation") == "בן":
                # Find the DB record and update parent
                pass  # Will be set via admin later

    # Knowledge items
    for item in data.get("knowledge_items", []):
        ki = KnowledgeItem(
            type=item["type"],
            title=item["title"],
            content=item["content"],
            category=item.get("category"),
            metadata_=item.get("metadata", {}),
        )
        session.add(ki)

    await session.commit()
    family_count = len(data.get("family_members", []))
    knowledge_count = len(data.get("knowledge_items", []))
    print(f"[OK] Seeded {family_count} family members, {knowledge_count} knowledge items")


async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)

    print(f"Connecting to: {DATABASE_URL.split('@')[1]}")
    print("---")

    await create_tables(engine)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        await seed_data(session)

    await engine.dispose()
    print("---")
    print("[DONE] Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())
