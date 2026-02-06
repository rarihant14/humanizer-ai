from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
groq_client = ChatGoogleGenerativeAI(api_key=os.getenv("GOOGLE_API_KEY"))

@tool
def preserve_meaning(original: str, rewritten: str) -> str:
    """Validates whether rewritten text preserves original meaning using Groq."""
    prompt = f"""
Check if the rewritten text below preserves the original meaning.
Return only 'Yes' or 'No' with a short reason.

Original: "{original}"
Rewritten: "{rewritten}"
"""

    try:
        response = ChatGoogleGenerativeAI.chat.completions.create(
            model="	gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that checks for semantic consistency."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Groq Error: {e}]"
