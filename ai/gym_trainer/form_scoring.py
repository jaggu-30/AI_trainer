from dataclasses import dataclass

from ai.gym_trainer.form_metrics import SquatFormMetrics


@dataclass
class FormScore:
    depth_score: float
    posture_score: float
    control_score: float
    overall_score: float
    rating: str


class SquatFormScorer:
    DEPTH_WEIGHT = 0.40
    POSTURE_WEIGHT = 0.30
    CONTROL_WEIGHT = 0.30

    def __init__(
        self,
        good_depth_angle: float = 100.0,
        maximum_torso_angle: float = 25.0,
    ):
        self.good_depth_angle = good_depth_angle
        self.maximum_torso_angle = maximum_torso_angle

    def calculate_depth_score(
        self,
        knee_angle: float,
    ) -> float:
        if knee_angle <= self.good_depth_angle:
            return 100.0

        standing_angle = 160.0

        if knee_angle >= standing_angle:
            return 0.0

        score = (
            (standing_angle - knee_angle)
            / (standing_angle - self.good_depth_angle)
        ) * 100.0

        return max(
            0.0,
            min(100.0, score),
        )

    def calculate_posture_score(
        self,
        torso_angle: float,
    ) -> float:
        if torso_angle <= 0:
            return 100.0

        if torso_angle >= self.maximum_torso_angle:
            return 0.0

        score = (
            1.0
            - torso_angle / self.maximum_torso_angle
        ) * 100.0

        return max(
            0.0,
            min(100.0, score),
        )

    def calculate_control_score(
        self,
        shoulder_hip_offset: float,
    ) -> float:
        maximum_offset = 0.20

        if shoulder_hip_offset <= 0:
            return 100.0

        if shoulder_hip_offset >= maximum_offset:
            return 0.0

        score = (
            1.0
            - shoulder_hip_offset / maximum_offset
        ) * 100.0

        return max(
            0.0,
            min(100.0, score),
        )

    @staticmethod
    def get_rating(
        score: float,
    ) -> str:
        if score >= 90:
            return "excellent"

        if score >= 75:
            return "good"

        if score >= 60:
            return "needs_improvement"

        return "poor"

    def score(
        self,
        metrics: SquatFormMetrics,
    ) -> FormScore:
        depth_score = self.calculate_depth_score(
            metrics.knee_angle
        )

        posture_score = self.calculate_posture_score(
            metrics.torso_angle
        )

        control_score = self.calculate_control_score(
            metrics.shoulder_hip_offset
        )

        overall_score = (
            depth_score * self.DEPTH_WEIGHT
            + posture_score * self.POSTURE_WEIGHT
            + control_score * self.CONTROL_WEIGHT
        )

        overall_score = round(
            max(0.0, min(100.0, overall_score)),
            2,
        )

        return FormScore(
            depth_score=round(depth_score, 2),
            posture_score=round(posture_score, 2),
            control_score=round(control_score, 2),
            overall_score=overall_score,
            rating=self.get_rating(
                overall_score
            ),
        )

    def score_by_phase(
        self,
        metrics: SquatFormMetrics,
        phase: str,
    ) -> FormScore:
        """
        Score a squat frame according to its movement phase.

        Standing frames are treated as neutral ready-position
        frames and are not penalized for squat depth.
        """

        if phase == "standing":
            return FormScore(
                depth_score=100.0,
                posture_score=100.0,
                control_score=100.0,
                overall_score=100.0,
                rating="excellent",
            )

        return self.score(metrics)