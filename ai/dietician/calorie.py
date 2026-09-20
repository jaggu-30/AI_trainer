from dataclasses import dataclass


@dataclass(frozen=True)
class CalorieResult:
    """Calculated daily calorie targets."""

    bmr: float
    maintenance_calories: float
    target_calories: float


class CalorieCalculator:
    """
    Calculate BMR, maintenance calories, and a goal-adjusted
    daily calorie target.
    """

    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }

    ACTIVITY_ALIASES = {
        "lightly_active": "light",
        "moderately_active": "moderate",
        "very_active": "very_active",
    }

    GOAL_ADJUSTMENTS = {
        "weight_loss": -500,
        "maintenance": 0,
        "weight_gain": 300,
        "muscle_gain": 300,
        "strength": 300,
    }

    GOAL_ALIASES = {
        "strength": "muscle_gain",
    }

    def calculate(
        self,
        age: int,
        weight_kg: float,
        height_cm: float,
        sex: str,
        activity_level: str,
        fitness_goal: str,
    ) -> CalorieResult:
        """
        Calculate BMR using the Mifflin-St Jeor equation.
        """

        if age <= 0:
            raise ValueError(
                "Age must be greater than zero."
            )

        if weight_kg <= 0:
            raise ValueError(
                "Weight must be greater than zero."
            )

        if height_cm <= 0:
            raise ValueError(
                "Height must be greater than zero."
            )

        normalized_sex = sex.strip().lower()

        if normalized_sex not in {"male", "female"}:
            raise ValueError(
                "Sex must be either 'male' or 'female'."
            )

        normalized_activity = (
            activity_level.strip().lower()
        )

        normalized_activity = self.ACTIVITY_ALIASES.get(
            normalized_activity,
            normalized_activity,
        )

        if normalized_activity not in self.ACTIVITY_MULTIPLIERS:
            raise ValueError(
                f"Unsupported activity level: "
                f"{activity_level}"
            )

        normalized_goal = fitness_goal.strip().lower()

        normalized_goal = self.GOAL_ALIASES.get(
            normalized_goal,
            normalized_goal,
        )

        if normalized_goal not in self.GOAL_ADJUSTMENTS:
            raise ValueError(
                f"Unsupported fitness goal: "
                f"{fitness_goal}"
            )

        bmr = self._calculate_bmr(
            age=age,
            weight_kg=weight_kg,
            height_cm=height_cm,
            sex=normalized_sex,
        )

        maintenance = (
            bmr
            * self.ACTIVITY_MULTIPLIERS[
                normalized_activity
            ]
        )

        target = (
            maintenance
            + self.GOAL_ADJUSTMENTS[
                normalized_goal
            ]
        )

        return CalorieResult(
            bmr=round(bmr, 2),
            maintenance_calories=round(
                maintenance,
                2,
            ),
            target_calories=round(
                max(target, 1200),
                2,
            ),
        )

    @staticmethod
    def _calculate_bmr(
        age: int,
        weight_kg: float,
        height_cm: float,
        sex: str,
    ) -> float:
        base = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
        )

        if sex == "male":
            return base + 5

        return base - 161
