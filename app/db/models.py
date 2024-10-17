import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    tests: Mapped[list["Test"]] = relationship(back_populates="creator")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    creator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    creator: Mapped[Optional["User"]] = relationship(back_populates="tests")
    text: Mapped[Optional[str]] = mapped_column(String(65535))
    generated: Mapped[Optional[dict]] = mapped_column(JSONB)
    questions: Mapped[list["Question"]] = relationship(back_populates="test")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    test_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tests.id"))
    test: Mapped[Optional["Test"]] = relationship(back_populates="questions")
    text: Mapped[Optional[str]] = mapped_column(String(255))
    answer: Mapped[Optional["Answer"]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id"))
    question: Mapped[Optional["Question"]] = relationship(back_populates="answer")
    text: Mapped[Optional[str]] = mapped_column(String(255))
    is_right: Mapped[Optional[bool]]
