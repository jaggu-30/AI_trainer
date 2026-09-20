import sys

sys.path.insert(0, "..")

from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)
from ai.gym_trainer.simulator import (
    generate_variable_squat_sequence,
)


MOVEMENT = [
    175.0,
    165.0,
    150.0,
    130.0,
    110.0,
    95.0,
    90.0,
    100.0,
    120.0,
    145.0,
    165.0,
    175.0,
]


def main():
    print("Testing variable squat session...")
    print()

    repetitions = [
        {
            "knee_angle": MOVEMENT,
            "torso_lean": 5.0,
        },
        {
            "knee_angle": MOVEMENT,
            "torso_lean": 10.0,
        },
        {
            "knee_angle": MOVEMENT,
            "torso_lean": 20.0,
        },
        {
            "knee_angle": MOVEMENT,
            "torso_lean": 30.0,
        },
        {
            "knee_angle": MOVEMENT,
            "torso_lean": 5.0,
        },
    ]

    frames = generate_variable_squat_sequence(
        repetitions
    )

    session = SquatSessionAnalyzer(
        smoothing_alpha=0.6,
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

    print()

    for rep in summary.repetition_scores:
        print(
            f"Rep {rep.repetition_number}: "
            f"{rep.overall_score:.2f} "
            f"({rep.rating})"
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

    assert len(frames) == 60

    assert summary.total_repetitions == 5

    assert len(
        summary.repetition_scores
    ) == 5

    scores = [
        rep.overall_score
        for rep in summary.repetition_scores
    ]

    assert len(set(scores)) > 1

    assert (
        summary.best_repetition_score
        > summary.worst_repetition_score
    )

    print(
        "Different form conditions produced "
        "different repetition scores."
    )

    print()

    print(
        "Variable repetition scoring test "
        "passed successfully."
    )


if __name__ == "__main__":
    main()