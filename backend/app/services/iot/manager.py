from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai.smart_gym.controller import SmartGymController
from ai.smart_gym.equipment import EquipmentCommand, EquipmentTelemetry

from app.db.database import SessionLocal
from app.models.iot import (
    IoTCommand,
    IoTEquipment,
    IoTTelemetry,
)
from app.services.iot.smart_gym_mqtt import SmartGymMQTTAdapter


class IoTManager:
    """Manage Smart Gym IoT services, MQTT, AI, and persistence."""

    def __init__(self) -> None:
        self.controller = SmartGymController()

        self.smart_gym = SmartGymMQTTAdapter(
            controller=self.controller,
            telemetry_handler=(
                self.handle_mqtt_telemetry
            ),
        )

        self.started = False

    def start(self) -> None:
        """Start the Smart Gym MQTT integration."""
        if self.started:
            return

        self.smart_gym.connect()
        self.started = True

        print(
            "IoT Manager: Smart Gym MQTT started"
        )

    def stop(self) -> None:
        """Stop the Smart Gym MQTT integration."""
        if not self.started:
            return

        self.smart_gym.disconnect()
        self.started = False

        print(
            "IoT Manager: Smart Gym MQTT stopped"
        )

    def handle_mqtt_telemetry(
        self,
        telemetry: EquipmentTelemetry,
    ) -> None:
        """
        Persist and process telemetry received through MQTT.

        A dedicated database session is created because the MQTT
        callback runs on the Paho network thread.
        """

        db = SessionLocal()

        try:
            commands = self.process_telemetry(
                db=db,
                telemetry=telemetry,
            )

            print(
                "MQTT telemetry processed:",
                telemetry.equipment_id,
            )

            print(
                "AI commands generated:",
                len(commands),
            )

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def process_telemetry(
        self,
        db: Session,
        telemetry: EquipmentTelemetry,
    ) -> list[EquipmentCommand]:
        """
        Process telemetry, persist it, generate AI commands,
        persist the commands, and publish them through MQTT.
        """

        equipment = self._get_or_create_equipment(
            db=db,
            telemetry=telemetry,
        )

        commands = self.controller.decide(
            telemetry
        )

        recorded_at = datetime.utcnow()

        telemetry_record = IoTTelemetry(
            equipment_id=equipment.id,
            resistance_level=(
                telemetry.resistance_level
            ),
            repetitions=telemetry.repetitions,
            performance_score=(
                telemetry.performance_score
            ),
            heart_rate=telemetry.heart_rate,
            fatigue_level=telemetry.fatigue_level,
            recorded_at=recorded_at,
        )

        db.add(
            telemetry_record
        )

        equipment.equipment_type = (
            telemetry.equipment_type
        )

        equipment.current_resistance = (
            telemetry.resistance_level
        )

        equipment.updated_at = recorded_at
        equipment.is_active = True

        for command in commands:
            db.add(
                IoTCommand(
                    equipment_id=equipment.id,
                    action=command.action,
                    value=command.value,
                    reason=command.reason,
                    created_at=recorded_at,
                )
            )

        db.commit()

        for command in commands:
            self.smart_gym.publish_command(
                command
            )

            print(
                "Smart Gym command:",
                {
                    "equipment_id": command.equipment_id,
                    "action": command.action,
                    "value": command.value,
                    "reason": command.reason,
                },
            )

        return commands

    def _get_or_create_equipment(
        self,
        db: Session,
        telemetry: EquipmentTelemetry,
    ) -> IoTEquipment:
        """Find equipment by external ID or create it."""

        statement = select(IoTEquipment).where(
            IoTEquipment.equipment_id
            == telemetry.equipment_id
        )

        equipment = db.scalar(
            statement
        )

        if equipment is None:
            equipment = IoTEquipment(
                equipment_id=telemetry.equipment_id,
                equipment_type=telemetry.equipment_type,
                current_resistance=(
                    telemetry.resistance_level
                ),
                is_active=True,
            )

            db.add(equipment)
            db.flush()

        return equipment

    def get_equipment(
        self,
        db: Session,
        equipment_id: str,
    ) -> IoTEquipment | None:
        """Return equipment by external equipment ID."""

        statement = select(IoTEquipment).where(
            IoTEquipment.equipment_id
            == equipment_id
        )

        return db.scalar(
            statement
        )

    def list_equipment(
        self,
        db: Session,
    ) -> list[IoTEquipment]:
        """Return all registered equipment."""

        statement = (
            select(IoTEquipment)
            .order_by(
                IoTEquipment.updated_at.desc(),
                IoTEquipment.id.desc(),
            )
        )

        return list(
            db.scalars(statement).all()
        )

    def get_latest_telemetry(
        self,
        db: Session,
        equipment_id: int,
    ) -> IoTTelemetry | None:
        """Return the latest telemetry for equipment."""

        statement = (
            select(IoTTelemetry)
            .where(
                IoTTelemetry.equipment_id
                == equipment_id
            )
            .order_by(
                IoTTelemetry.recorded_at.desc(),
                IoTTelemetry.id.desc(),
            )
            .limit(1)
        )

        return db.scalar(
            statement
        )

    def get_latest_command(
        self,
        db: Session,
        equipment_id: int,
    ) -> IoTCommand | None:
        """Return the latest AI command for equipment."""

        statement = (
            select(IoTCommand)
            .where(
                IoTCommand.equipment_id
                == equipment_id
            )
            .order_by(
                IoTCommand.created_at.desc(),
                IoTCommand.id.desc(),
            )
            .limit(1)
        )

        return db.scalar(
            statement
        )


iot_manager = IoTManager()