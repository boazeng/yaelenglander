"""
5000-whatsapp-connection
סוכן חיבור WhatsApp Business API
- שליחת הודעות טקסט, תמונות והודעות קוליות
- קבלת הודעות נכנסות (webhook)
- תבניות הודעות לימי הולדת
"""

import os
import json
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel
import httpx

# --- Config ---

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "yael_memorial_verify")
WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET", "")

BASE_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}"
HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
    "Content-Type": "application/json",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp-agent")

app = FastAPI(title="5000 - WhatsApp Connection Agent")


# --- Models ---

class SendMessageRequest(BaseModel):
    to: str
    message: str


class SendImageRequest(BaseModel):
    to: str
    image_url: str
    caption: Optional[str] = None


class SendAudioRequest(BaseModel):
    to: str
    audio_url: str


class BirthdayMessageRequest(BaseModel):
    to: str
    grandchild_name: str
    age: Optional[int] = None
    custom_message: Optional[str] = None


# --- WhatsApp API Core ---

async def send_whatsapp_request(payload: dict) -> dict:
    """שליחת בקשה ל-WhatsApp API"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/messages",
            headers=HEADERS,
            json=payload,
            timeout=30.0,
        )
        if response.status_code != 200:
            logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
        logger.info(f"Message sent successfully: {response.json()}")
        return response.json()


async def send_text_message(to: str, message: str) -> dict:
    """שליחת הודעת טקסט"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }
    return await send_whatsapp_request(payload)


async def send_image_message(to: str, image_url: str, caption: str = None) -> dict:
    """שליחת תמונה"""
    image_data = {"link": image_url}
    if caption:
        image_data["caption"] = caption
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": image_data,
    }
    return await send_whatsapp_request(payload)


async def send_audio_message(to: str, audio_url: str) -> dict:
    """שליחת הודעה קולית"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": {"link": audio_url},
    }
    return await send_whatsapp_request(payload)


async def mark_as_read(message_id: str) -> dict:
    """סימון הודעה כנקראה"""
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    return await send_whatsapp_request(payload)


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


# --- Webhook Signature Verification ---

def verify_signature(payload: bytes, signature: str) -> bool:
    """אימות חתימה מ-Meta"""
    if not WHATSAPP_APP_SECRET:
        return True
    expected = hmac.new(
        WHATSAPP_APP_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


def extract_messages(body: dict) -> list[dict]:
    """חילוץ הודעות נכנסות מה-webhook payload"""
    messages = []
    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                contact = next(
                    (c for c in value.get("contacts", [])
                     if c["wa_id"] == msg["from"]),
                    {},
                )
                messages.append({
                    "message_id": msg.get("id"),
                    "from": msg.get("from"),
                    "name": contact.get("profile", {}).get("name", ""),
                    "timestamp": msg.get("timestamp"),
                    "type": msg.get("type"),
                    "text": msg.get("text", {}).get("body", ""),
                })
    return messages


# --- API Routes ---

@app.get("/privacy-policy")
async def privacy_policy():
    """דף מדיניות פרטיות"""
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head><meta charset="UTF-8"><title>מדיניות פרטיות</title></head>
<body style="font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px">
<h1>מדיניות פרטיות - יעל אנגלנדר</h1>
<p>אפליקציה זו משמשת לשליחת הודעות זיכרון משפחתיות בלבד.</p>
<h2>מידע שנאסף</h2>
<p>האפליקציה מקבלת הודעות WhatsApp הנשלחות ישירות אליה, כולל שם השולח ומספר הטלפון.</p>
<h2>שימוש במידע</h2>
<p>המידע משמש אך ורק לצורך תגובה להודעות נכנסות. איננו משתפים מידע עם צדדים שלישיים.</p>
<h2>מחיקת מידע</h2>
<p>ניתן לבקש מחיקת מידע בכל עת באמצעות שליחת הודעה לאפליקציה.</p>
<h2>יצירת קשר</h2>
<p>לשאלות בנושא פרטיות, ניתן ליצור קשר דרך WhatsApp.</p>
</body></html>""")


@app.get("/health")
async def health_check():
    """בדיקת תקינות"""
    return {
        "status": "running",
        "agent": "5000-whatsapp-connection",
        "timestamp": datetime.now().isoformat(),
        "config": {
            "phone_number_id": bool(WHATSAPP_PHONE_NUMBER_ID),
            "api_token": bool(WHATSAPP_API_TOKEN),
        },
    }


@app.post("/send/text")
async def api_send_text(req: SendMessageRequest):
    """שליחת הודעת טקסט"""
    result = await send_text_message(req.to, req.message)
    return {"status": "sent", "result": result}


@app.post("/send/image")
async def api_send_image(req: SendImageRequest):
    """שליחת תמונה"""
    result = await send_image_message(req.to, req.image_url, req.caption)
    return {"status": "sent", "result": result}


@app.post("/send/audio")
async def api_send_audio(req: SendAudioRequest):
    """שליחת הודעה קולית"""
    result = await send_audio_message(req.to, req.audio_url)
    return {"status": "sent", "result": result}


@app.post("/send/birthday")
async def api_send_birthday(req: BirthdayMessageRequest):
    """שליחת הודעת יום הולדת"""
    message = build_birthday_message(req.grandchild_name, req.age, req.custom_message)
    result = await send_text_message(req.to, message)
    return {"status": "sent", "message": message, "result": result}


@app.get("/webhook")
async def webhook_verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """אימות webhook מ-Meta (GET)"""
    if hub_mode == "subscribe" and hub_token == WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook_receive(request: Request):
    """קבלת הודעות נכנסות (POST)"""
    signature = request.headers.get("X-Hub-Signature-256", "")
    body_bytes = await request.body()

    if not verify_signature(body_bytes, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    body = json.loads(body_bytes)
    messages = extract_messages(body)

    for msg in messages:
        logger.info(f"Incoming message from {msg['name']} ({msg['from']}): {msg['text']}")
        await mark_as_read(msg["message_id"])
        # TODO: forward to AI agent for response

    return {"status": "received", "messages_count": len(messages)}


# --- Entry Point ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
