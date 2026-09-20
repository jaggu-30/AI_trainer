from fastapi import APIRouter, HTTPException

from app.services.ai.gym_trainer.schemas import (
    GymTrainerFrameRequest,
    GymTrainerFrameResponse,
)

router = APIRouter(
    prefix="/api/v1/gym-trainer",
    tags=["Gym Trainer"],
)


@router.get("/health")
def gym_trainer_health():
    """
    Health endpoint for the Gym Trainer service.
    """

    return {
        "status": "healthy",
        "service": "gym-trainer",
    }


@router.post(
    "/frame",
    response_model=GymTrainerFrameResponse,
)
def analyze_frame(
    request: GymTrainerFrameRequest,
):
    """
    Temporary stub endpoint.

    The real GymTrainerService will be connected
    in the next step.
    """

    if request.exercise.lower() != "squat":
        raise HTTPException(
            status_code=400,
            detail="Only squat is currently supported.",
        )

    return GymTrainerFrameResponse(
        exercise="squat",
        knee_angle=90.0,
        phase="descending",
        repetitions=0,
        depth_score=100.0,
        posture_score=80.0,
        control_score=86.93,
        form_score=90.08,
        rating="excellent",
        feedback=[
            "Good squat depth.",
            "Good torso posture.",
            "Movement appears stable.",
        ],
    )