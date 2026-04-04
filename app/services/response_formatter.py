import os
from groq import Groq

# Use os.getenv directly, just like in ai_service.py
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def format_friendly_response(question: str, guide: dict) -> str:
    steps = "\n".join(f"• {step}" for step in guide.get("steps", []))
    donts = "\n".join(f"⚠️ {item}" for item in guide.get("dont", []))
    office = guide.get("office", "the relevant office")
    
    prompt = f"""
You are BDU SmartGuide, a friendly, empathetic AI assistant for Bahir Dar University students.

A student asked: "{question}"

Here is the official guidance:
✅ Steps to follow:
{steps}

❌ Avoid:
{donts}

📍 Visit: {office}

Please craft a warm, natural-language response that:
1. Clearly explains the steps in conversational tone
2. Gently weaves in the warnings
3. Ends with 'If you need further assistance, please visit ' + mentions the office name
4. Keeps it concise (3-5 short lines max)
5. Uses emojis sparingly for warmth if needed
6. Say something like "i dont know about the information you asked, please visit the student affairs office for help" if there is no category match or guide info, dont make up things or dont be vauge

Write in clear, simple English.
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Friendly Response Error: {e}")
        return f"I'm sorry you're dealing with this. Here's what to do:\n\n" \
               f"{' '.join(guide.get('steps', []))}\n\n" \
               f"Please visit: {office}. Avoid: {'; '.join(guide.get('dont', []))}"