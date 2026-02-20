"""Family tools — family tree queries."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy import select
from database.postgres.connection import async_session
from database.postgres.models import FamilyMember


async def get_family_tree(member_name: str | None = None) -> str:
    """Get family tree information, optionally filtered by name."""
    async with async_session() as session:
        if member_name:
            result = await session.execute(
                select(FamilyMember).where(FamilyMember.name.ilike(f"%{member_name}%"))
            )
        else:
            result = await session.execute(select(FamilyMember))

        members = result.scalars().all()

    if not members:
        if member_name:
            return f"לא מצאתי את {member_name} בעץ המשפחה."
        return "עץ המשפחה ריק."

    parts = []
    for m in members:
        line = f"- {m.name}"
        if m.relation:
            line += f" ({m.relation})"
        if m.details:
            line += f": {m.details}"
        parts.append(line)

    return "\n".join(parts)
