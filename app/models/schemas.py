from pydantic import BaseModel
from typing import Optional, List

class QuestionRequest(BaseModel):
    question: str
    language: Optional[str] = "english"

class GuideResponse(BaseModel):
    # Make original fields optional
    steps: Optional[List[str]] = None
    dont: Optional[List[str]] = None
    office: Optional[str] = None
    
    # New field for friendly mode
    message: Optional[str] = None

class RawDocumentRequest(BaseModel):
    document_text: str

class GenerateGuideResponse(BaseModel):
    ids: List[str]
    guides_count: int
    status: str

class UpdateGuideRequest(BaseModel):
    title: str
    steps: List[str]
    dont: List[str]
    office: str
    keywords: List[str]