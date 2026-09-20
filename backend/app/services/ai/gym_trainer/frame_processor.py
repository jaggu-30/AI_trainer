from pathlib import Path

import cv2
import numpy as np

from ai.gym_trainer.pose import PoseDetector, PoseLandmark


class GymTrainerFrameProcessor:
    """
    Converts an image frame into pose landmarks.

    This class is responsible only for computer vision.
    Exercise analysis remains inside GymTrainerService.
    """

    def __init__(
        self,
        model_path: str | None = None,
    ):
        if model_path is None:
            project_root = Path(__file__).resolve().parents[5]

            model_path = (
                project_root
                / "ai"
                / "models"
                / "gym_trainer"
                / "pose_landmarker_full.task"
            )

        self.model_path = str(model_path)

        self.pose_detector = PoseDetector(
            model_path=self.model_path,
        )

    def process_frame(
        self,
        frame: np.ndarray,
    ) -> list[PoseLandmark]:
        """
        Detect pose landmarks from a BGR OpenCV frame.
        """

        if frame is None or frame.size == 0:
            return []

        return self.pose_detector.detect(frame)

    def process_image_bytes(
        self,
        image_bytes: bytes,
    ) -> list[PoseLandmark]:
        """
        Decode image bytes and detect pose landmarks.
        """

        if not image_bytes:
            return []

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR,
        )

        if frame is None:
            return []

        return self.process_frame(frame)

    def close(self):
        self.pose_detector.close()