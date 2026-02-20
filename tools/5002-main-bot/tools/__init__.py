from .knowledge_tools import search_knowledge, add_story, add_recipe
from .memory_tools import get_user_facts, save_fact, search_conversations
from .family_tools import get_family_tree
from .media_tools import save_photo
from .schedule_tools import schedule_message

TOOL_MAP = {
    "search_knowledge": search_knowledge,
    "get_user_facts": get_user_facts,
    "save_fact": save_fact,
    "search_conversations": search_conversations,
    "get_family_tree": get_family_tree,
    "add_story": add_story,
    "add_recipe": add_recipe,
    "save_photo": save_photo,
    "schedule_message": schedule_message,
}
