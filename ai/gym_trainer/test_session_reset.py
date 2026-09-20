import sys

sys.path.insert(0, "..")

from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)
from ai.gym_trainer.simulator import (
    generate_squat_sequence,
)


def main():
    print("Testing squat session reset...")
    print()

    session = SquatSessionAnalyzer(
        smoothing_alpha=0.6,
    )

    first_session = generate_squat_sequence(
        repetitions=2,
    )

    for frame in first_session:
        result = session.process_frame(frame)
        assert result is not None

    first_summary = session.summary()

    print(
        f"First session repetitions: "
        f"{first_summary.total_repetitions}"
    )

    assert first_summary.total_repetitions == 2
    assert len(
        first_summary.repetition_scores
    ) == 2

    session.reset()

    reset_summary = session.summary()

    print(
        f"After reset repetitions: "
        f"{reset_summary.total_repetitions}"
    )

    print(
        f"After reset rep scores: "
        f"{len(reset_summary.repetition_scores)}"
    )

    assert reset_summary.total_repetitions == 0
    assert len(
        reset_summary.repetition_scores
    ) == 0
    assert len(session.results) == 0
    assert session.rep_tracker.active is False
    assert session.rep_tracker.repetition_number == 0

    second_session = generate_squat_sequence(
        repetitions=3,
    )

    for frame in second_session:
        result = session.process_frame(frame)
        assert result is not None

    second_summary = session.summary()

    print(
        f"Second session repetitions: "
        f"{second_summary.total_repetitions}"
    )

    assert second_summary.total_repetitions == 3
    assert len(
        second_summary.repetition_scores
    ) == 3

    print()
    print(
        "Session reset test passed successfully."
    )


if __name__ == "__main__":
    main()