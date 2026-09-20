from __future__ import annotations

import json
import threading
import time

import paho.mqtt.client as mqtt

from ai.smart_gym.equipment import (
    EquipmentCommand,
    EquipmentTelemetry,
    SmartEquipment,
)


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TELEMETRY_TOPIC = "ai-gym/equipment/telemetry"
COMMAND_TOPIC = "ai-gym/equipment/command"


class SmartGymDeviceSimulator:
    """Simulate a physical smart gym machine."""

    def __init__(
        self,
        equipment: SmartEquipment,
        repetitions: int,
        performance_score: float,
        heart_rate: float,
        fatigue_level: float,
    ) -> None:
        self.equipment = equipment

        self.repetitions = repetitions
        self.performance_score = performance_score
        self.heart_rate = heart_rate
        self.fatigue_level = fatigue_level

        self.received_commands: list[
            EquipmentCommand
        ] = []

        self.stop_event = threading.Event()

        self.client = mqtt.Client(
            callback_api_version=(
                mqtt.CallbackAPIVersion.VERSION2
            ),
            client_id=(
                f"simulator-{equipment.equipment_id}"
            ),
            protocol=mqtt.MQTTv5,
        )

        self.client.on_connect = (
            self._on_connect
        )

        self.client.on_message = (
            self._on_message
        )

    def start(self) -> None:
        """Connect to MQTT and wait for commands."""

        self.client.connect(
            BROKER_HOST,
            BROKER_PORT,
            keepalive=60,
        )

        self.client.loop_start()

        deadline = (
            time.monotonic() + 10
        )

        while (
            not self.client.is_connected()
            and time.monotonic() < deadline
        ):
            time.sleep(0.1)

        if not self.client.is_connected():
            raise TimeoutError(
                "Smart Gym simulator could not "
                "connect to MQTT broker."
            )

        self.publish_telemetry()

    def stop(self) -> None:
        """Stop the simulator."""

        self.stop_event.set()

        self.client.loop_stop()

        try:
            self.client.disconnect()
        except Exception:
            pass

    def publish_telemetry(self) -> EquipmentTelemetry:
        """Create and publish current telemetry."""

        telemetry = self.equipment.create_telemetry(
            repetitions=self.repetitions,
            performance_score=self.performance_score,
            heart_rate=self.heart_rate,
            fatigue_level=self.fatigue_level,
        )

        payload = {
            "equipment_id": telemetry.equipment_id,
            "equipment_type": telemetry.equipment_type,
            "resistance_level": (
                telemetry.resistance_level
            ),
            "repetitions": telemetry.repetitions,
            "performance_score": (
                telemetry.performance_score
            ),
            "heart_rate": telemetry.heart_rate,
            "fatigue_level": telemetry.fatigue_level,
        }

        result = self.client.publish(
            TELEMETRY_TOPIC,
            json.dumps(payload),
            qos=0,
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                "Failed to publish simulator telemetry."
            )

        print(
            "\nSimulator telemetry:",
            payload,
        )

        return telemetry

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: object,
        flags: object,
        reason_code: object,
        properties: object = None,
    ) -> None:
        if reason_code != 0:
            print(
                "Simulator MQTT connection failed:",
                reason_code,
            )
            return

        result, _ = client.subscribe(
            COMMAND_TOPIC
        )

        if result != mqtt.MQTT_ERR_SUCCESS:
            print(
                "Simulator command subscription failed:",
                result,
            )
            return

        print(
            "Simulator connected to MQTT."
        )

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: object,
        message: mqtt.MQTTMessage,
    ) -> None:
        if message.topic != COMMAND_TOPIC:
            return

        try:
            payload = json.loads(
                message.payload.decode(
                    "utf-8"
                )
            )

            command = EquipmentCommand(
                equipment_id=str(
                    payload["equipment_id"]
                ),
                action=str(
                    payload["action"]
                ),
                value=float(
                    payload["value"]
                ),
                reason=str(
                    payload["reason"]
                ),
            )

        except (
            ValueError,
            KeyError,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as exc:
            print(
                "Simulator received invalid command:",
                exc,
            )
            return

        if (
            command.equipment_id
            != self.equipment.equipment_id
        ):
            return

        print(
            "\nSimulator received command:",
            {
                "action": command.action,
                "value": command.value,
                "reason": command.reason,
            },
        )

        self.equipment.apply_command(
            command
        )

        self.received_commands.append(
            command
        )

        print(
            "Simulator resistance updated to:",
            self.equipment.resistance_level,
        )

        time.sleep(0.5)

        self.publish_telemetry()


def main() -> None:
    """Run one closed-loop Smart Gym simulation."""

    equipment = SmartEquipment(
        equipment_id="EQ-SIM-001",
        equipment_type="smart_strength_machine",
        resistance_level=10.0,
    )

    simulator = SmartGymDeviceSimulator(
        equipment=equipment,
        repetitions=12,
        performance_score=90.0,
        heart_rate=125.0,
        fatigue_level=30.0,
    )

    print(
        "Starting Smart Gym device simulator..."
    )

    simulator.start()

    try:
        deadline = (
            time.monotonic() + 15
        )

        while (
            not simulator.received_commands
            and time.monotonic() < deadline
        ):
            time.sleep(0.1)

        if not simulator.received_commands:
            raise RuntimeError(
                "Simulator did not receive an AI command."
            )

        print(
            "\nClosed-loop simulation complete."
        )

        print(
            "Final resistance:",
            simulator.equipment.resistance_level,
        )

    finally:
        simulator.stop()


if __name__ == "__main__":
    main()