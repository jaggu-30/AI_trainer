from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class WorkoutSession(Base):
    """
    Stores the performance results of a completed
    AI-analyzed workout session.
    """

    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    exercise: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    total_repetitions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    performance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    best_frame_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    worst_frame_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    depth_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    posture_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    control_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    average_repetition_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    best_repetition_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    worst_repetition_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    rating: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    warnings: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )