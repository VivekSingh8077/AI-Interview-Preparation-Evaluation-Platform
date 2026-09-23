from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class HumanEvaluation(Base):
    """
    Stores a human evaluator's score for a given answer, alongside the AI's
    own score, so §17 metrics (MAE, RMSE, Pearson/Spearman correlation) can
    be computed later by app/evaluation/human_comparison.py.
    """
    __tablename__ = "human_evaluations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), nullable=False, index=True)

    human_score: Mapped[float] = mapped_column(Float, nullable=False)  # e.g. on a 0-10 scale
    evaluator_name: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    answer = relationship("Answer", back_populates="human_evaluations")
