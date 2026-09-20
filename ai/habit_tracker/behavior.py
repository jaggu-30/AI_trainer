from dataclasses import dataclass

from ai.gym_buddy.memory import ConversationMemory


@dataclass(frozen=True)
class BehaviorAnalysis:
    consistency_score: float
    motivation_score: float
    emotional_stability_score: float
    behavioral_risk_score: float
    risk_level: str


class HabitBehaviorAnalyzer:
    """Analyze fitness-adherence signals from conversation memory."""

    def analyze(
        self,
        memory: ConversationMemory,
    ) -> BehaviorAnalysis:
        if memory.total_messages == 0:
            return BehaviorAnalysis(
                consistency_score=100.0,
                motivation_score=50.0,
                emotional_stability_score=100.0,
                behavioral_risk_score=0.0,
                risk_level="low",
            )

        negative_ratio = (
            memory.negative_messages
            / memory.total_messages
        )

        unmotivated_ratio = (
            memory.unmotivated_count
            / memory.total_messages
        )

        stressed_ratio = (
            memory.stressed_count
            / memory.total_messages
        )

        low_motivation_ratio = (
            memory.low_motivation_count
            / memory.total_messages
        )

        motivation_score = 100.0 - (
            (negative_ratio * 25.0)
            + (unmotivated_ratio * 35.0)
            + (low_motivation_ratio * 40.0)
        )

        emotional_stability_score = 100.0 - (
            stressed_ratio * 60.0
        )

        consistency_score = 100.0 - (
            unmotivated_ratio * 70.0
        )

        risk_score = (
            (100.0 - motivation_score) * 0.45
            + (100.0 - emotional_stability_score) * 0.25
            + (100.0 - consistency_score) * 0.30
        )

        if memory.motivation_trend == "declining":
            risk_score += 15.0

        elif memory.motivation_trend == "improving":
            risk_score -= 10.0

        risk_score = max(
            0.0,
            min(100.0, risk_score),
        )

        if risk_score >= 70.0:
            risk_level = "high"
        elif risk_score >= 40.0:
            risk_level = "medium"
        else:
            risk_level = "low"

        return BehaviorAnalysis(
            consistency_score=round(
                max(0.0, min(100.0, consistency_score)),
                2,
            ),
            motivation_score=round(
                max(0.0, min(100.0, motivation_score)),
                2,
            ),
            emotional_stability_score=round(
                max(0.0, min(100.0, emotional_stability_score)),
                2,
            ),
            behavioral_risk_score=round(
                risk_score,
                2,
            ),
            risk_level=risk_level,
        )