from fastapi import APIRouter, Query, HTTPException
from app.models.schemas import QuestionRequest, GuideResponse
from app.services.ai_service import classify_question
from app.services.guide_service import get_guide
from app.services.response_formatter import format_friendly_response

router = APIRouter()

@router.post("/ask", response_model=GuideResponse)
def ask_question(  # 🔹 Removed 'async'
    request: QuestionRequest,
    format: str = Query(default="json", pattern="^(json|friendly)$")  # 🔹 'pattern' replaces deprecated 'regex'
):
    try:
        # 🔹 Removed 'await' - these are synchronous functions
        category = classify_question(request.question)
        guide = get_guide(category)
        
        if format == "friendly":
            friendly_msg = format_friendly_response(request.question, guide)
            return GuideResponse(message=friendly_msg)
        else:
            return GuideResponse(
                steps=guide.get("steps"),
                dont=guide.get("dont"),
                office=guide.get("office")
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")