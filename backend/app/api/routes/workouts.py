from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.workout import WorkoutSession
from app.schemas.workout import (
    WorkoutHistoryResponse,
    WorkoutSessionResponse,
    WorkoutSummaryResponse,
)


router = APIRouter(
    prefix="/api/v1/workouts",
    tags=["Workouts"],
)


@router.get(
    "/summary",
    response_model=WorkoutSummaryResponse,
)
def get_workout_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return aggregate workout statistics for the
    authenticated user.
    """

    statement = select(
        func.count(WorkoutSession.id),
        func.coalesce(
            func.sum(
                WorkoutSession.total_repetitions
            ),
            0,
        ),
        func.coalesce(
            func.avg(
                WorkoutSession.performance_score
            ),
            0.0,
        ),
        func.coalesce(
            func.max(
                WorkoutSession.performance_score
            ),
            0.0,
        ),
        func.coalesce(
            func.avg(
                WorkoutSession.depth_score
            ),
            0.0,
        ),
        func.coalesce(
            func.avg(
                WorkoutSession.posture_score
            ),
            0.0,
        ),
        func.coalesce(
            func.avg(
                WorkoutSession.control_score
            ),
            0.0,
        ),
    ).where(
        WorkoutSession.user_id == current_user.id
    )

    result = db.execute(statement).one()

    (
        total_workouts,
        total_repetitions,
        average_performance_score,
        best_performance_score,
        average_depth_score,
        average_posture_score,
        average_control_score,
    ) = result

    return WorkoutSummaryResponse(
        total_workouts=int(total_workouts),
        total_repetitions=int(total_repetitions),
        average_performance_score=round(
            float(average_performance_score),
            2,
        ),
        best_performance_score=round(
            float(best_performance_score),
            2,
        ),
        average_depth_score=round(
            float(average_depth_score),
            2,
        ),
        average_posture_score=round(
            float(average_posture_score),
            2,
        ),
        average_control_score=round(
            float(average_control_score),
            2,
        ),
    )


@router.get(
    "",
    response_model=WorkoutHistoryResponse,
)
def get_workout_history(
    exercise: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return paginated workout history for the
    authenticated user.
    """

    filters = [
        WorkoutSession.user_id == current_user.id
    ]

    if exercise is not None:
        filters.append(
            WorkoutSession.exercise
            == exercise.strip().lower()
        )

    total_statement = select(
        func.count(WorkoutSession.id)
    ).where(*filters)

    total = db.scalar(total_statement) or 0

    history_statement = (
        select(WorkoutSession)
        .where(*filters)
        .order_by(
            WorkoutSession.completed_at.desc(),
            WorkoutSession.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    )

    items = list(
        db.scalars(history_statement).all()
    )

    return WorkoutHistoryResponse(
        items=[
            WorkoutSessionResponse.model_validate(
                workout
            )
            for workout in items
        ],
        total=int(total),
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{workout_id}",
    response_model=WorkoutSessionResponse,
)
def get_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return one workout session belonging to the
    authenticated user.
    """

    statement = select(WorkoutSession).where(
        WorkoutSession.id == workout_id,
        WorkoutSession.user_id == current_user.id,
    )

    workout = db.scalar(statement)

    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout session not found.",
        )

    return workout
