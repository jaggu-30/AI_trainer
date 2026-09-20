from ai.gym_trainer.form_metrics import SquatFormMetricsCalculator
from ai.gym_trainer.form_scoring import SquatFormScorer
from ai.gym_trainer.feedback import SquatFeedbackEngine
from ai.gym_trainer.squat_analyzer import SquatAnalyzer


class GymTrainerService:
    """
    Application service that connects the AI Gym Trainer
    components into one processing pipeline.
    """

    SUPPORTED_EXERCISES = {"squat"}

    def __init__(
        self,
        minimum_visibility: float = 0.5,
        smoothing_alpha: float = 0.6,
    ):
        self.squat_analyzer = SquatAnalyzer(
            minimum_visibility=minimum_visibility,
            smoothing_alpha=smoothing_alpha,
        )

        self.metrics_calculator = SquatFormMetricsCalculator()
        self.scorer = SquatFormScorer()
        self.feedback_engine = SquatFeedbackEngine()

    def process_squat(self, landmarks):
        """
        Process one frame of squat pose landmarks.
        """

        analysis = self.squat_analyzer.analyze(landmarks)

        if analysis is None:
            return None

        metrics = self.metrics_calculator.calculate(landmarks)

        if metrics is None:
            return None

        score = self.scorer.score_by_phase(
    		metrics=metrics,
    		phase=analysis.phase,
	)

        feedback = self.feedback_engine.generate(
            metrics=metrics,
            score=score,
	    phase=analysis.phase,
        )

        return {
            "exercise": "squat",
            "knee_angle": round(analysis.knee_angle, 2),
            "phase": analysis.phase,
            "repetitions": analysis.repetitions,
            "depth_score": score.depth_score,
            "posture_score": score.posture_score,
            "control_score": score.control_score,
            "form_score": score.overall_score,
            "rating": score.rating,
            "feedback": feedback.messages,
        }

    def process(self, exercise: str, landmarks):
        """
        Process a frame for the requested exercise.
        """

        normalized_exercise = exercise.strip().lower()

        if normalized_exercise not in self.SUPPORTED_EXERCISES:
            raise ValueError(
                f"Unsupported exercise: {exercise}"
            )

        if normalized_exercise == "squat":
            return self.process_squat(landmarks)

        return None

    def reset(self):
        """
        Reset the current trainer session.
        """

        self.squat_analyzer.reset()