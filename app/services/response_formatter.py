import os
from groq import Groq

# Use os.getenv directly, just like in ai_service.py
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def format_friendly_response(question: str, guide: dict, language: str = "english") -> str:
    steps = "\n".join(f"• {step}" for step in guide.get("steps", []))
    donts = "\n".join(f"⚠️ {item}" for item in guide.get("dont", []))
    office = guide.get("office", "the relevant office")
    
    amharic_instruction = ""
    if language.lower() == "amharic":
        amharic_instruction = "IMPORTANT: You MUST translate your entire final response perfectly into Amharic (አማርኛ). Do not output English."

    prompt = f"""
You are BDU SmartGuide, a friendly, empathetic AI assistant for Bahir Dar University students.

A student asked: "{question}"

Here is the official guidance:
✅ Steps to follow:
{steps}

❌ Avoid:
{donts}

📍 Visit: {office}

Please craft a warm, concise response that:
1. Directly answers the student's question by summarizing the necessary steps.
2. Mentions the exact office they need to visit ({office}).
3. EXTREMELY IMPORTANT: Keep the response very short! Maximum of 2-3 concise sentences. Do not list long bullet points. Write it like a quick text message to a friend.
4. If there are warnings to avoid, gently weave them in as a single short point.
5. If there is no specific guide matched or you don't know the answer, just say: "I don't have that specific information, please visit the relevant office for help." Do not make things up.

{amharic_instruction}
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Friendly Response Error: {e}")
        return "I'm currently unable to process your request. Please visit your department office."