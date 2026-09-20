from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EquipmentTelemetryRequest(BaseModel):
    """Telemetry submitted by Smart Gym equipment."""

    equipment_id: str = Field(
        min_length=1,
        max_length=100,
    )
    equipment_type: str = Field(
        min_length=1,
        max_length=100,
    )
    resistance_level: float = Field(
        ge=0,
    )
    repetitions: int = Field(
        ge=0,
    )
    performance_score: float = Field(
        ge=0,
        le=100,
    )
    heart_rate: float = Field(
        ge=0,
        le=250,
    )
    fatigue_level: float = Field(
        ge=0,
        le=100,
    )


class EquipmentCommandResponse(BaseModel):
    """AI-generated command for Smart Gym equipment."""

    equipment_id: str
    action: str
    value: float
    reason: str


class EquipmentTelemetryResponse(BaseModel):
    """Latest telemetry processed by the Smart Gym backend."""

    model_config = ConfigDict(from_attributes=True)

    equipment_id: str
    equipment_type: str
    resistance_level: float
    repetitions: int
    performance_score: float
    heart_rate: float
    fatigue_level: float
    received_at: datetime


class EquipmentStateResponse(BaseModel):
    """Current persisted state for one Smart Gym device."""

    equipment_id: str
    equipment_type: str
    resistance_level: float
    repetitions: int
    performance_score: float
    heart_rate: float
    fatigue_level: float
    last_action: str | None = None
    last_command_value: float | None = None
    last_command_reason: str | None = None
    updated_at: datetime


class SmartGymTelemetryResponse(BaseModel):
    """Result returned after processing equipment telemetry."""

    telemetry: EquipmentTelemetryResponse
    commands: list[EquipmentCommandResponse]


class IoTStatusResponse(BaseModel):
    """Current Smart Gym IoT subsystem status."""

    mqtt_connected: bool
    equipment_count: int
    equipment: list[EquipmentStateResponse]