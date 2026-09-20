from dataclasses import dataclass


@dataclass(frozen=True)
class Meal:
    """Represent one planned meal."""

    name: str
    calories: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float


@dataclass(frozen=True)
class MealPlan:
    """Represent a complete daily meal plan."""

    daily_calories: float
    meals: list[Meal]


class MealPlanner:
    """
    Generate a simple deterministic daily meal plan.

    The planner uses calorie targets and dietary preference
    to select a predefined meal structure.
    """

    CALORIE_DISTRIBUTION = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "snack": 0.15,
        "dinner": 0.25,
    }

    MEAL_TEMPLATES = {
        "balanced": {
            "breakfast": (
                "Oatmeal with milk, banana and eggs"
            ),
            "lunch": (
                "Rice, grilled chicken and mixed vegetables"
            ),
            "snack": (
                "Greek yogurt with fruit"
            ),
            "dinner": (
                "Whole-grain roti, paneer and vegetables"
            ),
        },
        "vegetarian": {
            "breakfast": (
                "Oatmeal with milk, banana and nuts"
            ),
            "lunch": (
                "Rice, dal, paneer and mixed vegetables"
            ),
            "snack": (
                "Greek yogurt with fruit"
            ),
            "dinner": (
                "Whole-grain roti, tofu and vegetables"
            ),
        },
        "vegan": {
            "breakfast": (
                "Oatmeal with soy milk, banana and nuts"
            ),
            "lunch": (
                "Rice, lentils and mixed vegetables"
            ),
            "snack": (
                "Fruit with roasted chickpeas"
            ),
            "dinner": (
                "Whole-grain roti, tofu and vegetables"
            ),
        },
    }

    def generate(
        self,
        daily_calories: float,
        dietary_preference: str = "balanced",
    ) -> MealPlan:
        """
        Generate a deterministic daily meal plan.
        """

        if daily_calories <= 0:
            raise ValueError(
                "Daily calories must be greater than zero."
            )

        preference = (
            dietary_preference.strip().lower()
        )

        if preference not in self.MEAL_TEMPLATES:
            raise ValueError(
                f"Unsupported dietary preference: "
                f"{dietary_preference}"
            )

        templates = self.MEAL_TEMPLATES[preference]

        meals = []

        for meal_type, proportion in (
            self.CALORIE_DISTRIBUTION.items()
        ):
            calories = daily_calories * proportion

            protein = calories * 0.25 / 4
            carbohydrates = calories * 0.50 / 4
            fat = calories * 0.25 / 9

            meals.append(
                Meal(
                    name=templates[meal_type],
                    calories=round(calories, 2),
                    protein_g=round(protein, 2),
                    carbohydrates_g=round(
                        carbohydrates,
                        2,
                    ),
                    fat_g=round(fat, 2),
                )
            )

        return MealPlan(
            daily_calories=round(
                daily_calories,
                2,
            ),
            meals=meals,
        )
