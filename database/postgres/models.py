"""SQLAlchemy ORM models for the Yael Englander bot."""

from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, Text, Boolean, Date, DateTime,
    ForeignKey, UniqueConstraint, JSON, func
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    category = Column(Text)  # people/place/event/theme/time/mood/object/style

    photos = relationship("Photo", secondary="photo_tags", back_populates="tags")


class PhotoTag(Base):
    __tablename__ = "photo_tags"

    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


class ApprovedMember(Base):
    __tablename__ = "approved_members"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=True)
    role = Column(Text, default="member")  # "admin" / "member"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    platform = Column(Text, nullable=False)           # "whatsapp" / "telegram"
    platform_user_id = Column(Text, nullable=False)    # phone number / telegram id
    display_name = Column(Text)
    relation_to_yael = Column(Text)                    # "בן", "נכדה", etc.
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("platform", "platform_user_id", name="uq_platform_user"),
    )

    conversations = relationship("Conversation", back_populates="user")
    facts = relationship("UserFact", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Text, nullable=False)    # "user" / "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")


class UserFact(Base):
    __tablename__ = "user_facts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fact = Column(Text, nullable=False)
    learned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="facts")


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    relation = Column(Text)                # "בן", "בת", "נכד", etc.
    parent_id = Column(Integer, ForeignKey("family_members.id"))
    birth_date = Column(Date)
    details = Column(Text)
    linked_user_id = Column(Integer, ForeignKey("users.id"))

    parent = relationship("FamilyMember", remote_side=[id])


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id = Column(Integer, primary_key=True)
    type = Column(Text, nullable=False)     # "story", "recipe", "pekiin", "personality"
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Text)
    metadata_ = Column("metadata", JSON, default={})


class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"

    id = Column(Integer, primary_key=True)
    target_user_id = Column(Integer, ForeignKey("users.id"))
    message_type = Column(Text, nullable=False)   # "birthday", "reminder", "custom"
    scheduled_date = Column(Date, nullable=False)
    custom_text = Column(Text)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    file_path = Column(Text, nullable=False)
    thumbnail_path = Column(Text)
    original_filename = Column(Text)
    caption = Column(Text)
    album = Column(Text)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    approved_member_id = Column(Integer, ForeignKey("approved_members.id"))
    uploaded_at = Column(DateTime, default=func.now())

    tags = relationship("Tag", secondary="photo_tags", back_populates="photos")
