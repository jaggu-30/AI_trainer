import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(PROJECT_ROOT))


from ai.gym_trainer.simulator import (
    generate_squat_sequence,
)

from app.services.ai.gym_trainer.performance_service import (
    GymTrainerPerformanceService,
)


def test_performance_service():
    print("Testing Gym Trainer Performance Service...")

    frames = generate_squat_sequence(
        repetitions=5
    )

    service = GymTrainerPerformanceService()

    report = service.analyze(
        exercise="squat",
        frames=frames,
    )

    print()
    print(f"Exercise: {report.exercise}")
    print(
        f"Total repetitions: "
        f"{report.total_repetitions}"
    )
    print(
        f"Performance score: "
        f"{report.performance_score}"
    )
    print(
        f"Best frame score: "
        f"{report.best_frame_score}"
    )
    print(
        f"Worst frame score: "
        f"{report.worst_frame_score}"
    )
    print(
        f"Depth score: "
        f"{report.depth_score}"
    )
    print(
        f"Posture score: "
        f"{report.posture_score}"
    )
    print(
        f"Control score: "
        f"{report.control_score}"
    )
    print(
        f"Average repetition score: "
        f"{report.average_repetition_score}"
    )
    print(
        f"Best repetition score: "
        f"{report.best_repetition_score}"
    )
    print(
        f"Worst repetition score: "
        f"{report.worst_repetition_score}"
    )
    print(
        f"Rating: "
        f"{report.rating}"
    )

    print()
    print("Repetition scores:")

    for repetition in report.repetition_scores:
        print(
            f"- Rep "
            f"{repetition.repetition_number}: "
            f"{repetition.overall_score} "
            f"({repetition.rating})"
        )

    print()
    print(
        f"Warnings: {report.warnings}"
    )

    assert report.exercise == "squat"
    assert report.total_repetitions == 5
    assert report.performance_score > 0

    assert (
        0 <= report.best_frame_score <= 100
    )

    assert (
        0 <= report.worst_frame_score <= 100
    )

    assert (
        0 <= report.depth_score <= 100
    )

    assert (
        0 <= report.posture_score <= 100
    )

    assert (
        0 <= report.control_score <= 100
    )

    assert (
        len(report.repetition_scores) == 5
    )

    print()
    print(
        "Gym Trainer Performance Service "
        "test passed successfully."
    )


def main():
    test_performance_service()


if __name__ == "__main__":
    main()