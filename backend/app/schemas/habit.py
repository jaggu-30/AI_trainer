from pydantic import BaseModel, Field


class HabitMemoryResponse(BaseModel):
    total_messages: int = Field(
        ge=0,
    )

    positive_messages: int = Field(
        ge=0,
    )

    negative_messages: int = Field(
        ge=0,
    )

    neutral_messages: int = Field(
        ge=0,
    )

    recent_sentiment: str
    recent_emotion: str
    recent_motivation_level: str

    unmotivated_count: int = Field(
        ge=0,
    )

    stressed_count: int = Field(
        ge=0,
    )

    low_motivation_count: int = Field(
        ge=0,
    )

    motivation_trend: str


class HabitBehaviorResponse(BaseModel):
    consistency_score: float = Field(
        ge=0,
        le=100,
    )

    motivation_score: float = Field(
        ge=0,
        le=100,
    )

    emotional_stability_score: float = Field(
        ge=0,
        le=100,
    )

    behavioral_risk_score: float = Field(
        ge=0,
        le=100,
    )

    risk_level: str


class HabitSkipRiskResponse(BaseModel):
    probability: float = Field(
        ge=0,
        le=100,
    )

    level: str

    reason: str


class HabitNudgeResponse(BaseModel):
    message: str
    urgency: str
    action: str


class HabitScheduleResponse(BaseModel):
    action: str
    intensity: str

    duration_minutes: int = Field(
        ge=0,
    )

    reason: str


class HabitAnalysisResponse(BaseModel):
    memory: HabitMemoryResponse
    behavior: HabitBehaviorResponse
    skip_risk: HabitSkipRiskResponse
    nudge: HabitNudgeResponse
    schedule: HabitScheduleResponse