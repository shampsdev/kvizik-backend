import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.ml_pipeline.AITestGenerator import AITestGenerator

from .auth import verify_token
from .database import get_db
from .jwt import create_access_token
from .models import Answer, Question, Test, User
from .schemas import QuizRequest, QuizResultRequest

router = APIRouter()


@router.post("/users")
def create_user_endpoint(db: Session = Depends(get_db)):
    user = User(id=uuid.uuid4())
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(data={"sub": str(user.id)})
    return {"auth_token": token}


test_generator = AITestGenerator().set_difficulty("easy").set_questions_amount(2)


@router.post("/quiz/generate")
def generate_quiz(
    request: QuizRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    user_id: uuid.UUID = uuid.UUID(token_data.get("sub"))
    try:
        ai_test = test_generator.generate_test(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate test: {e}")

    test = Test(creator_id=user_id, text=request.text, generated=ai_test.dict())

    db.add(test)
    db.commit()
    db.refresh(test)

    for q in ai_test.questions:
        question = Question(
            test_id=test.id,
            text=q.question,
        )
        db.add(question)

        db.commit()
        db.refresh(question)

        correct_answer = q.correct_answer

        for option in q.options:
            answer = Answer(
                question_id=question.id,
                text=option,
                is_right=(option == correct_answer),
            )
            db.add(answer)

    db.commit()
    return {"test_id": str(test.id)}


import uuid

from fastapi import HTTPException


@router.get("/quiz/{test_id}", dependencies=[Depends(verify_token)])
def get_quiz(test_id: str, db: Session = Depends(get_db)):
    try:
        print(test_id)
        test_id_uuid = uuid.UUID(test_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid test_id format")

    test = (
        db.query(Test)
        .options(joinedload(Test.questions).joinedload(Question.answers))
        .filter(Test.id == test_id_uuid)
        .first()
    )

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = []
    for question in test.questions:
        answers = [
            {"id": str(answer.id), "text": answer.text} for answer in question.answers
        ]
        questions.append(
            {"id": str(question.id), "text": question.text, "answers": answers}
        )

    result = {
        "id": str(test.id),
        "questions": questions,
    }
    return result


@router.post("/quiz/{test_id}/result")
def submit_quiz_results(
    test_id: str,
    result_request: QuizResultRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    test_id_uuid = uuid.UUID(test_id)

    test = (
        db.query(Test)
        .options(joinedload(Test.questions).joinedload(Question.answers))
        .filter(Test.id == test_id_uuid)
        .first()
    )

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    correct_answers_count = 0
    total_questions = len(result_request.answers)

    correct_answer_lookup = {
        answer.question.id: answer.id  # type:ignore
        for question in test.questions
        for answer in question.answers
        if answer.is_right
    }

    for answer in result_request.answers:
        if correct_answer_lookup.get(answer.question_id) == answer.answer_id:
            correct_answers_count += 1

    result = {
        "correct_answers": correct_answers_count,
        "total_questions": total_questions,
        "score": (
            (correct_answers_count / total_questions) * 100
            if total_questions > 0
            else 0
        ),
    }

    return result
