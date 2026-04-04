# app/services/ai_service.py
import os
from groq import Groq
from dotenv import load_dotenv
from functools import lru_cache
from app.core.firebase import get_db

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@lru_cache(maxsize=1)
def get_categories() -> list[str]:
    db = get_db()
    docs = db.collection("guides").stream()
    return [doc.id for doc in docs]

def classify_question(question: str) -> str:
    categories = get_categories()
    if not categories:
        return "unknown"

    prompt = f"""
    You are a routing assistant for BDU SmartGuide.
    Classify the following student question into EXACTLY ONE of these categories:
    {chr(10).join(f"- {c}" for c in categories)}

    Question: {question}

    Rules:
    - Return ONLY the exact category name.
    - Do not add quotes, explanations, or extra text.
    - If none match, return "unknown".
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.1,  # More deterministic
        )
        raw = response.choices[0].message.content.strip()
        # Remove accidental quotes the LLM might add
        cleaned = raw.strip("\"'")
        return cleaned if cleaned in categories else "unknown"
    except Exception as e:
        print(f"⚠️ AI Classification Error: {e}")
        return "unknown"