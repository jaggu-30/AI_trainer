from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationMemory:
    total_messages: int
    positive_messages: int
    negative_messages: int
    neutral_messages: int

    recent_sentiment: str
    recent_emotion: str
    recent_motivation_level: str

    unmotivated_count: int
    stressed_count: int
    low_motivation_count: int

    motivation_trend: str


class ConversationMemoryAnalyzer:
    """Build a fitness-focused emotional summary from chat history."""

    def analyze(self, messages) -> ConversationMemory:
        user_messages = [
            message
            for message in messages
            if message.role == "user"
        ]

        sentiments = [
            message.sentiment
            for message in user_messages
            if message.sentiment
        ]

        emotions = [
            message.emotion
            for message in user_messages
            if message.emotion
        ]

        motivation_levels = [
            message.motivation_level
            for message in user_messages
            if message.motivation_level
        ]

        total = len(sentiments)

        positive = sentiments.count("positive")
        negative = sentiments.count("negative")
        neutral = sentiments.count("neutral")

        recent_sentiment = (
            sentiments[-1]
            if sentiments
            else "neutral"
        )

        recent_emotion = (
            emotions[-1]
            if emotions
            else "neutral"
        )

        recent_motivation_level = (
            motivation_levels[-1]
            if motivation_levels
            else "moderate"
        )

        unmotivated_count = emotions.count("unmotivated")
        stressed_count = emotions.count("stressed")
        low_motivation_count = motivation_levels.count("low")

        if total < 2:
            motivation_trend = "stable"
        elif negative > positive:
            motivation_trend = "declining"
        elif positive > negative:
            motivation_trend = "improving"
        else:
            motivation_trend = "stable"

        return ConversationMemory(
            total_messages=total,
            positive_messages=positive,
            negative_messages=negative,
            neutral_messages=neutral,
            recent_sentiment=recent_sentiment,
            recent_emotion=recent_emotion,
            recent_motivation_level=recent_motivation_level,
            unmotivated_count=unmotivated_count,
            stressed_count=stressed_count,
            low_motivation_count=low_motivation_count,
            motivation_trend=motivation_trend,
        )