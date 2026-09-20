from pydantic import BaseModel, Field


class RepetitionPerformanceResponse(BaseModel):
    """
    Performance information for one completed repetition.
    """

    repetition_number: int = Field(
        ge=1
    )

    overall_score: float = Field(
        ge=0.0,
        le=100.0
    )

    depth_score: float = Field(
        ge=0.0,
        le=100.0
    )

    posture_score: float = Field(
        ge=0.0,
        le=100.0
    )

    control_score: float = Field(
        ge=0.0,
        le=100.0
    )

    rating: str


class PerformanceReportResponse(BaseModel):
    """
    API response representing the complete
    performance report for a workout session.
    """

    exercise: str

    total_repetitions: int = Field(
        ge=0
    )

    performance_score: float = Field(
        ge=0.0,
        le=100.0
    )

    best_frame_score: float = Field(
        ge=0.0,
        le=100.0
    )

    worst_frame_score: float = Field(
        ge=0.0,
        le=100.0
    )

    depth_score: float = Field(
        ge=0.0,
        le=100.0
    )

    posture_score: float = Field(
        ge=0.0,
        le=100.0
    )

    control_score: float = Field(
        ge=0.0,
        le=100.0
    )

    average_repetition_score: float = Field(
        ge=0.0,
        le=100.0
    )

    best_repetition_score: float = Field(
        ge=0.0,
        le=100.0
    )

    worst_repetition_score: float = Field(
        ge=0.0,
        le=100.0
    )

    rating: str

    warnings: list[str]

    repetition_scores: list[
        RepetitionPerformanceResponse
    ]
class SavedPerformanceResponse(BaseModel):
    """Performance report together with the saved workout."""

    workout: dict
    performance: PerformanceReportResponse