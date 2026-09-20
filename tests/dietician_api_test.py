import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


client = TestClient(app)


@pytest.fixture
def authenticated_client():
    """
    Return a TestClient with the authentication dependency
    overridden for deterministic API testing.

    The Dietician endpoint only needs an authenticated user;
    it does not access the user object itself.
    """

    def override_get_current_user():
        return object()

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        yield client
    finally:
        app.dependency_overrides.clear()


def test_dietician_health():
    response = client.get(
        "/api/v1/dietician/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "dietician"


def test_dietician_calculate_requires_authentication():
    response = client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "weight_loss",
        },
    )

    assert response.status_code == 401


def test_dietician_calculate_success(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "weight_loss",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["bmi"] == 22.86
    assert data["bmi_category"] == "normal"

    assert data["bmr"] == 1673.75

    assert data["activity_multiplier"] == 1.55
    assert data["activity_level"] == "moderate"

    assert data["calorie_target"] == 2094.31
    assert data["calorie_adjustment"] == -500.0

    assert data["protein_g"] == 112.0
    assert data["carbohydrates_g"] == 280.67
    assert data["fat_g"] == 58.18


def test_dietician_calculate_maintenance(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["bmi"] == 22.86
    assert data["bmi_category"] == "normal"

    assert data["bmr"] == 1673.75
    assert data["calorie_target"] == 2594.31
    assert data["calorie_adjustment"] == 0.0


def test_dietician_calculate_weight_gain(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "weight_gain",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["calorie_target"] == 2894.31
    assert data["calorie_adjustment"] == 300.0


def test_dietician_calculate_case_insensitive(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "MALE",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "MODERATE",
            "goal": "MAINTENANCE",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["bmi"] == 22.86
    assert data["bmi_category"] == "normal"
    assert data["calorie_target"] == 2594.31


def test_dietician_invalid_sex(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "other",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert "sex" in data["detail"].lower()


def test_dietician_invalid_activity_level(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "unknown",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert (
        "activity"
        in data["detail"].lower()
    )


def test_dietician_invalid_goal(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "unknown",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert "goal" in data["detail"].lower()


def test_dietician_invalid_age(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 12,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 422


def test_dietician_invalid_height(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 99,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 422


def test_dietician_invalid_weight(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 24,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 422


def test_dietician_missing_required_field(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
        },
    )

    assert response.status_code == 422


def test_dietician_response_has_all_fields(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/v1/dietician/calculate",
        json={
            "age": 25,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity_level": "moderate",
            "goal": "maintenance",
        },
    )

    assert response.status_code == 200

    data = response.json()

    expected_fields = {
        "bmi",
        "bmi_category",
        "bmr",
        "activity_multiplier",
        "activity_level",
        "calorie_target",
        "calorie_adjustment",
        "protein_g",
        "carbohydrates_g",
        "fat_g",
    }

    assert set(data.keys()) == expected_fields