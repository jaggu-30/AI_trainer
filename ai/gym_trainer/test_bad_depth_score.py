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

    good_landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    shallow_landmarks = create_squat_landmarks(
        knee_angle=130.0,
        torso_lean=5.0,
    )

    good_metrics = metrics_calculator.calculate(
        good_landmarks
    )

    shallow_metrics = metrics_calculator.calculate(
        shallow_landmarks
    )

    assert good_metrics is not None
    assert shallow_metrics is not None

    good_score = scorer.score(good_metrics)
    shallow_score = scorer.score(shallow_metrics)

    print("Testing depth-based form scoring...")
    print()

    print(
        f"Good squat depth score: "
        f"{good_score.depth_score:.2f}"
    )

    print(
        f"Shallow squat depth score: "
        f"{shallow_score.depth_score:.2f}"
    )

    assert good_score.depth_score > shallow_score.depth_score

    print()
    print(
        "Depth scoring test passed successfully."
    )


if __name__ == "__main__":
    main()