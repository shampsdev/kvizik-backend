from pydantic import BaseModel
import uuid
from typing import List


class QuizRequest(BaseModel):
    text: str


class QuizAnswer(BaseModel):
    question_id: uuid.UUID
    answer_id: uuid.UUID


class QuizResultRequest(BaseModel):
    answers: List[QuizAnswer]
