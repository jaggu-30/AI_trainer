from __future__ import annotations

import json
import time

import paho.mqtt.client as mqtt

from ai.smart_gym.equipment import EquipmentTelemetry
from app.services.iot.smart_gym_mqtt import SmartGymMQTTAdapter


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TELEMETRY_TOPIC = "ai-gym/equipment/telemetry"
COMMAND_TOPIC = "ai-gym/equipment/command"


received_commands: list[dict] = []


def on_command(
    client: mqtt.Client,
    userdata: object,
    message: mqtt.MQTTMessage,
) -> None:
    payload = json.loads(message.payload.decode("utf-8"))
    received_commands.append(payload)

    print("\nReceived command:")
    print(json.dumps(payload, indent=2))


def main() -> None:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="ai-gym-command-test",
        protocol=mqtt.MQTTv5,
    )

    client.on_message = on_command

    print("Connecting test subscriber...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.subscribe(COMMAND_TOPIC)

    client.loop_start()

    time.sleep(1)

    adapter = SmartGymMQTTAdapter()

    telemetry = EquipmentTelemetry(
        equipment_id="EQ-TEST-001",
        equipment_type="smart_strength_machine",
        resistance_level=10,
        repetitions=12,
        performance_score=90,
        heart_rate=125,
        fatigue_level=30,
    )

    print("\nPublishing simulated equipment telemetry:")
    print(telemetry)

    adapter.connect()

    time.sleep(1)

    adapter.publish_telemetry(telemetry)

    time.sleep(2)

    adapter.disconnect()

    client.loop_stop()
    client.disconnect()

    if not received_commands:
        raise RuntimeError(
            "No command was received from the Smart Gym MQTT pipeline."
        )

    command = received_commands[-1]

    assert command["equipment_id"] == "EQ-TEST-001"
    assert command["action"] == "increase_resistance"
    assert command["value"] == 1

    print("\nMQTT Smart Gym integration test: PASSED")


if __name__ == "__main__":
    main()