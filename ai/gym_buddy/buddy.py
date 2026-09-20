from dataclasses import dataclass

from ai.gym_buddy.emotion import EmotionState


@dataclass(frozen=True)
class BuddyResponse:
    message: str
    strategy: str


class VirtualGymBuddy:
    """Generate supportive fitness guidance based on emotional state."""

    def respond(
        self,
        emotion: EmotionState,
        user_message: str,
        fitness_goal: str | None = None,
    ) -> BuddyResponse:
        goal = fitness_goal or "your fitness goal"

        if emotion.emotion == "unmotivated":
            return BuddyResponse(
                message=(
                    "It sounds like your motivation is low today. "
                    f"Don't let one difficult day derail {goal}. "
                    "Focus on keeping your routine consistent rather than "
                    "being perfect."
                ),
                strategy="motivation_support",
            )

        if emotion.emotion == "stressed":
            return BuddyResponse(
                message=(
                    "You sound stressed and low on energy. "
            "Recovery matters too. "
            "Consider keeping today's fitness goal manageable "
            "and prioritizing recovery."
                ),
                strategy="stress_support",
            )

        if emotion.emotion == "positive":
            return BuddyResponse(
                message=(
                    "You're sounding motivated and positive. "
                    f"That is a strong mindset for {goal}. "
                    "Keep that momentum going and stay consistent."
                ),
                strategy="positive_reinforcement",
            )

        return BuddyResponse(
            message=(
                f"I'm here to help you stay consistent with {goal}. "
                "Tell me how you're feeling or what part of your "
                "fitness routine you want help with."
            ),
            strategy="general_support",
        )