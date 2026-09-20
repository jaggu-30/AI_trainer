"""Short-lived, private state for the live camera trainer."""

from dataclasses import dataclass, field
from threading import Lock
from time import monotonic
from uuid import uuid4

from app.services.ai.gym_trainer.frame_processor import (
    GymTrainerFrameProcessor,
)
from app.services.ai.gym_trainer.service import (
    GymTrainerService,
)


SESSION_IDLE_SECONDS = 20 * 60


@dataclass
class LiveTrainerSession:
    """One user's in-memory repetition counter and form state."""

    user_id: int
    trainer_service: GymTrainerService = field(
        default_factory=GymTrainerService,
    )
    last_seen: float = field(
        default_factory=monotonic,
    )
    lock: Lock = field(
        default_factory=Lock,
    )


class LiveTrainerSessionManager:
    """
    Processes stills from a browser camera without persisting camera frames.

    Pose detection is shared and serialized because the MediaPipe IMAGE
    landmarker is reused, while each user keeps an independent rep counter.
    """

    def __init__(
        self,
        session_idle_seconds: int = SESSION_IDLE_SECONDS,
    ):
        self.session_idle_seconds = session_idle_seconds
        self._sessions: dict[str, LiveTrainerSession] = {}
        self._sessions_lock = Lock()
        self._processor_lock = Lock()
        self._frame_processor: GymTrainerFrameProcessor | None = None

    def start_session(
        self,
        user_id: int,
    ) -> str:
        self._cleanup_expired_sessions()

        session_id = uuid4().hex

        with self._sessions_lock:
            self._sessions[session_id] = LiveTrainerSession(
                user_id=user_id,
            )

        return session_id

    def process_frame(
        self,
        *,
        session_id: str,
        user_id: int,
        image_bytes: bytes,
    ) -> dict:
        session = self._get_session(
            session_id=session_id,
            user_id=user_id,
        )

        with session.lock:
            with self._processor_lock:
                processor = self._get_frame_processor()
                landmarks = processor.process_image_bytes(
                    image_bytes,
                )

            session.last_seen = monotonic()

            if not landmarks:
                return {
                    "session_id": session_id,
                    "pose_detected": False,
                    "message": (
                        "Move back until your full body is visible "
                        "from the side."
                    ),
                    "analysis": None,
                    "landmarks": None,
                }

            live_landmarks = [
                {
                    "x": landmark.x,
                    "y": landmark.y,
                    "visibility": landmark.visibility,
                }
                for landmark in landmarks
            ]

            analysis = session.trainer_service.process(
                exercise="squat",
                landmarks=landmarks,
            )

            if analysis is None:
                return {
                    "session_id": session_id,
                    "pose_detected": True,
                    "message": (
                        "Keep your left shoulder, hip, knee, and ankle "
                        "visible to the camera."
                    ),
                    "analysis": None,
                    "landmarks": live_landmarks,
                }

            return {
                "session_id": session_id,
                "pose_detected": True,
                "message": "Live form analysis updated.",
                "analysis": analysis,
                "landmarks": live_landmarks,
            }

    def stop_session(
        self,
        *,
        session_id: str,
        user_id: int,
    ) -> bool:
        with self._sessions_lock:
            session = self._sessions.get(session_id)

            if session is None or session.user_id != user_id:
                return False

            del self._sessions[session_id]

        return True

    def close(self) -> None:
        with self._sessions_lock:
            self._sessions.clear()

        with self._processor_lock:
            if self._frame_processor is not None:
                self._frame_processor.close()
                self._frame_processor = None

    def _get_frame_processor(self) -> GymTrainerFrameProcessor:
        if self._frame_processor is None:
            self._frame_processor = GymTrainerFrameProcessor()

        return self._frame_processor

    def _get_session(
        self,
        *,
        session_id: str,
        user_id: int,
    ) -> LiveTrainerSession:
        self._cleanup_expired_sessions()

        with self._sessions_lock:
            session = self._sessions.get(session_id)

            if session is None or session.user_id != user_id:
                raise ValueError("Live workout session was not found.")

            return session

    def _cleanup_expired_sessions(self) -> None:
        expiry = monotonic() - self.session_idle_seconds

        with self._sessions_lock:
            expired = [
                session_id
                for session_id, session in self._sessions.items()
                if session.last_seen < expiry
            ]

            for session_id in expired:
                del self._sessions[session_id]
