import time
from uuid import uuid4

import requests
from ai.gym_trainer.simulator import generate_squat_sequence


BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/api/v1/auth/register"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
PERFORMANCE_URL = f"{BASE_URL}/api/v1/gym-trainer/performance"


def build_frames():
    """Convert simulated landmarks into API request frames."""

    landmarks_sequence = generate_squat_sequence(
        repetitions=5
    )

    frames = []

    for landmarks in landmarks_sequence:
        frame = []

        for landmark in landmarks:
            frame.append(
                {
                    "name": landmark.name,
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z,
                    "visibility": landmark.visibility,
                }
            )

        frames.append(frame)

    return frames


def main():
    print("Testing authenticated Gym Trainer performance persistence...")

    unique_id = uuid4().hex[:10]

    user_payload = {
        "full_name": f"Integration Test {unique_id}",
        "email": f"integration_{unique_id}@example.com",
        "password": "IntegrationTest123!",
        "age": 25,
        "height_cm": 175,
        "weight_kg": 70,
        "fitness_goal": "strength",
        "dietary_preference": "balanced",
        "activity_level": "moderate",
    }

    print()
    print("1. Registering test user...")

    register_response = requests.post(
        REGISTER_URL,
        json=user_payload,
        timeout=30,
    )

    print(
        f"Registration HTTP status: "
        f"{register_response.status_code}"
    )

    register_response.raise_for_status()

    registered_user = register_response.json()

    print(
        f"Registered user ID: "
        f"{registered_user['id']}"
    )

    print()
    print("2. Logging in test user...")

    login_response = requests.post(
        LOGIN_URL,
        data={
            "username": user_payload["email"],
            "password": user_payload["password"],
        },
        timeout=30,
    )

    print(
        f"Login HTTP status: "
        f"{login_response.status_code}"
    )

    login_response.raise_for_status()

    token_data = login_response.json()
    access_token = token_data["access_token"]

    assert token_data["token_type"] == "bearer"
    assert access_token

    print("JWT access token received successfully.")

    print()
    print("3. Generating simulated squat workout...")

    frames = build_frames()

    print(f"Frames generated: {len(frames)}")
    print(
        f"Landmarks per frame: "
        f"{len(frames[0])}"
    )

    payload = {
        "exercise": "squat",
        "frames": frames,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    print()
    print("4. Sending authenticated performance request...")

    performance_response = requests.post(
        PERFORMANCE_URL,
        json=payload,
        headers=headers,
        timeout=120,
    )

    print(
        f"Performance HTTP status: "
        f"{performance_response.status_code}"
    )

    performance_response.raise_for_status()

    report = performance_response.json()

    print()
    print(f"Exercise: {report['exercise']}")
    print(
        f"Total repetitions: "
        f"{report['total_repetitions']}"
    )
    print(
        f"Performance score: "
        f"{report['performance_score']}"
    )
    print(
        f"Rating: "
        f"{report['rating']}"
    )

    assert report["exercise"] == "squat"
    assert report["total_repetitions"] == 5
    assert report["performance_score"] > 0
    assert len(report["repetition_scores"]) == 5

    print()
    print("5. Verifying authenticated user profile...")

    me_response = requests.get(
        f"{BASE_URL}/api/v1/auth/me",
        headers=headers,
        timeout=30,
    )

    print(
        f"Profile HTTP status: "
        f"{me_response.status_code}"
    )

    me_response.raise_for_status()

    current_user = me_response.json()

    assert current_user["id"] == registered_user["id"]
    assert current_user["email"] == user_payload["email"]

    print(
        f"Authenticated user ID: "
        f"{current_user['id']}"
    )

    print()
    print(
        "Waiting briefly for the database transaction "
        "to become visible..."
    )

    time.sleep(0.5)

    print()
    print("Authenticated performance integration test passed successfully.")


if __name__ == "__main__":
    main()
