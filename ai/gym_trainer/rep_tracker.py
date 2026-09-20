from dataclasses import dataclass


@dataclass
class RepTrackerState:
    """
    Tracks the lifecycle of one repetition.
    """

    active: bool = False
    repetition_number: int = 0


class RepTracker:
    """
    Tracks when a repetition starts and completes
    based on squat movement phases.
    """

    def __init__(self):
        self.state = RepTrackerState()

    @property
    def active(self) -> bool:
        return self.state.active

    @property
    def repetition_number(self) -> int:
        return self.state.repetition_number

    def update(self, phase: str, repetitions: int) -> str:
        """
        Update repetition lifecycle.

        Returns one of:

            "idle"
            "started"
            "in_progress"
            "completed"
        """

        if not self.state.active:
            if phase == "descending":
                self.state.active = True
                return "started"

            return "idle"

        if repetitions > self.state.repetition_number:
            self.state.repetition_number = repetitions
            self.state.active = False

            return "completed"

        return "in_progress"

    def reset(self):
        self.state = RepTrackerState()