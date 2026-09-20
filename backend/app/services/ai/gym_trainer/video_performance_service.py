from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

from ai.gym_trainer.performance_report import (
    PerformanceReport,
    PerformanceReportGenerator,
)
from ai.gym_trainer.session_analyzer import (
    SessionFrameResult,
    SquatSessionAnalyzer,
)

from app.services.ai.gym_trainer.frame_processor import (
    GymTrainerFrameProcessor,
)
from app.services.ai.gym_trainer.video_processor import (
    GymTrainerVideoProcessor,
)


@dataclass
class VideoPerformanceResult:
    """
    Complete performance analysis of a recorded workout video.
    """

    exercise: str
    total_frames: int
    processed_frames: int
    detected_frames: int
    detection_rate: float
    performance: PerformanceReport | None
    frame_results: list[dict[str, Any]] = field(
        default_factory=list
    )


class GymTrainerVideoPerformanceService:
    """
    Connects video processing, pose detection,
    session analysis, and performance reporting.

    The default production path reads video frames and
    uses MediaPipe through GymTrainerFrameProcessor.

    A custom landmark provider can be supplied for deterministic
    automated testing.
    """

    SUPPORTED_EXERCISES = {
        "squat",
    }

    def __init__(
        self,
        video_path: str | None = None,
        landmark_provider: Callable[
            [Any],
            list | None,
        ]
        | None = None,
    ):
        if video_path is None and landmark_provider is None:
            raise ValueError(
                "Either video_path or landmark_provider "
                "must be provided."
            )

        self.video_processor = (
            GymTrainerVideoProcessor(
                video_path=video_path,
            )
            if video_path is not None
            else None
        )

        self.frame_processor = (
            GymTrainerFrameProcessor()
            if landmark_provider is None
            else None
        )

        self.landmark_provider = landmark_provider

        self.session_analyzer = (
            SquatSessionAnalyzer()
        )

        self.report_generator = (
            PerformanceReportGenerator()
        )

    def analyze(
        self,
        exercise: str = "squat",
    ) -> VideoPerformanceResult:
        """
        Analyze a complete workout video or landmark stream
        and generate a session-level performance report.
        """

        normalized_exercise = exercise.strip().lower()

        if normalized_exercise not in self.SUPPORTED_EXERCISES:
            raise ValueError(
                f"Unsupported exercise: {exercise}"
            )

        if (
            self.video_processor is None
            and self.landmark_provider is None
        ):
            raise RuntimeError(
                "No video processor or landmark provider "
                "is available."
            )

        total_frames = 0
        processed_frames = 0
        detected_frames = 0

        frame_results: list[
            dict[str, Any]
        ] = []

        def process_landmarks(
            landmarks,
            frame_number: int,
            timestamp_seconds: float,
        ) -> None:
            nonlocal detected_frames

            if not landmarks:
                return

            detected_frames += 1

            frame_analysis = (
                self.session_analyzer.process_frame(
                    landmarks
                )
            )

            if frame_analysis is None:
                return

            frame_results.append(
                {
                    "frame_number": frame_number,
                    "timestamp_seconds": round(
                        timestamp_seconds,
                        3,
                    ),
                    "phase": frame_analysis.phase,
                    "repetitions": (
                        frame_analysis.repetitions
                    ),
                    "knee_angle": round(
                        frame_analysis.knee_angle,
                        2,
                    ),
                    "form_score": (
                        frame_analysis.score.overall_score
                    ),
                    "depth_score": (
                        frame_analysis.score.depth_score
                    ),
                    "posture_score": (
                        frame_analysis.score.posture_score
                    ),
                    "control_score": (
                        frame_analysis.score.control_score
                    ),
                    "rating": (
                        frame_analysis.score.rating
                    ),
                    "feedback": (
                        frame_analysis.feedback.messages
                    ),
                }
            )

        try:
            if self.video_processor is not None:

                def process_video_frame(
                    video_frame,
                ) -> None:
                    nonlocal total_frames
                    nonlocal processed_frames

                    total_frames += 1

                    landmarks = (
                        self.frame_processor.process_frame(
                            video_frame.image
                        )
                    )

                    processed_frames += 1

                    process_landmarks(
                        landmarks=landmarks,
                        frame_number=(
                            video_frame.frame_number
                        ),
                        timestamp_seconds=(
                            video_frame.timestamp_seconds
                        ),
                    )

                self.video_processor.process(
                    process_video_frame
                )

            else:
                frames: Iterator[Any] = (
                    self.landmark_provider(None)
                    if callable(self.landmark_provider)
                    else iter(())
                )

                for frame in frames:
                    total_frames += 1
                    processed_frames += 1

                    if hasattr(
                        frame,
                        "landmarks",
                    ):
                        landmarks = frame.landmarks
                        frame_number = frame.frame_number
                        timestamp_seconds = (
                            frame.timestamp_seconds
                        )

                    else:
                        landmarks = frame
                        frame_number = (
                            total_frames - 1
                        )
                        timestamp_seconds = 0.0

                    process_landmarks(
                        landmarks=landmarks,
                        frame_number=frame_number,
                        timestamp_seconds=(
                            timestamp_seconds
                        ),
                    )

            summary = (
                self.session_analyzer.summary()
            )

            performance = None

            if detected_frames > 0:
                performance = (
                    self.report_generator.generate(
                        summary=summary,
                        exercise=normalized_exercise,
                    )
                )

            detection_rate = (
                detected_frames
                / processed_frames
                if processed_frames > 0
                else 0.0
            )

            return VideoPerformanceResult(
                exercise=normalized_exercise,
                total_frames=total_frames,
                processed_frames=processed_frames,
                detected_frames=detected_frames,
                detection_rate=round(
                    detection_rate,
                    4,
                ),
                performance=performance,
                frame_results=frame_results,
            )

        finally:
            self.reset()

    def reset(self) -> None:
        """
        Reset session-analysis state without releasing
        the pose detector.
        """

        self.session_analyzer.reset()

    def close(self) -> None:
        """
        Release computer-vision resources when present.
        """

        if self.frame_processor is not None:
            self.frame_processor.close()