from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """Find a user by email address."""

    statement = select(User).where(User.email == email)

    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """Create a new user with a securely hashed password."""

    hashed_password = hash_password(user_data.password)

    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password,
        age=user_data.age,
        height_cm=user_data.height_cm,
        weight_kg=user_data.weight_kg,
        sex=user_data.sex,
        fitness_goal=user_data.fitness_goal,
        dietary_preference=user_data.dietary_preference,
        activity_level=user_data.activity_level,
        workout_preference=user_data.workout_preference,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user using email and password."""

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user


def create_user_access_token(user: User) -> str:
    """Create a JWT access token for an authenticated user."""

    return create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )
