from dataclasses import dataclass

from ai.dietician.meal_planner import MealPlan


@dataclass(frozen=True)
class GroceryItem:
    """Represent one grocery-list item."""

    name: str
    quantity: float
    unit: str
    category: str


class GroceryListGenerator:
    """
    Convert a meal plan into a simple consolidated
    grocery list.
    """

    INGREDIENTS = {
        "Oatmeal with milk, banana and eggs": [
            ("oats", 80, "g", "grains"),
            ("milk", 250, "ml", "dairy"),
            ("banana", 1, "piece", "fruits"),
            ("eggs", 2, "piece", "protein"),
        ],
        "Rice, grilled chicken and mixed vegetables": [
            ("rice", 100, "g", "grains"),
            ("chicken", 150, "g", "protein"),
            ("mixed vegetables", 200, "g", "vegetables"),
        ],
        "Greek yogurt with fruit": [
            ("greek yogurt", 200, "g", "dairy"),
            ("mixed fruit", 150, "g", "fruits"),
        ],
        "Whole-grain roti, paneer and vegetables": [
            ("whole-grain flour", 100, "g", "grains"),
            ("paneer", 120, "g", "protein"),
            ("vegetables", 200, "g", "vegetables"),
        ],
        "Oatmeal with milk, banana and nuts": [
            ("oats", 80, "g", "grains"),
            ("milk", 250, "ml", "dairy"),
            ("banana", 1, "piece", "fruits"),
            ("mixed nuts", 30, "g", "fats"),
        ],
        "Rice, dal, paneer and mixed vegetables": [
            ("rice", 100, "g", "grains"),
            ("dal", 100, "g", "protein"),
            ("paneer", 100, "g", "protein"),
            ("mixed vegetables", 200, "g", "vegetables"),
        ],
        "Fruit with roasted chickpeas": [
            ("fruit", 150, "g", "fruits"),
            ("roasted chickpeas", 50, "g", "protein"),
        ],
        "Whole-grain roti, tofu and vegetables": [
            ("whole-grain flour", 100, "g", "grains"),
            ("tofu", 120, "g", "protein"),
            ("vegetables", 200, "g", "vegetables"),
        ],
        "Oatmeal with soy milk, banana and nuts": [
            ("oats", 80, "g", "grains"),
            ("soy milk", 250, "ml", "dairy-alternative"),
            ("banana", 1, "piece", "fruits"),
            ("mixed nuts", 30, "g", "fats"),
        ],
        "Rice, lentils and mixed vegetables": [
            ("rice", 100, "g", "grains"),
            ("lentils", 100, "g", "protein"),
            ("mixed vegetables", 200, "g", "vegetables"),
        ],
    }

    def generate(
        self,
        meal_plan: MealPlan,
    ) -> list[GroceryItem]:
        """Generate a consolidated grocery list."""

        if not meal_plan.meals:
            return []

        totals: dict[
            tuple[str, str, str],
            float,
        ] = {}

        for meal in meal_plan.meals:
            ingredients = self.INGREDIENTS.get(
                meal.name,
                [],
            )

            for name, quantity, unit, category in ingredients:
                key = (name, unit, category)
                totals[key] = (
                    totals.get(key, 0.0)
                    + quantity
                )

        items = [
            GroceryItem(
                name=name,
                quantity=round(quantity, 2),
                unit=unit,
                category=category,
            )
            for (name, unit, category), quantity
            in totals.items()
        ]

        return sorted(
            items,
            key=lambda item: (
                item.category,
                item.name,
            ),
        )
