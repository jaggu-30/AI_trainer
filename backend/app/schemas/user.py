from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr

    age: int | None = Field(
        default=None,
        ge=13,
        le=120,
    )

    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )

    weight_kg: float | None = Field(
        default=None,
        gt=0,
        le=500,
    )

    fitness_goal: str | None = Field(
        default=None,
        max_length=100,
    )

    dietary_preference: str | None = Field(
        default=None,
        max_length=100,
    )

    activity_level: str | None = Field(
        default=None,
        max_length=50,
    )

    sex: str | None = Field(
        default=None,
        max_length=20,
    )

    workout_preference: str | None = Field(
        default=None,
        max_length=50,
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserProfileUpdate(BaseModel):
    """Editable fitness details for an authenticated user."""

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    age: int | None = Field(
        default=None,
        ge=13,
        le=120,
    )

    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )

    weight_kg: float | None = Field(
        default=None,
        gt=0,
        le=500,
    )

    sex: str | None = Field(
        default=None,
        max_length=20,
    )

    fitness_goal: str | None = Field(
        default=None,
        max_length=100,
    )

    dietary_preference: str | None = Field(
        default=None,
        max_length=100,
    )

    activity_level: str | None = Field(
        default=None,
        max_length=50,
    )

    workout_preference: str | None = Field(
        default=None,
        max_length=50,
    )


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
