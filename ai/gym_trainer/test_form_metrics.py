import sys

sys.path.insert(0, "..")

from ai.gym_trainer.form_metrics import (
    SquatFormMetricsCalculator,
)
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    calculator = SquatFormMetricsCalculator()

    landmarks = create_squat_landmarks(90.0)

    metrics = calculator.calculate(landmarks)

    print("Testing squat form metrics...")
    print()

    assert metrics is not None

    print(f"Knee angle: {metrics.knee_angle:.2f}°")
    print(f"Hip angle: {metrics.hip_angle:.2f}°")
    print(f"Torso angle: {metrics.torso_angle:.2f}°")
    print(
        f"Shoulder-hip offset: "
        f"{metrics.shoulder_hip_offset:.4f}"
    )

    assert abs(metrics.knee_angle - 90.0) < 0.01
    assert metrics.hip_angle >= 0.0
    assert metrics.torso_angle >= 0.0
    assert metrics.shoulder_hip_offset >= 0.0

    print()
    print("Squat form metrics test passed successfully.")


if __name__ == "__main__":
    main()