from pydantic import BaseModel, Field

from app.schemas.workout import WorkoutSessionResponse
from app.services.ai.gym_trainer.performance_schemas import (
    RepetitionPerformanceResponse,
)


class VideoPerformanceMetadataResponse(BaseModel):
    total_frames: int = Field(
        ge=0,
    )

    processed_frames: int = Field(
        ge=0,
    )

    detected_frames: int = Field(
        ge=0,
    )

    detection_rate: float = Field(
        ge=0.0,
        le=1.0,
    )


class VideoPerformanceResponse(BaseModel):
    exercise: str

    video: VideoPerformanceMetadataResponse

    total_repetitions: int = Field(
        ge=0,
    )

    performance_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    best_frame_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    worst_frame_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    depth_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    posture_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    control_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    average_repetition_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    best_repetition_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    worst_repetition_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    rating: str

    warnings: list[str]

    repetition_scores: list[
        RepetitionPerformanceResponse
    ]

    workout: WorkoutSessionResponse