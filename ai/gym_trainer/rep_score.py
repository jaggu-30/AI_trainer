from dataclasses import dataclass


@dataclass
class RepScore:
    """
    Quality score for one completed repetition.
    """

    repetition_number: int
    overall_score: float
    depth_score: float
    posture_score: float
    control_score: float
    rating: str


class RepScoreAccumulator:
    """
    Collect frame-level form scores for one repetition.

    Scores are accumulated while the user performs
    a repetition and converted into one RepScore when
    the repetition is completed.
    """

    def __init__(self):
        self._scores = []

    @property
    def frame_count(self) -> int:
        return len(self._scores)

    def add(self, score) -> None:
        """
        Add one frame-level FormScore.
        """

        self._scores.append(score)

    def clear(self) -> None:
        """
        Remove all currently accumulated frame scores.
        """

        self._scores.clear()

    def is_empty(self) -> bool:
        return len(self._scores) == 0

    def calculate(
        self,
        repetition_number: int,
    ) -> RepScore | None:
        """
        Calculate the average score for the current
        repetition.
        """

        if self.is_empty():
            return None

        average_overall = sum(
            score.overall_score
            for score in self._scores
        ) / self.frame_count

        average_depth = sum(
            score.depth_score
            for score in self._scores
        ) / self.frame_count

        average_posture = sum(
            score.posture_score
            for score in self._scores
        ) / self.frame_count

        average_control = sum(
            score.control_score
            for score in self._scores
        ) / self.frame_count

        overall_score = round(
            average_overall,
            2,
        )

        return RepScore(
            repetition_number=repetition_number,
            overall_score=overall_score,
            depth_score=round(
                average_depth,
                2,
            ),
            posture_score=round(
                average_posture,
                2,
            ),
            control_score=round(
                average_control,
                2,
            ),
            rating=self._get_rating(
                overall_score
            ),
        )

    @staticmethod
    def _get_rating(score: float) -> str:
        if score >= 90:
            return "excellent"

        if score >= 75:
            return "good"

        if score >= 60:
            return "needs_improvement"

        return "poor"