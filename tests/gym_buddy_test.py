import pytest

from ai.gym_buddy.buddy import VirtualGymBuddy
from ai.gym_buddy.emotion import EmotionStateAnalyzer
from ai.gym_buddy.memory import ConversationMemoryAnalyzer
from ai.gym_buddy.sentiment import SentimentAnalyzer


class FakeMessage:
    def __init__(
        self,
        role,
        sentiment=None,
        emotion=None,
        motivation_level=None,
    ):
        self.role = role
        self.sentiment = sentiment
        self.emotion = emotion
        self.motivation_level = motivation_level


def test_positive_sentiment():
    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "I feel great and motivated today."
    )

    assert result.label == "positive"
    assert result.score > 0


def test_negative_sentiment():
    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "I feel stressed and tired today."
    )

    assert result.label == "negative"
    assert result.score < 0


def test_neutral_sentiment():
    analyzer = SentimentAnalyzer()

    result = analyzer.analyze(
        "Tell me about my fitness routine."
    )

    assert result.label == "neutral"
    assert result.score == 0.0


def test_unmotivated_emotion():
    analyzer = EmotionStateAnalyzer()

    result = analyzer.analyze(
        sentiment_label="negative",
        message="I want to skip workout today.",
    )

    assert result.emotion == "unmotivated"
    assert result.motivation_level == "low"
    assert result.confidence == 0.9


def test_stressed_emotion():
    analyzer = EmotionStateAnalyzer()

    result = analyzer.analyze(
        sentiment_label="negative",
        message="I feel very stressed today.",
    )

    assert result.emotion == "stressed"
    assert result.motivation_level == "low"
    assert result.confidence == 0.85


def test_positive_emotion():
    analyzer = EmotionStateAnalyzer()

    result = analyzer.analyze(
        sentiment_label="positive",
        message="I am feeling strong today.",
    )

    assert result.emotion == "positive"
    assert result.motivation_level == "high"
    assert result.confidence == 0.8


def test_neutral_emotion():
    analyzer = EmotionStateAnalyzer()

    result = analyzer.analyze(
        sentiment_label="neutral",
        message="What is my progress?",
    )

    assert result.emotion == "neutral"
    assert result.motivation_level == "moderate"
    assert result.confidence == 0.6


def test_unmotivated_buddy_response():
    sentiment_analyzer = SentimentAnalyzer()
    emotion_analyzer = EmotionStateAnalyzer()
    buddy = VirtualGymBuddy()

    sentiment = sentiment_analyzer.analyze(
        "I don't feel like training today."
    )

    emotion = emotion_analyzer.analyze(
        sentiment_label=sentiment.label,
        message="I don't feel like training today.",
    )

    result = buddy.respond(
        emotion=emotion,
        user_message=(
            "I don't feel like training today."
        ),
        fitness_goal="weight_loss",
    )

    assert result.strategy == "motivation_support"
    assert "motivation is low" in result.message


def test_stress_buddy_response():
    sentiment_analyzer = SentimentAnalyzer()
    emotion_analyzer = EmotionStateAnalyzer()
    buddy = VirtualGymBuddy()

    message = "I feel stressed today."

    sentiment = sentiment_analyzer.analyze(
        message
    )

    emotion = emotion_analyzer.analyze(
        sentiment_label=sentiment.label,
        message=message,
    )

    result = buddy.respond(
        emotion=emotion,
        user_message=message,
        fitness_goal="maintenance",
    )

    assert result.strategy == "stress_support"
    assert "Recovery matters" in result.message


def test_positive_buddy_response():
    sentiment_analyzer = SentimentAnalyzer()
    emotion_analyzer = EmotionStateAnalyzer()
    buddy = VirtualGymBuddy()

    message = "I feel great and motivated."

    sentiment = sentiment_analyzer.analyze(
        message
    )

    emotion = emotion_analyzer.analyze(
        sentiment_label=sentiment.label,
        message=message,
    )

    result = buddy.respond(
        emotion=emotion,
        user_message=message,
        fitness_goal="muscle_gain",
    )

    assert (
        result.strategy
        == "positive_reinforcement"
    )

    assert "strong mindset" in result.message


def test_general_buddy_response():
    buddy = VirtualGymBuddy()

    emotion = EmotionStateAnalyzer().analyze(
        sentiment_label="neutral",
        message="What should I focus on?",
    )

    result = buddy.respond(
        emotion=emotion,
        user_message="What should I focus on?",
        fitness_goal="fitness",
    )

    assert result.strategy == "general_support"
    assert "stay consistent" in result.message


def test_conversation_memory_empty():
    analyzer = ConversationMemoryAnalyzer()

    result = analyzer.analyze([])

    assert result.total_messages == 0
    assert result.positive_messages == 0
    assert result.negative_messages == 0
    assert result.neutral_messages == 0

    assert result.recent_sentiment == "neutral"
    assert result.recent_emotion == "neutral"
    assert (
        result.recent_motivation_level
        == "moderate"
    )

    assert result.unmotivated_count == 0
    assert result.stressed_count == 0
    assert result.low_motivation_count == 0

    assert result.motivation_trend == "stable"


def test_conversation_memory_improving():
    messages = [
        FakeMessage(
            role="user",
            sentiment="positive",
            emotion="positive",
            motivation_level="high",
        ),
        FakeMessage(
            role="assistant",
            sentiment="positive",
            emotion="positive",
            motivation_level="high",
        ),
        FakeMessage(
            role="user",
            sentiment="positive",
            emotion="positive",
            motivation_level="high",
        ),
    ]

    analyzer = ConversationMemoryAnalyzer()

    result = analyzer.analyze(messages)

    assert result.total_messages == 2
    assert result.positive_messages == 2
    assert result.negative_messages == 0
    assert result.neutral_messages == 0

    assert result.recent_sentiment == "positive"
    assert result.recent_emotion == "positive"
    assert result.recent_motivation_level == "high"

    assert result.motivation_trend == "improving"


def test_conversation_memory_declining():
    messages = [
        FakeMessage(
            role="user",
            sentiment="positive",
            emotion="positive",
            motivation_level="high",
        ),
        FakeMessage(
            role="user",
            sentiment="negative",
            emotion="stressed",
            motivation_level="low",
        ),
    ]

    analyzer = ConversationMemoryAnalyzer()

    result = analyzer.analyze(messages)

    assert result.total_messages == 2
    assert result.positive_messages == 1
    assert result.negative_messages == 1

    assert result.recent_sentiment == "negative"
    assert result.recent_emotion == "stressed"
    assert result.recent_motivation_level == "low"

    assert result.stressed_count == 1
    assert result.low_motivation_count == 1

    assert result.motivation_trend == "stable"


def test_conversation_memory_counts_unmotivated_messages():
    messages = [
        FakeMessage(
            role="user",
            sentiment="negative",
            emotion="unmotivated",
            motivation_level="low",
        ),
        FakeMessage(
            role="user",
            sentiment="negative",
            emotion="unmotivated",
            motivation_level="low",
        ),
        FakeMessage(
            role="user",
            sentiment="neutral",
            emotion="neutral",
            motivation_level="moderate",
        ),
    ]

    analyzer = ConversationMemoryAnalyzer()

    result = analyzer.analyze(messages)

    assert result.total_messages == 3
    assert result.unmotivated_count == 2
    assert result.low_motivation_count == 2
    assert result.stressed_count == 0


def test_case_normalization():
    sentiment = SentimentAnalyzer()

    result = sentiment.analyze(
        "   I   FEEL   GREAT   TODAY   "
    )

    assert result.label == "positive"
    assert result.score > 0


def test_buddy_uses_user_fitness_goal():
    buddy = VirtualGymBuddy()

    emotion = EmotionStateAnalyzer().analyze(
        sentiment_label="positive",
        message="I feel great.",
    )

    result = buddy.respond(
        emotion=emotion,
        user_message="I feel great.",
        fitness_goal="weight_loss",
    )

    assert result.strategy == "positive_reinforcement"
    assert "weight_loss" in result.message