import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    calculator = SquatFormMetricsCalculator()

    landmarks = create_squat_landmarks(90.0)

    landmarks = [
        landmark
        for landmark in landmarks
        if landmark.name != "LEFT_ANKLE"
    ]

    metrics = calculator.calculate(landmarks)

    print("Testing missing-landmark handling...")
    print()

    print(f"Metrics result: {metrics}")

    assert metrics is None

    print()
    print(
        "Missing-landmark form metrics test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()