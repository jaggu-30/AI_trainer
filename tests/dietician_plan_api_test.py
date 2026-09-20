from fastapi.testclient import TestClient
from app.api.dependencies import get_current_user
from app.main import app


client = TestClient(app)


def test_dietician_plan_requires_authentication():
    response = client.post(
        "/api/v1/dietician/plan",
        json={
            "sex": "male",
        },
    )

    assert response.status_code == 401


def test_dietician_plan_success():
    def override_get_current_user():
        class MockUser:
            age = 25
            height_cm = 175
            weight_kg = 70
            activity_level = "moderate"
            fitness_goal = "weight_loss"
            dietary_preference = "balanced"

        return MockUser()

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        response = client.post(
            "/api/v1/dietician/plan",
            json={
                "sex": "male",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["bmi"] == 22.86
        assert data["bmi_category"] == "normal"

        assert data["bmr"] == 1673.75

        assert (
            data["maintenance_calories"]
            == 2594.31
        )

        assert (
            data["target_calories"]
            == 2094.31
        )

        assert len(data["meals"]) == 4

        assert len(data["grocery_list"]) > 0

        meal_names = [
            meal["name"]
            for meal in data["meals"]
        ]

        assert (
            "Oatmeal with milk, banana and eggs"
            in meal_names
        )

    finally:
        app.dependency_overrides.clear()


def test_dietician_plan_uses_vegetarian_preference():
    def override_get_current_user():
        class MockUser:
            age = 25
            height_cm = 175
            weight_kg = 70
            activity_level = "moderate"
            fitness_goal = "maintenance"
            dietary_preference = "vegetarian"

        return MockUser()

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        response = client.post(
            "/api/v1/dietician/plan",
            json={
                "sex": "male",
            },
        )

        assert response.status_code == 200

        data = response.json()

        meal_names = [
            meal["name"]
            for meal in data["meals"]
        ]

        assert (
            "Rice, dal, paneer and mixed vegetables"
            in meal_names
        )

        grocery_names = [
            item["name"]
            for item in data["grocery_list"]
        ]

        assert "paneer" in grocery_names

    finally:
        app.dependency_overrides.clear()


def test_dietician_plan_missing_profile_value():
    def override_get_current_user():
        class MockUser:
            age = None
            height_cm = 175
            weight_kg = 70
            activity_level = "moderate"
            fitness_goal = "maintenance"
            dietary_preference = "balanced"

        return MockUser()

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        response = client.post(
            "/api/v1/dietician/plan",
            json={
                "sex": "male",
            },
        )

        assert response.status_code == 400

        data = response.json()

        assert (
            data["detail"]
            == "Age is required to generate "
            "a diet plan."
        )

    finally:
        app.dependency_overrides.clear()


def test_dietician_plan_invalid_sex():
    def override_get_current_user():
        class MockUser:
            age = 25
            height_cm = 175
            weight_kg = 70
            activity_level = "moderate"
            fitness_goal = "maintenance"
            dietary_preference = "balanced"

        return MockUser()

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        response = client.post(
            "/api/v1/dietician/plan",
            json={
                "sex": "other",
            },
        )

        assert response.status_code == 400

    finally:
        app.dependency_overrides.clear()