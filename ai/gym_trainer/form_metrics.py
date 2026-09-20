from dataclasses import dataclass

from ai.gym_trainer.angle import calculate_angle
from ai.gym_trainer.pose import PoseLandmark


@dataclass
class SquatFormMetrics:
    """
    Geometric measurements extracted from one squat pose.
    """

    knee_angle: float
    hip_angle: float
    torso_angle: float
    shoulder_hip_offset: float


class SquatFormMetricsCalculator:
    """
    Calculates multiple geometric metrics for squat form.

    The measurements are based on pose landmarks and are independent
    of repetition counting.
    """

    REQUIRED_LANDMARKS = (
        "LEFT_SHOULDER",
        "LEFT_HIP",
        "LEFT_KNEE",
        "LEFT_ANKLE",
    )

    @staticmethod
    def _landmark_map(
        landmarks: list[PoseLandmark],
    ) -> dict[str, PoseLandmark]:
        return {
            landmark.name: landmark
            for landmark in landmarks
        }

    def calculate(
        self,
        landmarks: list[PoseLandmark],
    ) -> SquatFormMetrics | None:
        """
        Calculate squat form metrics.

        Returns None when required landmarks are unavailable.
        """

        landmark_map = self._landmark_map(landmarks)

        if not all(
            name in landmark_map
            for name in self.REQUIRED_LANDMARKS
        ):
            return None

        shoulder = landmark_map["LEFT_SHOULDER"]
        hip = landmark_map["LEFT_HIP"]
        knee = landmark_map["LEFT_KNEE"]
        ankle = landmark_map["LEFT_ANKLE"]

        knee_angle = calculate_angle(
            hip,
            knee,
            ankle,
        )

        hip_angle = calculate_angle(
            shoulder,
            hip,
            knee,
        )

        torso_angle = self._calculate_torso_angle(
            shoulder,
            hip,
        )

        shoulder_hip_offset = abs(
            shoulder.x - hip.x
        )

        return SquatFormMetrics(
            knee_angle=knee_angle,
            hip_angle=hip_angle,
            torso_angle=torso_angle,
            shoulder_hip_offset=shoulder_hip_offset,
        )

    @staticmethod
    def _calculate_torso_angle(
        shoulder: PoseLandmark,
        hip: PoseLandmark,
    ) -> float:
        """
        Calculate torso inclination from vertical.

        0° means the shoulder is directly above the hip.
        Larger values indicate greater forward/backward inclination.
        """

        dx = shoulder.x - hip.x
        dy = shoulder.y - hip.y

        if dx == 0 and dy == 0:
            return 0.0

        import math

        angle_from_vertical = math.degrees(
            math.atan2(abs(dx), abs(dy))
        )

        return angle_from_vertical