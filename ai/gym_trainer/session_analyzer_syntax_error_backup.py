from dataclasses import dataclass, field

from ai.gym_trainer.feedback import (
    SquatFeedbackEngine,
    FeedbackResult,
)
from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.form_scoring import (
    FormScore,
    SquatFormScorer,
)
from ai.gym_trainer.rep_score import (
    RepScore,
    RepScoreAccumulator,
)
from ai.gym_trainer.rep_tracker import (
    RepTracker,
)
from ai.gym_trainer.squat_analyzer import (
    SquatAnalyzer,
)


@dataclass
class SessionFrameResult:
    """
    Analysis result for a single processed frame.
    """

    knee_angle: float
    phase: str
    repetitions: int
    score: FormScore
    feedback: FeedbackResult


@dataclass
class SquatSessionSummary:
    """
    Final summary of a complete squat session.
    """

    total_repetitions: int

    average_score: float
    best_score: float
    worst_score: float

    average_depth_score: float
    average_posture_score: float
    average_control_score: float

    repetition_scores: list[RepScore] = field(
        default_factory=list
    )

    average_repetition_score: float = 0.0
    best_repetition_score: float = 0.0
    worst_repetition_score: float = 0.0

    warnings: list[str] = field(
        default_factory=list
    )


class SquatSessionAnalyzer:
    """
    Processes squat frames and produces a complete
    workout-session summary.

    The analyzer maintains:

    1. Frame-level form analysis.
    2. Repetition-level quality scores.
    3. Repetition lifecycle state.
    """

    def __init__(
        self,
        minimum_visibility: float = 0.5,
        smoothing_alpha: float = 0.6,
    ):
        self.squat_analyzer = SquatAnalyzer(
            minimum_visibility=minimum_visibility,
            smoothing_alpha=smoothing_alpha,
        )

        self.metrics_calculator = (
            SquatFormMetricsCalculator()
        )

        self.scorer = SquatFormScorer()

        self.feedback_engine = (
            SquatFeedbackEngine()
        )

        self.rep_score_accumulator = (
            RepScoreAccumulator()
        )

        self.rep_tracker = RepTracker()

        self.results: list[
            SessionFrameResult
        ] = []

        self.repetition_scores: list[
            RepScore
        ] = []

    def process_frame(self, landmarks):
        """
        Process one frame of pose landmarks.
        """

        analysis = self.squat_analyzer.analyze(
            landmarks
        )

        if analysis is None:
            return None

        metrics = self.metrics_calculator.calculate(
            landmarks
        )

        if metrics is None:
            return None

        score = self.scorer.score(metrics)

        feedback = self.feedback_engine.generate(
            metrics=metrics,
            score=score,
        )

        result = SessionFrameResult(
            knee_angle=analysis.knee_angle,
            phase=analysis.phase,
            repetitions=analysis.repetitions,
            score=score,
            feedback=feedback,
        )

        self.results.append(result)

        lifecycle = self.rep_tracker.update(
            phase=analysis.phase,
            repetitions=analysis.repetitions,
        )

        if lifecycle in (
            "started",
            "in_progress",
        ):
            self.rep_score_accumulator.add(
                score
            )

        elif lifecycle == "completed":
            rep_score = (
                self.rep_score_accumulator.calculate(
                    repetition_number=(
                        self.rep_tracker.repetition_number
                    )
                )
            )

            if rep_score is not None:
                self.repetition_scores.append(
                    rep_score
                )

            self.rep_score_accumulator.clear()

        return result

    def summary(self) -> SquatSessionSummary:
        """
        Generate the final session summary.
        """

        if not self.results:
    		return SquatSessionSummary(
     		   total_repetitions=0,
       		   average_score=0.0,
        	   best_score=0.0,
        	   worst_score=0.0,
    	           average_depth_score=0.0,
    	           average_posture_score=0.0,
     	           average_control_score=0.0,
   		 )

        scores = [
            result.score.overall_score
            for result in self.results
        ]

        depth_scores = [
            result.score.depth_score
            for result in self.results
        ]

        posture_scores = [
            result.score.posture_score
            for result in self.results
        ]

        control_scores = [
            result.score.control_score
            for result in self.results
        ]

        repetition_values = [
            result.overall_score
            for result in self.repetition_scores
        ]

        warnings = []

        for result in self.results:
            for message in result.feedback.messages:
                if (
                    "too shallow"
                    in message.lower()
                    or "excessively"
                    in message.lower()
                    or "unstable"
                    in message.lower()
                ):
                    if message not in warnings:
                        warnings.append(message)

        average_repetition_score = 0.0
        best_repetition_score = 0.0
        worst_repetition_score = 0.0

        if repetition_values:
            average_repetition_score = round(
                sum(repetition_values)
                / len(repetition_values),
                2,
            )

            best_repetition_score = round(
                max(repetition_values),
                2,
            )

            worst_repetition_score = round(
                min(repetition_values),
                2,
            )

        return SquatSessionSummary(
            total_repetitions=(
                self.squat_analyzer
                .rep_counter
                .repetitions
            ),
            average_score=round(
                sum(scores) / len(scores),
                2,
            ),
            best_score=round(
                max(scores),
                2,
            ),
            worst_score=round(
                min(scores),
                2,
            ),
            average_depth_score=round(
                sum(depth_scores)
                / len(depth_scores),
                2,
            ),
            average_posture_score=round(
                sum(posture_scores)
                / len(posture_scores),
                2,
            ),
            average_control_score=round(
                sum(control_scores)
                / len(control_scores),
                2,
            ),
            repetition_scores=(
                self.repetition_scores.copy()
            ),
            average_repetition_score=(
                average_repetition_score
            ),
            best_repetition_score=(
                best_repetition_score
            ),
            worst_repetition_score=(
                worst_repetition_score
            ),
            warnings=warnings,
        )

    def reset(self):
        """
        Reset the current workout session.
        """

        self.squat_analyzer.reset()

        self.rep_score_accumulator.clear()

        self.rep_tracker.reset()

        self.results.clear()

        self.repetition_scores.clear()