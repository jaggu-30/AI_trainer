from ai.smart_gym.equipment import (
    EquipmentCommand,
    EquipmentTelemetry,
)


class SmartGymController:
    """Generate equipment and recovery decisions from telemetry."""

    def decide(
        self,
        telemetry: EquipmentTelemetry,
    ) -> list[EquipmentCommand]:
        commands: list[EquipmentCommand] = []

        if telemetry.fatigue_level >= 80:
            commands.append(
                EquipmentCommand(
                    equipment_id=telemetry.equipment_id,
                    action="decrease_resistance",
                    value=2.0,
                    reason=(
                        "High fatigue detected. "
                        "Reducing resistance for safer recovery."
                    ),
                )
            )

        elif (
            telemetry.performance_score >= 85
            and telemetry.fatigue_level <= 40
        ):
            commands.append(
                EquipmentCommand(
                    equipment_id=telemetry.equipment_id,
                    action="increase_resistance",
                    value=1.0,
                    reason=(
                        "Strong performance with low fatigue. "
                        "A small resistance increase is appropriate."
                    ),
                )
            )

        else:
            commands.append(
                EquipmentCommand(
                    equipment_id=telemetry.equipment_id,
                    action="set_resistance",
                    value=telemetry.resistance_level,
                    reason=(
                        "Performance and fatigue are within "
                        "the current training range."
                    ),
                )
            )

        return commands