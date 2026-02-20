"""Index knowledge items from PostgreSQL into Qdrant."""

import asyncio
import json
import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv

load_dotenv()

# Import from sibling packages
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.postgres.models import KnowledgeItem
from database.qdrant.client import QdrantManager, KNOWLEDGE_COLLECTION


DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://yael:yael123@localhost:5433/yael_englander"
)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


async def fetch_knowledge_items() -> list[dict]:
    """Fetch all knowledge items from PostgreSQL."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        result = await session.execute(select(KnowledgeItem))
        items = result.scalars().all()

    await engine.dispose()
    return items


def index_knowledge(items: list, qdrant: QdrantManager):
    """Index knowledge items into Qdrant."""
    if not items:
        print("[SKIP] No knowledge items to index")
        return

    batch = []
    for item in items:
        # Combine title + content for better search
        search_text = f"{item.title}\n{item.content}"
        batch.append({
            "id": item.id,
            "text": search_text,
            "payload": {
                "type": item.type,
                "title": item.title,
                "content": item.content,
                "category": item.category or "",
                "db_id": item.id,
            },
        })

    # Process in batches of 20 (OpenAI embedding API limit considerations)
    BATCH_SIZE = 20
    total = 0
    for i in range(0, len(batch), BATCH_SIZE):
        chunk = batch[i:i + BATCH_SIZE]
        qdrant.upsert_points_batch(KNOWLEDGE_COLLECTION, chunk)
        total += len(chunk)
        print(f"  Indexed {total}/{len(batch)} items...")

    print(f"[OK] Indexed {total} knowledge items into {KNOWLEDGE_COLLECTION}")


async def main():
    print("=== Qdrant Indexer ===")
    print()

    # 1. Ensure collections exist
    qdrant = QdrantManager()
    qdrant.ensure_collections()
    print()

    # 2. Fetch from PostgreSQL
    print("Fetching knowledge items from PostgreSQL...")
    items = await fetch_knowledge_items()
    print(f"Found {len(items)} items")
    print()

    # 3. Index into Qdrant
    print("Indexing into Qdrant...")
    index_knowledge(items, qdrant)
    print()

    # 4. Verify
    for collection in [KNOWLEDGE_COLLECTION]:
        count = qdrant.get_collection_count(collection)
        print(f"[VERIFY] {collection}: {count} points")

    print()
    print("[DONE] Indexing complete")


if __name__ == "__main__":
    asyncio.run(main())
