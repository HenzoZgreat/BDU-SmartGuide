# migrate_to_firebase.py
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Load your JSON
with open("app/data/knowledge_base.json", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# 3. Upload to Firestore
batch = db.batch()
guides_ref = db.collection("guides")

for doc_id, data in knowledge_base.items():
    doc_ref = guides_ref.document(doc_id)
    batch.set(doc_ref, data)

batch.commit()
print(f"✅ Successfully migrated {len(knowledge_base)} guides to Firestore!")