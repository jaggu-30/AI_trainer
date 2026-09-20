from __future__ import annotations

import requests

from ai.gym_trainer.video_session_simulator import (
    SquatVideoSessionSimulator,
)


BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
PERFORMANCE_URL = f"{BASE_URL}/api/v1/performance/session"
ANALYTICS_URL = f"{BASE_URL}/api/v1/analytics/summary"


TEST_EMAIL = "iot-test-user@example.com"
TEST_PASSWORD = "Mypassword123"


def convert_frames_to_payload() -> list[list[dict]]:
    """Convert simulated landmarks into API-compatible dictionaries."""

    simulator = SquatVideoSessionSimulator(
        repetitions=5,
        fps=30.0,
    )

    frames: list[list[dict]] = []

    for frame in simulator.frames():
        frame_landmarks = []

        for landmark in frame.landmarks:
            frame_landmarks.append(
                {
                    "name": landmark.name,
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z,
                    "visibility": landmark.visibility,
                }
            )

        frames.append(frame_landmarks)

    return frames


def main() -> None:
    """Run the complete simulated workout persistence test."""

    print("Generating simulated workout frames...")

    frames = convert_frames_to_payload()

    print(
        f"Generated {len(frames)} simulated frames."
    )

    login_response = requests.post(
        LOGIN_URL,
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
        timeout=30,
    )

    login_response.raise_for_status()

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "exercise": "squat",
        "frames": frames,
    }

    print(
        "Submitting simulated workout session..."
    )

    response = requests.post(
        PERFORMANCE_URL,
        json=payload,
        headers=headers,
        timeout=60,
    )

    print(
        "HTTP status:",
        response.status_code,
    )

    response.raise_for_status()

    result = response.json()

    print("\nSaved workout:")
    print(
        result["workout"]
    )

    print("\nPerformance:")
    print(
        {
            "exercise": result["exercise"],
            "total_repetitions": result[
                "total_repetitions"
            ],
            "performance_score": result[
                "performance_score"
            ],
            "rating": result["rating"],
        }
    )

    analytics_response = requests.get(
        ANALYTICS_URL,
        headers=headers,
        timeout=30,
    )

    analytics_response.raise_for_status()

    analytics = analytics_response.json()

    print("\nUpdated workout analytics:")
    print(
        analytics["workouts"]
    )

    print(
        "\nWorkout session persistence test: PASSED"
    )


if __name__ == "__main__":
    main()