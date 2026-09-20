from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.simulator import (
    generate_variable_squat_sequence,
)

from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)


def main():
    print(
        "Testing variable-quality squat session..."
    )
    print()

    repetitions = [
        {
            "knee_angle": [
                175,
                165,
                150,
                130,
                110,
                95,
                90,
                100,
                120,
                145,
                165,
                175,
            ],
            "torso_lean": 5,
        },
        {
            "knee_angle": [
                175,
                165,
                150,
                130,
                110,
                95,
                90,
                100,
                120,
                145,
                165,
                175,
            ],
            "torso_lean": 10,
        },
        {
            "knee_angle": [
                175,
                165,
                150,
                130,
                110,
                95,
                90,
                100,
                120,
                145,
                165,
                175,
            ],
            "torso_lean": 20,
        },
        {
            "knee_angle": [
                175,
                165,
                150,
                130,
                110,
                95,
                90,
                100,
                120,
                145,
                165,
                175,
            ],
            "torso_lean": 30,
        },
        {
            "knee_angle": [
                175,
                165,
                150,
                130,
                110,
                95,
                90,
                100,
                120,
                145,
                165,
                175,
            ],
            "torso_lean": 5,
        },
    ]

    sequence = generate_variable_squat_sequence(
        repetitions=repetitions
    )

    analyzer = SquatSessionAnalyzer()

    processed_frames = 0

    for landmarks in sequence:
        analyzer.process_frame(
            landmarks
        )

        processed_frames += 1

    summary = analyzer.summary()

    print(
        f"Processed frames: "
        f"{processed_frames}"
    )

    print(
        f"Total repetitions: "
        f"{summary.total_repetitions}"
    )

    print(
        f"Average frame score: "
        f"{summary.average_score}"
    )

    print(
        f"Best frame score: "
        f"{summary.best_score}"
    )

    print(
        f"Worst frame score: "
        f"{summary.worst_score}"
    )

    print(
        f"Average repetition score: "
        f"{summary.average_repetition_score}"
    )

    print(
        f"Best repetition score: "
        f"{summary.best_repetition_score}"
    )

    print(
        f"Worst repetition score: "
        f"{summary.worst_repetition_score}"
    )

    print()
    print("Repetition scores:")

    scores = []

    for repetition in summary.repetition_scores:
        score = repetition.overall_score

        scores.append(score)

        print(
            f"- Rep "
            f"{repetition.repetition_number}: "
            f"{score}"
        )

    print()

    if summary.warnings:
        print("Warnings:")

        for warning in summary.warnings:
            print(f"- {warning}")

    else:
        print("Warnings: None")

    assert processed_frames == 60

    assert (
        summary.total_repetitions == 5
    )

    assert len(scores) == 5

    assert len(set(scores)) > 1

    assert (
        summary.best_repetition_score
        >= summary.worst_repetition_score
    )

    print()
    print(
        "Variable-quality squat session "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()
