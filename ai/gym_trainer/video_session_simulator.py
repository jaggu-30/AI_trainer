from dataclasses import dataclass
from typing import Iterator

from ai.gym_trainer.simulator import (
    generate_squat_sequence,
)


@dataclass
class SimulatedVideoFrame:
    frame_number: int
    timestamp_seconds: float
    landmarks: list


class SquatVideoSessionSimulator:
    """
    Generates deterministic squat landmark frames.

    This is used for testing continuous workout
    analysis without requiring a person to exercise.
    """

    def __init__(
        self,
        repetitions: int = 5,
        fps: float = 30.0,
    ):
        self.repetitions = repetitions
        self.fps = fps

    def frames(self) -> Iterator[SimulatedVideoFrame]:
        sequence = generate_squat_sequence(
            repetitions=self.repetitions
        )

        for frame_number, landmarks in enumerate(
            sequence
        ):
            yield SimulatedVideoFrame(
                frame_number=frame_number,
                timestamp_seconds=(
                    frame_number / self.fps
                ),
                landmarks=landmarks,
            )