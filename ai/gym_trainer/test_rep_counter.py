import sys

sys.path.insert(0, "..")

from ai.gym_trainer.rep_counter import SquatRepCounter


def main() -> None:
    counter = SquatRepCounter()

    squat_angles = [
        175,
        170,
        155,
        135,
        110,
        95,
        90,
        100,
        120,
        145,
        165,
        175,
    ]

    for angle in squat_angles:
        state = counter.update(angle)

        print(
            f"Angle: {angle:>3}° | "
            f"Phase: {state.phase:<10} | "
            f"Reps: {state.repetitions}"
        )

    print()
    print("Final repetitions:", counter.repetitions)

    assert counter.repetitions == 1

    print("Squat repetition test passed successfully.")


if __name__ == "__main__":
    main()
