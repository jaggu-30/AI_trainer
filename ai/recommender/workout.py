from dataclasses import dataclass


@dataclass(frozen=True)
class WorkoutProgramRecommendation:
    name: str
    goal: str
    difficulty: str
    duration_minutes: int
    reason: str


class WorkoutProgramRecommender:
    """Recommend workout programs based on fitness goals."""

    PROGRAMS = [
        {
            "name": "Beginner Strength Builder",
            "goal": "strength",
            "difficulty": "beginner",
            "duration_minutes": 35,
        },
        {
            "name": "Muscle Growth Program",
            "goal": "muscle_gain",
            "difficulty": "intermediate",
            "duration_minutes": 50,
        },
        {
            "name": "Weight Loss & Conditioning",
            "goal": "weight_loss",
            "difficulty": "beginner",
            "duration_minutes": 40,
        },
        {
            "name": "Endurance Builder",
            "goal": "endurance",
            "difficulty": "intermediate",
            "duration_minutes": 45,
        },
        {
            "name": "General Fitness Foundation",
            "goal": "general_fitness",
            "difficulty": "beginner",
            "duration_minutes": 30,
        },
    ]

    def recommend(
        self,
        fitness_goal: str | None = None,
        limit: int = 3,
    ) -> list[WorkoutProgramRecommendation]:
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
            self.PROGRAMS,
            key=lambda program: (
                program["goal"] != goal,
                program["difficulty"] != "beginner",
            ),
        )

        recommendations = []

        for program in ranked[:limit]:
            if program["goal"] == goal:
                reason = (
                    f"This program directly matches your "
                    f"{fitness_goal or goal} goal."
                )
            else:
                reason = (
                    "This is an alternative program that can "
                    "support your overall fitness."
                )

            recommendations.append(
                WorkoutProgramRecommendation(
                    name=program["name"],
                    goal=program["goal"],
                    difficulty=program["difficulty"],
                    duration_minutes=program["duration_minutes"],
                    reason=reason,
                )
            )

        return recommendations