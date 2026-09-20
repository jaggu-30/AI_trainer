from types import SimpleNamespace

from ai.recommender.challenge import (
    ChallengeRecommender,
)
from ai.recommender.gym import (
    GymRecommender,
)
from ai.recommender.workout import (
    WorkoutProgramRecommender,
)
from app.services.ai.recommender_service import (
    RecommenderService,
)


def test_weight_loss_challenge_is_ranked_first():
    recommender = ChallengeRecommender()

    recommendations = recommender.recommend(
        fitness_goal="weight_loss",
    )

    assert len(recommendations) == 3

    assert (
        recommendations[0].name
        == "21-Day Weight Loss Challenge"
    )

    assert (
        recommendations[0].goal
        == "weight_loss"
    )

    assert (
        "weight_loss"
        in recommendations[0].reason
    )


def test_goal_alias_for_muscle_gain():
    recommender = ChallengeRecommender()

    recommendations = recommender.recommend(
        fitness_goal="muscle",
    )

    assert (
        recommendations[0].name
        == "14-Day Muscle Builder Challenge"
    )

    assert (
        recommendations[0].goal
        == "muscle_gain"
    )


def test_challenge_limit_is_respected():
    recommender = ChallengeRecommender()

    recommendations = recommender.recommend(
        fitness_goal="strength",
        limit=2,
    )

    assert len(recommendations) == 2


def test_weight_loss_workout_is_ranked_first():
    recommender = WorkoutProgramRecommender()

    recommendations = recommender.recommend(
        fitness_goal="weight_loss",
    )

    assert len(recommendations) == 3

    assert (
        recommendations[0].name
        == "Weight Loss & Conditioning"
    )

    assert (
        recommendations[0].goal
        == "weight_loss"
    )


def test_workout_goal_alias():
    recommender = WorkoutProgramRecommender()

    recommendations = recommender.recommend(
        fitness_goal="strength training",
    )

    assert (
        recommendations[0].name
        == "Beginner Strength Builder"
    )

    assert (
        recommendations[0].goal
        == "strength"
    )


def test_workout_limit_is_respected():
    recommender = WorkoutProgramRecommender()

    recommendations = recommender.recommend(
        fitness_goal="endurance",
        limit=1,
    )

    assert len(recommendations) == 1

    assert (
        recommendations[0].name
        == "Endurance Builder"
    )


def test_gym_distance_filter():
    recommender = GymRecommender()

    gyms = [
        {
            "name": "Nearby Gym",
            "distance_km": 3,
            "rating": 4.5,
            "specialties": [
                "weight loss",
                "cardio",
            ],
        },
        {
            "name": "Far Gym",
            "distance_km": 15,
            "rating": 5.0,
            "specialties": [
                "weight loss",
            ],
        },
    ]

    recommendations = recommender.recommend(
        gyms=gyms,
        fitness_goal="weight_loss",
        max_distance_km=10,
    )

    assert len(recommendations) == 1
    assert (
        recommendations[0].name
        == "Nearby Gym"
    )


def test_gym_goal_matching_affects_ranking():
    recommender = GymRecommender()

    gyms = [
        {
            "name": "General Gym",
            "distance_km": 2,
            "rating": 4.9,
            "specialties": [
                "general fitness",
            ],
        },
        {
            "name": "Strength Gym",
            "distance_km": 4,
            "rating": 4.2,
            "specialties": [
                "strength",
                "weights",
            ],
        },
    ]

    recommendations = recommender.recommend(
        gyms=gyms,
        fitness_goal="strength",
        max_distance_km=10,
    )

    assert (
        recommendations[0].name
        == "Strength Gym"
    )


def test_gym_recommendation_is_sorted_by_score():
    recommender = GymRecommender()

    gyms = [
        {
            "name": "Excellent Gym",
            "distance_km": 2,
            "rating": 4.8,
            "specialties": [
                "fitness",
            ],
        },
        {
            "name": "Goal Gym",
            "distance_km": 3,
            "rating": 4.0,
            "specialties": [
                "strength",
            ],
        },
    ]

    recommendations = recommender.recommend(
        gyms=gyms,
        fitness_goal="strength",
        max_distance_km=10,
    )

    assert (
        recommendations[0].name
        == "Goal Gym"
    )


def test_unified_recommender_service():
    service = RecommenderService()

    user = SimpleNamespace(
        fitness_goal="weight_loss"
    )

    gyms = [
        {
            "name": "Weight Loss Gym",
            "distance_km": 2,
            "rating": 4.5,
            "specialties": [
                "weight loss",
                "cardio",
            ],
        },
        {
            "name": "General Gym",
            "distance_km": 5,
            "rating": 4.0,
            "specialties": [
                "fitness",
            ],
        },
    ]

    result = service.recommend(
        user=user,
        gyms=gyms,
        max_distance_km=10,
    )

    assert len(result.gyms) == 2
    assert len(result.workouts) == 3
    assert len(result.challenges) == 3

    assert (
        result.gyms[0].name
        == "Weight Loss Gym"
    )

    assert (
        result.workouts[0].goal
        == "weight_loss"
    )

    assert (
        result.challenges[0].goal
        == "weight_loss"
    )


def test_unified_recommender_handles_no_gyms():
    service = RecommenderService()

    user = SimpleNamespace(
        fitness_goal="strength"
    )

    result = service.recommend(
        user=user,
        gyms=[],
        max_distance_km=10,
    )

    assert result.gyms == []
    assert len(result.workouts) == 3
    assert len(result.challenges) == 3