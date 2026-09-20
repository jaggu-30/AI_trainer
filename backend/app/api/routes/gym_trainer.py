import shutil
import tempfile
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from ai.gym_trainer.pose import PoseLandmark

from app.api.dependencies import get_current_user
from app.services.ai.gym_trainer.schemas import (
    GymTrainerFrameRequest,
    GymTrainerFrameResponse,
    LiveTrainerFrameResponse,
    LiveTrainerSessionResponse,
)
from app.services.ai.gym_trainer.live_session import (
    SESSION_IDLE_SECONDS,
    LiveTrainerSessionManager,
)
from app.services.ai.gym_trainer.service import (
    GymTrainerService,
)
from app.services.ai.gym_trainer.video_analysis import (
    GymTrainerVideoAnalysisService,
)
from app.services.ai.gym_trainer.video_schemas import (
    GymTrainerVideoAnalysisResponse,
    VideoFrameAnalysisResponse,
)


router = APIRouter(
    prefix="/api/v1/gym-trainer",
    tags=["Gym Trainer"],
)


trainer_service = GymTrainerService()
live_session_manager = LiveTrainerSessionManager()


MAX_LIVE_FRAME_BYTES = 2 * 1024 * 1024
ALLOWED_LIVE_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
}


@router.get("/health")
def gym_trainer_health():
    return {
        "status": "healthy",
        "service": "gym-trainer",
    }


@router.post(
    "/live/start",
    response_model=LiveTrainerSessionResponse,
)
def start_live_trainer(
    current_user=Depends(get_current_user),
):
    """Start a private, short-lived real-time squat coaching session."""

    session_id = live_session_manager.start_session(
        user_id=current_user.id,
    )

    return LiveTrainerSessionResponse(
        session_id=session_id,
        exercise="squat",
        expires_in_seconds=SESSION_IDLE_SECONDS,
    )


@router.post(
    "/live/frame",
    response_model=LiveTrainerFrameResponse,
)
async def analyze_live_trainer_frame(
    session_id: str = Form(...),
    image: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    """Analyze one camera still without writing the image to disk."""

    if image.content_type not in ALLOWED_LIVE_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Use a JPEG, PNG, or WebP camera frame.",
        )

    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A camera frame is required.",
        )

    if len(image_bytes) > MAX_LIVE_FRAME_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Camera frame is too large. Use the standard camera quality.",
        )

    try:
        return live_session_manager.process_frame(
            session_id=session_id,
            user_id=current_user.id,
            image_bytes=image_bytes,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Live pose detection is not available right now.",
        ) from error


@router.delete(
    "/live/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def stop_live_trainer(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """End the live session and discard its in-memory rep-counter state."""

    stopped = live_session_manager.stop_session(
        session_id=session_id,
        user_id=current_user.id,
    )

    if not stopped:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live workout session was not found.",
        )


@router.post(
    "/frame",
    response_model=GymTrainerFrameResponse,
)
def analyze_frame(
    request: GymTrainerFrameRequest,
):
    try:
        landmarks = [
            PoseLandmark(
                name=landmark.name,
                x=landmark.x,
                y=landmark.y,
                z=landmark.z,
                visibility=landmark.visibility,
            )
            for landmark in request.landmarks
        ]

        result = trainer_service.process(
            exercise=request.exercise,
            landmarks=landmarks,
        )

        if result is None:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Unable to analyze the supplied "
                    "pose landmarks."
                ),
            )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.post(
    "/video",
    response_model=GymTrainerVideoAnalysisResponse,
)
async def analyze_video(
    video: UploadFile = File(...),
    exercise: str = "squat",
):
    """
    Analyze a recorded workout video.

    The uploaded video is stored temporarily,
    analyzed frame by frame, and deleted after processing.
    """

    if not video.filename:
        raise HTTPException(
            status_code=400,
            detail="A video file is required.",
        )

    extension = Path(
        video.filename
    ).suffix.lower()

    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
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
            status_code=400,
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

            service = GymTrainerVideoAnalysisService(
                video_path=str(temp_path),
            )

            try:
                result = service.analyze(
                    exercise=normalized_exercise,
                )
            finally:
                service.close()

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except RuntimeError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Video analysis failed."
            ),
        ) from error

    detection_rate = (
        result.detected_frames
        / result.processed_frames
        if result.processed_frames > 0
        else 0.0
    )

    return GymTrainerVideoAnalysisResponse(
        exercise=normalized_exercise,
        total_frames=result.total_frames,
        processed_frames=result.processed_frames,
        detected_frames=result.detected_frames,
        detection_rate=round(
            detection_rate,
            4,
        ),
        results=[
            VideoFrameAnalysisResponse(
                frame_number=item[
                    "frame_number"
                ],
                timestamp_seconds=item[
                    "timestamp_seconds"
                ],
                analysis=item[
                    "analysis"
                ],
            )
            for item in result.results
        ],
    )
