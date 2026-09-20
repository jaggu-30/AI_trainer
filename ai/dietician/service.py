from dataclasses import dataclass

from ai.dietician.bmi import BMICalculator
from ai.dietician.calorie import CalorieCalculator
from ai.dietician.grocery import GroceryListGenerator, GroceryItem
from ai.dietician.meal_planner import MealPlan, MealPlanner


@dataclass(frozen=True)
class DietPlanData:
    """Structured data produced by the Dietician engine."""

    bmi: float
    bmi_category: str
    bmr: float
    maintenance_calories: float
    target_calories: float
    meal_plan: MealPlan
    grocery_items: list[GroceryItem]


class DieticianService:
    """Combine all deterministic Dietician components."""

    def __init__(self):
        self.bmi_calculator = BMICalculator()
        self.calorie_calculator = CalorieCalculator()
        self.meal_planner = MealPlanner()
        self.grocery_generator = GroceryListGenerator()

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
        """Generate a complete structured diet plan."""

        bmi_result = self.bmi_calculator.calculate(
            weight_kg=weight_kg,
            height_cm=height_cm,
        )

        calorie_result = self.calorie_calculator.calculate(
            age=age,
            weight_kg=weight_kg,
            height_cm=height_cm,
            sex=sex,
            activity_level=activity_level,
            fitness_goal=fitness_goal,
        )

        meal_plan = self.meal_planner.generate(
            daily_calories=calorie_result.target_calories,
            dietary_preference=dietary_preference,
        )

        grocery_items = self.grocery_generator.generate(
            meal_plan=meal_plan,
        )

        return DietPlanData(
            bmi=bmi_result.bmi,
            bmi_category=bmi_result.category,
            bmr=calorie_result.bmr,
            maintenance_calories=(
                calorie_result.maintenance_calories
            ),
            target_calories=calorie_result.target_calories,
            meal_plan=meal_plan,
            grocery_items=grocery_items,
        )
