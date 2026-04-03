import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_question(question: str) -> str:
    prompt = f"""
    Classify this question into one of the categories:
    - lost_id
    - missed_registration
    - grade_complaint

    Question: {question}

    Only return the category name.
    """

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
)

    return response.choices[0].message.content.strip()