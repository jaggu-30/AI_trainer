from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AdminUserSummary(BaseModel):
    total_users: int = Field(ge=0)
    active_users: int = Field(ge=0)
    inactive_users: int = Field(ge=0)
    admin_users: int = Field(ge=0)


class AdminWorkoutSummary(BaseModel):
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


class AdminNutritionSummary(BaseModel):
    total_food_entries: int = Field(ge=0)
    total_calories: float = Field(ge=0)
    total_protein_g: float = Field(ge=0)
    total_carbohydrates_g: float = Field(ge=0)
    total_fat_g: float = Field(ge=0)


class AdminChatSummary(BaseModel):
    total_sessions: int = Field(ge=0)
    total_messages: int = Field(ge=0)
    user_messages: int = Field(ge=0)
    assistant_messages: int = Field(ge=0)


class AdminSmartGymSummary(BaseModel):
    equipment_count: int = Field(ge=0)
    telemetry_samples: int = Field(ge=0)
    total_commands: int = Field(ge=0)
    increase_commands: int = Field(ge=0)
    decrease_commands: int = Field(ge=0)


class AdminSummaryResponse(BaseModel):
    users: AdminUserSummary
    workouts: AdminWorkoutSummary
    nutrition: AdminNutritionSummary
    chat: AdminChatSummary
    smart_gym: AdminSmartGymSummary


class AdminUserResponse(BaseModel):
    """A privacy-conscious user record for the admin directory."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime


class AdminUserListResponse(BaseModel):
    items: list[AdminUserResponse]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)


class AdminUserStatusUpdate(BaseModel):
    is_active: bool
