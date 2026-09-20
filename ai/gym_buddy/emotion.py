from dataclasses import dataclass


@dataclass(frozen=True)
class EmotionState:
    emotion: str
    motivation_level: str
    confidence: float


class EmotionStateAnalyzer:
    """Infer a simple fitness-oriented emotional state."""

    UNMOTIVATED_PHRASES = (
        "don't feel like",
        "do not feel like",
        "cannot motivate",
        "can't motivate",
        "not motivated",
        "not feeling motivated",
        "want to skip",
        "want to quit",
        "skip workout",
        "skipping workout",
        "feel like skipping",
        "feeling like skipping",
        "might skip",
        "may skip",
        "probably skip",
    )

    STRESS_PHRASES = (
        "feel stressed",
        "feeling stressed",
        "very stressed",
        "under stress",
        "too much stress",
    )

    def analyze(
        self,
        sentiment_label: str,
        message: str,
    ) -> EmotionState:
        text = " ".join(message.lower().split())

        if any(
            phrase in text
            for phrase in self.UNMOTIVATED_PHRASES
        ):
            return EmotionState(
                emotion="unmotivated",
                motivation_level="low",
                confidence=0.9,
            )

        if any(
            phrase in text
            for phrase in self.STRESS_PHRASES
        ):
            return EmotionState(
                emotion="stressed",
                motivation_level="low",
                confidence=0.85,
            )

        if sentiment_label == "positive":
            return EmotionState(
                emotion="positive",
                motivation_level="high",
                confidence=0.8,
            )

        if sentiment_label == "negative":
            return EmotionState(
                emotion="stressed",
                motivation_level="low",
                confidence=0.7,
            )

        return EmotionState(
            emotion="neutral",
            motivation_level="moderate",
            confidence=0.6,
        )