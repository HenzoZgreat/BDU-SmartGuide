from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class GuideResponse(BaseModel):
    steps: list[str]
    dont: list[str]
    office: str