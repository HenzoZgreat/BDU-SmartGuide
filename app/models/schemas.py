from pydantic import BaseModel
from typing import Optional, List

class QuestionRequest(BaseModel):
    question: str

class GuideResponse(BaseModel):
    # Make original fields optional
    steps: Optional[List[str]] = None
    dont: Optional[List[str]] = None
    office: Optional[str] = None
    
    # New field for friendly mode
    message: Optional[str] = None