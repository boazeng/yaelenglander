"""Claude Vision auto-tagger — analyzes photos and returns Hebrew tags."""

import base64
import json
import logging
from pathlib import Path

import anthropic

from backend.config import ANTHROPIC_API_KEY, CLAUDE_VISION_MODEL

logger = logging.getLogger("photo-tagger")

TAGGER_PROMPT = """אתה מערכת תיוג תמונות לאתר הנצחה משפחתי של יעל אנגלנדר מפקיעין.
נתח את התמונה ותן עד 20 תגיות בעברית.

קטגוריות תגיות (תן לפחות תגית אחת מכל קטגוריה רלוונטית):
- אנשים: כמה אנשים, גיל משוער, מגדר (למשל: "אישה מבוגרת", "ילדים", "זוג", "משפחה גדולה")
- מקומות: סוג המקום (למשל: "בית", "חצר", "טבע", "כפר", "עיר", "בית כנסת", "מטבח")
- אירועים: סוג האירוע (למשל: "חתונה", "יום הולדת", "חג", "סדר פסח", "שבת", "טיול")
- תקופה: הערכה (למשל: "שנות ה-50", "שנות ה-70", "ילדות", "נעורים", "זקנה")
- נושאים: מה קורה בתמונה (למשל: "בישול", "אוכל", "לימודים", "עבודה", "משחק")
- אווירה: תחושה (למשל: "שמח", "חגיגי", "רגוע", "נוסטלגי", "יומיומי", "רשמי")
- אובייקטים: פריטים בולטים (למשל: "שולחן ערוך", "ספרים", "פרחים", "עצים")
- סגנון: סוג הצילום (למשל: "שחור-לבן", "צבעוני", "ספיה", "תמונת פורטרט", "תמונה קבוצתית")

חשוב:
- תגיות קצרות (1-3 מילים כל אחת)
- בעברית בלבד
- מקסימום 20 תגיות
- תגיות רלוונטיות בלבד (אל תמציא)

החזר JSON בלבד בפורמט: {"tags": ["תגית1", "תגית2", ...]}"""

client = None


def _get_client():
    global client
    if client is None:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return client


def _get_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    types = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
        ".gif": "image/gif", ".bmp": "image/bmp",
    }
    return types.get(suffix, "image/jpeg")


async def auto_tag_photo(image_path: str) -> list[str]:
    """Send image to Claude Vision and get up to 20 Hebrew tags."""
    path = Path(image_path)
    if not path.exists():
        logger.error(f"Image not found: {image_path}")
        return []

    image_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    media_type = _get_media_type(path)

    try:
        response = _get_client().messages.create(
            model=CLAUDE_VISION_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": TAGGER_PROMPT},
                ],
            }],
        )

        text = response.content[0].text.strip()
        # Extract JSON from response (may be wrapped in markdown code block)
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        data = json.loads(text)
        tags = data.get("tags", [])
        return tags[:20]

    except Exception as e:
        logger.error(f"Claude Vision error: {e}")
        return []
