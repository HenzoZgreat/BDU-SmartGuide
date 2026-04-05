import json
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException
from app.models.schemas import QuestionRequest, GuideResponse, RawDocumentRequest, GenerateGuideResponse, UpdateGuideRequest
from app.services.ai_service import classify_question, extract_guide_from_document, clear_categories_cache
from app.services.guide_service import get_guide
from app.core.firebase import get_db
import re
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

@router.get("/guides")
def get_guides():
    db = get_db()
    docs = db.collection("guides").stream()
    guides = []
    for doc in docs:
        data = doc.to_dict()
        key = doc.id
        title = data.get("title") or " ".join(word.capitalize() for word in key.split("_"))
        guides.append({
            "id": key,
            "title": title,
            "steps": data.get("steps", []),
            "dont": data.get("dont", []),
            "office": data.get("office", "N/A"),
            "keywords": data.get("keywords", []),
            "tag": "Campus Guide",
            "tagColor": "primary",
            "icon": "help-circle"
        })
    return {"guides": guides, "total": len(guides)}

@router.get("/stats")
def get_stats():
    db = get_db()
    docs = db.collection("guides").stream()
    guides_cache = [doc.to_dict() for doc in docs]
    offices = set(v.get("office") for v in guides_cache if v.get("office"))
    return {
        "totalGuides": len(guides_cache),
        "totalOffices": len(offices),
        "systemStatus": "Online",
        "apiStatus": "Healthy"
    }

@router.post("/admin/generate-guide", response_model=GenerateGuideResponse)
def generate_guide(request: RawDocumentRequest):
    try:
        # Extract structured logic via Groq
        result = extract_guide_from_document(request.document_text)
        guides_array = result.get("guides", [])
        
        saved_ids = []
        db = get_db()
        
        for guide in guides_array:
            # Generate stable ID from the title
            title = guide.get("title", "Unknown Guide")
            doc_id = re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')
            if not doc_id:
                import uuid
                doc_id = f"guide_{uuid.uuid4().hex[:8]}"
            
            # Make sure we don't accidentally overwrite if title is same, append a short hash
            import uuid
            doc_id = f"{doc_id}_{uuid.uuid4().hex[:4]}"
                
            # Save explicitly to Firebase under 'guides' collection
            db.collection("guides").document(doc_id).set(guide)
            saved_ids.append(doc_id)
        
        clear_categories_cache()
        
        return GenerateGuideResponse(
            ids=saved_ids,
            guides_count=len(saved_ids),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing raw document: {str(e)}")

@router.put("/guides/{guide_id}")
def update_guide(guide_id: str, request: UpdateGuideRequest):
    try:
        db = get_db()
        doc_ref = db.collection("guides").document(guide_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Guide not found")
        
        doc_ref.update({
            "title": request.title,
            "steps": request.steps,
            "dont": request.dont,
            "office": request.office,
            "keywords": request.keywords
        })
        clear_categories_cache()
        return {"status": "success", "message": "Guide updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating guide: {str(e)}")

@router.delete("/guides/{guide_id}")
def delete_guide(guide_id: str):
    try:
        db = get_db()
        doc_ref = db.collection("guides").document(guide_id)
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Guide not found")
        
        doc_ref.delete()
        clear_categories_cache()
        return {"status": "success", "message": "Guide deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting guide: {str(e)}")