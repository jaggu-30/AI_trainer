from dataclasses import dataclass

from ai.gym_buddy.memory import ConversationMemory
from ai.habit_tracker.behavior import (
    BehaviorAnalysis,
    HabitBehaviorAnalyzer,
)
from ai.habit_tracker.nudge import (
    MotivationalNudge,
    MotivationalNudgeGenerator,
)
from ai.habit_tracker.prediction import (
    SkipRisk,
    WorkoutSkipPredictor,
)
from ai.habit_tracker.schedule import (
    DynamicScheduleAdjuster,
    ScheduleAdjustment,
)
from app.models.user import User


@dataclass(frozen=True)
class HabitTrackerAnalysis:
    memory: ConversationMemory
    behavior: BehaviorAnalysis
    skip_risk: SkipRisk
    nudge: MotivationalNudge
    schedule: ScheduleAdjustment


class HabitTrackerService:
    """Application service for AI fitness habit analysis."""

    def __init__(self) -> None:
        self.behavior_analyzer = HabitBehaviorAnalyzer()
        self.skip_predictor = WorkoutSkipPredictor()
        self.nudge_generator = MotivationalNudgeGenerator()
        self.schedule_adjuster = DynamicScheduleAdjuster()

    def analyze(
        self,
        user: User,
        memory: ConversationMemory,
    ) -> HabitTrackerAnalysis:
        behavior = self.behavior_analyzer.analyze(memory)

        skip_risk = self.skip_predictor.predict(
            behavior
        )

        nudge = self.nudge_generator.generate(
            risk=skip_risk,
            fitness_goal=user.fitness_goal,
        )

        schedule = self.schedule_adjuster.adjust(
            risk=skip_risk,
            motivation_level=memory.recent_motivation_level,
            fitness_goal=user.fitness_goal,
        )

        return HabitTrackerAnalysis(
            memory=memory,
            behavior=behavior,
            skip_risk=skip_risk,
            nudge=nudge,
            schedule=schedule,
        )