from dataclasses import dataclass


@dataclass
class FormFeedback:
    status: str
    message: str
    score: int


class SquatFormAnalyzer:
    """
    Analyze basic squat depth and standing position.

    This is an initial rule-based form-analysis layer.
    Later it can be extended with additional biomechanical
    features and learned models.
    """

    def __init__(
        self,
        good_depth_angle: float = 100.0,
        minimum_standing_angle: float = 160.0,
    ):
        self.good_depth_angle = good_depth_angle
        self.minimum_standing_angle = minimum_standing_angle

    def analyze(
        self,
        knee_angle: float,
        phase: str,
    ) -> FormFeedback:

        if phase == "bottom":
            if knee_angle <= self.good_depth_angle:
                return FormFeedback(
                    status="good",
                    message="Good squat depth.",
                    score=100,
                )

            return FormFeedback(
                status="warning",
                message="Squat depth is too shallow. Try going lower.",
                score=70,
            )

        if phase == "standing":
            if knee_angle >= self.minimum_standing_angle:
                return FormFeedback(
                    status="good",
                    message="Good standing position.",
                    score=100,
                )

            return FormFeedback(
                status="warning",
                message="Stand up fully before starting the next repetition.",
                score=75,
            )

        if phase == "descending":
            return FormFeedback(
                status="info",
                message="Keep descending with controlled movement.",
                score=90,
            )

        if phase == "ascending":
            return FormFeedback(
                status="info",
                message="Drive upward and complete the repetition.",
                score=90,
            )

        return FormFeedback(
            status="info",
            message="Continue the movement.",
            score=80,
        )
