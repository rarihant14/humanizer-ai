import json
import os

MEMORY_FILE = "style_memory.json"

DEFAULT_STYLE = {
    "avg_sentence_length": 14,
    "formality": "neutral",
    "emoji_usage": False
}

def load_style():
    if not os.path.exists(MEMORY_FILE):
        return DEFAULT_STYLE.copy()
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_style(style):
    with open(MEMORY_FILE, "w") as f:
        json.dump(style, f, indent=2)

def update_style_from_text(text: str):
    words = text.split()
    sentences = text.count(".") + text.count("!") + 1

    avg_len = len(words) // max(sentences, 1)

    style = load_style()
    style["avg_sentence_length"] = round(
        (style["avg_sentence_length"] + avg_len) / 2
    )

    style["emoji_usage"] = any(char in text for char in "😂🔥😄✨")

    save_style(style)
    return style
