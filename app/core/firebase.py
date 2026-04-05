# app/core/firebase.py
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def get_db():
    if not firebase_admin._apps:
        # First try to parse credentials from a JSON string in environment variable
        # This is expected when deployed on platforms like Railway
        cred_json_str = os.getenv("FIREBASE_CREDENTIALS")
        
        # Fallback to local file path
        cred_path = os.getenv("FIREBASE_CRED_PATH")
        
        if cred_json_str:
            cred_dict = json.loads(cred_json_str)
            cred = credentials.Certificate(cred_dict)
        elif cred_path:
            cred = credentials.Certificate(cred_path)
        else:
            raise ValueError("Neither FIREBASE_CREDENTIALS nor FIREBASE_CRED_PATH is set")
            
        firebase_admin.initialize_app(cred)
    return firestore.client()