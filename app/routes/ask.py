from fastapi import APIRouter
from app.models.schemas import QuestionRequest
from app.services.ai_service import classify_question
from app.services.guide_service import get_guide

router = APIRouter()

@router.post("/ask")
def ask_question(request: QuestionRequest):
    category = classify_question(request.question)
    response = get_guide(category)
    return response