from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


client = TestClient(app)


def create_user(
    user_id: int = 1,
    is_admin: bool = False,
):
    return SimpleNamespace(
        id=user_id,
        full_name="Admin API Test User",
        email="admin-api@test.com",
        is_admin=is_admin,
        is_active=True,
        age=25,
        height_cm=175,
        weight_kg=70,
        fitness_goal="weight_loss",
        dietary_preference="balanced",
        activity_level="moderate",
    )


def test_admin_summary_requires_authentication():
    app.dependency_overrides.clear()

    response = client.get(
        "/api/v1/admin/summary"
    )

    assert response.status_code == 401


def test_admin_summary_rejects_normal_user():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=1,
        is_admin=False,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 403

        data = response.json()

        assert (
            data["detail"]
            == "Administrator access required."
        )

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_accepts_admin_user():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=2,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        data = response.json()

        assert set(data.keys()) == {
            "users",
            "workouts",
            "nutrition",
            "chat",
            "smart_gym",
        }

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_user_section():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=3,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        users = response.json()["users"]

        assert set(users.keys()) == {
            "total_users",
            "active_users",
            "inactive_users",
            "admin_users",
        }

        assert users["total_users"] >= 0
        assert users["active_users"] >= 0
        assert users["inactive_users"] >= 0
        assert users["admin_users"] >= 0

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_workout_section():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=4,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        workouts = response.json()["workouts"]

        assert set(workouts.keys()) == {
            "total_workouts",
            "total_repetitions",
            "average_performance_score",
            "best_performance_score",
        }

        assert workouts["total_workouts"] >= 0
        assert workouts["total_repetitions"] >= 0

        assert (
            0
            <= workouts[
                "average_performance_score"
            ]
            <= 100
        )

        assert (
            0
            <= workouts[
                "best_performance_score"
            ]
            <= 100
        )

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_nutrition_section():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=5,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        nutrition = response.json()["nutrition"]

        assert set(nutrition.keys()) == {
            "total_food_entries",
            "total_calories",
            "total_protein_g",
            "total_carbohydrates_g",
            "total_fat_g",
        }

        assert (
            nutrition["total_food_entries"]
            >= 0
        )

        assert (
            nutrition["total_calories"]
            >= 0
        )

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_chat_section():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=6,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        chat = response.json()["chat"]

        assert set(chat.keys()) == {
            "total_sessions",
            "total_messages",
            "user_messages",
            "assistant_messages",
        }

        assert chat["total_sessions"] >= 0
        assert chat["total_messages"] >= 0
        assert chat["user_messages"] >= 0
        assert chat["assistant_messages"] >= 0

    finally:
        app.dependency_overrides.clear()


def test_admin_summary_smart_gym_section():
    app.dependency_overrides[
        get_current_user
    ] = lambda: create_user(
        user_id=7,
        is_admin=True,
    )

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

        smart_gym = response.json()[
            "smart_gym"
        ]

        assert set(
            smart_gym.keys()
        ) == {
            "equipment_count",
            "telemetry_samples",
            "total_commands",
            "increase_commands",
            "decrease_commands",
        }

        assert (
            smart_gym["equipment_count"]
            >= 0
        )

        assert (
            smart_gym["telemetry_samples"]
            >= 0
        )

        assert (
            smart_gym["total_commands"]
            >= 0
        )

    finally:
        app.dependency_overrides.clear()


def test_non_admin_flag_is_enforced():
    normal_user = create_user(
        user_id=8,
        is_admin=False,
    )

    app.dependency_overrides[
        get_current_user
    ] = lambda: normal_user

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 403

        assert (
            response.json()["detail"]
            == "Administrator access required."
        )

    finally:
        app.dependency_overrides.clear()


def test_admin_flag_allows_access():
    admin_user = create_user(
        user_id=9,
        is_admin=True,
    )

    app.dependency_overrides[
        get_current_user
    ] = lambda: admin_user

    try:
        response = client.get(
            "/api/v1/admin/summary"
        )

        assert response.status_code == 200

    finally:
        app.dependency_overrides.clear()