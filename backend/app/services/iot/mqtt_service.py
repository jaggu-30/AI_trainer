from __future__ import annotations

import json
import threading
from collections.abc import Callable
from typing import Any

import paho.mqtt.client as mqtt

from app.core.config import settings


MessageHandler = Callable[[str, dict[str, Any]], None]


class MQTTService:
    """Small wrapper around the Paho MQTT client."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        client_id: str = "ai-gym-backend",
    ) -> None:
        self.host = host or settings.mqtt_broker_host
        self.port = port or settings.mqtt_broker_port
        self.client_id = client_id

        self._client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.client_id,
            protocol=mqtt.MQTTv5,
        )

        self._connected = threading.Event()
        self._message_handler: MessageHandler | None = None

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()

    def set_message_handler(self, handler: MessageHandler) -> None:
        self._message_handler = handler

    def connect(self, timeout: float = 10.0) -> None:
        """
        Connect to the MQTT broker and wait for the connection
        callback before returning.
        """
        self._connected.clear()

        self._client.connect(
            self.host,
            self.port,
            keepalive=60,
        )

        self._client.loop_start()

        if not self._connected.wait(timeout=timeout):
            self._client.loop_stop()
            raise TimeoutError(
                f"Timed out waiting for MQTT broker connection "
                f"at {self.host}:{self.port}"
            )

    def disconnect(self) -> None:
        """Disconnect from the broker and stop the network loop."""
        try:
            if self.is_connected:
                self._client.disconnect()
        finally:
            self._client.loop_stop()
            self._connected.clear()

    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Subscribe to an MQTT topic."""
        if not self.is_connected:
            raise RuntimeError("MQTT client is not connected")

        result, _ = self._client.subscribe(
            topic,
            qos=qos,
        )

        if result != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                f"Failed to subscribe to topic '{topic}'. "
                f"Result: {result}"
            )

    def publish(
        self,
        topic: str,
        payload: dict[str, Any],
        qos: int = 0,
        retain: bool = False,
    ) -> None:
        """Publish a JSON payload to an MQTT topic."""
        if not self.is_connected:
            raise RuntimeError("MQTT client is not connected")

        message = json.dumps(payload)

        result = self._client.publish(
            topic,
            payload=message,
            qos=qos,
            retain=retain,
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                f"Failed to publish to topic '{topic}'. "
                f"Result: {result.rc}"
            )

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: Any,
        reason_code: Any,
        properties: Any = None,
    ) -> None:
        """
        Paho MQTT v5 connection callback.
        Reason code 0 means successful connection.
        """
        if reason_code == 0:
            self._connected.set()
            print(
                f"MQTT connected to {self.host}:{self.port}"
            )
        else:
            self._connected.clear()
            print(
                f"MQTT connection failed: {reason_code}"
            )

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        disconnect_flags: Any,
        reason_code: Any,
        properties: Any = None,
    ) -> None:
        self._connected.clear()
        print(
            f"MQTT disconnected: {reason_code}"
        )

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: Any,
        message: mqtt.MQTTMessage,
    ) -> None:
        try:
            payload = json.loads(
                message.payload.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ):
            payload = {
                "raw": message.payload.decode(
                    "utf-8",
                    errors="replace",
                )
            }

        if self._message_handler is not None:
            self._message_handler(
                message.topic,
                payload,
            )