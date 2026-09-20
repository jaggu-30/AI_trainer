from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from ai.gym_trainer.performance_report import PerformanceReport

from app.models.user import User
from app.models.workout import WorkoutSession


class WorkoutPersistenceService:
    """Persist completed AI-analyzed workout sessions."""

    def save_report(
        self,
        db: Session,
        user: User,
        report: PerformanceReport,
        started_at: datetime | None = None,
    ) -> WorkoutSession:
        """Save a performance report as a workout session."""

        completed_at = datetime.utcnow()

        if started_at is None:
            started_at = completed_at

        workout = WorkoutSession(
            user_id=user.id,
            exercise=report.exercise,
            total_repetitions=report.total_repetitions,
            performance_score=report.performance_score,
            best_frame_score=report.best_frame_score,
            worst_frame_score=report.worst_frame_score,
            depth_score=report.depth_score,
            posture_score=report.posture_score,
            control_score=report.control_score,
            average_repetition_score=(
                report.average_repetition_score
            ),
            best_repetition_score=(
                report.best_repetition_score
            ),
            worst_repetition_score=(
                report.worst_repetition_score
            ),
            rating=report.rating,
            warnings=(
                "\n".join(report.warnings)
                if report.warnings
                else None
            ),
            started_at=started_at,
            completed_at=completed_at,
        )

        db.add(workout)
        db.commit()
        db.refresh(workout)

        return workout