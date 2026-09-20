from dataclasses import dataclass

from ai.gym_trainer.angle import calculate_angle
from ai.gym_trainer.pose import PoseLandmark
from ai.gym_trainer.rep_counter import RepCounterState, SquatRepCounter


@dataclass
class SquatAnalysis:
    knee_angle: float
    phase: str
    repetitions: int


class SquatAnalyzer:
    """
    End-to-end squat analysis using pose landmarks.

    Pipeline:
        landmarks
            ↓
        hip-knee-ankle angle
            ↓
        squat state machine
            ↓
        repetition count
    """

    def __init__(self) -> None:
        self.rep_counter = SquatRepCounter()

    @staticmethod
    def _landmark_map(
        landmarks: list[PoseLandmark],
    ) -> dict[str, PoseLandmark]:
        return {
            landmark.name: landmark
            for landmark in landmarks
        }

    def analyze(
        self,
        landmarks: list[PoseLandmark],
    ) -> SquatAnalysis | None:
        landmark_map = self._landmark_map(landmarks)

        required = (
            "LEFT_HIP",
            "LEFT_KNEE",
            "LEFT_ANKLE",
        )

        if not all(
            name in landmark_map
            for name in required
        ):
            return None

        hip = landmark_map["LEFT_HIP"]
        knee = landmark_map["LEFT_KNEE"]
        ankle = landmark_map["LEFT_ANKLE"]

        knee_angle = calculate_angle(
            hip,
            knee,
            ankle,
        )

        state: RepCounterState = self.rep_counter.update(
            knee_angle
        )

        return SquatAnalysis(
            knee_angle=knee_angle,
            phase=state.phase,
            repetitions=state.repetitions,
        )

    def reset(self) -> None:
        self.rep_counter.reset()
