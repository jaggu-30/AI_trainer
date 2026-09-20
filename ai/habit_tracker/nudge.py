from dataclasses import dataclass

from ai.habit_tracker.prediction import SkipRisk


@dataclass(frozen=True)
class MotivationalNudge:
    message: str
    urgency: str
    action: str


class MotivationalNudgeGenerator:
    """Generate motivational guidance from workout skip risk."""

    def generate(
        self,
        risk: SkipRisk,
        fitness_goal: str | None = None,
    ) -> MotivationalNudge:
        goal = fitness_goal or "your fitness goal"

        if risk.level == "high":
            return MotivationalNudge(
                message=(
                    "Your recent motivation signals suggest that "
                    "you may be at risk of skipping your workout. "
                    f"Stay focused on {goal} and keep your routine "
                    "consistent. One difficult day does not define "
                    "your progress."
                ),
                urgency="high",
                action="send_immediate_nudge",
            )

        if risk.level == "medium":
            return MotivationalNudge(
                message=(
                    "Your motivation looks a little inconsistent "
                    "recently. Keep your next fitness session simple "
                    f"and stay focused on {goal}."
                ),
                urgency="medium",
                action="send_supportive_nudge",
            )

        return MotivationalNudge(
            message=(
                f"Your recent behavior looks stable. Keep building "
                f"consistency toward {goal}."
            ),
            urgency="low",
            action="maintain_motivation",
        )