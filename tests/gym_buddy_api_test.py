from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_current_user
from app.db.database import Base, get_db
from app.main import app
from app.models.chat import ChatMessage, ChatSession
from app.services.ai.gym_buddy_service import GymBuddyService
from app.api.routes import chat as chat_route


DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_test_database():
    Base.metadata.create_all(bind=engine)


def drop_test_database():
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_database():
    create_test_database()

    try:
        yield
    finally:
        drop_test_database()


@pytest.fixture
def db_session(test_database):
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_client(db_session):
    current_user = SimpleNamespace(
        id=1,
        full_name="Test User",
        age=25,
        height_cm=175,
        weight_kg=70,
        activity_level="moderate",
        fitness_goal="weight_loss",
        dietary_preference="balanced",
    )

    def override_get_db():
        yield db_session

    def override_get_current_user():
        return current_user

    app.dependency_overrides[
        get_db
    ] = override_get_db

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    with TestClient(app) as client:
        yield client, current_user

    app.dependency_overrides.clear()


def patch_dietician_response(monkeypatch):
    def fake_respond(
        self,
        db,
        user,
        user_message,
        sex,
    ):
        return (
            "Your nutrition profile is being tracked "
            "and your fitness goal is weight_loss.",
            "general",
        )

    monkeypatch.setattr(
        chat_route.DieticianChatService,
        "respond",
        fake_respond,
    )


def test_create_chat_session(test_client):
    client, current_user = test_client

    response = client.post(
        "/api/v1/chat/sessions",
        json={
            "title": "My Gym Buddy Chat",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["title"] == "My Gym Buddy Chat"

    with TestingSessionLocal() as db:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == data["id"]
            )
            .first()
        )

        assert session is not None
        assert session.user_id == current_user.id


def test_list_chat_sessions(test_client):
    client, _ = test_client

    client.post(
        "/api/v1/chat/sessions",
        json={
            "title": "Session One",
        },
    )

    client.post(
        "/api/v1/chat/sessions",
        json={
            "title": "Session Two",
        },
    )

    response = client.get(
        "/api/v1/chat/sessions"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 2
    assert len(data["items"]) >= 2


def test_chat_creates_session_and_persists_messages(
    test_client,
    monkeypatch,
):
    client, current_user = test_client

    patch_dietician_response(monkeypatch)

    response = client.post(
        "/api/v1/chat",
        json={
            "message": (
                "I feel great and motivated today."
            ),
            "sex": "male",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] > 0
    assert data["message_id"] > 0

    assert data["message"]
    assert data["intent"]

    assert data["sentiment"] == "positive"
    assert data["emotion"] == "positive"
    assert data["motivation_level"] == "high"
    assert data["strategy"] == (
        "positive_reinforcement"
    )

    with TestingSessionLocal() as db:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id
                == data["session_id"]
            )
            .first()
        )

        assert session is not None
        assert session.user_id == current_user.id

        messages = (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id
                == data["session_id"]
            )
            .order_by(ChatMessage.id.asc())
            .all()
        )

        assert len(messages) == 2

        assert messages[0].role == "user"
        assert (
            messages[0].content
            == "I feel great and motivated today."
        )

        assert messages[1].role == "assistant"
        assert messages[1].content == data["message"]


def test_unmotivated_message_uses_gym_buddy_response(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    response = client.post(
        "/api/v1/chat",
        json={
            "message": (
                "I don't feel like training today."
            ),
            "sex": "male",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["emotion"] == "unmotivated"
    assert data["motivation_level"] == "low"
    assert data["strategy"] == "motivation_support"

    assert "motivation is low" in data["message"]


def test_stressed_message_uses_gym_buddy_response(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "I feel very stressed today.",
            "sex": "male",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["emotion"] == "stressed"
    assert data["motivation_level"] == "low"
    assert data["strategy"] == "stress_support"

    assert "Recovery matters" in data["message"]


def test_chat_history_contains_persisted_messages(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    chat_response = client.post(
        "/api/v1/chat",
        json={
            "message": "I feel great today.",
            "sex": "male",
        },
    )

    assert chat_response.status_code == 200

    session_id = chat_response.json()["session_id"]

    history_response = client.get(
        f"/api/v1/chat/sessions/{session_id}"
    )

    assert history_response.status_code == 200

    data = history_response.json()

    assert data["session"]["id"] == session_id
    assert len(data["messages"]) == 2

    assert data["messages"][0]["role"] == "user"
    assert (
        data["messages"][0]["content"]
        == "I feel great today."
    )

    assert (
        data["messages"][1]["role"]
        == "assistant"
    )


def test_chat_reuses_existing_session(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    first_response = client.post(
        "/api/v1/chat",
        json={
            "message": "I feel great today.",
            "sex": "male",
        },
    )

    assert first_response.status_code == 200

    first_session_id = (
        first_response.json()["session_id"]
    )

    second_response = client.post(
        "/api/v1/chat",
        json={
            "message": "I am still motivated.",
            "sex": "male",
            "session_id": first_session_id,
        },
    )

    assert second_response.status_code == 200

    second_session_id = (
        second_response.json()["session_id"]
    )

    assert (
        second_session_id
        == first_session_id
    )

    with TestingSessionLocal() as db:
        messages = (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id
                == first_session_id
            )
            .order_by(ChatMessage.id.asc())
            .all()
        )

        assert len(messages) == 4


def test_chat_invalid_session_returns_404(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello gym buddy.",
            "sex": "male",
            "session_id": 999999,
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Chat session not found."
    )


def test_session_history_not_accessible_to_other_user(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    create_response = client.post(
        "/api/v1/chat/sessions",
        json={
            "title": "Private Session",
        },
    )

    assert create_response.status_code == 201

    session_id = (
        create_response.json()["id"]
    )

    second_user = SimpleNamespace(
        id=2,
        full_name="Second User",
        age=30,
        height_cm=180,
        weight_kg=80,
        activity_level="moderate",
        fitness_goal="maintenance",
        dietary_preference="balanced",
    )

    original_override = (
        app.dependency_overrides[
            get_current_user
        ]
    )

    app.dependency_overrides[
        get_current_user
    ] = lambda: second_user

    try:
        response = client.get(
            f"/api/v1/chat/sessions/{session_id}"
        )

        assert response.status_code == 404

        assert (
            response.json()["detail"]
            == "Chat session not found."
        )

    finally:
        app.dependency_overrides[
            get_current_user
        ] = original_override


def test_delete_chat_session(
    test_client,
):
    client, _ = test_client

    create_response = client.post(
        "/api/v1/chat/sessions",
        json={
            "title": "Delete Me",
        },
    )

    assert create_response.status_code == 201

    session_id = (
        create_response.json()["id"]
    )

    delete_response = client.delete(
        f"/api/v1/chat/sessions/{session_id}"
    )

    assert delete_response.status_code == 204

    history_response = client.get(
        f"/api/v1/chat/sessions/{session_id}"
    )

    assert history_response.status_code == 404


def test_empty_message_is_rejected(
    test_client,
):
    client, _ = test_client

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
            "sex": "male",
        },
    )

    assert response.status_code == 422


def test_missing_sex_is_rejected(
    test_client,
):
    client, _ = test_client

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello gym buddy.",
        },
    )

    assert response.status_code == 422


def test_chat_response_has_expected_fields(
    test_client,
    monkeypatch,
):
    client, _ = test_client

    patch_dietician_response(monkeypatch)

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "I feel great today.",
            "sex": "male",
        },
    )

    assert response.status_code == 200

    data = response.json()

    expected_fields = {
        "session_id",
        "message_id",
        "message",
        "intent",
        "sentiment",
        "emotion",
        "motivation_level",
        "emotion_confidence",
        "strategy",
    }

    assert set(data.keys()) == expected_fields


def test_gym_buddy_service_uses_history(
    monkeypatch,
):
    captured = {}

    original_analyze = GymBuddyService.analyze

    def wrapped_analyze(
        self,
        user,
        message,
        history=None,
    ):
        captured["history"] = list(
            history or []
        )

        return original_analyze(
            self,
            user=user,
            message=message,
            history=history,
        )

    monkeypatch.setattr(
        GymBuddyService,
        "analyze",
        wrapped_analyze,
    )

    service = GymBuddyService()

    user = SimpleNamespace(
        fitness_goal="weight_loss"
    )

    history = [
        SimpleNamespace(
            role="user",
            sentiment="negative",
            emotion="stressed",
            motivation_level="low",
        )
    ]

    result = service.analyze(
        user=user,
        message="I feel better today.",
        history=history,
    )

    assert result.response.strategy == (
        "positive_reinforcement"
    )

    assert len(captured["history"]) == 1
    assert (
        captured["history"][0].emotion
        == "stressed"
    )