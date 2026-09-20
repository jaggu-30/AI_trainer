import sys
import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python test_workout_history.py <email> <password>"
        )

    email = sys.argv[1]
    password = sys.argv[2]

    print("Testing authenticated workout history...")

    login_response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
        timeout=30,
    )

    print(
        f"Login HTTP status: "
        f"{login_response.status_code}"
    )

    login_response.raise_for_status()

    token_data = login_response.json()

    assert token_data["token_type"] == "bearer"
    assert token_data["access_token"]

    token = token_data["access_token"]

    history_response = requests.get(
        f"{BASE_URL}/api/v1/workouts",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=30,
    )

    print(
        f"History HTTP status: "
        f"{history_response.status_code}"
    )

    history_response.raise_for_status()

    workouts = history_response.json()

    print(
        f"Workout count: "
        f"{len(workouts)}"
    )

    for workout in workouts:
        print()
        print(f"Workout ID: {workout['id']}")
        print(f"Exercise: {workout['exercise']}")
        print(
            f"Repetitions: "
            f"{workout['total_repetitions']}"
        )
        print(
            f"Performance: "
            f"{workout['performance_score']}"
        )
        print(f"Rating: {workout['rating']}")

    assert len(workouts) >= 1
    assert workouts[0]["exercise"] == "squat"
    assert workouts[0]["total_repetitions"] == 5

    print()
    print(
        "Authenticated workout history "
        "test passed successfully."
    )


if __name__ == "__main__":
    main()
