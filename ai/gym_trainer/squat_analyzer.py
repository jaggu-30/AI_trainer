from dataclasses import dataclass

from ai.gym_trainer.angle import calculate_angle
from ai.gym_trainer.landmark_filter import LandmarkFilter
from ai.gym_trainer.rep_counter import SquatRepCounter
from ai.gym_trainer.smoother import AngleSmoother


@dataclass
class SquatAnalysis:
    knee_angle: float
    phase: str
    repetitions: int


class SquatAnalyzer:
    """
    Complete squat-analysis pipeline.

    Pipeline:
        landmarks
            ↓
        confidence filtering
            ↓
        knee-angle calculation
            ↓
        angle smoothing
            ↓
        repetition counting
    """

    REQUIRED_LANDMARKS = (
        "LEFT_HIP",
        "LEFT_KNEE",
        "LEFT_ANKLE",
    )

    def __init__(
    self,
    minimum_visibility: float = 0.5,
    smoothing_alpha: float = 0.6,
):
        self.landmark_filter = LandmarkFilter(
            minimum_visibility=minimum_visibility
        )

        self.angle_smoother = AngleSmoother(
    alpha=smoothing_alpha
)

        self.rep_counter = SquatRepCounter()

    @staticmethod
    def _landmark_map(landmarks):
        return {
            landmark.name: landmark
            for landmark in landmarks
        }

    def analyze(self, landmarks):
        """
        Analyze one pose frame.

        Returns:
            SquatAnalysis | None
        """

        if not landmarks:
            return None

        filtered_landmarks = self.landmark_filter.filter(
            landmarks
        )

        if not self.landmark_filter.has_required_landmarks(
            filtered_landmarks,
            self.REQUIRED_LANDMARKS,
        ):
            return None

        landmark_map = self._landmark_map(
            filtered_landmarks
        )

        hip = landmark_map["LEFT_HIP"]
        knee = landmark_map["LEFT_KNEE"]
        ankle = landmark_map["LEFT_ANKLE"]

        raw_knee_angle = calculate_angle(
            hip,
            knee,
            ankle,
        )

        smoothed_knee_angle = self.angle_smoother.update(
            raw_knee_angle
        )

        state = self.rep_counter.update(
            smoothed_knee_angle
        )

        return SquatAnalysis(
            knee_angle=smoothed_knee_angle,
            phase=state.phase,
            repetitions=state.repetitions,
        )

    def reset(self):
        """
        Reset the complete squat-analysis state.
        """

        self.rep_counter.reset()
        self.angle_smoother.reset()