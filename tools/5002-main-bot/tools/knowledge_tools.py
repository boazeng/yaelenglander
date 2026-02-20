"""Knowledge tools — search, add stories, add recipes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from database.qdrant.client import QdrantManager, KNOWLEDGE_COLLECTION
from database.postgres.connection import async_session
from database.postgres.models import KnowledgeItem


_qdrant = None


def _get_qdrant() -> QdrantManager:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantManager()
    return _qdrant


async def search_knowledge(query: str, type: str = "all") -> str:
    """Search stories, recipes, and Pekiin knowledge."""
    qm = _get_qdrant()
    type_filter = type if type != "all" else None
    results = qm.search(KNOWLEDGE_COLLECTION, query, limit=3, type_filter=type_filter)

    if not results:
        return "לא מצאתי מידע רלוונטי."

    parts = []
    for r in results:
        parts.append(f"[{r['type']}] {r['title']}\n{r['content']}")
    return "\n---\n".join(parts)


async def add_story(title: str, content: str, category: str = "כללי") -> str:
    """Add a new story to the knowledge base."""
    async with async_session() as session:
        item = KnowledgeItem(
            type="story", title=title, content=content, category=category
        )
        session.add(item)
        await session.commit()
        db_id = item.id

    # Index into Qdrant
    qm = _get_qdrant()
    qm.upsert_point(
        KNOWLEDGE_COLLECTION,
        point_id=db_id,
        text=f"{title}\n{content}",
        payload={"type": "story", "title": title, "content": content, "category": category, "db_id": db_id},
    )
    return f"הסיפור '{title}' נשמר בהצלחה!"


async def add_recipe(title: str, content: str, ingredients: list[str] | None = None) -> str:
    """Add a new recipe to the knowledge base."""
    full_content = content
    if ingredients:
        full_content += "\n\nמרכיבים: " + ", ".join(ingredients)

    async with async_session() as session:
        item = KnowledgeItem(
            type="recipe", title=title, content=full_content, category="מתכונים"
        )
        session.add(item)
        await session.commit()
        db_id = item.id

    qm = _get_qdrant()
    qm.upsert_point(
        KNOWLEDGE_COLLECTION,
        point_id=db_id,
        text=f"{title}\n{full_content}",
        payload={"type": "recipe", "title": title, "content": full_content, "category": "מתכונים", "db_id": db_id},
    )
    return f"המתכון '{title}' נשמר בהצלחה!"
