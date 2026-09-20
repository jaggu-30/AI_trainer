import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.form_scoring import SquatFormScorer
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    metrics_calculator = SquatFormMetricsCalculator()
    scorer = SquatFormScorer()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    metrics = metrics_calculator.calculate(
        landmarks
    )

    assert metrics is not None

    result = scorer.score(metrics)

    print("Testing squat form scoring...")
    print()

    print(f"Depth score: {result.depth_score:.2f}")
    print(f"Posture score: {result.posture_score:.2f}")
    print(f"Control score: {result.control_score:.2f}")
    print(f"Overall score: {result.overall_score:.2f}")
    print(f"Rating: {result.rating}")

    assert result.depth_score == 100.0
    assert result.posture_score > 0.0
    assert result.control_score > 0.0
    assert 0.0 <= result.overall_score <= 100.0

    print()
    print(
        "Squat form scoring test passed successfully."
    )


if __name__ == "__main__":
    main()