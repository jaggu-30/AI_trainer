from pydantic import BaseModel, Field


class PoseLandmarkInput(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )

    x: float

    y: float

    z: float

    visibility: float = Field(
        ge=0.0,
        le=1.0,
    )


class GymTrainerFrameRequest(BaseModel):
    """
    Request containing exercise information and
    pose landmarks detected from a frame.
    """

    exercise: str = Field(
        default="squat",
        min_length=1,
        max_length=50,
    )

    landmarks: list[PoseLandmarkInput] = Field(
        min_length=1,
    )


class GymTrainerFrameResponse(BaseModel):
    """
    Result returned after analyzing one frame.
    """

    exercise: str

    knee_angle: float

    phase: str

    repetitions: int

    depth_score: float

    posture_score: float

    control_score: float

    form_score: float

    rating: str

    feedback: list[str]


class LiveTrainerSessionResponse(BaseModel):
    """A private in-memory session for a live camera workout."""

    session_id: str
    exercise: str
    expires_in_seconds: int = Field(
        gt=0,
    )


class LiveTrainerLandmark(BaseModel):
    """A normalized pose point returned only for the active camera frame."""

    x: float
    y: float
    visibility: float = Field(
        ge=0.0,
        le=1.0,
    )


class LiveTrainerFrameResponse(BaseModel):
    """Live pose result for one camera image. Camera images are not stored."""

    session_id: str
    pose_detected: bool
    message: str
    analysis: GymTrainerFrameResponse | None = None
    landmarks: list[LiveTrainerLandmark] | None = None
