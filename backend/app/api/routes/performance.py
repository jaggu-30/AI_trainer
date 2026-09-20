import shutil
import tempfile
from datetime import date
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.performance import WeeklyPerformanceResponse
from app.schemas.video_performance import (
    VideoPerformanceResponse,
)
from app.schemas.workout_performance import (
    SavedWorkoutPerformanceResponse,
)
from app.services.ai.gym_trainer.performance_request_schemas import (
    GymTrainerPerformanceRequest,
)
from app.services.ai.gym_trainer.performance_service import (
    GymTrainerPerformanceService,
)
from app.services.ai.gym_trainer.video_performance_service import (
    GymTrainerVideoPerformanceService,
)
from app.services.ai.weekly_performance_service import (
    WeeklyPerformanceService,
)
from app.services.workout_persistence import (
    WorkoutPersistenceService,
)


router = APIRouter(
    prefix="/api/v1/performance",
    tags=["performance"],
)


performance_service = GymTrainerPerformanceService()
persistence_service = WorkoutPersistenceService()


ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
}


@router.post(
    "/session",
    response_model=SavedWorkoutPerformanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_and_save_session(
    request: GymTrainerPerformanceRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Analyze a complete workout session and save
    the resulting performance report.
    """

    try:
        report = performance_service.analyze(
            exercise=request.exercise,
            frames=request.frames,
        )

        workout = persistence_service.save_report(
            db=db,
            user=current_user,
            report=report,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error

    return SavedWorkoutPerformanceResponse(
        exercise=report.exercise,
        total_repetitions=report.total_repetitions,
        performance_score=report.performance_score,
        best_frame_score=report.best_frame_score,
        worst_frame_score=report.worst_frame_score,
        depth_score=report.depth_score,
        posture_score=report.posture_score,
        control_score=report.control_score,
        average_repetition_score=(
            report.average_repetition_score
        ),
        best_repetition_score=(
            report.best_repetition_score
        ),
        worst_repetition_score=(
            report.worst_repetition_score
        ),
        rating=report.rating,
        warnings=report.warnings,
        repetition_scores=[
            {
                "repetition_number": (
                    item.repetition_number
                ),
                "overall_score": (
                    item.overall_score
                ),
                "depth_score": (
                    item.depth_score
                ),
                "posture_score": (
                    item.posture_score
                ),
                "control_score": (
                    item.control_score
                ),
                "rating": item.rating,
            }
            for item in report.repetition_scores
        ],
        workout=workout,
    )


@router.post(
    "/video",
    response_model=VideoPerformanceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def analyze_and_save_video(
    video: UploadFile = File(...),
    exercise: str = "squat",
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Analyze a recorded workout video,
    generate a performance report,
    and save the completed workout.
    """

    if not video.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A video file is required.",
        )

    extension = Path(
        video.filename
    ).suffix.lower()

    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported video format. "
                "Use MP4, MOV, AVI, or MKV."
            ),
        )

    normalized_exercise = (
        exercise.strip().lower()
    )

    if not normalized_exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise cannot be empty.",
        )

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = (
                Path(temp_dir)
                / f"workout{extension}"
            )

            with temp_path.open(
                "wb"
            ) as output_file:
                shutil.copyfileobj(
                    video.file,
                    output_file,
                )

            service = (
                GymTrainerVideoPerformanceService(
                    video_path=str(temp_path),
                )
            )

            try:
                result = service.analyze(
                    exercise=normalized_exercise,
                )
            finally:
                service.close()

        if result.performance is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                ),
                detail=(
                    "No valid human pose was detected "
                    "in the uploaded workout video."
                ),
            )

        workout = (
            persistence_service.save_report(
                db=db,
                user=current_user,
                report=result.performance,
            )
        )

        performance = result.performance

        return VideoPerformanceResponse(
            exercise=performance.exercise,
            video={
                "total_frames": (
                    result.total_frames
                ),
                "processed_frames": (
                    result.processed_frames
                ),
                "detected_frames": (
                    result.detected_frames
                ),
                "detection_rate": (
                    result.detection_rate
                ),
            },
            total_repetitions=(
                performance.total_repetitions
            ),
            performance_score=(
                performance.performance_score
            ),
            best_frame_score=(
                performance.best_frame_score
            ),
            worst_frame_score=(
                performance.worst_frame_score
            ),
            depth_score=performance.depth_score,
            posture_score=performance.posture_score,
            control_score=performance.control_score,
            average_repetition_score=(
                performance.average_repetition_score
            ),
            best_repetition_score=(
                performance.best_repetition_score
            ),
            worst_repetition_score=(
                performance.worst_repetition_score
            ),
            rating=performance.rating,
            warnings=performance.warnings,
            repetition_scores=[
                {
                    "repetition_number": (
                        item.repetition_number
                    ),
                    "overall_score": (
                        item.overall_score
                    ),
                    "depth_score": (
                        item.depth_score
                    ),
                    "posture_score": (
                        item.posture_score
                    ),
                    "control_score": (
                        item.control_score
                    ),
                    "rating": item.rating,
                }
                for item in performance.repetition_scores
            ],
            workout=workout,
        )

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error

    except RuntimeError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail=str(error),
        ) from error


@router.get(
    "/weekly",
    response_model=WeeklyPerformanceResponse,
)
def weekly_performance(
    week_start: date | None = None,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Return weekly workout performance.
    """

    if (
        week_start is not None
        and week_start.weekday() != 0
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail="week_start must be a Monday.",
        )

    service = WeeklyPerformanceService()

    report = service.generate_report(
        db=db,
        user=current_user,
        week_start=week_start,
    )

    return WeeklyPerformanceResponse(
        week_start=report.week_start,
        week_end=report.week_end,
        workout_count=report.workout_count,
        total_repetitions=report.total_repetitions,
        average_performance_score=(
            report.average_performance_score
        ),
        best_performance_score=(
            report.best_performance_score
        ),
        worst_performance_score=(
            report.worst_performance_score
        ),
        average_depth_score=(
            report.average_depth_score
        ),
        average_posture_score=(
            report.average_posture_score
        ),
        average_control_score=(
            report.average_control_score
        ),
        performance_trend=report.performance_trend,
        summary=report.summary,
    )