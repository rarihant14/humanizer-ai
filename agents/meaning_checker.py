from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import difflib

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Check semantic consistency."),
    ("human", "Original:\n{original}\n\nRewritten:\n{rewritten}\nAnswer Yes or No with a short reason.")
])

def heuristic_check(original, rewritten):
    ratio = difflib.SequenceMatcher(None, original, rewritten).ratio()
    return ratio > 0.55  # adjustable threshold

def preserve_meaning(original, rewritten):
    try:
        gemini_resp = llm.invoke(
            prompt.format(original=original, rewritten=rewritten)
        ).content.strip()

        gemini_yes = gemini_resp.lower().startswith("yes")
        heuristic_yes = heuristic_check(original, rewritten)

        disagreement = gemini_yes != heuristic_yes

        return {
            "gemini": gemini_resp,
            "heuristic": "Yes" if heuristic_yes else "No",
            "disagreement": disagreement
        }

    except Exception as e:
        return {
            "gemini": f"Error: {e}",
            "heuristic": "Unknown",
            "disagreement": True
        }
