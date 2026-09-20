from pydantic import BaseModel, Field


class UserProfileUpdate(BaseModel):
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