from dataclasses import dataclass
from datetime import date
from statistics import mean


@dataclass(frozen=True)
class WeeklyPerformanceReport:
    week_start: date
    week_end: date

    workout_count: int
    total_repetitions: int

    average_performance_score: float
    best_performance_score: float
    worst_performance_score: float

    average_depth_score: float
    average_posture_score: float
    average_control_score: float

    performance_trend: str
    summary: str


class WeeklyPerformanceAnalyzer:
    """Aggregate workout performance into a weekly progress report."""

    def analyze(
        self,
        sessions,
        week_start: date,
        week_end: date,
    ) -> WeeklyPerformanceReport:
        filtered_sessions = [
            session
            for session in sessions
            if session.started_at.date() >= week_start
            and session.started_at.date() <= week_end
        ]

        if not filtered_sessions:
            return WeeklyPerformanceReport(
                week_start=week_start,
                week_end=week_end,
                workout_count=0,
                total_repetitions=0,
                average_performance_score=0.0,
                best_performance_score=0.0,
                worst_performance_score=0.0,
                average_depth_score=0.0,
                average_posture_score=0.0,
                average_control_score=0.0,
                performance_trend="no_data",
                summary="No workouts were recorded during this week.",
            )

        performance_scores = [
            float(session.performance_score)
            for session in filtered_sessions
        ]

        depth_scores = [
            float(session.depth_score)
            for session in filtered_sessions
        ]

        posture_scores = [
            float(session.posture_score)
            for session in filtered_sessions
        ]

        control_scores = [
            float(session.control_score)
            for session in filtered_sessions
        ]

        total_repetitions = sum(
            int(session.total_repetitions)
            for session in filtered_sessions
        )

        average_score = mean(performance_scores)
        best_score = max(performance_scores)
        worst_score = min(performance_scores)

        trend = self._calculate_trend(
            filtered_sessions
        )

        summary = self._build_summary(
            workout_count=len(filtered_sessions),
            total_repetitions=total_repetitions,
            average_score=average_score,
            trend=trend,
        )

        return WeeklyPerformanceReport(
            week_start=week_start,
            week_end=week_end,
            workout_count=len(filtered_sessions),
            total_repetitions=total_repetitions,
            average_performance_score=round(
                average_score,
                2,
            ),
            best_performance_score=round(
                best_score,
                2,
            ),
            worst_performance_score=round(
                worst_score,
                2,
            ),
            average_depth_score=round(
                mean(depth_scores),
                2,
            ),
            average_posture_score=round(
                mean(posture_scores),
                2,
            ),
            average_control_score=round(
                mean(control_scores),
                2,
            ),
            performance_trend=trend,
            summary=summary,
        )

    @staticmethod
    def _calculate_trend(
        sessions,
    ) -> str:
        ordered = sorted(
            sessions,
            key=lambda session: session.started_at,
        )

        if len(ordered) < 2:
            return "stable"

        first = float(
            ordered[0].performance_score
        )
        last = float(
            ordered[-1].performance_score
        )

        difference = last - first

        if difference >= 5:
            return "improving"

        if difference <= -5:
            return "declining"

        return "stable"

    @staticmethod
    def _build_summary(
        workout_count: int,
        total_repetitions: int,
        average_score: float,
        trend: str,
    ) -> str:
        if trend == "improving":
            trend_text = "Performance is improving."
        elif trend == "declining":
            trend_text = "Performance is declining."
        else:
            trend_text = "Performance is relatively stable."

        return (
            f"You completed {workout_count} workout(s) "
            f"with {total_repetitions} total repetitions. "
            f"Your average performance score was "
            f"{average_score:.2f}. "
            f"{trend_text}"
        )