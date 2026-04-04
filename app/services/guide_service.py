# app/services/guide_service.py
from app.core.firebase import get_db

db = get_db()
guides_ref = db.collection("guides")

def get_guide(category: str) -> dict:
    # Prevent empty/invalid doc IDs from crashing Firestore
    if not category or category == "unknown":
        return {
            "steps": ["I couldn't understand your request. Please rephrase or visit the Student Affairs Office for help."],
            "dont": [],
            "office": "Student Affairs Office"
        }
    
    try:
        doc = guides_ref.document(category).get()
        if doc.exists:
            return doc.to_dict()
        return {
            "steps": ["Guide not found. Please contact your department office."],
            "dont": [],
            "office": "Department Office"
        }
    except Exception as e:
        print(f"⚠️ Firestore Error: {e}")
        return {
            "steps": ["System temporarily unavailable. Please try again later."],
            "dont": [],
            "office": "ICT Support Office"
        }