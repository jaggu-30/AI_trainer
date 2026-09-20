from dataclasses import dataclass

from ai.smart_gym.equipment import EquipmentTelemetry


@dataclass(frozen=True)
class RecoveryRecommendation:
    rest_minutes: int
    intensity: str
    reason: str


class RecoveryAdvisor:
    """Recommend rest and training intensity from telemetry."""

    def recommend(
        self,
        telemetry: EquipmentTelemetry,
    ) -> RecoveryRecommendation:
        if telemetry.fatigue_level >= 80:
            return RecoveryRecommendation(
                rest_minutes=5,
                intensity="light",
                reason=(
                    "High fatigue detected. Increase recovery "
                    "time and reduce training intensity."
                ),
            )

        if telemetry.fatigue_level >= 50:
            return RecoveryRecommendation(
                rest_minutes=3,
                intensity="moderate",
                reason=(
                    "Moderate fatigue detected. Use moderate "
                    "intensity with additional recovery."
                ),
            )

        return RecoveryRecommendation(
            rest_minutes=1,
            intensity="high"
            if telemetry.performance_score >= 85
            else "moderate",
            reason=(
                "Fatigue is controlled. Continue within "
                "the current training intensity."
            ),
        )