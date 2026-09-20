import sys

sys.path.insert(0, "..")

from ai.gym_trainer.feedback import SquatFeedbackEngine
from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.form_scoring import SquatFormScorer
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    metrics_calculator = SquatFormMetricsCalculator()
    scorer = SquatFormScorer()
    feedback_engine = SquatFeedbackEngine()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    metrics = metrics_calculator.calculate(
        landmarks
    )

    assert metrics is not None

    score = scorer.score(metrics)

    feedback = feedback_engine.generate(
        metrics=metrics,
        score=score,
    )

    print("Testing squat feedback engine...")
    print()

    print(f"Status: {feedback.status}")

    for message in feedback.messages:
        print(f"- {message}")

    assert len(feedback.messages) == 3
    assert feedback.status == "excellent"

    print()
    print(
        "Squat feedback engine test passed successfully."
    )


if __name__ == "__main__":
    main()