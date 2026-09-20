from dataclasses import dataclass

from ai.dietician.grocery import (
    GroceryItem,
    GroceryListGenerator,
)
from ai.dietician.meal_planner import (
    MealPlan,
    MealPlanner,
)

from app.services.ai.dietician.calculation_service import (
    DieticianCalculationService,
)


@dataclass(frozen=True)
class DietPlanData:
    """
    Structured data used by the Dietician API
    and conversational AI services.
    """

    bmi: float
    bmi_category: str

    bmr: float
    maintenance_calories: float
    target_calories: float

    meal_plan: MealPlan
    grocery_items: list[GroceryItem]


class DieticianService:
    """
    Generate a complete personalized Dietician plan.

    Calculation, meal planning, and grocery generation
    are kept as separate responsibilities while being
    orchestrated through one backend service.
    """

    def __init__(self) -> None:
        self.calculation_service = (
            DieticianCalculationService()
        )

        self.meal_planner = MealPlanner()

        self.grocery_generator = (
            GroceryListGenerator()
        )

    def generate_plan(
        self,
        age: int,
        weight_kg: float,
        height_cm: float,
        sex: str,
        activity_level: str,
        fitness_goal: str,
        dietary_preference: str = "balanced",
    ) -> DietPlanData:
        """
        Generate a complete deterministic daily diet plan.
        """

        calculation = (
            self.calculation_service.calculate(
                age=age,
                sex=sex,
                height_cm=height_cm,
                weight_kg=weight_kg,
                activity_level=activity_level,
                goal=fitness_goal,
            )
        )

        meal_plan = self.meal_planner.generate(
            daily_calories=calculation.calorie_target,
            dietary_preference=dietary_preference,
        )

        grocery_items = (
            self.grocery_generator.generate(
                meal_plan=meal_plan,
            )
        )

        return DietPlanData(
            bmi=calculation.bmi,
            bmi_category=calculation.bmi_category,
            bmr=calculation.bmr,
            maintenance_calories=(
                calculation.maintenance_calories
            ),
            target_calories=(
                calculation.calorie_target
            ),
            meal_plan=meal_plan,
            grocery_items=grocery_items,
        )