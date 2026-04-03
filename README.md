# BDU Smart Guide

BDU Smart Guide is a simple FastAPI service that helps students get quick guidance for common campus-related issues. A user's question is classified with Groq, then mapped to a local knowledge base that returns steps to follow, things to avoid, and the office to visit.

## Features

- Accepts student questions through a REST API
- Classifies questions into predefined categories using Groq
- Returns structured guidance from a local JSON knowledge base
- Lightweight project structure that is easy to extend

## Current Categories

The classifier is currently designed to recognize these categories:

- `lost_id`
- `missed_registration`
- `grade_complaint`

At the moment, the bundled knowledge base only includes a filled response for `lost_id`.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Groq API
- Pydantic
- Python Dotenv

## Project Structure

```text
BDU-SmartGuide/
|-- app/
|   |-- core/
|   |   `-- config.py
|   |-- data/
|   |   `-- knowledge_base.json
|   |-- models/
|   |   `-- schemas.py
|   |-- routes/
|   |   `-- ask.py
|   |-- services/
|   |   |-- ai_service.py
|   |   `-- guide_service.py
|   `-- main.py
|-- requirements.txt
`-- README.md
```

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd BDU-SmartGuide
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

Note: the current implementation uses `GROQ_API_KEY`. `OPENAI_API_KEY` is loaded in the config file but is not used by the running API flow right now.

## Running the App

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive docs:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoint

### `POST /ask`

Send a question:

```json
{
  "question": "I lost my student ID card. What should I do?"
}
```

Example response for a recognized category:

```json
{
  "steps": [
    "Go to student affairs office",
    "Bring 2 passport photos",
    "Pay replacement fee"
  ],
  "dont": [
    "Do not delay more than 3 days"
  ],
  "office": "Student Affairs Office"
}
```

Fallback response when no matching guide is found:

```json
{
  "steps": [
    "Sorry, I couldn't understand your request."
  ],
  "dont": [],
  "office": "N/A"
}
```

## How It Works

1. The client sends a question to `POST /ask`.
2. The app sends that question to Groq for category classification.
3. The predicted category is used to look up a response in `app/data/knowledge_base.json`.
4. The matching guide is returned as JSON.

## Extending the Knowledge Base

To support more student issues:

1. Add a new category entry to `app/data/knowledge_base.json`.
2. Make sure the category name matches what the classifier can return.
3. Add `steps`, `dont`, and `office` values for that category.

## Notes

- The API route does not currently validate whether the model returned an unexpected category.
- The knowledge base is loaded from a local JSON file at startup/import time.
- `GuideResponse` exists in the models file, but the route does not currently declare it as the response model.

## License

Add your preferred license information here.
