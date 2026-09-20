from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ai.smart_gym.equipment import EquipmentTelemetry

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.iot import (
    EquipmentCommandResponse,
    EquipmentStateResponse,
    EquipmentTelemetryResponse,
    EquipmentTelemetryRequest,
    IoTStatusResponse,
    SmartGymTelemetryResponse,
)
from app.services.iot.manager import iot_manager


router = APIRouter(
    prefix="/api/v1/iot",
    tags=["Smart Gym IoT"],
)


def _build_equipment_state(
    db: Session,
    equipment,
) -> EquipmentStateResponse:
    """Build an equipment response from its latest persisted data."""

    latest_telemetry = (
        iot_manager.get_latest_telemetry(
            db=db,
            equipment_id=equipment.id,
        )
    )

    latest_command = (
        iot_manager.get_latest_command(
            db=db,
            equipment_id=equipment.id,
        )
    )

    return EquipmentStateResponse(
        equipment_id=equipment.equipment_id,
        equipment_type=equipment.equipment_type,
        resistance_level=equipment.current_resistance,
        repetitions=(
            latest_telemetry.repetitions
            if latest_telemetry
            else 0
        ),
        performance_score=(
            latest_telemetry.performance_score
            if latest_telemetry
            else 0.0
        ),
        heart_rate=(
            latest_telemetry.heart_rate
            if latest_telemetry
            else 0.0
        ),
        fatigue_level=(
            latest_telemetry.fatigue_level
            if latest_telemetry
            else 0.0
        ),
        last_action=(
            latest_command.action
            if latest_command
            else None
        ),
        last_command_value=(
            latest_command.value
            if latest_command
            else None
        ),
        last_command_reason=(
            latest_command.reason
            if latest_command
            else None
        ),
        updated_at=equipment.updated_at,
    )


@router.get(
    "/status",
    response_model=IoTStatusResponse,
)
def get_iot_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the current Smart Gym IoT subsystem status."""

    equipment = iot_manager.list_equipment(
        db
    )

    return IoTStatusResponse(
        mqtt_connected=(
            iot_manager.smart_gym.mqtt.is_connected
        ),
        equipment_count=len(equipment),
        equipment=[
            _build_equipment_state(
                db=db,
                equipment=item,
            )
            for item in equipment
        ],
    )


@router.post(
    "/equipment/telemetry",
    response_model=SmartGymTelemetryResponse,
)
def process_equipment_telemetry(
    request: EquipmentTelemetryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Process equipment telemetry through the Smart Gym AI."""

    if not iot_manager.started:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Smart Gym IoT service is not running.",
        )

    telemetry = EquipmentTelemetry(
        equipment_id=request.equipment_id,
        equipment_type=request.equipment_type,
        resistance_level=request.resistance_level,
        repetitions=request.repetitions,
        performance_score=request.performance_score,
        heart_rate=request.heart_rate,
        fatigue_level=request.fatigue_level,
    )

    commands = iot_manager.process_telemetry(
        db=db,
        telemetry=telemetry,
    )

    equipment = iot_manager.get_equipment(
        db=db,
        equipment_id=telemetry.equipment_id,
    )

    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Equipment state could not be stored.",
        )

    return SmartGymTelemetryResponse(
        telemetry=EquipmentTelemetryResponse(
            equipment_id=telemetry.equipment_id,
            equipment_type=telemetry.equipment_type,
            resistance_level=telemetry.resistance_level,
            repetitions=telemetry.repetitions,
            performance_score=telemetry.performance_score,
            heart_rate=telemetry.heart_rate,
            fatigue_level=telemetry.fatigue_level,
            received_at=equipment.updated_at,
        ),
        commands=[
            EquipmentCommandResponse(
                equipment_id=command.equipment_id,
                action=command.action,
                value=command.value,
                reason=command.reason,
            )
            for command in commands
        ],
    )


@router.get(
    "/equipment",
    response_model=list[EquipmentStateResponse],
)
def list_equipment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all registered Smart Gym equipment."""

    equipment = iot_manager.list_equipment(
        db
    )

    return [
        _build_equipment_state(
            db=db,
            equipment=item,
        )
        for item in equipment
    ]


@router.get(
    "/equipment/{equipment_id}",
    response_model=EquipmentStateResponse,
)
def get_equipment(
    equipment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return one registered Smart Gym equipment device."""

    equipment = iot_manager.get_equipment(
        db=db,
        equipment_id=equipment_id,
    )

    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found.",
        )

    return _build_equipment_state(
        db=db,
        equipment=equipment,
    )