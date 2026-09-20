from dataclasses import dataclass


@dataclass(frozen=True)
class GymRecommendation:
    name: str
    distance_km: float
    rating: float
    specialties: list[str]
    reason: str


class GymRecommender:
    """Recommend gyms based on user goals and distance."""

    def recommend(
        self,
        gyms: list[dict],
        fitness_goal: str | None = None,
        max_distance_km: float = 10.0,
    ) -> list[GymRecommendation]:
        goal = (fitness_goal or "general fitness").lower()

        candidates = [
            gym
            for gym in gyms
            if float(gym.get("distance_km", 999))
            <= max_distance_km
        ]

        recommendations = []

        for gym in candidates:
            specialties = [
                str(item)
                for item in gym.get("specialties", [])
            ]

            goal_match = any(
                goal_keyword in " ".join(specialties).lower()
                for goal_keyword in self._goal_keywords(goal)
            )

            rating = float(gym.get("rating", 0.0))
            distance = float(gym.get("distance_km", 999))

            score = rating

            if goal_match:
                score += 2.0

            score -= distance * 0.1

            reason = self._build_reason(
                goal_match=goal_match,
                distance=distance,
            )

            recommendations.append(
                (
                    score,
                    GymRecommendation(
                        name=str(gym.get("name", "Unnamed Gym")),
                        distance_km=round(distance, 2),
                        rating=round(rating, 2),
                        specialties=specialties,
                        reason=reason,
                    ),
                )
            )

        recommendations.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            recommendation
            for _, recommendation in recommendations
        ]

    @staticmethod
    def _goal_keywords(goal: str) -> list[str]:
        if "weight" in goal:
            return ["weight", "cardio", "fitness"]

        if "muscle" in goal:
            return ["muscle", "strength", "weights"]

        if "strength" in goal:
            return ["strength", "weights"]

        if "endurance" in goal:
            return ["endurance", "cardio", "running"]

        return ["fitness", "general"]

    @staticmethod
    def _build_reason(
        goal_match: bool,
        distance: float,
    ) -> str:
        if goal_match:
            return (
                "This gym matches your fitness goal "
                f"and is {distance:.1f} km away."
            )

        return (
            f"This gym is a nearby option at "
            f"{distance:.1f} km."
        )