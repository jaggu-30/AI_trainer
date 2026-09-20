from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NutritionLogCreate(BaseModel):
    """Create one food-intake entry."""

    food_name: str = Field(
        min_length=1,
        max_length=150,
    )

    quantity: float = Field(
        gt=0,
    )

    calories: float = Field(
        ge=0,
        le=10000,
    )

    protein_g: float = Field(
        ge=0,
        le=1000,
    )

    carbohydrates_g: float = Field(
        ge=0,
        le=1000,
    )

    fat_g: float = Field(
        ge=0,
        le=1000,
    )

    consumed_at: datetime | None = None


class NutritionLogResponse(BaseModel):
    """Return one saved nutrition-intake entry."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    food_name: str
    quantity: float
    calories: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float
    consumed_at: datetime


class NutritionSummaryResponse(BaseModel):
    """Return aggregated nutrition intake."""

    total_entries: int = Field(
        ge=0,
    )

    total_calories: float = Field(
        ge=0,
    )

    total_protein_g: float = Field(
        ge=0,
    )

    total_carbohydrates_g: float = Field(
        ge=0,
    )

    total_fat_g: float = Field(
        ge=0,
    )
