from dataclasses import dataclass, field
from typing import Any

from app.services.ai.gym_trainer.frame_processor import (
    GymTrainerFrameProcessor,
)
from app.services.ai.gym_trainer.service import (
    GymTrainerService,
)
from app.services.ai.gym_trainer.video_processor import (
    GymTrainerVideoProcessor,
)


@dataclass
class VideoAnalysisResult:
    total_frames: int
    processed_frames: int
    detected_frames: int
    results: list[dict[str, Any]] = field(
        default_factory=list
    )


class GymTrainerVideoAnalysisService:
    """
    Connects video processing, pose detection,
    and gym trainer analysis.
    """

    def __init__(
        self,
        video_path: str,
    ):
        self.video_processor = (
            GymTrainerVideoProcessor(
                video_path=video_path
            )
        )

        self.frame_processor = (
            GymTrainerFrameProcessor()
        )

        self.trainer_service = (
            GymTrainerService()
        )

    def analyze(
        self,
        exercise: str = "squat",
    ) -> VideoAnalysisResult:

        results: list[dict[str, Any]] = []

        total_frames = 0
        processed_frames = 0
        detected_frames = 0

        def process_frame(video_frame):
            nonlocal total_frames
            nonlocal processed_frames
            nonlocal detected_frames

            total_frames += 1

            landmarks = (
                self.frame_processor.process_frame(
                    video_frame.image
                )
            )

            processed_frames += 1

            if not landmarks:
                return

            detected_frames += 1

            analysis = (
                self.trainer_service.process(
                    exercise=exercise,
                    landmarks=landmarks,
                )
            )

            if analysis is None:
                return

            results.append(
                {
                    "frame_number": (
                        video_frame.frame_number
                    ),
                    "timestamp_seconds": round(
                        video_frame.timestamp_seconds,
                        3,
                    ),
                    "analysis": analysis,
                }
            )

        try:
            self.video_processor.process(
                process_frame
            )

            return VideoAnalysisResult(
                total_frames=total_frames,
                processed_frames=processed_frames,
                detected_frames=detected_frames,
                results=results,
            )

        finally:
            self.frame_processor.close()

    def close(self):
        self.frame_processor.close()