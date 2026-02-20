"""Main Bot Server — FastAPI :5002 — receives messages, responds as Yael."""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sqlalchemy import select
from database.postgres.connection import async_session
from database.postgres.models import User, Conversation

from .config import BOT_PORT, MAX_CONVERSATION_HISTORY
from .ai_engine import chat

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("bot_server")

app = FastAPI(title="Yael Bot", version="1.0")


class ChatRequest(BaseModel):
    platform: str            # "whatsapp" / "telegram"
    platform_user_id: str    # phone number / telegram id
    user_name: str | None = None
    message: str
    image_url: str | None = None


class ChatResponse(BaseModel):
    reply: str
    user_id: int


async def get_or_create_user(platform: str, platform_user_id: str, display_name: str | None) -> User:
    """Find existing user or create new one."""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(
                User.platform == platform,
                User.platform_user_id == platform_user_id,
            )
        )
        user = result.scalar_one_or_none()

        if user:
            user.last_seen = datetime.utcnow()
            if display_name and not user.display_name:
                user.display_name = display_name
            await session.commit()
            return user

        user = User(
            platform=platform,
            platform_user_id=platform_user_id,
            display_name=display_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info(f"New user: {display_name} ({platform}/{platform_user_id})")
        return user


async def get_conversation_history(user_id: int) -> list[dict]:
    """Get recent conversation messages for context."""
    async with async_session() as session:
        result = await session.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.timestamp.desc())
            .limit(MAX_CONVERSATION_HISTORY)
        )
        messages = result.scalars().all()

    # Reverse to chronological order
    messages.reverse()
    return [{"role": m.role, "content": m.content} for m in messages]


async def save_message(user_id: int, role: str, content: str):
    """Save a message to conversation history."""
    async with async_session() as session:
        msg = Conversation(user_id=user_id, role=role, content=content)
        session.add(msg)
        await session.commit()


@app.post("/chat", response_model=ChatResponse)
async def handle_chat(req: ChatRequest):
    """Main chat endpoint — receives a message, returns Yael's response."""
    logger.info(f"[{req.platform}] {req.user_name or req.platform_user_id}: {req.message[:80]}")

    # 1. Get or create user
    user = await get_or_create_user(req.platform, req.platform_user_id, req.user_name)

    # 2. Save incoming message
    message_text = req.message
    if req.image_url:
        message_text += f"\n[תמונה: {req.image_url}]"
    await save_message(user.id, "user", message_text)

    # 3. Get conversation history
    history = await get_conversation_history(user.id)

    # 4. Call AI engine
    reply = await chat(
        user_message=message_text,
        conversation_history=history[:-1],  # exclude the message we just saved
        user_id=user.id,
        user_name=user.display_name,
    )

    # 5. Save bot response
    await save_message(user.id, "assistant", reply)

    logger.info(f"[REPLY] {reply[:80]}")
    return ChatResponse(reply=reply, user_id=user.id)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "yael-bot", "port": BOT_PORT}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=BOT_PORT)
