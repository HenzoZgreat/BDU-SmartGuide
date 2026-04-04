import json

with open("app/data/knowledge_base.json", encoding="utf-8") as f:
    knowledge_base = json.load(f)

def get_guide(category: str):
    return knowledge_base.get(category, {
        "steps": ["Sorry, I couldn't understand your request."],
        "dont": [],
        "office": "N/A"
    })