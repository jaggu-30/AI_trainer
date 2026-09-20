from pydantic import BaseModel, Field

from app.services.ai.gym_trainer.schemas import (
    PoseLandmarkInput,
)


class GymTrainerPerformanceRequest(BaseModel):
    """
    Request containing a complete sequence of pose frames
    for performance analysis.
    """

    exercise: str = Field(
        default="squat",
        min_length=1,
        max_length=50,
    )

    frames: list[list[PoseLandmarkInput]] = Field(
        min_length=1,
    )