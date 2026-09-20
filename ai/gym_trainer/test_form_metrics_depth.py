import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    calculator = SquatFormMetricsCalculator()

    test_angles = [
        170.0,
        130.0,
        100.0,
        90.0,
    ]

    print("Testing form metrics across squat depths...")
    print()

    previous_knee_angle = None

    for angle in test_angles:
        landmarks = create_squat_landmarks(angle)

        metrics = calculator.calculate(landmarks)

        assert metrics is not None

        print(
            f"Input knee angle: {angle:>6.1f}° | "
            f"Measured: {metrics.knee_angle:>6.1f}° | "
            f"Hip: {metrics.hip_angle:>6.1f}° | "
            f"Torso: {metrics.torso_angle:>6.1f}°"
        )

        assert abs(
            metrics.knee_angle - angle
        ) < 0.01

        if previous_knee_angle is not None:
            assert metrics.knee_angle < previous_knee_angle

        previous_knee_angle = metrics.knee_angle

    print()
    print(
        "Form metrics depth test passed successfully."
    )


if __name__ == "__main__":
    main()