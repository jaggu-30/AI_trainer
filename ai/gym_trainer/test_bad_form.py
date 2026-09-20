import sys

sys.path.insert(0, "..")

from ai.gym_trainer.feedback import SquatFeedbackEngine
from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.form_scoring import SquatFormScorer
from ai.gym_trainer.simulator import create_squat_landmarks


def test_shallow_squat():
    metrics_calculator = SquatFormMetricsCalculator()
    scorer = SquatFormScorer()
    feedback_engine = SquatFeedbackEngine()

    landmarks = create_squat_landmarks(
        knee_angle=130.0,
        torso_lean=5.0,
    )

    metrics = metrics_calculator.calculate(landmarks)

    assert metrics is not None

    score = scorer.score(metrics)

    feedback = feedback_engine.generate(
        metrics=metrics,
        score=score,
    )

    print("SHALLOW SQUAT")
    print(f"Overall score: {score.overall_score:.2f}")
    print(f"Rating: {score.rating}")

    for message in feedback.messages:
        print(f"- {message}")

    assert score.depth_score < 100.0
    assert any(
        "shallow" in message.lower()
        for message in feedback.messages
    )


def test_excessive_torso_lean():
    metrics_calculator = SquatFormMetricsCalculator()
    scorer = SquatFormScorer()
    feedback_engine = SquatFeedbackEngine()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=35.0,
    )

    metrics = metrics_calculator.calculate(landmarks)

    assert metrics is not None

    score = scorer.score(metrics)

    feedback = feedback_engine.generate(
        metrics=metrics,
        score=score,
    )

    print()
    print("EXCESSIVE TORSO LEAN")
    print(f"Overall score: {score.overall_score:.2f}")
    print(f"Rating: {score.rating}")

    for message in feedback.messages:
        print(f"- {message}")

    assert metrics.torso_angle > 25.0
    assert score.posture_score == 0.0
    assert any(
        "excessively" in message.lower()
        for message in feedback.messages
    )


def main():
    print("Testing bad-form detection...")
    print()

    test_shallow_squat()
    test_excessive_torso_lean()

    print()
    print("Bad-form detection tests passed successfully.")


if __name__ == "__main__":
    main()