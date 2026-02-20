"""Photo routes — upload, list, detail, delete, tags."""

import os
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.postgres.models import Photo, Tag, PhotoTag, ApprovedMember
from backend.dependencies import get_db, get_current_user, get_admin_user
from backend.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from .service import save_file, get_image_dimensions, save_photo_to_db, update_photo_tags
from .tagger import auto_tag_photo

logger = logging.getLogger("photo-routes")
router = APIRouter(prefix="/photos", tags=["photos"])


class TagOut(BaseModel):
    id: int
    name: str
    category: str | None = None


class PhotoOut(BaseModel):
    id: int
    file_url: str
    thumb_url: str
    original_filename: str | None = None
    caption: str | None = None
    width: int | None = None
    height: int | None = None
    file_size: int | None = None
    uploaded_by: str | None = None
    uploaded_at: str | None = None
    tags: list[str] = []


def _photo_to_out(photo: Photo, tags: list[str] | None = None, uploader_name: str | None = None) -> PhotoOut:
    """Convert Photo ORM to response model."""
    file_id = Path(photo.file_path).stem
    suffix = Path(photo.file_path).suffix
    return PhotoOut(
        id=photo.id,
        file_url=f"/files/photos/originals/{file_id}{suffix}",
        thumb_url=f"/files/photos/thumbs/{file_id}{suffix}",
        original_filename=photo.original_filename,
        caption=photo.caption,
        width=photo.width,
        height=photo.height,
        file_size=photo.file_size,
        uploaded_by=uploader_name,
        uploaded_at=photo.uploaded_at.isoformat() if photo.uploaded_at else None,
        tags=tags if tags is not None else [],
    )


@router.post("/upload", response_model=PhotoOut)
async def upload_photo(
    file: UploadFile = File(...),
    caption: str = Form(None),
    db: AsyncSession = Depends(get_db),
    user: ApprovedMember = Depends(get_current_user),
):
    # Validate file type
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"סוג קובץ לא נתמך: {ext}")

    # Read file
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(400, "הקובץ גדול מדי (מקסימום 20MB)")
    if len(file_bytes) == 0:
        raise HTTPException(400, "קובץ ריק")

    # Save file + thumbnail
    file_id, original_path, thumb_path = await save_file(file_bytes, file.filename)

    # Get dimensions
    width, height = get_image_dimensions(original_path)

    # Auto-tag with Claude Vision
    tag_names = await auto_tag_photo(original_path)
    logger.info(f"Auto-tagged photo {file_id}: {tag_names}")

    # Save to DB
    photo = await save_photo_to_db(
        db=db,
        file_path=original_path,
        thumb_path=thumb_path,
        original_filename=file.filename,
        caption=caption,
        file_size=len(file_bytes),
        width=width,
        height=height,
        member_id=user.id,
        tag_names=tag_names,
    )

    return _photo_to_out(photo, tags=tag_names, uploader_name=user.name)


@router.get("", response_model=list[PhotoOut])
async def list_photos(
    tags: str = Query(None, description="סינון לפי תגיות (מופרדות בפסיקים)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Photo).order_by(Photo.uploaded_at.desc()).offset(offset).limit(limit)

    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            query = (
                query
                .join(PhotoTag, Photo.id == PhotoTag.photo_id)
                .join(Tag, PhotoTag.tag_id == Tag.id)
                .where(Tag.name.in_(tag_list))
                .distinct()
            )

    result = await db.execute(query)
    photos = result.scalars().all()

    # Load tags for each photo
    out = []
    for photo in photos:
        tag_result = await db.execute(
            select(Tag.name)
            .join(PhotoTag, Tag.id == PhotoTag.tag_id)
            .where(PhotoTag.photo_id == photo.id)
        )
        tag_names = [r[0] for r in tag_result.all()]

        # Get uploader name
        uploader = None
        if photo.approved_member_id:
            m_result = await db.execute(
                select(ApprovedMember.name).where(ApprovedMember.id == photo.approved_member_id)
            )
            uploader = m_result.scalar_one_or_none()

        out.append(_photo_to_out(photo, tags=tag_names, uploader_name=uploader))

    return out


@router.get("/tags", response_model=list[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tag, func.count(PhotoTag.photo_id).label("count"))
        .outerjoin(PhotoTag, Tag.id == PhotoTag.tag_id)
        .group_by(Tag.id)
        .order_by(func.count(PhotoTag.photo_id).desc())
    )
    return [TagOut(id=tag.id, name=tag.name, category=tag.category) for tag, _ in result.all()]


@router.get("/{photo_id}", response_model=PhotoOut)
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(404, "תמונה לא נמצאה")

    tag_result = await db.execute(
        select(Tag.name).join(PhotoTag, Tag.id == PhotoTag.tag_id).where(PhotoTag.photo_id == photo.id)
    )
    tag_names = [r[0] for r in tag_result.all()]

    uploader = None
    if photo.approved_member_id:
        m_result = await db.execute(
            select(ApprovedMember.name).where(ApprovedMember.id == photo.approved_member_id)
        )
        uploader = m_result.scalar_one_or_none()

    return _photo_to_out(photo, tags=tag_names, uploader_name=uploader)


@router.patch("/{photo_id}/tags", response_model=PhotoOut)
async def update_tags(
    photo_id: int,
    tags: list[str],
    db: AsyncSession = Depends(get_db),
    user: ApprovedMember = Depends(get_current_user),
):
    photo = await update_photo_tags(db, photo_id, tags)
    if not photo:
        raise HTTPException(404, "תמונה לא נמצאה")

    tag_result = await db.execute(
        select(Tag.name).join(PhotoTag, Tag.id == PhotoTag.tag_id).where(PhotoTag.photo_id == photo.id)
    )
    tag_names = [r[0] for r in tag_result.all()]
    return _photo_to_out(photo, tags=tag_names, uploader_name=user.name)


@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    user: ApprovedMember = Depends(get_admin_user),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(404, "תמונה לא נמצאה")

    # Delete files
    for path_str in [photo.file_path, photo.thumbnail_path]:
        if path_str:
            p = Path(path_str)
            if p.exists():
                p.unlink()

    # Delete DB records
    await db.execute(PhotoTag.__table__.delete().where(PhotoTag.photo_id == photo_id))
    await db.delete(photo)
    await db.commit()
    return {"ok": True, "message": "התמונה נמחקה"}
