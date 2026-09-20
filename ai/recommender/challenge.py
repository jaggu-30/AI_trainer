from dataclasses import dataclass


@dataclass(frozen=True)
class FitnessChallenge:
    name: str
    goal: str
    duration_days: int
    difficulty: str
    reason: str


class ChallengeRecommender:
    """Recommend fitness challenges based on user goals."""

    CHALLENGES = [
        {
            "name": "7-Day Consistency Challenge",
            "goal": "general_fitness",
            "duration_days": 7,
            "difficulty": "beginner",
        },
        {
            "name": "14-Day Strength Challenge",
            "goal": "strength",
            "duration_days": 14,
            "difficulty": "intermediate",
        },
        {
            "name": "21-Day Weight Loss Challenge",
            "goal": "weight_loss",
            "duration_days": 21,
            "difficulty": "beginner",
        },
        {
            "name": "14-Day Muscle Builder Challenge",
            "goal": "muscle_gain",
            "duration_days": 14,
            "difficulty": "intermediate",
        },
        {
            "name": "10-Day Endurance Challenge",
            "goal": "endurance",
            "duration_days": 10,
            "difficulty": "intermediate",
        },
    ]

    def recommend(
        self,
        fitness_goal: str | None = None,
        limit: int = 3,
    ) -> list[FitnessChallenge]:
        goal = (fitness_goal or "general_fitness").lower()

        aliases = {
            "muscle": "muscle_gain",
            "muscle gain": "muscle_gain",
            "strength training": "strength",
            "weight loss": "weight_loss",
            "fat loss": "weight_loss",
            "endurance training": "endurance",
        }

        goal = aliases.get(goal, goal)

        ranked = sorted(
            self.CHALLENGES,
            key=lambda challenge: (
                challenge["goal"] != goal,
                challenge["difficulty"] != "beginner",
            ),
        )

        recommendations = []

        for challenge in ranked[:limit]:
            if challenge["goal"] == goal:
                reason = (
                    f"This challenge is designed around your "
                    f"{fitness_goal or goal} goal."
                )
            else:
                reason = (
                    "This challenge provides an alternative way "
                    "to build consistency."
                )

            recommendations.append(
                FitnessChallenge(
                    name=challenge["name"],
                    goal=challenge["goal"],
                    duration_days=challenge["duration_days"],
                    difficulty=challenge["difficulty"],
                    reason=reason,
                )
            )

        return recommendations