from pydantic import BaseModel, Field


class GymCandidateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200,
    )

    distance_km: float = Field(
        ge=0,
    )

    rating: float = Field(
        ge=0,
        le=5,
    )

    specialties: list[str] = Field(
        default_factory=list,
    )


class RecommendationRequest(BaseModel):
    gyms: list[GymCandidateRequest] = Field(
        default_factory=list,
    )

    max_distance_km: float = Field(
        default=10.0,
        ge=0,
        le=100,
    )


class GymRecommendationResponse(BaseModel):
    name: str
    distance_km: float
    rating: float
    specialties: list[str]
    reason: str


class WorkoutRecommendationResponse(BaseModel):
    name: str
    goal: str
    difficulty: str
    duration_minutes: int = Field(
        ge=0,
    )
    reason: str


class ChallengeRecommendationResponse(BaseModel):
    name: str
    goal: str
    duration_days: int = Field(
        gt=0,
    )
    difficulty: str
    reason: str


class RecommendationResponse(BaseModel):
    gyms: list[GymRecommendationResponse]
    workouts: list[
        WorkoutRecommendationResponse
    ]
    challenges: list[
        ChallengeRecommendationResponse
    ]