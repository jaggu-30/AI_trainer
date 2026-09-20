from dataclasses import dataclass

from ai.recommender.challenge import (
    ChallengeRecommender,
    FitnessChallenge,
)
from ai.recommender.gym import (
    GymRecommendation,
    GymRecommender,
)
from ai.recommender.workout import (
    WorkoutProgramRecommendation,
    WorkoutProgramRecommender,
)
from app.models.user import User


@dataclass(frozen=True)
class RecommendationBundle:
    gyms: list[GymRecommendation]
    workouts: list[WorkoutProgramRecommendation]
    challenges: list[FitnessChallenge]


class RecommenderService:
    """Unified recommendation service."""

    def __init__(self) -> None:
        self.gym_recommender = GymRecommender()
        self.workout_recommender = WorkoutProgramRecommender()
        self.challenge_recommender = ChallengeRecommender()

    def recommend(
        self,
        user: User,
        gyms: list[dict],
        max_distance_km: float = 10.0,
    ) -> RecommendationBundle:
        gyms_result = self.gym_recommender.recommend(
            gyms=gyms,
            fitness_goal=user.fitness_goal,
            max_distance_km=max_distance_km,
        )

        workouts = self.workout_recommender.recommend(
            fitness_goal=user.fitness_goal,
        )

        challenges = self.challenge_recommender.recommend(
            fitness_goal=user.fitness_goal,
        )

        return RecommendationBundle(
            gyms=gyms_result,
            workouts=workouts,
            challenges=challenges,
        )