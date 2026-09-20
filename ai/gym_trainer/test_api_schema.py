from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.simulator import create_squat_landmarks
from app.services.ai.gym_trainer.schemas import (
    GymTrainerFrameRequest,
    GymTrainerFrameResponse,
)


def main():
    print("Testing Gym Trainer API schemas...")
    print()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    landmark_data = [
        {
            "name": landmark.name,
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z,
            "visibility": landmark.visibility,
        }
        for landmark in landmarks
    ]

    request = GymTrainerFrameRequest(
        exercise="squat",
        landmarks=landmark_data,
    )

    print(f"Request exercise: {request.exercise}")
    print(f"Landmarks received: {len(request.landmarks)}")

    assert request.exercise == "squat"
    assert len(request.landmarks) == 33

    first_landmark = request.landmarks[0]

    print(f"First landmark: {first_landmark.name}")
    print(f"First landmark visibility: {first_landmark.visibility}")

    assert first_landmark.name
    assert 0.0 <= first_landmark.visibility <= 1.0

    response = GymTrainerFrameResponse(
        exercise="squat",
        knee_angle=90.0,
        phase="bottom",
        repetitions=0,
        depth_score=100.0,
        posture_score=80.0,
        control_score=86.93,
        form_score=90.08,
        rating="excellent",
        feedback=[
            "Good squat depth.",
            "Good torso posture.",
            "Movement appears stable.",
        ],
    )

    print()
    print(f"Response exercise: {response.exercise}")
    print(f"Form score: {response.form_score:.2f}")
    print(f"Rating: {response.rating}")
    print(f"Feedback count: {len(response.feedback)}")

    assert response.exercise == "squat"
    assert response.repetitions == 0
    assert 0 <= response.form_score <= 100
    assert response.rating in {
        "excellent",
        "good",
        "needs_improvement",
        "poor",
    }
    assert len(response.feedback) == 3

    print()
    print("Gym Trainer API schema test passed successfully.")


if __name__ == "__main__":
    main()