"""
5001-telegram-connection
סוכן חיבור Telegram Bot API
- קבלת הודעות ותגובה אוטומטית
- שליחת הודעות טקסט, תמונות והודעות קוליות
- תבניות הודעות לימי הולדת
"""

import os
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

# --- Config ---

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("telegram-agent")

app = FastAPI(title="5001 - Telegram Connection Agent")


# --- Models ---

class SendMessageRequest(BaseModel):
    chat_id: int
    message: str


class SendImageRequest(BaseModel):
    chat_id: int
    image_url: str
    caption: Optional[str] = None


class SendAudioRequest(BaseModel):
    chat_id: int
    audio_url: str
    caption: Optional[str] = None


class BirthdayMessageRequest(BaseModel):
    chat_id: int
    grandchild_name: str
    age: Optional[int] = None
    custom_message: Optional[str] = None


# --- Telegram API Core ---

async def telegram_request(method: str, payload: dict) -> dict:
    """שליחת בקשה ל-Telegram API"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/{method}",
            json=payload,
            timeout=30.0,
        )
        data = response.json()
        if not data.get("ok"):
            logger.error(f"Telegram API error: {data}")
            raise HTTPException(status_code=400, detail=data.get("description", "Unknown error"))
        logger.info(f"Telegram {method} success")
        return data


async def send_text_message(chat_id: int, text: str) -> dict:
    """שליחת הודעת טקסט"""
    return await telegram_request("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    })


async def send_image_message(chat_id: int, image_url: str, caption: str = None) -> dict:
    """שליחת תמונה"""
    payload = {"chat_id": chat_id, "photo": image_url}
    if caption:
        payload["caption"] = caption
    return await telegram_request("sendPhoto", payload)


async def send_audio_message(chat_id: int, audio_url: str, caption: str = None) -> dict:
    """שליחת הודעה קולית"""
    payload = {"chat_id": chat_id, "voice": audio_url}
    if caption:
        payload["caption"] = caption
    return await telegram_request("sendVoice", payload)


async def set_webhook(url: str) -> dict:
    """הגדרת webhook"""
    return await telegram_request("setWebhook", {"url": url})


async def delete_webhook() -> dict:
    """מחיקת webhook"""
    return await telegram_request("deleteWebhook", {})


async def get_bot_info() -> dict:
    """מידע על הבוט"""
    return await telegram_request("getMe", {})


# --- Birthday Templates ---

BIRTHDAY_TEMPLATES = [
    "שלום {name} היקר/ה שלי! סבתא יעל כאן. מזל טוב ליום ההולדת! "
    "אני כל כך גאה בך. שיהיה לך יום מלא שמחה ואהבה. ❤️",

    "{name} אהוב/ת שלי, היום יום מיוחד! "
    "מזל טוב בן/בת {age}! סבתא תמיד איתך בלב. "
    "שתמשיך/י לגדול ולפרוח. 🎂",

    "היי {name}! סבתא יעל שולחת לך חיבוק גדול ליום ההולדת. "
    "כמו שתמיד אמרתי - אתה/את האור של המשפחה. מזל טוב! 🌟",
]


def build_birthday_message(
    grandchild_name: str,
    age: int = None,
    custom_message: str = None,
) -> str:
    """בניית הודעת יום הולדת"""
    if custom_message:
        return custom_message

    import random
    template = random.choice(BIRTHDAY_TEMPLATES)
    message = template.replace("{name}", grandchild_name)
    if age:
        message = message.replace("{age}", str(age))
    else:
        message = message.replace("בן/בת {age}! ", "")
    return message


# --- Incoming Message Handler ---

def extract_message(update: dict) -> Optional[dict]:
    """חילוץ הודעה נכנסת מ-update"""
    msg = update.get("message")
    if not msg:
        return None
    return {
        "message_id": msg.get("message_id"),
        "chat_id": msg["chat"]["id"],
        "from_id": msg.get("from", {}).get("id"),
        "first_name": msg.get("from", {}).get("first_name", ""),
        "last_name": msg.get("from", {}).get("last_name", ""),
        "text": msg.get("text", ""),
        "date": msg.get("date"),
    }


# --- API Routes ---

@app.get("/health")
async def health_check():
    """בדיקת תקינות"""
    return {
        "status": "running",
        "agent": "5001-telegram-connection",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "bot_token": bool(TELEGRAM_BOT_TOKEN),
        },
    }


@app.get("/bot-info")
async def api_bot_info():
    """מידע על הבוט"""
    return await get_bot_info()


@app.post("/send/text")
async def api_send_text(req: SendMessageRequest):
    """שליחת הודעת טקסט"""
    result = await send_text_message(req.chat_id, req.message)
    return {"status": "sent", "result": result}


@app.post("/send/image")
async def api_send_image(req: SendImageRequest):
    """שליחת תמונה"""
    result = await send_image_message(req.chat_id, req.image_url, req.caption)
    return {"status": "sent", "result": result}


@app.post("/send/audio")
async def api_send_audio(req: SendAudioRequest):
    """שליחת הודעה קולית"""
    result = await send_audio_message(req.chat_id, req.audio_url, req.caption)
    return {"status": "sent", "result": result}


@app.post("/send/birthday")
async def api_send_birthday(req: BirthdayMessageRequest):
    """שליחת הודעת יום הולדת"""
    message = build_birthday_message(req.grandchild_name, req.age, req.custom_message)
    result = await send_text_message(req.chat_id, message)
    return {"status": "sent", "message": message, "result": result}


@app.post("/webhook")
async def webhook_receive(request: Request):
    """קבלת הודעות נכנסות מטלגרם"""
    update = await request.json()
    msg = extract_message(update)

    if not msg:
        return {"status": "no_message"}

    logger.info(f"Incoming: {msg['first_name']} ({msg['chat_id']}): {msg['text']}")

    # TODO: forward to AI agent for response
    # For now, echo acknowledgment
    if msg["text"] == "/start":
        await send_text_message(
            msg["chat_id"],
            "שלום! אני יעל אנגלנדר. אפשר לשאול אותי על סיפורים, מתכונים, ועל החיים בפקיעין. 💛"
        )

    return {"status": "received", "chat_id": msg["chat_id"]}


@app.post("/webhook/setup")
async def api_setup_webhook(url: str):
    """הגדרת webhook URL"""
    result = await set_webhook(f"{url}/webhook")
    return {"status": "webhook_set", "result": result}


# --- Entry Point ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
