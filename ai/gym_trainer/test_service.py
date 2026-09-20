from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))

from app.services.ai.gym_trainer.service import GymTrainerService
from ai.gym_trainer.simulator import create_squat_landmarks


def main():
    print("Testing Gym Trainer service...")
    print()

    service = GymTrainerService()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    result = service.process(
        exercise="squat",
        landmarks=landmarks,
    )

    assert result is not None

    print(f"Exercise: {result['exercise']}")
    print(f"Knee angle: {result['knee_angle']}")
    print(f"Phase: {result['phase']}")
    print(f"Repetitions: {result['repetitions']}")
    print(f"Form score: {result['form_score']}")
    print(f"Rating: {result['rating']}")

    print("Feedback:")

    for message in result["feedback"]:
        print(f"- {message}")

    assert result["exercise"] == "squat"
    assert result["repetitions"] == 0
    assert result["knee_angle"] > 0
    assert 0 <= result["form_score"] <= 100
    assert result["rating"] in {
        "excellent",
        "good",
        "needs_improvement",
        "poor",
    }
    assert len(result["feedback"]) == 3

    print()
    print("Testing unsupported exercise...")

    try:
        service.process(
            exercise="unknown_exercise",
            landmarks=landmarks,
        )
    except ValueError as error:
        print(f"Correctly rejected: {error}")
    else:
        raise AssertionError(
            "Unsupported exercise was not rejected."
        )

    print()
    print("Gym Trainer service test passed successfully.")


if __name__ == "__main__":
    main()