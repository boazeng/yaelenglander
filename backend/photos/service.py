"""Photo service — file handling, thumbnails, DB operations."""

import uuid
import logging
from pathlib import Path

from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.models import Photo, Tag, PhotoTag
from backend.config import ORIGINALS_DIR, THUMBS_DIR, THUMBNAIL_SIZE

logger = logging.getLogger("photo-service")


async def save_file(file_bytes: bytes, original_filename: str) -> tuple[str, str, str]:
    """Save original file and create thumbnail. Returns (file_id, original_path, thumb_path)."""
    suffix = Path(original_filename).suffix.lower() or ".jpg"
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{suffix}"

    original_path = ORIGINALS_DIR / filename
    thumb_path = THUMBS_DIR / filename

    # Save original
    original_path.write_bytes(file_bytes)

    # Create thumbnail
    try:
        with Image.open(original_path) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_path, "JPEG", quality=85)
    except Exception as e:
        logger.error(f"Thumbnail creation failed: {e}")
        # Copy original as thumb fallback
        thumb_path.write_bytes(file_bytes)

    return file_id, str(original_path), str(thumb_path)


def get_image_dimensions(file_path: str) -> tuple[int, int]:
    """Get width and height of an image."""
    try:
        with Image.open(file_path) as img:
            return img.size
    except Exception:
        return (0, 0)


async def save_photo_to_db(
    db: AsyncSession,
    file_path: str,
    thumb_path: str,
    original_filename: str,
    caption: str | None,
    file_size: int,
    width: int,
    height: int,
    member_id: int,
    tag_names: list[str],
) -> Photo:
    """Save photo record and associate tags."""
    photo = Photo(
        file_path=file_path,
        thumbnail_path=thumb_path,
        original_filename=original_filename,
        caption=caption,
        file_size=file_size,
        width=width,
        height=height,
        approved_member_id=member_id,
    )
    db.add(photo)
    await db.flush()

    # Upsert tags and create associations
    for tag_name in tag_names:
        tag_name = tag_name.strip()
        if not tag_name:
            continue
        result = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            await db.flush()
        assoc = PhotoTag(photo_id=photo.id, tag_id=tag.id)
        db.add(assoc)

    await db.commit()
    await db.refresh(photo)
    return photo


async def update_photo_tags(
    db: AsyncSession, photo_id: int, tag_names: list[str]
) -> Photo:
    """Replace all tags on a photo."""
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        return None

    # Remove existing associations
    await db.execute(
        PhotoTag.__table__.delete().where(PhotoTag.photo_id == photo_id)
    )

    # Add new tags
    for tag_name in tag_names:
        tag_name = tag_name.strip()
        if not tag_name:
            continue
        result = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            await db.flush()
        assoc = PhotoTag(photo_id=photo.id, tag_id=tag.id)
        db.add(assoc)

    await db.commit()
    await db.refresh(photo)
    return photo
