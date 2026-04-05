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

def clear_categories_cache():
    get_categories.cache_clear()

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

def extract_guide_from_document(raw_text: str) -> dict:
    prompt = f"""
    You are an expert technical writer, metadata extractor, and multi-lingual translator.
    Your task is to analyze the following raw document text, break it down into DISTINCT topics/rulesets, translate everything perfectly into English if it is in another language, and extract structured guides.
    
    Convert the text into a JSON object with this exact structure containing an array of guides:
    {{
        "guides": [
            {{
                "title": "A short, concise title in English (max 5 words)",
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "steps": ["Step 1 description in English...", "Step 2 description in English..."],
                "dont": ["Do not...", "Avoid..."],
                "office": "The specific office responsible, or 'N/A' if not mentioned"
            }}
        ]
    }}
    
    Document text:
    {raw_text}
    
    Rules:
    - ALWAYS output ONLY valid JSON.
    - Output an object containing a single key "guides" mapped to an ARRAY of guide objects.
    - If the document contains multiple distinct topics or rulesets, split them into multiple guide objects inside the array.
    - AUTOMATICALLY TRANSLATE all output content (titles, steps, donts, keywords) flawlessly into ENGLISH, no matter what the input language is.
    - EXHAUSTIVELY extract EVERY single actionable rule, step, or requirement into the "steps" array. Do not skip or summarize rules. List them out point by point completely.
    - EXHAUSTIVELY extract ALL warnings, restrictions, or negative instructions for the "dont" array.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # More capable model for comprehensive extraction
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ AI Guide Extraction Error: {e}")
        raise e