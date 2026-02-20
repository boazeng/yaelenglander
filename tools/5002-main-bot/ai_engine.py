"""AI Engine — OpenAI GPT-4o with function calling (tool use)."""

import json
import logging
from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL
from .system_prompt import build_system_prompt
from .tools import TOOL_MAP

logger = logging.getLogger("ai_engine")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Tool definitions for OpenAI function calling ---

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "חיפוש סיפורים, מתכונים, ומידע על פקיעין בבסיס הידע",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "מה לחפש"},
                    "type": {"type": "string", "enum": ["story", "recipe", "pekiin", "all"], "description": "סוג תוכן"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_facts",
            "description": "שליפת עובדות ידועות על המשתמש הנוכחי (ימי הולדת, אירועים, העדפות)",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_fact",
            "description": "שמירת עובדה חדשה שנלמדה על המשתמש (יום הולדת, אירוע, שינוי חשוב)",
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {"type": "string", "description": "העובדה לשמירה"}
                },
                "required": ["fact"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_conversations",
            "description": "חיפוש שיחות ישנות רלוונטיות עם המשתמש",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "מה לחפש בשיחות"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_family_tree",
            "description": "שליפת מידע על עץ המשפחה של יעל",
            "parameters": {
                "type": "object",
                "properties": {
                    "member_name": {"type": "string", "description": "שם בן משפחה (אופציונלי)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_story",
            "description": "הוספת סיפור חדש לבסיס הידע ולאתר",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת הסיפור"},
                    "content": {"type": "string", "description": "תוכן הסיפור"},
                    "category": {"type": "string", "description": "קטגוריה"}
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_recipe",
            "description": "הוספת מתכון חדש לבסיס הידע",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "שם המתכון"},
                    "content": {"type": "string", "description": "תיאור והוראות הכנה"},
                    "ingredients": {"type": "array", "items": {"type": "string"}, "description": "רשימת מרכיבים"}
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_photo",
            "description": "שמירת תמונה שנשלחה על ידי המשתמש",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_url": {"type": "string", "description": "URL של התמונה"},
                    "caption": {"type": "string", "description": "תיאור התמונה"},
                    "album": {"type": "string", "description": "אלבום"}
                },
                "required": ["image_url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_message",
            "description": "תזמון הודעה עתידית (יום הולדת, תזכורת)",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_user": {"type": "string", "description": "למי ההודעה"},
                    "message_type": {"type": "string", "enum": ["birthday", "reminder", "custom"]},
                    "scheduled_date": {"type": "string", "description": "תאריך בפורמט YYYY-MM-DD"},
                    "custom_text": {"type": "string", "description": "טקסט מותאם אישית"}
                },
                "required": ["target_user", "message_type", "scheduled_date"]
            }
        }
    },
]


async def execute_tool(name: str, arguments: dict, user_id: int) -> str:
    """Execute a tool by name and return the result string."""
    func = TOOL_MAP.get(name)
    if not func:
        return f"כלי לא מוכר: {name}"

    # Inject user_id into tools that need it
    if "user_id" in func.__code__.co_varnames:
        arguments["user_id"] = user_id

    try:
        result = await func(**arguments)
        logger.info(f"Tool {name}: {result[:100]}")
        return result
    except Exception as e:
        logger.error(f"Tool {name} error: {e}")
        return f"שגיאה בהפעלת {name}: {str(e)}"


async def chat(
    user_message: str,
    conversation_history: list[dict],
    user_id: int,
    user_name: str | None = None,
) -> str:
    """Send a message to GPT-4o with tools and return the final response."""

    system = build_system_prompt(user_name)
    messages = [{"role": "system", "content": system}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    max_iterations = 5

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        choice = response.choices[0]

        # If no tool calls — return the text response
        if choice.finish_reason == "stop" or not choice.message.tool_calls:
            return choice.message.content or ""

        # Process tool calls
        messages.append(choice.message)

        for tool_call in choice.message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            logger.info(f"Tool call: {fn_name}({fn_args})")

            result = await execute_tool(fn_name, fn_args, user_id)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    # Safety fallback
    return "סליחה מותק, קצת התבלבלתי. תנסה שוב?"
