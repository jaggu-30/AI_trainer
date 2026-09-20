from dataclasses import dataclass

from ai.gym_buddy.buddy import BuddyResponse, VirtualGymBuddy
from ai.gym_buddy.emotion import EmotionState, EmotionStateAnalyzer
from ai.gym_buddy.memory import (
    ConversationMemory,
    ConversationMemoryAnalyzer,
)
from ai.gym_buddy.sentiment import SentimentAnalyzer, SentimentResult
from app.models.chat import ChatMessage
from app.models.user import User


@dataclass(frozen=True)
class GymBuddyAnalysis:
    sentiment: SentimentResult
    emotion: EmotionState
    response: BuddyResponse
    memory: ConversationMemory


class GymBuddyService:
    """Application service for Virtual Gym Buddy analysis."""

    def __init__(self) -> None:
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_analyzer = EmotionStateAnalyzer()
        self.memory_analyzer = ConversationMemoryAnalyzer()
        self.buddy = VirtualGymBuddy()

    def analyze(
        self,
        user: User,
        message: str,
        history: list[ChatMessage] | None = None,
    ) -> GymBuddyAnalysis:
        sentiment = self.sentiment_analyzer.analyze(message)

        emotion = self.emotion_analyzer.analyze(
            sentiment_label=sentiment.label,
            message=message,
        )

        memory_messages = list(history or [])

        response = self.buddy.respond(
            emotion=emotion,
            user_message=message,
            fitness_goal=user.fitness_goal,
        )

        memory = self.memory_analyzer.analyze(memory_messages)

        return GymBuddyAnalysis(
            sentiment=sentiment,
            emotion=emotion,
            response=response,
            memory=memory,
        )