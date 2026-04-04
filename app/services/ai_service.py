import os
from groq import Groq
from dotenv import load_dotenv
from app.services.guide_service import knowledge_base

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_question(question: str) -> str:
    categories = list(knowledge_base.keys())

    prompt = f"""
        Classify this question into one of the categories:
        {chr(10).join(f"- {c}" for c in categories)}

        Question: {question}

        Only return the category name.
    """

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
)

    return response.choices[0].message.content.strip()