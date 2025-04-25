from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str


class ValidationInput(BaseModel):
    full_answer: str
