from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.question import InterviewType, Difficulty


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    type: Mapped[InterviewType] = mapped_column(Enum(InterviewType), nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), nullable=False)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    user = relationship("User", back_populates="interviews")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete-orphan")
