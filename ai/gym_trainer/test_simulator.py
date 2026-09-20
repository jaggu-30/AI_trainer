import sys

sys.path.insert(0, "..")

from ai.gym_trainer.angle import calculate_angle
from ai.gym_trainer.simulator import (
    create_squat_landmarks,
    generate_squat_sequence,
)


def main():
    print("Testing synthetic squat geometry...")
    print()

    test_angles = [
        175.0,
        170.0,
        150.0,
        130.0,
        110.0,
        100.0,
        90.0,
        80.0,
        60.0,
    ]

    for requested_angle in test_angles:
        landmarks = create_squat_landmarks(
            requested_angle
        )

        landmark_map = {
            landmark.name: landmark
            for landmark in landmarks
        }

        measured_angle = calculate_angle(
            landmark_map["LEFT_HIP"],
            landmark_map["LEFT_KNEE"],
            landmark_map["LEFT_ANKLE"],
        )

        print(
            f"Requested: {requested_angle:>6.1f}° | "
            f"Measured: {measured_angle:>6.1f}°"
        )

        assert abs(
            measured_angle - requested_angle
        ) < 0.01

    print()
    print(
        "Synthetic angle geometry test "
        "passed successfully."
    )

    sequence = generate_squat_sequence(5)

    expected_frames = 5 * 12

    print()
    print(f"Generated frames: {len(sequence)}")
    print(f"Expected frames: {expected_frames}")

    assert len(sequence) == expected_frames

    print(
        "Synthetic squat sequence test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()