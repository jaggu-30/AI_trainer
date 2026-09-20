from ai.dietician.intent import DietIntent, DietIntentDetector
from ai.dietician.context import DietConversationContext


class DietConversationEngine:
    """Deterministic dietician conversation engine."""

    def __init__(self) -> None:
        self.intent_detector = DietIntentDetector()

    def respond(
        self,
        user_message: str,
        context: DietConversationContext,
    ) -> str:
        intent = self.intent_detector.detect(user_message)

        if intent == DietIntent.BMI:
            return self._bmi_response(context)

        if intent == DietIntent.CALORIES:
            return self._calorie_response(context)

        if intent == DietIntent.MEAL_PLAN:
            return self._meal_plan_response(context)

        if intent == DietIntent.GROCERY_LIST:
            return self._grocery_response(context)

        if intent == DietIntent.NUTRITION_SUMMARY:
            return self._nutrition_response(context)

        if intent == DietIntent.DIETARY_PREFERENCE:
            return self._dietary_preference_response(context)

        return self._general_response(context)

    def _bmi_response(
        self,
        context: DietConversationContext,
    ) -> str:
        diet_plan = context.diet_plan

        return (
            f"Your BMI is {diet_plan.bmi:.2f}, "
            f"which is classified as {diet_plan.bmi_category}. "
            "Your BMI is one input used by the Dietician "
            "when generating your plan."
        )

    def _calorie_response(
        self,
        context: DietConversationContext,
    ) -> str:
        diet_plan = context.diet_plan

        return (
            f"Your estimated daily maintenance requirement is "
            f"{diet_plan.maintenance_calories:.2f} kcal. "
            f"Your current target is "
            f"{diet_plan.target_calories:.2f} kcal per day."
        )

    def _meal_plan_response(
        self,
        context: DietConversationContext,
    ) -> str:
        meal_plan = context.diet_plan.meal_plan

        meal_lines = []

        for meal in meal_plan.meals:
            meal_lines.append(
                f"{meal.name}: {meal.calories:.0f} kcal, "
                f"{meal.protein_g:.1f} g protein, "
                f"{meal.carbohydrates_g:.1f} g carbohydrates, "
                f"{meal.fat_g:.1f} g fat"
            )

        return (
            f"Here is your daily meal plan for "
            f"{meal_plan.daily_calories:.0f} kcal:\n"
            + "\n".join(meal_lines)
        )

    def _grocery_response(
        self,
        context: DietConversationContext,
    ) -> str:
        groceries = context.diet_plan.grocery_items

        if not groceries:
            return "No grocery items are available for your current meal plan."

        lines = [
            f"- {item.name}: {item.quantity:g} {item.unit}"
            for item in groceries
        ]

        return "Your grocery list is:\n" + "\n".join(lines)

    def _nutrition_response(
        self,
        context: DietConversationContext,
    ) -> str:
        summary = context.nutrition_summary

        return (
            f"Your recorded intake is "
            f"{summary['calories']:.2f} kcal, "
            f"{summary['protein_g']:.2f} g protein, "
            f"{summary['carbohydrates_g']:.2f} g carbohydrates, "
            f"and {summary['fat_g']:.2f} g fat."
        )

    def _dietary_preference_response(
        self,
        context: DietConversationContext,
    ) -> str:
        diet_plan = context.diet_plan

        return (
            "Your current meal plan uses the "
            f"{diet_plan.meal_plan.preference} dietary preference."
        )

    def _general_response(
        self,
        context: DietConversationContext,
    ) -> str:
        diet_plan = context.diet_plan

        return (
            "I can help with your BMI, calorie target, meal plan, "
            "grocery list, nutrition intake, and dietary preferences. "
            f"Your current target is {diet_plan.target_calories:.2f} kcal/day."
        )