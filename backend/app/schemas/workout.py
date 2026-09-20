from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkoutSessionResponse(BaseModel):
    """Return a saved workout session to the authenticated user."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    exercise: str
    total_repetitions: int = Field(ge=0)
    performance_score: float = Field(ge=0, le=100)
    best_frame_score: float = Field(ge=0, le=100)
    worst_frame_score: float = Field(ge=0, le=100)
    depth_score: float = Field(ge=0, le=100)
    posture_score: float = Field(ge=0, le=100)
    control_score: float = Field(ge=0, le=100)
    average_repetition_score: float = Field(ge=0, le=100)
    best_repetition_score: float = Field(ge=0, le=100)
    worst_repetition_score: float = Field(ge=0, le=100)
    rating: str
    warnings: str | None = None
    started_at: datetime
    completed_at: datetime


class WorkoutHistoryResponse(BaseModel):
    """Return paginated workout history."""

    items: list[WorkoutSessionResponse]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)


class WorkoutSummaryResponse(BaseModel):
    """Return aggregate fitness statistics for the authenticated user."""

    total_workouts: int = Field(ge=0)
    total_repetitions: int = Field(ge=0)
    average_performance_score: float = Field(
        ge=0,
        le=100,
    )
    best_performance_score: float = Field(
        ge=0,
        le=100,
    )
    average_depth_score: float = Field(
        ge=0,
        le=100,
    )
    average_posture_score: float = Field(
        ge=0,
        le=100,
    )
    average_control_score: float = Field(
        ge=0,
        le=100,
    )
