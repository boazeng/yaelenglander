"""Schedule tools — schedule future messages."""

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from database.postgres.connection import async_session
from database.postgres.models import ScheduledMessage


async def schedule_message(
    target_user: str,
    message_type: str = "custom",
    scheduled_date: str = "",
    custom_text: str = "",
    user_id: int = 0,
) -> str:
    """Schedule a future message (birthday, reminder, etc.)."""
    try:
        sched_date = datetime.strptime(scheduled_date, "%Y-%m-%d").date() if scheduled_date else date.today()
    except ValueError:
        return f"תאריך לא תקין: {scheduled_date}. השתמשי בפורמט YYYY-MM-DD."

    async with async_session() as session:
        msg = ScheduledMessage(
            target_user_id=user_id if user_id else None,
            message_type=message_type,
            scheduled_date=sched_date,
            custom_text=custom_text or f"הודעה ל{target_user}",
        )
        session.add(msg)
        await session.commit()

    return f"תזמנתי הודעת {message_type} ל{target_user} בתאריך {sched_date}."
