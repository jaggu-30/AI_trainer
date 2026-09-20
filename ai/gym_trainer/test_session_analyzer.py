import sys

sys.path.insert(0, "..")

from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)
from ai.gym_trainer.simulator import (
    generate_squat_sequence,
)


def main():
    print("Testing complete squat session analyzer...")
    print()

    session = SquatSessionAnalyzer(
        smoothing_alpha=0.6,
    )

    frames = generate_squat_sequence(
        repetitions=5,
    )

    for frame in frames:
        result = session.process_frame(frame)

        assert result is not None

    summary = session.summary()

    print(
        f"Frames processed: "
        f"{len(frames)}"
    )

    print(
        f"Total repetitions: "
        f"{summary.total_repetitions}"
    )

    print(
        f"Average frame score: "
        f"{summary.average_score:.2f}"
    )

    print(
        f"Best frame score: "
        f"{summary.best_score:.2f}"
    )

    print(
        f"Worst frame score: "
        f"{summary.worst_score:.2f}"
    )

    print()

    print(
        f"Average repetition score: "
        f"{summary.average_repetition_score:.2f}"
    )

    print(
        f"Best repetition score: "
        f"{summary.best_repetition_score:.2f}"
    )

    print(
        f"Worst repetition score: "
        f"{summary.worst_repetition_score:.2f}"
    )

    print()

    for rep in summary.repetition_scores:
        print(
            f"Rep {rep.repetition_number}: "
            f"{rep.overall_score:.2f} "
            f"({rep.rating})"
        )

    print()

    print(
        f"Average depth score: "
        f"{summary.average_depth_score:.2f}"
    )

    print(
        f"Average posture score: "
        f"{summary.average_posture_score:.2f}"
    )

    print(
        f"Average control score: "
        f"{summary.average_control_score:.2f}"
    )

    print()

    assert len(frames) == 60
    assert summary.total_repetitions == 5

    assert len(
        summary.repetition_scores
    ) == 5

    assert (
        summary.average_repetition_score
        > 0.0
    )

    assert (
        summary.best_repetition_score
        >= summary.average_repetition_score
    )

    assert (
        summary.worst_repetition_score
        <= summary.average_repetition_score
    )

    print(
        "Complete squat session analyzer "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()