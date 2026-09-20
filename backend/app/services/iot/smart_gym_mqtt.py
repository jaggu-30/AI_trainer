from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ai.smart_gym.controller import SmartGymController
from ai.smart_gym.equipment import EquipmentCommand, EquipmentTelemetry

from app.services.iot.mqtt_service import MQTTService


TelemetryHandler = Callable[[EquipmentTelemetry], None]


class SmartGymMQTTAdapter:
    """Connect Smart Gym equipment telemetry and commands through MQTT."""

    TELEMETRY_TOPIC = "ai-gym/equipment/telemetry"
    COMMAND_TOPIC = "ai-gym/equipment/command"
    RECOVERY_TOPIC = "ai-gym/equipment/recovery"

    def __init__(
        self,
        mqtt_service: MQTTService | None = None,
        controller: SmartGymController | None = None,
        telemetry_handler: TelemetryHandler | None = None,
    ) -> None:
        self.mqtt = mqtt_service or MQTTService()
        self.controller = controller or SmartGymController()
        self.telemetry_handler = telemetry_handler

        self.mqtt.set_message_handler(
            self._handle_message
        )

    def connect(self) -> None:
        """Connect to MQTT and subscribe to equipment telemetry."""
        self.mqtt.connect()
        self.mqtt.subscribe(
            self.TELEMETRY_TOPIC
        )

    def disconnect(self) -> None:
        """Disconnect from MQTT."""
        self.mqtt.disconnect()

    def publish_telemetry(
        self,
        telemetry: EquipmentTelemetry,
    ) -> None:
        """Publish equipment telemetry to MQTT."""

        payload = {
            "equipment_id": telemetry.equipment_id,
            "equipment_type": telemetry.equipment_type,
            "resistance_level": telemetry.resistance_level,
            "repetitions": telemetry.repetitions,
            "performance_score": telemetry.performance_score,
            "heart_rate": telemetry.heart_rate,
            "fatigue_level": telemetry.fatigue_level,
        }

        self.mqtt.publish(
            self.TELEMETRY_TOPIC,
            payload,
        )

    def publish_command(
        self,
        command: EquipmentCommand,
    ) -> None:
        """Publish one AI-generated equipment command."""

        self.mqtt.publish(
            self.COMMAND_TOPIC,
            {
                "equipment_id": command.equipment_id,
                "action": command.action,
                "value": command.value,
                "reason": command.reason,
            },
        )

    def _handle_message(
        self,
        topic: str,
        payload: dict[str, Any],
    ) -> None:
        """Handle incoming equipment telemetry."""

        if topic != self.TELEMETRY_TOPIC:
            return

        telemetry = EquipmentTelemetry(
            equipment_id=str(
                payload["equipment_id"]
            ),
            equipment_type=str(
                payload["equipment_type"]
            ),
            resistance_level=float(
                payload["resistance_level"]
            ),
            repetitions=int(
                payload["repetitions"]
            ),
            performance_score=float(
                payload["performance_score"]
            ),
            heart_rate=float(
                payload["heart_rate"]
            ),
            fatigue_level=float(
                payload["fatigue_level"]
            ),
        )

        if self.telemetry_handler is not None:
            self.telemetry_handler(
                telemetry
            )
            return

        commands = self.controller.decide(
            telemetry
        )

        if not isinstance(commands, list):
            commands = [commands]

        for command in commands:
            self.publish_command(
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