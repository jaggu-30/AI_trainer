from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.models.chat import ChatMessage, ChatSession
from app.models.iot import (
    IoTCommand,
    IoTEquipment,
    IoTTelemetry,
)
from app.models.nutrition import NutritionLog
from app.models.user import User
from app.models.workout import WorkoutSession
from app.services.admin import AdminService


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


def test_admin_summary_empty_database():
    db = TestingSessionLocal()

    try:
        service = AdminService()

        result = service.generate_summary(
            db=db,
        )

        assert result.users.total_users == 0
        assert result.users.active_users == 0
        assert result.users.inactive_users == 0
        assert result.users.admin_users == 0

        assert (
            result.workouts.total_workouts
            == 0
        )

        assert (
            result.nutrition.total_food_entries
            == 0
        )

        assert (
            result.chat.total_sessions
            == 0
        )

        assert (
            result.smart_gym.equipment_count
            == 0
        )

    finally:
        db.close()


def test_admin_summary_counts_users():
    db = TestingSessionLocal()

    try:
        users = [
            User(
                full_name="Admin User",
                email="admin@test.com",
                password_hash="hash",
                is_active=True,
                is_admin=True,
            ),
            User(
                full_name="Active User",
                email="active@test.com",
                password_hash="hash",
                is_active=True,
                is_admin=False,
            ),
            User(
                full_name="Inactive User",
                email="inactive@test.com",
                password_hash="hash",
                is_active=False,
                is_admin=False,
            ),
        ]

        db.add_all(users)
        db.commit()

        result = AdminService().generate_summary(
            db=db,
        )

        assert result.users.total_users == 3
        assert result.users.active_users == 2
        assert result.users.inactive_users == 1
        assert result.users.admin_users == 1

    finally:
        db.close()


def test_admin_summary_counts_workouts():
    db = TestingSessionLocal()

    try:
        user = User(
            full_name="Workout User",
            email="workout@test.com",
            password_hash="hash",
            is_active=True,
            is_admin=False,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        workout = WorkoutSession(
            user_id=user.id,
            exercise="squat",
            total_repetitions=10,
            performance_score=80.0,
            best_frame_score=88.0,
            worst_frame_score=72.0,
            depth_score=80.0,
            posture_score=82.0,
            control_score=78.0,
            average_repetition_score=80.0,
            best_repetition_score=85.0,
            worst_repetition_score=75.0,
            rating="good",
            warnings=None,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )

        db.add(workout)
        db.commit()

        result = AdminService().generate_summary(
            db=db,
        )

        assert (
            result.workouts.total_workouts
            == 1
        )

        assert (
            result.workouts.total_repetitions
            == 10
        )

        assert (
            result.workouts.average_performance_score
            == 80.0
        )

        assert (
            result.workouts.best_performance_score
            == 80.0
        )

    finally:
        db.close()


def test_admin_summary_counts_nutrition():
    db = TestingSessionLocal()

    try:
        user = User(
            full_name="Nutrition User",
            email="nutrition@test.com",
            password_hash="hash",
            is_active=True,
            is_admin=False,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        nutrition = NutritionLog(
            user_id=user.id,
            food_name="Oats",
            quantity=80.0,
            calories=300.0,
            protein_g=10.0,
            carbohydrates_g=50.0,
            fat_g=7.0,
            consumed_at=datetime.utcnow(),
        )

        db.add(nutrition)
        db.commit()

        result = AdminService().generate_summary(
            db=db,
        )

        assert (
            result.nutrition.total_food_entries
            == 1
        )

        assert (
            result.nutrition.total_calories
            == 300.0
        )

        assert (
            result.nutrition.total_protein_g
            == 10.0
        )

        assert (
            result.nutrition.total_carbohydrates_g
            == 50.0
        )

        assert (
            result.nutrition.total_fat_g
            == 7.0
        )

    finally:
        db.close()


def test_admin_summary_counts_chat():
    db = TestingSessionLocal()

    try:
        user = User(
            full_name="Chat User",
            email="chat@test.com",
            password_hash="hash",
            is_active=True,
            is_admin=False,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        session = ChatSession(
            user_id=user.id,
            title="Admin Test Chat",
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        messages = [
            ChatMessage(
                session_id=session.id,
                role="user",
                content="Hello",
            ),
            ChatMessage(
                session_id=session.id,
                role="assistant",
                content="Hello!",
            ),
            ChatMessage(
                session_id=session.id,
                role="user",
                content="How is my progress?",
            ),
        ]

        db.add_all(messages)
        db.commit()

        result = AdminService().generate_summary(
            db=db,
        )

        assert (
            result.chat.total_sessions
            == 1
        )

        assert (
            result.chat.total_messages
            == 3
        )

        assert (
            result.chat.user_messages
            == 2
        )

        assert (
            result.chat.assistant_messages
            == 1
        )

    finally:
        db.close()


def test_admin_summary_counts_smart_gym():
    db = TestingSessionLocal()

    try:
        equipment = IoTEquipment(
            equipment_id="ADMIN-EQ-001",
            equipment_type="resistance_machine",
            current_resistance=10.0,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(equipment)
        db.commit()
        db.refresh(equipment)

        telemetry = IoTTelemetry(
            equipment_id=equipment.id,
            resistance_level=10.0,
            repetitions=12,
            performance_score=90.0,
            heart_rate=120.0,
            fatigue_level=20.0,
            recorded_at=datetime.utcnow(),
        )

        db.add(telemetry)

        increase = IoTCommand(
            equipment_id=equipment.id,
            action="increase_resistance",
            value=1.0,
            reason="Performance is high.",
            created_at=datetime.utcnow(),
        )

        decrease = IoTCommand(
            equipment_id=equipment.id,
            action="decrease_resistance",
            value=2.0,
            reason="Fatigue is high.",
            created_at=datetime.utcnow(),
        )

        db.add_all(
            [
                increase,
                decrease,
            ]
        )

        db.commit()

        result = AdminService().generate_summary(
            db=db,
        )

        assert (
            result.smart_gym.equipment_count
            == 1
        )

        assert (
            result.smart_gym.telemetry_samples
            == 1
        )

        assert (
            result.smart_gym.total_commands
            == 2
        )

        assert (
            result.smart_gym.increase_commands
            == 1
        )

        assert (
            result.smart_gym.decrease_commands
            == 1
        )

    finally:
        db.close()