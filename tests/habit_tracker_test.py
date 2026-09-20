from types import SimpleNamespace

from ai.gym_buddy.memory import ConversationMemory
from ai.habit_tracker.behavior import (
    HabitBehaviorAnalyzer,
)
from ai.habit_tracker.nudge import (
    MotivationalNudgeGenerator,
)
from ai.habit_tracker.prediction import (
    WorkoutSkipPredictor,
)
from ai.habit_tracker.schedule import (
    DynamicScheduleAdjuster,
)
from app.services.ai.habit_tracker_service import (
    HabitTrackerService,
)


def test_empty_memory_is_low_risk():
    memory = ConversationMemory(
        total_messages=0,
        positive_messages=0,
        negative_messages=0,
        neutral_messages=0,
        recent_sentiment="neutral",
        recent_emotion="neutral",
        recent_motivation_level="moderate",
        unmotivated_count=0,
        stressed_count=0,
        low_motivation_count=0,
        motivation_trend="stable",
    )

    analyzer = HabitBehaviorAnalyzer()

    result = analyzer.analyze(memory)

    assert result.consistency_score == 100.0
    assert result.motivation_score == 50.0
    assert (
        result.emotional_stability_score
        == 100.0
    )
    assert result.behavioral_risk_score == 0.0
    assert result.risk_level == "low"


def test_high_risk_behavior():
    memory = ConversationMemory(
        total_messages=10,
        positive_messages=0,
        negative_messages=8,
        neutral_messages=2,
        recent_sentiment="negative",
        recent_emotion="unmotivated",
        recent_motivation_level="low",
        unmotivated_count=8,
        stressed_count=7,
        low_motivation_count=8,
        motivation_trend="declining",
    )

    analyzer = HabitBehaviorAnalyzer()

    result = analyzer.analyze(memory)

    assert result.behavioral_risk_score >= 70.0
    assert result.risk_level == "high"


def test_improving_behavior_has_low_risk():
    improving_memory = ConversationMemory(
        total_messages=4,
        positive_messages=4,
        negative_messages=0,
        neutral_messages=0,
        recent_sentiment="positive",
        recent_emotion="positive",
        recent_motivation_level="high",
        unmotivated_count=0,
        stressed_count=0,
        low_motivation_count=0,
        motivation_trend="improving",
    )

    analyzer = HabitBehaviorAnalyzer()

    result = analyzer.analyze(
        improving_memory
    )

    assert result.behavioral_risk_score == 0.0
    assert result.risk_level == "low"


def test_declining_trend_increases_risk():
    improving_memory = ConversationMemory(
        total_messages=4,
        positive_messages=3,
        negative_messages=1,
        neutral_messages=0,
        recent_sentiment="positive",
        recent_emotion="positive",
        recent_motivation_level="high",
        unmotivated_count=0,
        stressed_count=0,
        low_motivation_count=0,
        motivation_trend="improving",
    )

    declining_memory = ConversationMemory(
        total_messages=4,
        positive_messages=3,
        negative_messages=1,
        neutral_messages=0,
        recent_sentiment="positive",
        recent_emotion="positive",
        recent_motivation_level="high",
        unmotivated_count=0,
        stressed_count=0,
        low_motivation_count=0,
        motivation_trend="declining",
    )

    analyzer = HabitBehaviorAnalyzer()

    improving = analyzer.analyze(
        improving_memory
    )

    declining = analyzer.analyze(
        declining_memory
    )

    assert (
        declining.behavioral_risk_score
        > improving.behavioral_risk_score
    )


def test_skip_risk_matches_behavior_risk():
    behavior = HabitBehaviorAnalyzer().analyze(
        ConversationMemory(
            total_messages=10,
            positive_messages=1,
            negative_messages=7,
            neutral_messages=2,
            recent_sentiment="negative",
            recent_emotion="stressed",
            recent_motivation_level="low",
            unmotivated_count=7,
            stressed_count=6,
            low_motivation_count=7,
            motivation_trend="declining",
        )
    )

    result = WorkoutSkipPredictor().predict(
        behavior
    )

    assert (
        result.probability
        == behavior.behavioral_risk_score
    )

    assert result.level == behavior.risk_level
    assert result.reason


def test_high_risk_nudge():
    behavior = SimpleNamespace(
        behavioral_risk_score=85.0,
        risk_level="high",
    )

    risk = WorkoutSkipPredictor().predict(
        behavior
    )

    nudge = MotivationalNudgeGenerator().generate(
        risk=risk,
        fitness_goal="weight_loss",
    )

    assert nudge.urgency == "high"
    assert nudge.action == (
        "send_immediate_nudge"
    )

    assert "weight_loss" in nudge.message


def test_medium_risk_schedule():
    behavior = SimpleNamespace(
        behavioral_risk_score=50.0,
        risk_level="medium",
    )

    risk = WorkoutSkipPredictor().predict(
        behavior
    )

    schedule = DynamicScheduleAdjuster().adjust(
        risk=risk,
        motivation_level="moderate",
        fitness_goal="maintenance",
    )

    assert schedule.action == (
        "simplify_workout"
    )
    assert schedule.intensity == "moderate"
    assert schedule.duration_minutes == 30


def test_low_risk_schedule():
    behavior = SimpleNamespace(
        behavioral_risk_score=10.0,
        risk_level="low",
    )

    risk = WorkoutSkipPredictor().predict(
        behavior
    )

    schedule = DynamicScheduleAdjuster().adjust(
        risk=risk,
        motivation_level="high",
        fitness_goal="muscle_gain",
    )

    assert schedule.action == "keep_schedule"
    assert schedule.intensity == "planned"
    assert schedule.duration_minutes == 45


def test_habit_tracker_service_combines_components():
    user = SimpleNamespace(
        fitness_goal="weight_loss"
    )

    memory = ConversationMemory(
        total_messages=3,
        positive_messages=0,
        negative_messages=3,
        neutral_messages=0,
        recent_sentiment="negative",
        recent_emotion="unmotivated",
        recent_motivation_level="low",
        unmotivated_count=3,
        stressed_count=2,
        low_motivation_count=3,
        motivation_trend="declining",
    )

    service = HabitTrackerService()

    result = service.analyze(
        user=user,
        memory=memory,
    )

    assert result.memory == memory
    assert result.behavior.risk_level in {
        "low",
        "medium",
        "high",
    }

    assert result.skip_risk.level == (
        result.behavior.risk_level
    )

    assert result.nudge.message
    assert result.schedule.reason