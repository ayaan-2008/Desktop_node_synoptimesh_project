# ==========================================
# SYNOPTIMESH — SEARCH ENGINE
# ==========================================

from rapidfuzz import fuzz

# ==========================================
# SUGGESTIONS DATABASE
# ==========================================

SEARCH_SUGGESTIONS = [

    # DESKTOP
    "open chrome",
    "open notepad",
    "open calculator",
    "open camera",
    "open vscode",
    "open spotify",
    "open discord",
    "open whatsapp",
    "open file explorer",
    "open task manager",
    "open settings",

    # MEDIA
    "play music",
    "play lofi",
    "play youtube",

    # SEARCH
    "search google",
    "search youtube",
    "search web",

    # ACTIONS
    "write in notepad",
    "take screenshot",
    "take selfie",
    "take photo",
    "record video",
    "shutdown",
    "restart",
    "lock screen",

    # AI
    "ask ai",
    "open ai",
    "chat ai",
]

# ==========================================
# NORMALIZE
# ==========================================

def normalize(text):
    text = text.lower().strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text

# ==========================================
# SUGGEST COMMANDS
# ==========================================

def suggest_commands(user_input):

    user_input = normalize(user_input)

    if user_input == "":
        return []

    prefix_matches = []
    fuzzy_matches  = []

    for item in SEARCH_SUGGESTIONS:

        if item.startswith(user_input):
            prefix_matches.append(item)
        else:
            score = max(
                fuzz.partial_ratio(user_input, item),
                fuzz.token_sort_ratio(user_input, item)
            )
            if score > 65:
                fuzzy_matches.append((score, item))

    fuzzy_matches.sort(reverse=True)
    ranked = [item for score, item in fuzzy_matches]

    return (prefix_matches + ranked)[:5]