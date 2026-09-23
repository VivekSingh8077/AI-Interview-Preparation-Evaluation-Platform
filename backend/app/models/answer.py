from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)

    answer_text: Mapped[str] = mapped_column(Text, nullable=False)

    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    semantic_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    concept_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    grammar_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Structured feedback: {"strengths": [...], "weaknesses": [...], "suggestions": [...],
    #                        "covered_concepts": [...], "missing_concepts": [...]}
    feedback: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    interview = relationship("Interview", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    human_evaluations = relationship("HumanEvaluation", back_populates="answer", cascade="all, delete-orphan")
