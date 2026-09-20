from dataclasses import dataclass, field

from ai.gym_trainer.rep_score import RepScore
from ai.gym_trainer.session_analyzer import SquatSessionSummary


@dataclass
class PerformanceReport:
    exercise: str
    total_repetitions: int

    performance_score: float
    best_frame_score: float
    worst_frame_score: float

    depth_score: float
    posture_score: float
    control_score: float

    average_repetition_score: float
    best_repetition_score: float
    worst_repetition_score: float

    rating: str
    warnings: list[str] = field(default_factory=list)

    repetition_scores: list[RepScore] = field(default_factory=list)


class PerformanceReportGenerator:
    """
    Converts a completed squat session summary into a
    frontend-friendly performance report.
    """

    def generate(
        self,
        summary: SquatSessionSummary,
        exercise: str = "squat",
    ) -> PerformanceReport:
        return PerformanceReport(
            exercise=exercise,
            total_repetitions=summary.total_repetitions,
            performance_score=summary.average_repetition_score,
            best_frame_score=summary.best_score,
            worst_frame_score=summary.worst_score,
            depth_score=summary.average_depth_score,
            posture_score=summary.average_posture_score,
            control_score=summary.average_control_score,
            average_repetition_score=summary.average_repetition_score,
            best_repetition_score=summary.best_repetition_score,
            worst_repetition_score=summary.worst_repetition_score,
            rating=self._calculate_rating(
                summary.average_repetition_score
            ),
            warnings=summary.warnings.copy(),
            repetition_scores=summary.repetition_scores.copy(),
        )

    @staticmethod
    def _calculate_rating(score: float) -> str:
        if score >= 90:
            return "excellent"

        if score >= 75:
            return "good"

        if score >= 60:
            return "needs_improvement"

        return "poor"