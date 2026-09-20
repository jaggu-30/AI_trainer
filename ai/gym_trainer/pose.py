from dataclasses import dataclass

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks.python import vision


@dataclass
class PoseLandmark:
    name: str
    x: float
    y: float
    z: float
    visibility: float


class PoseDetector:
    def __init__(
        self,
        model_path: str = "../ai/models/gym_trainer/pose_landmarker_full.task",
        min_pose_detection_confidence: float = 0.5,
        min_pose_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        base_options = mp.tasks.BaseOptions(
            model_asset_path=model_path,
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_pose_detection_confidence=min_pose_detection_confidence,
            min_pose_presence_confidence=min_pose_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
            output_segmentation_masks=False,
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(
            options
        )

    def detect(self, frame: np.ndarray) -> list[PoseLandmark]:
        """
        Detect a human pose from an OpenCV BGR image.

        Returns up to 33 pose landmarks for the first detected person.
        """
        if frame is None or frame.size == 0:
            return []

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame,
        )

        result = self.landmarker.detect(mp_image)

        if not result.pose_landmarks:
            return []

        pose_landmarks = result.pose_landmarks[0]

        landmarks = []

        for index, landmark in enumerate(pose_landmarks):
            landmark_name = vision.PoseLandmark(index).name

            landmarks.append(
                PoseLandmark(
                    name=landmark_name,
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility,
                )
            )

        return landmarks

    def draw_landmarks(
        self,
        frame: np.ndarray,
        landmarks: list[PoseLandmark],
    ) -> np.ndarray:
        """
        Draw detected pose landmarks and skeleton connections.
        """
        output = frame.copy()

        if not landmarks:
            return output

        height, width = output.shape[:2]

        points: dict[str, tuple[int, int]] = {}

        for landmark in landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)

            # Ignore landmarks far outside the image.
            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            points[landmark.name] = (x, y)

            cv2.circle(
                output,
                (x, y),
                5,
                (0, 255, 0),
                -1,
            )

        connections = vision.PoseLandmarksConnections.POSE_LANDMARKS

        for connection in connections:
            start_name = vision.PoseLandmark(
                connection.start
            ).name

            end_name = vision.PoseLandmark(
                connection.end
            ).name

            if start_name not in points or end_name not in points:
                continue

            cv2.line(
                output,
                points[start_name],
                points[end_name],
                (0, 255, 0),
                2,
            )

        return output

    def close(self) -> None:
        self.landmarker.close()
