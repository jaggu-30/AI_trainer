from app.schemas.workout import WorkoutSessionResponse
from app.services.ai.gym_trainer.performance_schemas import (
    PerformanceReportResponse,
)


class SavedWorkoutPerformanceResponse(
    PerformanceReportResponse
):
    """Return AI performance together with the saved workout."""

    workout: WorkoutSessionResponse