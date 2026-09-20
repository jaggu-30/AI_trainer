from datetime import date, timedelta

from sqlalchemy.orm import Session

from ai.pose_analyzer.weekly import (
    WeeklyPerformanceAnalyzer,
    WeeklyPerformanceReport,
)
from app.models.user import User
from app.models.workout import WorkoutSession


class WeeklyPerformanceService:
    """Generate weekly performance reports from stored workouts."""

    def __init__(self) -> None:
        self.analyzer = WeeklyPerformanceAnalyzer()

    def generate_report(
        self,
        db: Session,
        user: User,
        week_start: date | None = None,
    ) -> WeeklyPerformanceReport:
        if week_start is None:
            week_end = date.today()
            week_start = week_end - timedelta(days=6)
        else:
            week_end = week_start + timedelta(days=6)

        sessions = (
            db.query(WorkoutSession)
            .filter(
                WorkoutSession.user_id == user.id,
                WorkoutSession.started_at >= week_start,
                WorkoutSession.started_at < week_end + timedelta(days=1),
            )
            .order_by(
                WorkoutSession.started_at.asc()
            )
            .all()
        )

        return self.analyzer.analyze(
            sessions=sessions,
            week_start=week_start,
            week_end=week_end,
        )