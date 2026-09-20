from dataclasses import dataclass

from ai.gym_trainer.form_metrics import SquatFormMetrics
from ai.gym_trainer.form_scoring import FormScore


@dataclass
class FeedbackResult:
    messages: list[str]
    status: str


class SquatFeedbackEngine:
    def __init__(
        self,
        good_depth_angle: float = 100.0,
        shallow_depth_angle: float = 120.0,
        good_torso_angle: float = 15.0,
        maximum_torso_angle: float = 25.0,
        stable_offset: float = 0.10,
        unstable_offset: float = 0.20,
    ):
        self.good_depth_angle = good_depth_angle
        self.shallow_depth_angle = shallow_depth_angle
        self.good_torso_angle = good_torso_angle
        self.maximum_torso_angle = maximum_torso_angle
        self.stable_offset = stable_offset
        self.unstable_offset = unstable_offset

    def analyze_depth(
        self,
        knee_angle: float,
        phase: str,
    ) -> str:
        if phase == "standing":
            return "Ready position. Begin the next repetition."

        if phase == "descending":
            return "Keep descending with controlled movement."

        if phase == "bottom":
            if knee_angle <= self.good_depth_angle:
                return "Good squat depth."

            if knee_angle <= self.shallow_depth_angle:
                return "Squat depth is slightly shallow."

            return "Squat depth is too shallow."

        if phase == "ascending":
            return "Drive upward and complete the repetition."

        return "Continue the movement."

    def analyze_posture(
        self,
        torso_angle: float,
        phase: str,
    ) -> str:
        if torso_angle <= self.good_torso_angle:
            return "Good torso posture."

        if torso_angle <= self.maximum_torso_angle:
            return "Torso posture needs improvement."

        return "Torso is leaning excessively."

    def analyze_control(
        self,
        shoulder_hip_offset: float,
    ) -> str:
        if shoulder_hip_offset <= self.stable_offset:
            return "Movement appears stable."

        if shoulder_hip_offset <= self.unstable_offset:
            return "Movement stability could be improved."

        return "Movement appears unstable."

    def _generate_metric_feedback(
        self,
        metrics: SquatFormMetrics,
    ) -> list[str]:
        messages: list[str] = []

        if metrics.knee_angle <= self.good_depth_angle:
            messages.append("Good squat depth.")
        elif metrics.knee_angle <= self.shallow_depth_angle:
            messages.append("Squat depth is slightly shallow.")
        else:
            messages.append("Squat depth is too shallow.")

        messages.append(
            self.analyze_posture(
                metrics.torso_angle,
                phase="metric",
            )
        )

        messages.append(
            self.analyze_control(
                metrics.shoulder_hip_offset,
            )
        )

        return messages

    def generate(
        self,
        metrics: SquatFormMetrics,
        score: FormScore,
        phase: str | None = None,
    ) -> FeedbackResult:
        if phase is None:
            messages = self._generate_metric_feedback(metrics)

        elif phase == "standing":
            messages = [
                "Ready position. Begin the next repetition.",
                "Good torso posture.",
                "Movement appears stable.",
            ]

        elif phase == "descending":
            messages = [
                self.analyze_depth(
                    metrics.knee_angle,
                    phase,
                ),
                self.analyze_posture(
                    metrics.torso_angle,
                    phase,
                ),
                self.analyze_control(
                    metrics.shoulder_hip_offset,
                ),
            ]

        elif phase == "bottom":
            messages = [
                self.analyze_depth(
                    metrics.knee_angle,
                    phase,
                ),
                self.analyze_posture(
                    metrics.torso_angle,
                    phase,
                ),
                self.analyze_control(
                    metrics.shoulder_hip_offset,
                ),
            ]

        elif phase == "ascending":
            messages = [
                "Drive upward and complete the repetition.",
                self.analyze_posture(
                    metrics.torso_angle,
                    phase,
                ),
                self.analyze_control(
                    metrics.shoulder_hip_offset,
                ),
            ]

        else:
            messages = [
                "Continue the movement.",
                self.analyze_posture(
                    metrics.torso_angle,
                    phase,
                ),
                self.analyze_control(
                    metrics.shoulder_hip_offset,
                ),
            ]

        status_map = {
            "excellent": "excellent",
            "good": "good",
            "needs_improvement": "needs_improvement",
            "poor": "poor",
        }

        status = status_map.get(
            score.rating,
            "needs_improvement",
        )

        return FeedbackResult(
            messages=messages,
            status=status,
        )