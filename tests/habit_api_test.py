from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_current_user
from app.db.database import Base, get_db
from app.main import app
from app.models.chat import ChatMessage, ChatSession
from app.services.chat import add_chat_message


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


Base.metadata.create_all(bind=engine)


class MockUser:
    def __init__(
        self,
        user_id: int = 1,
        fitness_goal: str = "weight_loss",
    ):
        self.id = user_id
        self.full_name = "Habit Test User"
        self.age = 25
        self.height_cm = 175
        self.weight_kg = 70
        self.activity_level = "moderate"
        self.fitness_goal = fitness_goal
        self.dietary_preference = "balanced"


def create_user_chat_data(
    db,
    user_id: int,
    messages: list[dict],
):
    session = ChatSession(
        user_id=user_id,
        title="Habit Test Session",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    for item in messages:
        add_chat_message(
            db=db,
            session=session,
            role="user",
            content=item["content"],
            sentiment=item["sentiment"],
            emotion=item["emotion"],
            motivation_level=item[
                "motivation_level"
            ],
        )

    return session


def test_habit_analysis_requires_authentication():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/habits/analysis"
        )

    assert response.status_code == 401


def test_habit_analysis_empty_history():
    db = TestingSessionLocal()

    user = MockUser(
        user_id=1,
    )

    def override_get_db():
        yield db

    def override_get_current_user():
        return user

    app.dependency_overrides[
        get_db
    ] = override_get_db

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/habits/analysis"
            )

        assert response.status_code == 200

        data = response.json()

        assert data["memory"]["total_messages"] == 0

        assert (
            data["behavior"]["risk_level"]
            == "low"
        )

        assert (
            data["behavior"][
                "behavioral_risk_score"
            ]
            == 0.0
        )

        assert (
            data["skip_risk"]["level"]
            == "low"
        )

        assert (
            data["nudge"]["urgency"]
            == "low"
        )

        assert (
            data["schedule"]["action"]
            == "keep_schedule"
        )

    finally:
        app.dependency_overrides.clear()
        db.close()


def test_habit_analysis_detects_high_risk_behavior():
    db = TestingSessionLocal()

    user = MockUser(
        user_id=2,
        fitness_goal="weight_loss",
    )

    create_user_chat_data(
        db=db,
        user_id=user.id,
        messages=[
            {
                "content": "I feel stressed.",
                "sentiment": "negative",
                "emotion": "stressed",
                "motivation_level": "low",
            },
            {
                "content": "I want to skip my workout.",
                "sentiment": "negative",
                "emotion": "unmotivated",
                "motivation_level": "low",
            },
            {
                "content": "I am stressed and unmotivated.",
                "sentiment": "negative",
                "emotion": "stressed",
                "motivation_level": "low",
            },
            {
                "content": "I want to quit.",
                "sentiment": "negative",
                "emotion": "unmotivated",
                "motivation_level": "low",
            },
        ],
    )

    def override_get_db():
        yield db

    def override_get_current_user():
        return user

    app.dependency_overrides[
        get_db
    ] = override_get_db

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/habits/analysis"
            )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["memory"]["total_messages"]
            == 4
        )

        assert (
            data["memory"]["negative_messages"]
            == 4
        )

        assert (
            data["memory"]["unmotivated_count"]
            == 2
        )

        assert (
            data["memory"]["stressed_count"]
            == 2
        )

        assert (
            data["memory"]["low_motivation_count"]
            == 4
        )

        assert (
            data["memory"][
                "motivation_trend"
            ]
            == "declining"
        )

        assert (
            data["behavior"]["risk_level"]
            == "high"
        )

        assert (
            data["skip_risk"]["level"]
            == "high"
        )

        assert (
            data["skip_risk"]["probability"]
            >= 70.0
        )

        assert (
            data["nudge"]["urgency"]
            == "high"
        )

        assert (
            data["nudge"]["action"]
            == "send_immediate_nudge"
        )

        assert (
            data["schedule"]["action"]
            == "reduce_workout_load"
        )

        assert (
            data["schedule"]["duration_minutes"]
            == 20
        )

    finally:
        app.dependency_overrides.clear()
        db.close()


def test_habit_analysis_is_user_scoped():
    db = TestingSessionLocal()

    first_user = MockUser(
        user_id=3,
        fitness_goal="weight_loss",
    )

    second_user = MockUser(
        user_id=4,
        fitness_goal="maintenance",
    )

    create_user_chat_data(
        db=db,
        user_id=first_user.id,
        messages=[
            {
                "content": "I want to skip my workout.",
                "sentiment": "negative",
                "emotion": "unmotivated",
                "motivation_level": "low",
            },
        ],
    )

    create_user_chat_data(
        db=db,
        user_id=second_user.id,
        messages=[
            {
                "content": "I feel great today.",
                "sentiment": "positive",
                "emotion": "positive",
                "motivation_level": "high",
            },
        ],
    )

    def override_get_db():
        yield db

    app.dependency_overrides[
        get_db
    ] = override_get_db

    try:
        app.dependency_overrides[
            get_current_user
        ] = lambda: first_user

        with TestClient(app) as client:
            first_response = client.get(
                "/api/v1/habits/analysis"
            )

        assert (
            first_response.status_code
            == 200
        )

        first_data = first_response.json()

        assert (
            first_data["memory"][
                "total_messages"
            ]
            == 1
        )

        assert (
            first_data["memory"][
                "unmotivated_count"
            ]
            == 1
        )

        app.dependency_overrides[
            get_current_user
        ] = lambda: second_user

        with TestClient(app) as client:
            second_response = client.get(
                "/api/v1/habits/analysis"
            )

        assert (
            second_response.status_code
            == 200
        )

        second_data = second_response.json()

        assert (
            second_data["memory"][
                "total_messages"
            ]
            == 1
        )

        assert (
            second_data["memory"][
                "positive_messages"
            ]
            == 1
        )

        assert (
            second_data["memory"][
                "unmotivated_count"
            ]
            == 0
        )

    finally:
        app.dependency_overrides.clear()
        db.close()


def test_habit_analysis_response_structure():
    db = TestingSessionLocal()

    user = MockUser(
        user_id=5,
    )

    def override_get_db():
        yield db

    def override_get_current_user():
        return user

    app.dependency_overrides[
        get_db
    ] = override_get_db

    app.dependency_overrides[
        get_current_user
    ] = override_get_current_user

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/habits/analysis"
            )

        assert response.status_code == 200

        data = response.json()

        assert set(data.keys()) == {
            "memory",
            "behavior",
            "skip_risk",
            "nudge",
            "schedule",
        }

        assert set(
            data["behavior"].keys()
        ) == {
            "consistency_score",
            "motivation_score",
            "emotional_stability_score",
            "behavioral_risk_score",
            "risk_level",
        }

        assert set(
            data["skip_risk"].keys()
        ) == {
            "probability",
            "level",
            "reason",
        }

        assert set(
            data["nudge"].keys()
        ) == {
            "message",
            "urgency",
            "action",
        }

        assert set(
            data["schedule"].keys()
        ) == {
            "action",
            "intensity",
            "duration_minutes",
            "reason",
        }

    finally:
        app.dependency_overrides.clear()
        db.close()