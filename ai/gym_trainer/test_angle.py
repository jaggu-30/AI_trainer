import sys

sys.path.insert(0, "..")

from ai.gym_trainer.angle import calculate_angle
from ai.gym_trainer.pose import PoseLandmark


def main() -> None:
    point_a = PoseLandmark(
        name="A",
        x=0.0,
        y=1.0,
        z=0.0,
        visibility=1.0,
    )

    point_b = PoseLandmark(
        name="B",
        x=0.0,
        y=0.0,
        z=0.0,
        visibility=1.0,
    )

    point_c = PoseLandmark(
        name="C",
        x=1.0,
        y=0.0,
        z=0.0,
        visibility=1.0,
    )

    angle = calculate_angle(
        point_a,
        point_b,
        point_c,
    )

    print(f"Calculated angle: {angle:.2f} degrees")

    assert abs(angle - 90.0) < 0.001

    print("Angle calculation test passed successfully.")


if __name__ == "__main__":
    main()
