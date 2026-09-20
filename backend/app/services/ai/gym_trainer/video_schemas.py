from typing import Any

from pydantic import BaseModel, Field


class VideoFrameAnalysisResponse(BaseModel):
    frame_number: int = Field(
        ge=0,
    )

    timestamp_seconds: float = Field(
        ge=0.0,
    )

    analysis: Any


class GymTrainerVideoAnalysisResponse(BaseModel):
    exercise: str

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

    results: list[VideoFrameAnalysisResponse]