from dataclasses import dataclass

from ai.dietician.service import DietPlanData


@dataclass(frozen=True)
class DietConversationContext:
    """Structured information available to the Dietician chatbot."""

    diet_plan: DietPlanData
    nutrition_summary: dict[str, float]


class DietContextBuilder:
    """Build chatbot context from structured Dietician data."""

    def build(
        self,
        diet_plan: DietPlanData,
        nutrition_summary: dict[str, float] | None = None,
    ) -> DietConversationContext:
        """Create a conversation context."""

        return DietConversationContext(
            diet_plan=diet_plan,
            nutrition_summary=(
                nutrition_summary
                if nutrition_summary is not None
                else {
                    "total_entries": 0,
                    "total_calories": 0.0,
                    "total_protein_g": 0.0,
                    "total_carbohydrates_g": 0.0,
                    "total_fat_g": 0.0,
                }
            ),
        )
