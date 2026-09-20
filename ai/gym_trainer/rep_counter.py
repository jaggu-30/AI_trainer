from dataclasses import dataclass


@dataclass
class RepCounterState:
    phase: str = "standing"
    repetitions: int = 0
    last_angle: float | None = None


class SquatRepCounter:
    """
    Count squat repetitions using knee-angle movement.

    A complete repetition is:

        standing
            ↓
        descending
            ↓
          bottom
            ↓
        ascending
            ↓
        standing
    """

    def __init__(
        self,
        standing_angle: float = 160.0,
        bottom_angle: float = 100.0,
    ):
        if bottom_angle >= standing_angle:
            raise ValueError(
                "bottom_angle must be smaller than standing_angle."
            )

        self.standing_angle = standing_angle
        self.bottom_angle = bottom_angle

        self.state = RepCounterState()

    @property
    def repetitions(self) -> int:
        return self.state.repetitions

    @property
    def phase(self) -> str:
        return self.state.phase

    def update(self, knee_angle: float) -> RepCounterState:
        """
        Update the squat state using the current knee angle.
        """

        self.state.last_angle = knee_angle

        if self.state.phase == "standing":
            if knee_angle < self.standing_angle:
                self.state.phase = "descending"

        elif self.state.phase == "descending":
            if knee_angle <= self.bottom_angle:
                self.state.phase = "bottom"

            elif knee_angle >= self.standing_angle:
                self.state.phase = "standing"

        elif self.state.phase == "bottom":
            if knee_angle > self.bottom_angle:
                self.state.phase = "ascending"

        elif self.state.phase == "ascending":
            if knee_angle >= self.standing_angle:
                self.state.repetitions += 1
                self.state.phase = "standing"

        return self.state

    def reset(self) -> None:
        """Reset the repetition counter."""
        self.state = RepCounterState()
