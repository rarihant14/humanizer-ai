from langchain_core.tools import tool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from agents.style_memory import load_style


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b",
    temperature=0.7
)

persona_prompts = {
    "default": "Natural human tone.",
    "gen z": "Gen Z slang, casual, short punchy lines.",
    "sarcastic": "Dry humor and wit.",
    "academic": "Formal, scholarly tone.",
    "emotional": "Personal and expressive."
}

@tool
def human_style_rewriter(text: str, persona: str = "default") -> str:
    """Always returns a STRING. Never None."""
    
    persona_note = persona_prompts.get(persona.lower(), "")
    
    prompt = f"""

You are rewriting AI-generated text to sound like a real human.

STRICT RULES (must follow):
- Do NOT reuse the original sentence structure
- Do NOT mirror phrasing from the original text
- Freely change sentence order if it feels more natural
- Vary sentence length (mix short + long)
- Use contractions naturally (I'm, it's, don't, etc.)
- Add slight imperfections like pauses, casual wording, or hesitation
- You do NOT have to follow grammar rules strictly
- Do NOT sound formal, robotic, or overly confident
- Keep the meaning the same, but rewrite freely
- Do NOT add headings or hashtags

TONE & STYLE:
- Write like a human talking to another human
- Be emotional, natural, and conversational
- Keep confidence low and humble
- It should feel spontaneous, not polished
- Avoid corporate or academic language

Here are examples of how humans actually write:
"I just wanted to say thanks for everything."
"It’s funny how life works sometimes, you know?"
"I wasn’t really expecting that to happen."
"To be honest, I kind of liked the old way better."
"Sometimes, you just have to let go and see what happens."
"You know how we talk, right?"
"Can you be happy?"


Persona: {persona_note}

Text:
{text}
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception:
        # HARD FALLBACK (never break pipeline)
        return text
