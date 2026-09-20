from dataclasses import dataclass

from ai.habit_tracker.prediction import SkipRisk


@dataclass(frozen=True)
class ScheduleAdjustment:
    action: str
    intensity: str
    duration_minutes: int
    reason: str


class DynamicScheduleAdjuster:
    """Adjust the planned workout based on behavioral risk."""

    def adjust(
        self,
        risk: SkipRisk,
        motivation_level: str,
        fitness_goal: str | None = None,
    ) -> ScheduleAdjustment:
        goal = fitness_goal or "your fitness goal"

        if risk.level == "high":
            return ScheduleAdjustment(
                action="reduce_workout_load",
                intensity="light",
                duration_minutes=20,
                reason=(
                    f"High skip risk detected. A shorter and lighter "
                    f"session is recommended to maintain consistency "
                    f"toward {goal}."
                ),
            )

        if risk.level == "medium":
            return ScheduleAdjustment(
                action="simplify_workout",
                intensity="moderate",
                duration_minutes=30,
                reason=(
                    f"Moderate skip risk detected. Simplify the next "
                    f"session and keep the workload manageable while "
                    f"working toward {goal}."
                ),
            )

        return ScheduleAdjustment(
            action="keep_schedule",
            intensity="planned",
            duration_minutes=45,
            reason=(
                f"Behavioral signals are stable. Keep the planned "
                f"schedule for {goal}."
            ),
        )