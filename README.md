# BDU Smart Guide Backend 🚀

BDU Smart Guide is a FastAPI service powered by AI to help students navigate campus life. It serves as both a conversational guide backend and an intelligent administrative platform capable of parsing unstructured documents into structured guides.

## 🔥 Key Features

- **Conversational AI (`/ask`)**: Categorizes student questions via Groq LLM and retrieves dynamic structured routes for campus processes.
- **AI Document Parsing Pipeline (`/admin/generate-guide`)**: Allows admins to input raw, unstructured text (like Student Rules and Manuals in localized languages). The backend uses an LLM to extract logical processes, translate them to English, and structure them into JSON formats to automatically insert into the database.
- **Dynamic Database via Firestore**: Integrates directly with Firebase Firestore for real-time CRUD and high accessibility.
- **Data Migration Utils**: Includes a customized `migrate_to_firebase.py` executable to move legacy data to the cloud effortlessly.

## 🛠️ Tech Stack

- **Framework**: Python 3.10+, FastAPI & Uvicorn
- **Database Backend**: Firebase Admin SDK (Cloud Firestore)
- **AI & Integrations**: Groq API, OpenAI (optional) 
- **Validation**: Pydantic

## 📂 Project Structure

```text
BDU-SmartGuide/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── data/
│   │   └── knowledge_base.json         # Legacy local snapshot
│   ├── models/
│   │   └── schemas.py
│   ├── routes/
│   │   └── ask.py                      # REST Endpoint definition
│   ├── services/
│   │   ├── ai_service.py               # Handles the Groq Document Parser logic
│   │   └── guide_service.py            # Interfaces with Firestore
│   └── main.py                         # FastAPI Application entrypoint
├── migrate_to_firebase.py              # Firestore seeding script
├── firebase-key.json                   # Service Account configuration keys
└── requirements.txt
```

## ⚙️ Setup & Installation

1. Clone the repository and navigate inside:
   ```bash
   git clone <your-repository-url>
   cd BDU-SmartGuide
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Environment Setup (`.env`):
   Create a `.env` in the root:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Firebase Setup**: 
   Ensure `firebase-key.json` (your Google service account JSON) is placed in the root directory. Run the initial migration if needed to seed the Database:
   ```bash
   python migrate_to_firebase.py
   ```

## 🚀 Running the App

Start the server locally:
```bash
uvicorn app.main:app --reload
```

Interactive documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧠 How the AI Pipeline Works

1. **Document Ingestion**: Admins send unformatted text to `/admin/generate-guide`.
2. **AI Refinement**: The AI service (`ai_service.py`) processes this raw text context, parsing it for logical procedures (identifying steps, warnings, keywords, and responsible offices).
3. **Database Sink**: Once validated by Pydantic models, the structured guides are written to Firebase Firestore.
4. **Student Usage**: When a student asks a query via `/ask`, their semantic intent maps directly to these dynamically updated Firestore documents to provide them instantaneous guidance.
