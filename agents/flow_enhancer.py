from langchain_core.tools import tool
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="whisper-large-v3-turbo",
    temperature=0.93   # higher = more natural flow
)

@tool
def enhance_flow(text: str) -> str:
    """
    Improves sentence flow AFTER rewriting.
    Does not preserve original structure.
    """

    prompt = f"""
You are refining already rewritten text.

Rules:
- Improve transitions between sentences
- Merge or split sentences if it sounds more natural
- Do NOT revert to original wording
- Make it feel casually human, not polished AI

Text:
{text}

Return improved version:
"""

    try:
        return llm.invoke(prompt).content.strip()
    except Exception:
        return text
