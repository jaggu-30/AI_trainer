import uuid

import requests

from ai.gym_trainer.simulator import generate_squat_sequence


BASE_URL = "http://127.0.0.1:8000"

REGISTER_URL = f"{BASE_URL}/api/v1/auth/register"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
PERFORMANCE_URL = (
    f"{BASE_URL}/api/v1/gym-trainer/performance"
)
WORKOUTS_URL = f"{BASE_URL}/api/v1/workouts"


def register_user(
    full_name: str,
    email: str,
    password: str,
) -> dict:
    response = requests.post(
        REGISTER_URL,
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
            "age": 25,
            "height_cm": 175,
            "weight_kg": 70,
            "fitness_goal": "strength",
            "dietary_preference": "balanced",
            "activity_level": "moderate",
        },
        timeout=30,
    )

    print(
        f"Registration status for {email}: "
        f"{response.status_code}"
    )

    response.raise_for_status()

    return response.json()


def login_user(
    email: str,
    password: str,
) -> str:
    response = requests.post(
        LOGIN_URL,
        data={
            "username": email,
            "password": password,
        },
        timeout=30,
    )

    print(
        f"Login status for {email}: "
        f"{response.status_code}"
    )

    response.raise_for_status()

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["access_token"]

    return data["access_token"]


def build_simulated_frames() -> list[list[dict]]:
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


def create_workout(
    token: str,
    frames: list[list[dict]],
) -> dict:
    response = requests.post(
        PERFORMANCE_URL,
        json={
            "exercise": "squat",
            "frames": frames,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=120,
    )

    print(
        f"Performance status: "
        f"{response.status_code}"
    )

    response.raise_for_status()

    data = response.json()

    assert data["exercise"] == "squat"
    assert data["total_repetitions"] == 5
    assert data["performance_score"] > 0

    return data


def get_workouts(token: str) -> list[dict]:
    response = requests.get(
        WORKOUTS_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=30,
    )

    print(
        f"Workout history status: "
        f"{response.status_code}"
    )

    response.raise_for_status()

    return response.json()


def main():
    print(
        "Testing workout history user isolation..."
    )

    unique_id = uuid.uuid4().hex[:10]

    user_a_email = (
        f"isolation_a_{unique_id}@example.com"
    )
    user_b_email = (
        f"isolation_b_{unique_id}@example.com"
    )
    password = "IsolationTest123!"

    print()
    print("1. Creating User A...")

    user_a = register_user(
        full_name="Isolation Test User A",
        email=user_a_email,
        password=password,
    )

    print(f"User A ID: {user_a['id']}")

    print()
    print("2. Logging in User A...")

    token_a = login_user(
        email=user_a_email,
        password=password,
    )

    print()
    print("3. Generating simulated workout...")

    frames = build_simulated_frames()

    print(f"Frames generated: {len(frames)}")
    print(
        f"Landmarks per frame: "
        f"{len(frames[0])}"
    )

    print()
    print("4. Creating workout for User A...")

    workout = create_workout(
        token=token_a,
        frames=frames,
    )

    print(
        f"User A workout score: "
        f"{workout['performance_score']}"
    )

    print()
    print("5. Checking User A workout history...")

    user_a_workouts = get_workouts(token_a)

    print(
        f"User A workout count: "
        f"{len(user_a_workouts)}"
    )

    assert len(user_a_workouts) >= 1

    assert any(
        item["total_repetitions"] == 5
        for item in user_a_workouts
    )

    print()
    print("6. Creating User B...")

    user_b = register_user(
        full_name="Isolation Test User B",
        email=user_b_email,
        password=password,
    )

    print(f"User B ID: {user_b['id']}")

    print()
    print("7. Logging in User B...")

    token_b = login_user(
        email=user_b_email,
        password=password,
    )

    print()
    print("8. Checking User B workout history...")

    user_b_workouts = get_workouts(token_b)

    print(
        f"User B workout count: "
        f"{len(user_b_workouts)}"
    )

    assert len(user_b_workouts) == 0

    print()
    print(
        "Workout history user isolation "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()
