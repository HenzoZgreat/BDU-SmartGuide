# app/core/firebase.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def get_db():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CRED_PATH")
        if not cred_path:
            raise ValueError("FIREBASE_CRED_PATH not set in .env")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()