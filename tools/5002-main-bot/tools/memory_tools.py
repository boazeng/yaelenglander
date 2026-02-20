"""Memory tools — user facts and conversation search."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy import select
from database.postgres.connection import async_session
from database.postgres.models import UserFact, Conversation
from database.qdrant.client import QdrantManager, CONVERSATIONS_COLLECTION


_qdrant = None


def _get_qdrant() -> QdrantManager:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantManager()
    return _qdrant


async def get_user_facts(user_id: int = 0) -> str:
    """Get all known facts about the current user."""
    if not user_id:
        return "לא ידוע מי המשתמש."

    async with async_session() as session:
        result = await session.execute(
            select(UserFact).where(UserFact.user_id == user_id).order_by(UserFact.learned_at.desc()).limit(20)
        )
        facts = result.scalars().all()

    if not facts:
        return "אין עובדות ידועות על המשתמש הזה עדיין."

    return "\n".join(f"- {f.fact}" for f in facts)


async def save_fact(fact: str, user_id: int = 0) -> str:
    """Save a new fact learned about the user."""
    if not user_id:
        return "לא ניתן לשמור — לא ידוע מי המשתמש."

    async with async_session() as session:
        uf = UserFact(user_id=user_id, fact=fact)
        session.add(uf)
        await session.commit()

    return f"שמרתי: {fact}"


async def search_conversations(query: str, user_id: int = 0) -> str:
    """Search past conversations for relevant context."""
    qm = _get_qdrant()
    results = qm.search(CONVERSATIONS_COLLECTION, query, limit=5)

    if not results:
        return "לא מצאתי שיחות קודמות רלוונטיות."

    parts = []
    for r in results:
        parts.append(f"{r.get('role', '?')}: {r.get('content', '')}")
    return "\n".join(parts)
