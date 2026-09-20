from dataclasses import dataclass

from ai.habit_tracker.behavior import BehaviorAnalysis


@dataclass(frozen=True)
class SkipRisk:
    probability: float
    level: str
    reason: str


class WorkoutSkipPredictor:
    """Estimate workout-skipping risk from behavioral signals."""

    def predict(
        self,
        behavior: BehaviorAnalysis,
    ) -> SkipRisk:
        probability = behavior.behavioral_risk_score

        if behavior.risk_level == "high":
            reason = (
                "Recent emotional and motivation signals indicate "
                "a high risk of skipping a planned workout."
            )
        elif behavior.risk_level == "medium":
            reason = (
                "Recent behavior indicates some risk of missing "
                "a planned workout."
            )
        else:
            reason = (
                "Recent behavior does not indicate a significant "
                "workout-skipping risk."
            )

        return SkipRisk(
            probability=round(probability, 2),
            level=behavior.risk_level,
            reason=reason,
        )