"""Media tools — save photos."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from database.postgres.connection import async_session
from database.postgres.models import Photo

PHOTOS_DIR = Path(__file__).parent.parent.parent.parent / "files" / "photos"


async def save_photo(image_url: str, caption: str = "", album: str = "כללי", user_id: int = 0) -> str:
    """Save a photo reference to the database."""
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

    async with async_session() as session:
        photo = Photo(
            file_path=image_url,
            caption=caption,
            album=album,
            uploaded_by=user_id if user_id else None,
        )
        session.add(photo)
        await session.commit()

    return f"התמונה נשמרה! {f'תיאור: {caption}' if caption else ''}"
