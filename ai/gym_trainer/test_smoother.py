import sys

sys.path.insert(0, "..")

from ai.gym_trainer.smoother import AngleSmoother


def main():
    smoother = AngleSmoother(alpha=0.6)

    test_angles = [
        90.0,
        94.0,
        89.0,
        93.0,
        91.0,
    ]

    print("Testing EMA angle smoother...")
    print()

    previous_smoothed = None

    for angle in test_angles:
        smoothed = smoother.update(angle)

        print(
            f"Raw angle: {angle:>6.1f}° | "
            f"Smoothed angle: {smoothed:>6.1f}°"
        )

        if previous_smoothed is not None:
            assert smoothed != previous_smoothed

        previous_smoothed = smoothed

    assert smoother.sample_count == 1

    smoother.reset()

    assert smoother.sample_count == 0

    print()
    print("EMA angle smoother test passed successfully.")


if __name__ == "__main__":
    main()