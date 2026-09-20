from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.video_session_simulator import (
    SquatVideoSessionSimulator,
)

from ai.gym_trainer.session_analyzer import (
    SquatSessionAnalyzer,
)


def main():
    print(
        "Testing complete squat workout session analysis..."
    )
    print()

    simulator = SquatVideoSessionSimulator(
        repetitions=5,
        fps=30.0,
    )

    analyzer = SquatSessionAnalyzer()

    processed_frames = 0

    for frame in simulator.frames():
        analyzer.process_frame(
            frame.landmarks
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
        f"Average depth score: "
        f"{summary.average_depth_score}"
    )

    print(
        f"Average posture score: "
        f"{summary.average_posture_score}"
    )

    print(
        f"Average control score: "
        f"{summary.average_control_score}"
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

    for repetition in summary.repetition_scores:
        print(
            f"- Rep "
            f"{repetition.repetition_number}: "
            f"{repetition.overall_score}"
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

    assert (
        summary.average_score > 0
    )

    assert (
        summary.best_score
        >= summary.worst_score
    )

    assert len(
        summary.repetition_scores
    ) == 5

    print()
    print(
        "Complete squat workout session "
        "analysis test passed successfully."
    )


if __name__ == "__main__":
    main()