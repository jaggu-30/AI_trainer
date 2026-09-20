from enum import Enum


class DietIntent(str, Enum):
    """Supported Dietician conversation intents."""

    BMI = "bmi"
    CALORIES = "calories"
    MEAL_PLAN = "meal_plan"
    GROCERY_LIST = "grocery_list"
    NUTRITION_SUMMARY = "nutrition_summary"
    DIETARY_PREFERENCE = "dietary_preference"
    GENERAL = "general"


class DietIntentDetector:
    """Detect a diet-related intent from a user message."""

    INTENT_KEYWORDS = {
        DietIntent.BMI: (
            "bmi",
            "body mass index",
            "body-mass index",
        ),
        DietIntent.CALORIES: (
            "calorie",
            "calories",
            "kcal",
            "how much should i eat",
        ),
        DietIntent.MEAL_PLAN: (
            "meal plan",
            "meal",
            "eat today",
            "what should i eat",
            "food plan",
        ),
        DietIntent.GROCERY_LIST: (
            "grocery",
            "groceries",
            "shopping list",
            "buy",
            "shopping",
        ),
        DietIntent.NUTRITION_SUMMARY: (
            "nutrition",
            "nutritional intake",
            "intake",
            "consumed",
            "eaten",
        ),
        DietIntent.DIETARY_PREFERENCE: (
            "vegetarian",
            "vegan",
            "balanced",
            "diet preference",
        ),
    }

    def detect(self, message: str) -> DietIntent:
        """Return the most relevant intent for a message."""

        normalized = " ".join(
            message.strip().lower().split()
        )

        if not normalized:
            return DietIntent.GENERAL

        for intent, keywords in self.INTENT_KEYWORDS.items():
            if any(
                keyword in normalized
                for keyword in keywords
            ):
                return intent

        return DietIntent.GENERAL
