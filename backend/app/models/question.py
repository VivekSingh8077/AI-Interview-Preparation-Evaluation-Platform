import enum

from sqlalchemy import String, Text, Enum, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class InterviewType(str, enum.Enum):
    TECHNICAL = "technical"
    HR = "hr"


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[InterviewType] = mapped_column(Enum(InterviewType), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), nullable=False, index=True)

    # Nullable: HR questions typically have no single reference answer (§4)
    reference_answer: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Rubric components for completeness scoring, e.g. ["definition","cause","effect","example","solution"]
    rubric: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Flat keyword list, used as a fallback/supplement to semantic concept matching
    keywords: Mapped[list | None] = mapped_column(JSON, nullable=True)

    concepts = relationship("QuestionConcept", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question")


class QuestionConcept(Base):
    __tablename__ = "question_concepts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)
    concept: Mapped[str] = mapped_column(String(200), nullable=False)

    question = relationship("Question", back_populates="concepts")
