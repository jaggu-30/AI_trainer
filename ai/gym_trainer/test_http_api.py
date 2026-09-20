import sys
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BACKEND_ROOT))


from ai.gym_trainer.simulator import create_squat_landmarks


API_URL = "http://127.0.0.1:8000/api/v1/gym-trainer/frame"


def main():
    print("Testing Gym Trainer HTTP API...")
    print()

    landmarks = create_squat_landmarks(
        knee_angle=90.0,
        torso_lean=5.0,
    )

    payload = {
        "exercise": "squat",
        "landmarks": [
            {
                "name": landmark.name,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility,
            }
            for landmark in landmarks
        ],
    }

    print(f"Sending landmarks: {len(landmarks)}")

    response = requests.post(
        API_URL,
        json=payload,
        timeout=10,
    )

    print(f"HTTP status: {response.status_code}")
    print()

    data = response.json()

    print(f"Exercise: {data['exercise']}")
    print(f"Knee angle: {data['knee_angle']}")
    print(f"Phase: {data['phase']}")
    print(f"Repetitions: {data['repetitions']}")
    print(f"Depth score: {data['depth_score']}")
    print(f"Posture score: {data['posture_score']}")
    print(f"Control score: {data['control_score']}")
    print(f"Form score: {data['form_score']}")
    print(f"Rating: {data['rating']}")

    print()
    print("Feedback:")

    for message in data["feedback"]:
        print(f"- {message}")

    assert response.status_code == 200
    assert data["exercise"] == "squat"
    assert data["knee_angle"] > 0
    assert 0 <= data["form_score"] <= 100
    assert data["rating"] in {
        "excellent",
        "good",
        "needs_improvement",
        "poor",
    }
    assert len(data["feedback"]) == 3

    print()
    print("Gym Trainer HTTP API test passed successfully.")


if __name__ == "__main__":
    main()