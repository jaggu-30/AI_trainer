from datetime import datetime

from pydantic import BaseModel, Field


class WorkoutAnalyticsResponse(BaseModel):
    """Workout statistics for an authenticated user."""

    total_workouts: int = Field(ge=0)
    total_repetitions: int = Field(ge=0)
    average_performance_score: float = Field(
        ge=0,
        le=100,
    )
    best_performance_score: float = Field(
        ge=0,
        le=100,
    )


class NutritionAnalyticsResponse(BaseModel):
    """Nutrition statistics for an authenticated user."""

    total_food_entries: int = Field(ge=0)
    total_calories: float = Field(ge=0)
    total_protein_g: float = Field(ge=0)
    total_carbohydrates_g: float = Field(ge=0)
    total_fat_g: float = Field(ge=0)


class SmartGymAnalyticsResponse(BaseModel):
    """Smart Gym equipment and AI command statistics."""

    equipment_count: int = Field(ge=0)
    telemetry_samples: int = Field(ge=0)
    average_performance_score: float = Field(
        ge=0,
        le=100,
    )
    average_fatigue_level: float = Field(
        ge=0,
        le=100,
    )
    average_heart_rate: float = Field(
        ge=0,
    )
    average_resistance: float = Field(
        ge=0,
    )
    total_commands: int = Field(ge=0)
    increase_commands: int = Field(ge=0)
    decrease_commands: int = Field(ge=0)


class FitnessAnalyticsResponse(BaseModel):
    """Unified analytics response."""

    generated_at: datetime
    workouts: WorkoutAnalyticsResponse
    nutrition: NutritionAnalyticsResponse
    smart_gym: SmartGymAnalyticsResponse