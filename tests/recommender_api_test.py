from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


client = TestClient(app)


def authenticated_user(
    fitness_goal="weight_loss",
):
    return SimpleNamespace(
        id=100,
        full_name="Recommendation Test User",
        age=25,
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        fitness_goal=fitness_goal,
        dietary_preference="balanced",
    )


def test_recommendation_api_requires_authentication():
    response = client.post(
        "/api/v1/recommendations",
        json={
            "gyms": [],
        },
    )

    assert response.status_code == 401


def test_recommendation_api_success():
    app.dependency_overrides[
        get_current_user
    ] = lambda: authenticated_user()

    try:
        response = client.post(
            "/api/v1/recommendations",
            json={
                "gyms": [
                    {
                        "name": "Weight Loss Gym",
                        "distance_km": 2,
                        "rating": 4.5,
                        "specialties": [
                            "weight loss",
                            "cardio",
                        ],
                    },
                    {
                        "name": "General Gym",
                        "distance_km": 5,
                        "rating": 4.0,
                        "specialties": [
                            "fitness",
                        ],
                    },
                ],
                "max_distance_km": 10,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert set(data.keys()) == {
            "gyms",
            "workouts",
            "challenges",
        }

        assert len(data["gyms"]) == 2
        assert len(data["workouts"]) == 3
        assert len(data["challenges"]) == 3

        assert (
            data["gyms"][0]["name"]
            == "Weight Loss Gym"
        )

        assert (
            data["workouts"][0]["goal"]
            == "weight_loss"
        )

        assert (
            data["challenges"][0]["goal"]
            == "weight_loss"
        )

    finally:
        app.dependency_overrides.clear()


def test_recommendation_api_distance_filter():
    app.dependency_overrides[
        get_current_user
    ] = lambda: authenticated_user()

    try:
        response = client.post(
            "/api/v1/recommendations",
            json={
                "gyms": [
                    {
                        "name": "Nearby Gym",
                        "distance_km": 3,
                        "rating": 4.5,
                        "specialties": [
                            "weight loss",
                        ],
                    },
                    {
                        "name": "Far Gym",
                        "distance_km": 20,
                        "rating": 5.0,
                        "specialties": [
                            "weight loss",
                        ],
                    },
                ],
                "max_distance_km": 10,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data["gyms"]) == 1

        assert (
            data["gyms"][0]["name"]
            == "Nearby Gym"
        )

    finally:
        app.dependency_overrides.clear()


def test_recommendation_api_strength_goal():
    app.dependency_overrides[
        get_current_user
    ] = lambda: authenticated_user(
        fitness_goal="strength"
    )

    try:
        response = client.post(
            "/api/v1/recommendations",
            json={
                "gyms": [
                    {
                        "name": "Strength Center",
                        "distance_km": 4,
                        "rating": 4.3,
                        "specialties": [
                            "strength",
                            "weights",
                        ],
                    },
                    {
                        "name": "General Gym",
                        "distance_km": 2,
                        "rating": 4.8,
                        "specialties": [
                            "fitness",
                        ],
                    },
                ],
                "max_distance_km": 10,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["workouts"][0]["name"]
            == "Beginner Strength Builder"
        )

        assert (
            data["challenges"][0]["name"]
            == "14-Day Strength Challenge"
        )

        assert (
            data["gyms"][0]["name"]
            == "Strength Center"
        )

    finally:
        app.dependency_overrides.clear()


def test_recommendation_api_empty_gyms():
    app.dependency_overrides[
        get_current_user
    ] = lambda: authenticated_user()

    try:
        response = client.post(
            "/api/v1/recommendations",
            json={
                "gyms": [],
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["gyms"] == []
        assert len(data["workouts"]) == 3
        assert len(data["challenges"]) == 3

    finally:
        app.dependency_overrides.clear()


def test_recommendation_api_invalid_distance():
    app.dependency_overrides[
        get_current_user
    ] = lambda: authenticated_user()

    try:
        response = client.post(
            "/api/v1/recommendations",
            json={
                "gyms": [],
                "max_distance_km": -1,
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()