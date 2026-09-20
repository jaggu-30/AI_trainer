from dataclasses import dataclass


@dataclass(frozen=True)
class EquipmentTelemetry:
    equipment_id: str
    equipment_type: str
    resistance_level: float
    repetitions: int
    performance_score: float
    heart_rate: float
    fatigue_level: float


@dataclass(frozen=True)
class EquipmentCommand:
    equipment_id: str
    action: str
    value: float
    reason: str


class SmartEquipment:
    """Represent simulated smart gym equipment."""

    def __init__(
        self,
        equipment_id: str,
        equipment_type: str,
        resistance_level: float = 10.0,
    ) -> None:
        self.equipment_id = equipment_id
        self.equipment_type = equipment_type
        self.resistance_level = resistance_level

    def create_telemetry(
        self,
        repetitions: int,
        performance_score: float,
        heart_rate: float,
        fatigue_level: float,
    ) -> EquipmentTelemetry:
        return EquipmentTelemetry(
            equipment_id=self.equipment_id,
            equipment_type=self.equipment_type,
            resistance_level=self.resistance_level,
            repetitions=repetitions,
            performance_score=performance_score,
            heart_rate=heart_rate,
            fatigue_level=fatigue_level,
        )

    def apply_command(
        self,
        command: EquipmentCommand,
    ) -> None:
        if command.action == "increase_resistance":
            self.resistance_level += command.value

        elif command.action == "decrease_resistance":
            self.resistance_level = max(
                0.0,
                self.resistance_level - command.value,
            )

        elif command.action == "set_resistance":
            self.resistance_level = max(
                0.0,
                command.value,
            )