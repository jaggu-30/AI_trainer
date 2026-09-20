import sys

sys.path.insert(0, "..")

from ai.gym_trainer.rep_tracker import RepTracker


def main():
    print("Testing repetition lifecycle tracker...")
    print()

    tracker = RepTracker()

    result = tracker.update(
        phase="standing",
        repetitions=0,
    )

    print(f"Standing: {result}")
    assert result == "idle"

    result = tracker.update(
        phase="descending",
        repetitions=0,
    )

    print(f"Descending: {result}")
    assert result == "started"
    assert tracker.active is True

    result = tracker.update(
        phase="bottom",
        repetitions=0,
    )

    print(f"Bottom: {result}")
    assert result == "in_progress"

    result = tracker.update(
        phase="ascending",
        repetitions=0,
    )

    print(f"Ascending: {result}")
    assert result == "in_progress"

    result = tracker.update(
        phase="standing",
        repetitions=1,
    )

    print(f"Completed: {result}")

    assert result == "completed"
    assert tracker.active is False
    assert tracker.repetition_number == 1

    print()
    print(
        "Repetition lifecycle tracker test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()