from dataclasses import dataclass


@dataclass(frozen=True)
class SentimentResult:
    label: str
    score: float


class SentimentAnalyzer:
    """Lightweight deterministic sentiment analyzer for local use."""

    POSITIVE_WORDS = {
        "good",
        "great",
        "happy",
        "motivated",
        "excited",
        "strong",
        "better",
        "awesome",
        "proud",
        "progress",
        "love",
        "enjoy",
        "success",
        "successful",
    }

    NEGATIVE_WORDS = {
        "bad",
        "sad",
        "tired",
        "stressed",
        "stress",
        "angry",
        "frustrated",
        "unmotivated",
        "lazy",
        "hate",
        "failed",
        "failure",
        "worried",
        "anxious",
        "difficult",
        "hard",
        "skip",
        "skipping",
    }

    NEGATIVE_PHRASES = {
        "do not feel like",
        "don't feel like",
        "do not want to",
        "don't want to",
        "not motivated",
        "not feeling motivated",
        "want to skip",
        "want to quit",
        "feel exhausted",
        "feel drained",
    }

    POSITIVE_PHRASES = {
        "feel great",
        "feeling great",
        "feel motivated",
        "feeling motivated",
        "feeling strong",
        "feel strong",
        "doing well",
        "feeling better",
    }

    def analyze(self, text: str) -> SentimentResult:
        normalized = " ".join(text.lower().split())

        positive = 0
        negative = 0

        positive += sum(
            1 for phrase in self.POSITIVE_PHRASES
            if phrase in normalized
        )

        negative += sum(
            1 for phrase in self.NEGATIVE_PHRASES
            if phrase in normalized
        )

        words = {
            word.strip(".,!?;:()[]{}\"'")
            for word in normalized.split()
        }

        positive += len(words & self.POSITIVE_WORDS)
        negative += len(words & self.NEGATIVE_WORDS)

        if positive == 0 and negative == 0:
            return SentimentResult(
                label="neutral",
                score=0.0,
            )

        total = positive + negative
        score = (positive - negative) / total

        if score > 0:
            label = "positive"
        elif score < 0:
            label = "negative"
        else:
            label = "neutral"

        return SentimentResult(
            label=label,
            score=round(score, 3),
        )