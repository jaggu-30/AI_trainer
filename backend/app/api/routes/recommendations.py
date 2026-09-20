from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.recommendation import (
    ChallengeRecommendationResponse,
    GymRecommendationResponse,
    RecommendationRequest,
    RecommendationResponse,
    WorkoutRecommendationResponse,
)
from app.services.ai.recommender_service import (
    RecommenderService,
)


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


recommender_service = RecommenderService()


@router.post(
    "",
    response_model=RecommendationResponse,
)
def get_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate personalized gym, workout-program,
    and fitness-challenge recommendations.
    """

    gyms = [
        {
            "name": gym.name,
            "distance_km": gym.distance_km,
            "rating": gym.rating,
            "specialties": gym.specialties,
        }
        for gym in request.gyms
    ]

    recommendations = (
        recommender_service.recommend(
            user=current_user,
            gyms=gyms,
            max_distance_km=(
                request.max_distance_km
            ),
        )
    )

    return RecommendationResponse(
        gyms=[
            GymRecommendationResponse(
                name=gym.name,
                distance_km=gym.distance_km,
                rating=gym.rating,
                specialties=gym.specialties,
                reason=gym.reason,
            )
            for gym in recommendations.gyms
        ],
        workouts=[
            WorkoutRecommendationResponse(
                name=workout.name,
                goal=workout.goal,
                difficulty=workout.difficulty,
                duration_minutes=(
                    workout.duration_minutes
                ),
                reason=workout.reason,
            )
            for workout in recommendations.workouts
        ],
        challenges=[
            ChallengeRecommendationResponse(
                name=challenge.name,
                goal=challenge.goal,
                duration_days=(
                    challenge.duration_days
                ),
                difficulty=challenge.difficulty,
                reason=challenge.reason,
            )
            for challenge in recommendations.challenges
        ],
    )